import copy
from modules.measure import Measure
from modules.measure import EditDescriptor
from modules import measure_utils
import sys

EditType = EditDescriptor.EditType

def usage():
    print('''
    uketabs
    A simple command line ukulele tab editor

    help
        show this help message
    exit / quit / q
        exit program
    load [filename]
        load ascii tab file that has been created with this editor
    save [filename]
        save tab as plain text file
        if filename unspecified, overwrites last saved file
    new
        create blank document
    show
        display current tab
    mpl [measures per line]
        adjust measures displayed per line (default = 4)
    autospace
        toggle autospace mode (default = ON)
        autospace mode: a blank column is automatically appended whenever
        a non-blank column is added
    bar / b
        append a new measure
    barline [measure #] [column #]
        insert a barline at the specified measure and column
    del barline [measure #]
        delete the barline before the specified measure
    [column]
        append a new column to the last measure
        specify columns with four space-separated tokens, in top-down order
            for example:
            2 3 2 0
            - - - 4
            7- 8- 9- 10
        unspecified tokens are interpreted as '-'
            for example:
            - 3 becomes - 3 - -
            4 becomes 4 - - -
            a blank line becomes - - - -
        columns can also be specified with chord names
        the most common fingering will be applied
        all major, minor, and 7 chords supported
            examples:
            F becomes 0 1 0 2
            Am becomes 0 0 0 2
            G7 becomes 1 2 1 0
            Bb becomes 1 1 2 3
    del / d
        delete the last column of the last measure
        when in autospace mode, deletes last 2 columns
    del measure [measure #]
        delete the given measure
    insert measure [measure #]
        insert a blank measure at a given location
    copy measure [measure #]
        copy the given measure to the clipboard
    copy range [begin] [end]
        copy the range of measures to the clipboard
    paste
        append the clipboard to the end of the tab
    paste insert [measure #]
        insert the clipboard at the specified measure number
    insert [measure #] [column #] [column]
        insert a column in the given measure at the given column number
    edit [measure #] [column #] [column]
        replace the specified column with a new one
    del [measure #] [column #]
        delete the specified column
    ''')


