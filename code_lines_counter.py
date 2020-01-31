#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os.path
from comment_symbol_table_generator import CommentSymbolTable

single_line_comment_symbol = ""
multi_line_comment_start_symbol = ""
multi_line_comment_end_symbol = ""

total_lines = 0
comment_lines = 0
single_line_comment_lines = 0
block_line_comments = 0
comment_lines_in_block = 0
todo_count = 0

multi_line_comment_flag = False


def record_single_comment_string(single_comment_string):
    global comment_lines, single_line_comment_lines, todo_count
    comment_lines += 1
    single_line_comment_lines += 1
    todo_count += len(re.findall("TODO", single_comment_string.group(0)))


def record_multi_comment_string(multi_line_string, line_str):
    global comment_lines, comment_lines_in_block, block_line_comments, todo_count, multi_line_comment_flag

    comment_lines += 1
    comment_lines_in_block += 1
    block_line_comments += 1
    multi_line_content = re.search(re.escape(multi_line_comment_start_symbol) + ".*" + re.escape(multi_line_comment_end_symbol),
                                   line_str)
    if multi_line_content is not None:
        todo_count += len(re.findall("TODO", multi_line_content.group(0)))
        match_comments(line_str[multi_line_content.end():])
    else:
        todo_count += len(re.findall("TODO", multi_line_string.group(0)))
        multi_line_comment_flag = True


def match_comments(line_str):
    """This function takes in a string and process any comments that are in the string."""
    global single_line_comment_symbol, multi_line_comment_start_symbol, multi_line_comment_end_symbol, total_lines, comment_lines, single_line_comment_lines, block_line_comments, \
        comment_lines_in_block, todo_count, multi_line_comment_flag

    # single_comment_match and multi_line_match are regex match object
    # If none of comment is found, the object is None.
    single_comment_match = re.search(re.escape(single_line_comment_symbol) + ".*", line_str)
    multi_line_match = re.search(re.escape(multi_line_comment_start_symbol) + ".*", line_str)

    # multi_line_comment_flag determines if the function is in the state of multi_line comments
    # flag is true after a multi_line_start_symbol has be detected and false after end symbol.
    if multi_line_comment_flag:
        comment_lines += 1
        comment_lines_in_block += 1
        multi_line_end_string = re.match(".*?" + re.escape(multi_line_comment_end_symbol), line_str)
        if multi_line_end_string is not None:
            multi_line_comment_flag = False
            todo_count += len(re.findall("TODO", multi_line_end_string.group(0)))
            # calling match_comments again will process the remaining of the string after
            # the end of the multi_line_comments
            match_comments(line_str[multi_line_end_string.end():])
        else:
            todo_count += len(re.findall("TODO", line_str))
    elif single_comment_match is not None and multi_line_match is not None:
        if single_comment_match.start() < multi_line_match.start():
            record_single_comment_string(single_comment_match)
        else:
            record_multi_comment_string(multi_line_match, line_str)
    elif single_comment_match is not None:
        record_single_comment_string(single_comment_match)
    elif multi_line_match is not None:
        record_multi_comment_string(multi_line_match, line_str)


def main():
    global single_line_comment_symbol, multi_line_comment_start_symbol, multi_line_comment_end_symbol, total_lines, comment_lines, single_line_comment_lines, block_line_comments, \
        comment_lines_in_block, todo_count, multi_line_comment_flag

    # check for valid command line inputs

    if len(sys.argv) != 2:
        print("This program consumes one parameter, the path to file you want to check. Please try again.")
        return

    program_path = sys.argv[1]

    # splitext retrieves the extension of the path in the format of ".js" or ".py"
    extension = os.path.splitext(program_path)[1]

    # retrieve the comment symbols from CommentSymbolTable
    cst = CommentSymbolTable()
    comment_table = cst.get_symbols(extension)
    if comment_table is None:
        print("cannot find the corresponding comment symbols for this file extension: ", extension)
        return

    single_line_comment_symbol = comment_table[cst.SINGLE_LINE_COMMENT_SYMBOL]
    multi_line_comment_start_symbol = comment_table[cst.MULTI_LINE_COMMENT_START_SYMBOL]
    multi_line_comment_end_symbol = comment_table[cst.MULTI_LINE_COMMENT_END_SYMBOL]

    with open(program_path) as file:
        line = file.readline()
        total_lines = 1
        while line:
            match_comments(line)
            line = file.readline()
            total_lines += 1

    # printing the results
    print("Total number of lines: ", total_lines)
    print("Total number of comment lines: ", comment_lines)
    print("Total number of single line comments: ", single_line_comment_lines)
    print("Total number of comment lines within block comments: ", comment_lines_in_block)
    print("Total number of block line comments: ", block_line_comments)
    print("Total number of TODOs: ", todo_count)


if __name__ == "__main__":
    main()
