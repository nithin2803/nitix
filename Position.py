class Position:
    def __init__(self, index, line_no, column, file_name, file_text):
        self.index = index
        self.line_no = line_no
        self.column = column
        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_char=None):
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line_no += 1
            self.column = 0

        return self

    def copy(self):
        return Position(self.index, self.line_no, self.column, self.file_name, self.file_text)