def main():
    # Settings
    mpl = 4  # Measures per line
    auto_save = "my_song.txt"
    autospace = True

    # Initialize list of measures
    measures = [Measure()]

    # clipboard for copy/paste
    clipboard = []

    # Last edit
    last_edit = EditDescriptor(EditType.INSERT, 0, 0)

    measure_utils.write_measures(measures, mpl, last_edit=last_edit)
    while True:
        command = raw_input(">> ")
        if command in ["exit", "quit", "q"]:
            break
        elif command == "help":
            usage()
        elif command == "show":
            measure_utils.write_measures(measures, mpl, last_edit=last_edit)
        elif command.startswith("mpl"):
            command = command.split()
            try:
                if len(command) < 2:
                    raise ValueError("mpl command requires integer argument.")
                new_mpl = int(command[1])
                mpl = new_mpl
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Parse error: {}".format(e))
        elif command == "autospace":
            autospace = not autospace
            print("autospace mode turned {}".format("ON" if autospace else "OFF"))
        elif command.startswith("load"):
            command = command.split()
            try:
                if len(command) < 2:
                    raise ValueError("load requires filename argument.")
                filename = command[1]
                measures = measure_utils.load_tab_from_ascii(filename)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
                auto_save = filename
            except Exception as e:
                print("Error loading file: {}".format(e.message))
        elif command.startswith("save"):
            command = command.split()
            if len(command) > 1:
                filename = command[1]
            else:
                filename = auto_save
            try:
                measure_utils.write_measures(measures, mpl, filename)
                print("Successfully saved to {}".format(filename))
                auto_save = filename
            except Exception as e:
                print("Error saving file: {}".format(e.message))
        elif command == "new":
            measures = [Measure()]
            last_edit = EditDescriptor(EditType.INSERT, 0, 0)
            measure_utils.write_measures(measures, mpl, last_edit=last_edit)
        elif command in ["bar", "b"]:
            measures.append(Measure())
            last_edit = EditDescriptor(EditType.INSERT, len(measures) - 1, 0)
            measure_utils.write_measures(measures, mpl, last_edit=last_edit)
        elif command.startswith("barline"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("barline command must specify measure number and column index.")
                measure_num = int(command[1])-1
                if measure_num < 0 or measure_num > len(measures) - 1:
                    raise ValueError("Measure number out of range.")
                col_num = int(command[2])-1
                split = measure_utils.split_measure(measures[measure_num], col_num)
                measures[measure_num] = split[0]
                measures.insert(measure_num+1, split[1])
                last_edit = EditDescriptor(EditType.INSERT, measure_num + 1, 0)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error inserting barline: {}".format(e.message))
        elif command.startswith("del barline"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("del barline command must specify measure number.")
                measure_num = int(command[2])-1
                if measure_num == 0:
                    raise ValueError("Cannot remove initial barline.")
                elif measure_num < 0 or measure_num > len(measures) - 1:
                    raise ValueError("Measure number out of range.")
                col_num = len(measures[measure_num - 1].columns) - 1
                merged = measure_utils.merge_measures(measures[measure_num - 1], measures[measure_num])
                measures[measure_num - 1] = merged
                measures.pop(measure_num)
                last_edit = EditDescriptor(EditType.DELETE, measure_num - 1, col_num)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error deleting barline: {}".format(e.message))
        elif command in ["del", "d"]:
            try:
                if len(measures[-1].columns) <= 1 and len(measures) > 1:
                    measures.pop()
                elif len(measures[-1].columns) > 1:
                    measures[-1].delete()
                    if autospace and len(measures[-1].columns) > 1:
                        measures[-1].delete()
                last_edit = EditDescriptor(EditType.DELETE, len(measures) - 1, len(measures[-1].columns) - 1)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error removing last entry: {}".format(e.message))
        elif command.startswith("insert measure"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("insert measure requires index argument.")
                measure_num = int(command[2])-1
                if measure_num < 0 or measure_num > len(measures) - 1:
                    raise ValueError("Measure number out of range.")
                measures.insert(measure_num, Measure())
                last_edit = EditDescriptor(EditType.INSERT, measure_num, 0)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error inserting measure: {}".format(e.message))
        elif command.startswith("del measure") or command.startswith("delete measure"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("delete measure requires measure number argument.")
                measure_num = int(command[2])-1
                if measure_num < 0 or measure_num > len(measures) - 1:
                    raise ValueError("Measure number out of range.")
                if len(measures) == 1:
                    raise ValueError("Cannot delete the only measure.")
                measures.pop(measure_num)
                last_edit = EditDescriptor(EditType.DELETE, measure_num - 1, len(measures[measure_num-1].columns) - 1)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error deleting measure: {}".format(e.message))
        elif command.startswith("copy measure"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("copy measure requires measure number argument.")
                measure_num = int(command[2])-1
                if measure_num < 0 or measure_num > len(measures) - 1:
                    raise ValueError("Measure number out of range.")
                clipboard = [copy.deepcopy(measures[measure_num])]
                print("Copied measure {}. Use 'paste' or 'paste insert'.".format(measure_num+1))
            except Exception as e:
                print("Error copying measure: {}".format(e.message))
        elif command.startswith("copy range"):
            command = command.split()
            try:
                if len(command) < 4:
                    raise ValueError("copy range requires begin and end range argument.")
                begin_range = int(command[2])-1
                end_range = int(command[3])
                if begin_range < 0 or begin_range > len(measures) - 1:
                    raise ValueError("Range begins out of range.")
                if end_range < 0 or end_range > len(measures):
                    raise ValueError("Range ends out of range.")
                if begin_range + 1 > end_range:
                    raise ValueError("Range specifiers out of order.")
                clipboard = copy.deepcopy(measures[begin_range:end_range])
                print("Copied measures {}-{}. Use 'paste' or 'paste insert'.".format(begin_range+1, end_range))
            except Exception as e:
                print("Error copying measures: {}".format(e.message))
        elif command.startswith("paste insert"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("paste insert requires index argument.")
                if len(clipboard) > 0:
                    measure_num = int(command[2])-1
                    if measure_num < 0 or measure_num > len(measures) - 1:
                        raise ValueError("Measure number out of range.")
                    measures[measure_num:measure_num] = copy.deepcopy(clipboard)
                    # TODO: Allow edit ranges.
                    last_edit = None
                    measure_utils.write_measures(measures, mpl, last_edit=last_edit)
                else:
                    print("Clipboard empty")
            except Exception as e:
                print("Error pasting measures: {}".format(e.message))
        elif command == "paste":
            try:
                if len(clipboard) > 0:
                    measures.extend(copy.deepcopy(clipboard))
                    # TODO: Allow edit ranges.
                    last_edit = None
                    measure_utils.write_measures(measures, mpl, last_edit=last_edit)
                else:
                    print("Clipboard empty")
            except Exception as e:
                print("Error pasting measures: {}".format(e.message))
        elif command.startswith("edit"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("edit command requires measure number and column number.")
                measure_num = int(command[1])-1
                if measure_num < 0 or measure_num > len(measures) - 1:
                    raise ValueError("Measure number out of range")
                col_num = int(command[2])-1
                col = ' '.join(command[3:])
                measures[measure_num].update(col_num, col)
                last_edit = EditDescriptor(EditType.UPDATE, measure_num, col_num)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error editing column: {}".format(e.message))
        elif command.startswith("insert"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("insert command requires measure number and column index.")
                measure_num = int(command[1])-1
                if measure_num < 0 or measure_num > len(measures) - 1:
                    raise ValueError("Measure number out of range")
                col_num = int(command[2])-1
                col = ' '.join(command[3:])
                measures[measure_num].insert(col_num, col)
                last_edit = EditDescriptor(EditType.INSERT, measure_num, col_num)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error inserting column: {}".format(e.message))
        elif command.startswith("del") or command.startswith("delete"):
            command = command.split()
            try:
                if len(command) < 3:
                    raise ValueError("delete command requires measure number and column index.")
                measure_num = int(command[1])-1
                if measure_num < 0 or measure_num > len(measures) - 1:
                    raise ValueError("Measure number out of range")
                col_num = int(command[2])-1
                measures[measure_num].delete(col_num)
                last_edit = EditDescriptor(EditType.DELETE, measure_num, col_num - 1)
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error deleting column: {}".format(e.message))
        else:
            try:
                measures[-1].append(command)
                last_edit = EditDescriptor(EditType.INSERT, len(measures) - 1, len(measures[-1].columns) - 1)
                if autospace and command != '' and set(command.split()) != set(['-']):
                    measures[-1].append('')
                measure_utils.write_measures(measures, mpl, last_edit=last_edit)
            except Exception as e:
                print("Error adding column: {}".format(e.message))

if __name__ == '__main__':
    main()
