import sys

def remove_chars_from_beginning(file, num_chars):
  # Open the input file in read mode and the output file in write mode
  with open(file, 'r') as f_in, open(f'{file}_modified.txt', 'w') as f_out:
    # Iterate over the lines in the input file
    for line in f_in:
      # Remove the specified number of characters from the beginning of the line
      modified_line = line[num_chars:]
      # Write the modified line to the output file
      f_out.write(modified_line)

def main():
  # Check that the correct number of command line arguments were provided
  if len(sys.argv) != 3:
    print('Usage: python remove_chars_from_beginning.py <file> <num_chars>')
    sys.exit(1)

  # Get the file name and number of characters to remove from the command line arguments
  file = sys.argv[1]
  num_chars = int(sys.argv[2])

  # Remove the specified number of characters from the beginning of each line in the file
  remove_chars_from_beginning(file, num_chars)

if __name__ == '__main__':
  main()