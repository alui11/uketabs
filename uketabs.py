import contextlib
import copy
import pickle
import sys

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def usage():
    print('''
    uketabs
    A simple command line ukulele tab editor

    help
        show this help message
    exit / quit / q
        exit program
    load [filename]
        load tab file that has been saved with this editor
    save [filename]
        save tab as pickle file that can be reloaded with this editor
        if filename unspecified, overwrites last loaded or saved file
    export [filename]
        save tab as plain text file
        if filename unspecified, overwrites last exported file
    new
        create blank document
    show
        display current tab
    mpl [measures per line]
        adjust measures displayed per line (default = 4)
    bar
        append a new measure
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
        all major, minor, and 7 chords supported (flats only)
            examples:
            F becomes 0 1 0 2
            Am becomes 0 0 0 2
            G7 becomes 1 2 1 0
            Bb becomes 1 1 2 3
    del
        delete the last column of the last measure
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
    paste insert
        insert the clipboard at the specified measure number
    insert [measure #] [column #] [column]
        insert a column in the given measure at the given column number
    edit [measure #] [column #] [column]
        replace the specified column with a new one
    del [measure #] [column #]
        delete the specified column
    ''')

chords = {'A': ['0', '0', '1', '2'],
        'Am': ['0', '0', '0', '2'],
        'A7': ['0', '0', '1', '0'],
        'Bb': ['1', '1', '2', '3'],
        'Bbm': ['1', '1', '1', '3'],
        'Bb7': ['1', '1', '2', '1'],
        'B': ['2', '2', '3', '4'],
        'Bm': ['2', '2', '2', '4'],
        'B7': ['2', '2', '3', '2'],
        'C': ['3', '0', '0', '0'],
        'Cm': ['3', '3', '3', '0'],
        'C7': ['1', '0', '0', '0'],
        'Db': ['4', '1', '1', '1'],
        'Dbm': ['4', '4', '4', '1'],
        'Db7': ['2', '1', '1', '1'],
        'D': ['0', '2', '2', '2'],
        'Dm': ['0', '1', '2', '2'],
        'D7': ['3', '2', '2', '2'],
        'Eb': ['1', '3', '3', '0'],
        'Ebm': ['1', '2', '3', '3'],
        'Eb7': ['4', '3', '3', '3'],
        'E': ['2', '4', '4', '4'],
        'Em': ['2', '3', '4', '0'],
        'E7': ['2', '0', '2', '1'],
        'F': ['0', '1', '0', '2'],
        'Fm': ['3', '1', '0', '1'],
        'F7': ['3', '1', '3', '2'],
        'Gb': ['1', '2', '1', '3'],
        'Gbm': ['0', '2', '1', '2'],
        'Gb7': ['4', '2', '4', '3'],
        'G': ['2', '3', '2', '0'],
        'Gm': ['1', '3', '2', '0'],
        'G7': ['2', '1', '2', '0'],
        'Ab': ['3', '4', '3', '5'],
        'Abm': ['2', '4', '3', '4'],
        'Ab7': ['3', '2', '3', '1'],
        }

def chunker(seq, size):
    seq = list(enumerate(seq))
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def display(song, measures_per_line, filename=None):
    with smart_open(filename) as fh:
        for measure_group in chunker(song, measures_per_line):
            fh.write(str(measure_group[0][0]+1))
            fh.write('\n')
            for row in range(4):
                for measure_num, measure in measure_group:
                    for i, column in enumerate(measure):
                        if i == 0:
                            fh.write('|')
                        fh.write(column[row])
                if measure_num == len(song)-1:
                    fh.write('||')
                elif (measure_num + 1) % measures_per_line == 0:
                    fh.write('|')
                fh.write('\n')
            fh.write('\n')

