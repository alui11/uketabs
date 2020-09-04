from measure import Measure
import measure_utils
import os
import tempfile
import unittest

class MeasureUtilsTest(unittest.TestCase):
    def testChunker(self):
        seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        chunked = list(measure_utils.chunker(seq, 5))
        self.assertEqual(chunked, [[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
            [(5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]])
        chunked = list(measure_utils.chunker(seq, 3))
        self.assertEqual(chunked, [[(0, 1), (1, 2), (2, 3)],
            [(3, 4), (4, 5), (5, 6)], [(6, 7), (7, 8), (8, 9)], [(9, 10)]])

    def testSplitMeasure(self):
        measure = Measure()
        measure.append('1 1 1 1')
        measures = measure_utils.split_measure(measure, 1)
        self.assertEqual(len(measures), 2)
        self.assertEqual(len(measures[0].columns), 1)
        self.assertEqual(measures[0].columns[0].value, ['-', '-', '-', '-'])
        self.assertEqual(len(measures[1].columns), 1)
        self.assertEqual(measures[1].columns[0].value, ['1', '1', '1', '1'])
        with self.assertRaises(ValueError, msg="Column index out of range."):
            measure_utils.split_measure(measure, 2)

    def testMergeMeasures(self):
        measure1 = Measure()
        measure2 = Measure()
        measure2.append('1')
        merged = measure_utils.merge_measures(measure1, measure2)
        self.assertEqual(len(merged.columns), 2)
        self.assertEqual(merged.columns[0].value, ['-', '-', '-', '-'])
        self.assertEqual(merged.columns[1].value, ['1', '-', '-', '-'])

    def testWriteMeasures(self):
        measure1 = Measure()
        measure2 = Measure()
        measure2.append('C7')
        measure3 = Measure()
        measure3.update(0, 'F')
        measures = [measure1, measure2, measure3]

        outfile_path = tempfile.mkstemp()[1]
        try:
            measure_utils.write_measures(measures, 2, outfile_path)
            contents = open(outfile_path).read()
        finally:
            os.remove(outfile_path)
        self.assertEqual(contents,
                '''1\n|-|-1|\n|-|-0|\n|-|-0|\n|-|-0|\n\n3\n|0||\n|1||\n|0||\n|2||\n\n''')


if __name__ == '__main__':
    unittest.main()
