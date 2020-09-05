'''
measure_utils.py
'''
from colorama import init
init()
from colorama import Fore, Back, Style
import contextlib
from measure import Measure
from measure import EditDescriptor
import sys

@contextlib.contextmanager
def smart_open(filename=None):
    '''Opens file if `filename`, else returns sys.stdout.'''
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def chunker(seq, size):
    '''Divides a sequence into chunks of size `size`. Enumerates
    seq before chunking.'''
    seq = list(enumerate(seq))
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def split_measure(measure, index):
    '''Splits Measure into two Measures at the given index.

    Args:
        measure: the Measure object to be split.
        index: the index of the column that will begin the
          second measure after splitting.

    Returns:
        A list of 2 Measure objects.
    '''
    if index < 0 or index > len(measure.columns) - 1:
        raise ValueError("Column index out of range.")
    return [Measure(measure.columns[:index]), Measure(measure.columns[index:])]

def merge_measures(measure1, measure2):
    '''Merges two measures into a single measure, removing first column
    of second measure.'''
    return Measure(measure1.columns + measure2.columns[1:])

def write_measures(measures, measures_per_line, filename=None, last_edit=None):
    '''Prints list of measures in a human-readable format.

    Adds barlines between measures, measure numbers, double barline at
    piece end.

    Args:
        measures: A list of Measure objects.
        measures_per_line: prints this many measures per line of music.
        filename: File to write to. Prints to sys.stdout if None.
    '''
    with smart_open(filename) as fh: 
        for measure_group in chunker(measures, measures_per_line):
            fh.write(str(measure_group[0][0]+1))  # Write measure number.
            fh.write('\n')
            for row in range(4):  # Measures are 4 rows tall.
                for measure_num, measure in measure_group:
                    fh.write('|')
                    for column_num, column in enumerate(measure.columns):
                        if last_edit and last_edit.measure_num == measure_num and last_edit.column_num == column_num:
                            if last_edit.type == EditDescriptor.EditType.INSERT:
                                color = Fore.GREEN
                            elif last_edit.type == EditDescriptor.EditType.UPDATE:
                                color = Fore.YELLOW
                            elif last_edit.type == EditDescriptor.EditType.DELETE:
                                color = Fore.RED
                            else:
                                raise ValueError("Unknown edit type")
                        else:
                            color = ''
                        fh.write(color + column.value[row])
                        if color:
                            fh.write(Style.RESET_ALL)
                if measure_num == len(measures)-1:
                    fh.write('||')
                elif (measure_num + 1) % measures_per_line == 0:
                    fh.write('|')
                fh.write('\n')
            fh.write('\n')

def load_tab_from_ascii_lines(lines):
    '''Loads tab from a list of ascii lines into a list of Measure
    objects. Lines beginning with '|' must be part of measures, and
    all other lines are ignored.'''
    measures = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('|'):
            tab_line = []
            for _ in range(4):
                tab_line.append(filter(None, lines[i].strip().split('|')))
                i += 1
            for m in range(len(tab_line[0])):
                measure = Measure()
                measure.delete()
                for c in range(len(tab_line[0][m])):
                    measure.append(' '.join([tab_line[l][m][c] for l in range(4)]))
                measures.append(measure)
        else:
            i += 1
    return measures
            

def load_tab_from_ascii(filename):
    '''Loads ascii tab from file into a list of Measure objects. Lines
    beginning with '|' in the file must be part of measures, and all
    other lines are ignored.'''
    with open(filename) as f:
        lines = f.readlines()
    return load_tab_from_ascii_lines(lines)
