# HACK symbol for match nothing is 'a^'

class CommentSymbolTable:
    SINGLE_LINE_COMMENT_SYMBOL = "slcs"
    MULTI_LINE_COMMENT_START_SYMBOL = "mlcss"
    MULTI_LINE_COMMENT_END_SYMBOL = "mlces"

    # given a file extension, return the dictionary corresponding to the comment_symbol used
    # in the language. If none found, return None.
    def get_symbols(self, extension):
        for supported_extensions, comment_symbols in self.COMMENT_SYMBOL_TABLE:
            if extension in supported_extensions:
                return comment_symbols
        return None

    # COMMENT_SYMBOL_TABLE stores all the extensions and their corresponding comment_symbol in a list of tuples.
    # the tuple is of ( list of supported extensions, dictionary of comment_symbol)
    # This table is compiled by myself and you are welcome to add to the table.
    COMMENT_SYMBOL_TABLE = [
        ([".js", ".jsx", ".ts", ".tsx", ".c", ".cc", ".cpp", ".go", ".jsp", ".jspx", ".swift", ".php", ".cs", ".kt",
         ".m", ".rs"], {
            SINGLE_LINE_COMMENT_SYMBOL: "//",
            MULTI_LINE_COMMENT_START_SYMBOL: "/*",
            MULTI_LINE_COMMENT_END_SYMBOL: "*/"
        }),
        ([".html"], {
            SINGLE_LINE_COMMENT_SYMBOL: "a^",
            MULTI_LINE_COMMENT_START_SYMBOL: "<!--",
            MULTI_LINE_COMMENT_END_SYMBOL: "-->"
        }),
        ([".py", ".pl", ".rb"], {
            SINGLE_LINE_COMMENT_SYMBOL: "#",
            MULTI_LINE_COMMENT_START_SYMBOL: "^a",
            MULTI_LINE_COMMENT_END_SYMBOL: "^a"
        }),
        ([".tex", ".mat", ".erl"], {
            SINGLE_LINE_COMMENT_SYMBOL: "%",
            MULTI_LINE_COMMENT_START_SYMBOL: "^a",
            MULTI_LINE_COMMENT_END_SYMBOL: "^a"
        }),
        ([".sql"], {
            SINGLE_LINE_COMMENT_SYMBOL: "--",
            MULTI_LINE_COMMENT_START_SYMBOL: "/*",
            MULTI_LINE_COMMENT_END_SYMBOL: "*/"
        }),
        ([".hs"], {
            SINGLE_LINE_COMMENT_SYMBOL: "--",
            MULTI_LINE_COMMENT_START_SYMBOL: "{-",
            MULTI_LINE_COMMENT_END_SYMBOL: "-}"
        }),
        ([".asm"], {
            SINGLE_LINE_COMMENT_SYMBOL: ";",
            MULTI_LINE_COMMENT_START_SYMBOL: "^a",
            MULTI_LINE_COMMENT_END_SYMBOL: "^a"
        }),
        ([".rkt"], {
            SINGLE_LINE_COMMENT_SYMBOL: ";",
            MULTI_LINE_COMMENT_START_SYMBOL: "#|",
            MULTI_LINE_COMMENT_END_SYMBOL: "|#"
        })
    ]
