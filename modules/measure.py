'''
measure.py
'''
import constants
import copy


class Column():
    def __init__(self, column_str='- - - -'):
        self.value = self.normalize(column_str)
    
    def normalize(self, column_str):
        '''Check that column string is valid and convert to 4-token list.

        Args:
            column_str: Space-separated list of tokens.
        Returns:
            List of 4 string tokens.
        Raises:
            ValueError: if number of tokens exceeds 4 or if token lengths
              do not match.
        '''
        column = column_str.split()
        if len(column) > 4:
            raise ValueError("Column specification has too many elements.")
        if len(column) == 1 and column[0] in constants.CHORDS:
            column = copy.deepcopy(constants.CHORDS[column[0]])
        while len(column) < 4:
            column.append('-')
        if len(set(map(len, column))) > 1:
            raise ValueError("Column tokens must be of equal length.")
        return column

    def update(self, column_str):
        self.value = self.normalize(column_str)


class Measure():
    def __init__(self, column_list=None):
        if column_list:
            self.columns = copy.deepcopy(column_list)
        else:
            self.columns = [Column()]

    def assert_in_range(self, index):
        if index < 0 or index > len(self.columns) - 1:
            raise ValueError("Column index out of range.")

    def insert(self, index, column_str):
        if index < 0 or index > len(self.columns):
            raise ValueError("Column index out of range.")
        self.columns.insert(index, Column(column_str))

    def append(self, column_str):
        self.columns.append(Column(column_str))

    def update(self, index, column_str):
        self.assert_in_range(index)
        self.columns[index].update(column_str)

    def delete(self, index=None):
        if index:
            self.assert_in_range(index)
            self.columns.pop(index)
        elif len(self.columns) > 0:
            self.columns.pop(-1)
        else:
            raise ValueError("Column index out of range.")


class EditDescriptor():
    class EditType:
        INSERT = 0
        UPDATE = 1
        DELETE = 2

    def __init__(self, edit_type, measure_num, column_num):
        self.type = edit_type
        self.measure_num = measure_num
        self.column_num = column_num

