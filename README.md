# CodeLinesCounter
##Introduction and Background
This is a line counter for any file, this primarily keep track of the number of lines that are comments.
Comments are unique and crucial building block of a good piece of code. 
The number of comment lines, as well as good choices for variable name contribute to the clarity and maintainability of code.
The details on the nature of comments can be found here: http://www.gavilan.edu/csis/languages/comments.html#_Toc53710121

## Usage
This is a python script that is meant to be run on the command line. 
Open the directory with the script and enter the following command:
 
 `python code_lines_counter.py <FILE_PATH>`  

## Implementation Details
The script primarily uses regular expressions to match with the comment symbols. The two type of comments, single line and multi line comment requires
very different process procedures. Below I will explain the main implementation ideas of this script, for sake of example we will use `"//"` for single line comment and `"/* */"` for multi line comment.

For single line comments, each line is matched with the regex `"\/\/.*"` which will match the comment symbol and anything after it that is on the same line. 

For multi line quotes this is a bit more complicated. Each line is matched with `\/\*.*`, which is the beginning of a multi line comment, 
then we check if the comment ends on the same line. If not, then we turn on the "multi line comment flag" and proceed to the next line. The flag is meant to represent the state
as we enter the next line, telling the program if this line is a comment or not. 

While the flag is on, we actively check for the end of the comment with regex `".*?\*\/"` the `?` makes the expression lazy and this will match with the first end comment symbol of the line. 
This is important as multiple multi line comments can exist on one line. We solve this edge case by checking the remaining line after the end comment symbol for comments.

## Multi Language Support
This script will automatically check the extension of the file and use the corresponding comment symbols. I have personally compiled a table `comment_symbol_table.csv` in the folder with some of the most popular languages and file formats. 
However this is still very incomplete and you can add to the table if you wish.

Some additional notes:
- For languages that does not have a particular comment symbol (HTML does not have single line comment and python does not have multi line comment), use the regex `"a^"` as the matching symbol. 
This regular expression will guarantee to match nothing (Since `^` represents the beginning of a line and there cannot be anything before the beginning of the line).

## Known Issues

This is a very naive implementation of analysing comments in a file, so there are many edge cases that have not been addressed.
These edge cases are mostly non-trivial and very complicated to solve, I believe there is no elegant general solution to this kind of problem. 
A parser will be needed and is largely outside of the scope of a personal project.


- In python there is no official multi line comment symbol. However, it is a convention to use the multi line string symbol `'''` as a work-around. This relies on the fact that the string will have no effect and be ignored by the program. However, there will be cases when a multi lines string does have an effect. The location of the string determines if its a comment or not. Thus a parser or something more powerful is required to make distinctions between them.

- There will also be cases where the comment symbol appears but have no effect, this can be the case where it appears in a string like `print("Here is a symbol // .")`. This will be mistakenly treated as a line of comment by the script because it cannot distinguish between if the symbol has an effect or not. 
