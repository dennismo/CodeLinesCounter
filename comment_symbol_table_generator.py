# HACK in comment_symbol table, symbol for match nothing is "a^"
import csv


class CommentSymbolTable:
    SINGLE_LINE_COMMENT_SYMBOL = "slcs"
    MULTI_LINE_COMMENT_START_SYMBOL = "mlcss"
    MULTI_LINE_COMMENT_END_SYMBOL = "mlces"

    comment_symbol_dict = {}

    def __init__(self):
        with open("comment_symbol_table.csv", mode="r") as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                self.comment_symbol_dict[row["extension"]] = {
                    self.SINGLE_LINE_COMMENT_SYMBOL: row["single_line_comment_symbol"],
                    self.MULTI_LINE_COMMENT_START_SYMBOL: row["multi_line_comment_start_symbol"],
                    self.MULTI_LINE_COMMENT_END_SYMBOL: row["multi_line_comment_end_symbol"]
                }

    # given a file extension, return the dictionary corresponding to the comment_symbol used
    # in the language. If none found, return None.
    def get_symbols(self, extension):
        return self.comment_symbol_dict.get(extension, None)
