class Play:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def seePlays(self):
        return 'row: ' + str(self.row) + 'col: ' + str(self.col)

    def hash(self):
        return str(self.row) + ',' + str(self.col)
    