def main():
    # Settings
    measures_per_line = 4
    auto_save = "my_song.tab"
    auto_export = "my_song.txt"

    #list of measures
    #each measure is a list of columns
    #each column is a list of 4 characters
    measures = [[['-', '-', '-', '-']]]

    # clipboard for copy/paste
    clipboard = []

    display(measures, measures_per_line)
    while True:
        command = raw_input(">> ")
        if command in ["exit", "quit", "q"]:
            break
        elif command == "help":
            usage()
        elif command == "debug":
            print(measures)
        elif command == "show":
            display(measures, measures_per_line)
        elif command.startswith("mpl"):
            command = command.split()
            try:
                mpl = int(command[1])
                measures_per_line = mpl
                display(measures, measures_per_line)
            except:
                usage()
        elif command.startswith("load"):
            try:
                filename = command.split()[1]
                with open(filename, "rb") as f:
                    measures = pickle.load(f)
                display(measures, measures_per_line)
                auto_save = filename
            except:
                usage()
        elif command.startswith("save"):
            try:
                command = command.split()
                if len(command) > 1:
                    filename = command[1]
                else:
                    filename = auto_save
                with open(filename, "wb") as f:
                    pickle.dump(measures, f)
                print("Successfully saved to {}".format(filename))
                auto_save = filename
            except:
                usage()
        elif command.startswith("export"):
            try:
                command = command.split()
                if len(command) > 1:
                    filename = command[1]
                else:
                    filename = auto_export
                display(measures, measures_per_line, filename)
                print("Successfully exported to {}".format(filename))
                auto_export = filename
            except:
                usage()
        elif command == "new":
            measures = [[['-', '-', '-', '-']]]
            display(measures, measures_per_line)
        elif command == "bar":
            measures.append([['-', '-', '-', '-']])
            display(measures, measures_per_line)
        elif command =="del":
            measures[-1].pop()
            display(measures, measures_per_line)
        elif command.startswith("insert measure"):
            command = command.split()
            try:
                measure_num = int(command[2])-1
                measures.insert(measure_num, [['-', '-', '-', '-']])
                display(measures, measures_per_line)
            except:
                usage()
        elif command.startswith("del measure"):
            command = command.split()
            try:
                measure_num = int(command[2])-1
                measures.pop(measure_num)
                display(measures, measures_per_line)
            except:
                usage()
        elif command.startswith("copy measure"):
            command = command.split()
            try:
                measure_num = int(command[2])-1
                clipboard = [copy.deepcopy(measures[measure_num])]
                print("Copied measure {}. Use 'paste' or 'paste insert'.".format(measure_num+1))
            except:
                usage()
        elif command.startswith("copy range"):
            command = command.split()
            try:
                begin_range = int(command[2])-1
                end_range = int(command[3])
                clipboard = copy.deepcopy(measures[begin_range:end_range])
                print("Copied measures {}-{}. Use 'paste' or 'paste insert'.".format(begin_range+1, end_range))
            except:
                usage()
        elif command.startswith("paste insert"):
            command = command.split()
            try:
                if len(clipboard) > 0:
                    measure_num = int(command[2])-1
                    measures[measure_num:measure_num] = copy.deepcopy(clipboard)
                    display(measures, measures_per_line)
                else:
                    print("Clipboard empty")
            except:
                usage()
        elif command == "paste":
            try:
                if len(clipboard) > 0:
                    measures.extend(copy.deepcopy(clipboard))
                    display(measures, measures_per_line)
                else:
                    print("Clipboard empty")
            except:
                usage()
        elif command.startswith("edit"):
            command = command.split()
            try:
                measure_num = int(command[1])-1
                col_num = int(command[2])-1
                col = command[3:]
                if col[0] in chords:
                    col = chords[col[0]]
                while len(col) < 4:
                    col.append('-')
                for i in range(4):
                    measures[measure_num][col_num][i] = col[i]
                display(measures, measures_per_line)
            except:
                usage()
        elif command.startswith("insert"):
            command = command.split()
            try:
                measure_num = int(command[1])-1
                col_num = int(command[2])-1
                col = command[3:]
                if col[0] in chords:
                    col = chords[col[0]]
                while len(col) < 4:
                    col.append('-')
                measures[measure_num].insert(col_num, col)
                display(measures, measures_per_line)
            except:
                usage()
        elif command.startswith("del"):
            command = command.split()
            try:
                measure_num = int(command[1])-1
                col_num = int(command[2])-1
                measures[measure_num].pop(col_num)
                display(measures, measures_per_line)
            except:
                usage()
        else:
            if command == "space":
                col = ['-', '-', '-', '-']
            elif command in chords:
                col = chords[command]
            else:
                col = command.split()
            while len(col) < 4:
                col.append('-')
            measures[-1].append(col)
            display(measures, measures_per_line)

main()

# todo
# arrow keys
# ask to save before quitting / loading
# new document
