'''
measure_utils.py
'''
import contextlib
from measure import Measure
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

def write_measures(measures, measures_per_line, filename=None):
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
                    for column in measure.columns:
                        fh.write(column.value[row])
                if measure_num == len(measures)-1:
                    fh.write('||')
                elif (measure_num + 1) % measures_per_line == 0:
                    fh.write('|')
                fh.write('\n')
            fh.write('\n')
