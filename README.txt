- To use parser
Create an input file with the Lexp code.
Then open terminal in this folder and input
"python3 parser.py <input_file_title>.txt" (default output file will apply)
or
"python3 parser.py <input_file_title>.txt <output_file_title>.txt"




- To use a scaner open the terminal in this folder and input
"python3 ./scaner.py <input_file_title>.txt <output_file_title>.txt" to your command line tool.
Usecase example:
"python3 ./scaner.py input_file.txt output_file.txt"

! Input file has to be present to avoid error.
! Output file will be created automatically with the title offered if it does not exist yet.

- The scaner may be also used with string as an input, generating tokens right into the command line interface.
For this type of usage open the terminal in this folder and input
'python3 ./scaner.py "(any strings written in Lexp for tokenization)"'
Usecase example:
'python3 ./scaner.py "34 + 89 - x * y23
cxo6y / 67z23 * 56& 34 * x
2 + x"'

- To use the scaner in parser, it is intended to be copied to the same folder and imported as a module,
what allows to use a scaner function dirrectly.
Usecase example:

from scaner import scaner

# To scan a single line for it's tokens
result = scaner("34 + 89 - x * y23")[0]["tokens"]

# To scan a whole code at once (multiple lines separated by "\n")
# ! Principle of the longest substring is not violated.
# Each new line will be parsed into the separate dictionary.

result = scaner(
    """34 + 89 - x * y23
cxo6y / 67z23 * 56& 34 * x
2 + x"""
)
