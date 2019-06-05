class FileReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.table = []

    def open(self):
        self.file = open(self.filename, 'r')

    def column_count(self):
        line_array = self.file.readline().split(' ')
        self.file.seek(0)
        return len(line_array)

    def close(self):
        self.file.close()

    def set_table(self):
        table = []
        for line in self.file:
            table.append(list(map(float, line.split(' '))))
        self.table = table

    def get_table(self):
        return self.table
