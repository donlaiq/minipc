input_file = 'prompt.txt'
output_file = 'output.txt'

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
        # rstrip removes trailing whitespace and newlines
        # We append a backslash and a newline
        modified_line = line.rstrip() + "\\\n"
        f_out.write(modified_line)
