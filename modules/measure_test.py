from measure import Column
from measure import Measure
import unittest

class ColumnTest(unittest.TestCase):
    def testNormalize(self):
        column = Column()
        self.assertEqual(column.normalize('1'), ['1', '-', '-', '-'])
        self.assertEqual(column.normalize(''), ['-', '-', '-', '-'])
        self.assertEqual(column.normalize('- - - 3'), ['-', '-', '-', '3'])
        self.assertEqual(column.normalize('F'), ['0', '1', '0', '2'])
        with self.assertRaises(ValueError, msg="Column specification has too many elements."):
            column.normalize('- - - - -')
        with self.assertRaises(ValueError, msg="Column tokens must be of equal length."):
            column.normalize('1 2 10 -')

    def testConstructColumn(self):
        column = Column()
        self.assertEqual(column.value, ['-', '-', '-', '-'])
        column = Column('1 2 3')
        self.assertEqual(column.value, ['1', '2', '3' ,'-'])

    def testUpdate(self):
        column = Column()
        column.update('1 2 3')
        self.assertEqual(column.value, ['1', '2', '3' ,'-'])


class MeasureTest(unittest.TestCase):
    def testConstructMeasure(self):
        measure = Measure()
        column = Column()
        self.assertEqual(len(measure.columns), 1)
        self.assertEqual(measure.columns[0].value, column.value)

    def testAppend(self):
        measure = Measure()
        column = Column()
        measure.append('')
        self.assertEqual(len(measure.columns), 2)
        self.assertEqual(measure.columns[0].value, column.value)

    def testInsert(self):
        measure = Measure()
        measure.append('')
        measure.insert(1, '4 4 4')
        measure.insert(3, '5 - - -')
        self.assertEqual(len(measure.columns), 4)
        self.assertEqual(measure.columns[0].value, ['-', '-', '-', '-'])
        self.assertEqual(measure.columns[1].value, ['4', '4', '4', '-'])
        self.assertEqual(measure.columns[2].value, ['-', '-', '-', '-'])
        self.assertEqual(measure.columns[3].value, ['5', '-', '-', '-'])
        with self.assertRaises(ValueError, msg="Column index out of range."):
            measure.insert(5, '')

    def testUpdate(self):
        measure = Measure()
        measure.update(0, '1')
        self.assertEqual(len(measure.columns), 1)
        self.assertEqual(measure.columns[0].value, ['1', '-', '-', '-'])
        with self.assertRaises(ValueError, msg="Column index out of range."):
            measure.update(1, '')

    def testDelete(self):
        measure = Measure()
        measure.delete(0)
        self.assertEqual(len(measure.columns), 0)
        measure.append('')
        measure.delete()
        self.assertEqual(len(measure.columns), 0)
        with self.assertRaises(ValueError, msg="Column index out of range."):
            measure.delete(0)


if __name__ == '__main__':
    unittest.main()
