import re
import sys

single_line_comment_symbol = "//"
multi_line_comment_start = "/*"
multi_line_comment_end = "*/"

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
    multi_line_content = re.match(re.escape(multi_line_comment_start) + ".*" + re.escape(multi_line_comment_end),
                                  line_str)

    if multi_line_content is not None:
        todo_count += len(re.findall("TODO", multi_line_content.group(0)))
        match_comments(line_str[:multi_line_content.end()])
    else:
        todo_count += len(re.findall("TODO", multi_line_string.group(0)))
        multi_line_comment_flag = True


def match_comments(line_str):
    global single_line_comment_symbol, multi_line_comment_start, multi_line_comment_end, total_lines, comment_lines, single_line_comment_lines, block_line_comments, \
        comment_lines_in_block, todo_count, multi_line_comment_flag
    #import pdb; pdb.set_trace()

    single_comment_string = re.match(re.escape(single_line_comment_symbol) + ".*", line_str)
    multi_line_string = re.match(re.escape(multi_line_comment_start) + ".*", line_str)

    if multi_line_comment_flag:
        comment_lines += 1
        comment_lines_in_block += 1
        multi_line_end_string = re.match(".*?" + re.escape(multi_line_comment_end), line_str)
        if multi_line_end_string is not None:
            multi_line_comment_flag = False
            todo_count += len(re.findall("TODO", multi_line_end_string.group(0)))
            match_comments(line_str[:multi_line_end_string.end()])
        else:
            todo_count += len(re.findall("TODO", line_str))
    elif single_comment_string is not None and multi_line_string is not None:
        if single_comment_string.start() < multi_line_string.start():
            record_single_comment_string(single_comment_string)
        else:
            record_multi_comment_string(multi_line_string, line_str)
    elif single_comment_string is not None:
        record_single_comment_string(single_comment_string)
    elif multi_line_string is not None:
        record_multi_comment_string(multi_line_string, line_str)


def main():
    # TODO check for valid command line input
    global single_line_comment_symbol, multi_line_comment_start, multi_line_comment_end, total_lines, comment_lines, single_line_comment_lines, block_line_comments, \
        comment_lines_in_block, todo_count, multi_line_comment_flag
    program_path = sys.argv[1]

    with open(program_path) as file:
        line = file.readline()
        total_lines = 1
        while line:
            match_comments(line)
            line = file.readline()
            total_lines += 1

    print("Total # of lines:", total_lines)
    print("Total # of comment lines:", comment_lines)
    print("Total # of single line comments: ", single_line_comment_lines)
    print("Total # of comment lines within block comments:", comment_lines_in_block)
    print("Total # of block line comments:", block_line_comments)
    print("Total # of TODO’s: ", todo_count)


if __name__ == "__main__":
    main()
