#!/opt/homebrew/bin/python3

'''
The newly-improved calibration document consists of lines of text; 
each line originally contained a specific calibration value that the 
Elves now need to recover. On each line, the calibration value can be 
found by combining the first digit and the last digit (in that order) 
to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. 
Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of 
the calibration values?

approach: use 2 pointers to find the first digit encounter for each line
'''

import argparse

def solve(lines):
    total = 0
    for l in lines:
        start_digit, end_digit = None, None

        # get start digit
        for left in range(len(l)):
            if l[left].isdigit():
                start_digit = l[left]
                break
        if not start_digit:
            raise Exception(f"there was not anything digit in line {l}")
        for right in range(len(l) - 1, -1, -1):
            if l[right].isdigit():
                end_digit = l[right]
                break
        total += int(start_digit + end_digit)
    return total


def main():
    parser = argparse.ArgumentParser(description='Advent of code day 1 part 1')
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as input_file:
            lines = [line.strip() for line in input_file]
            print(solve(lines))
    except FileNotFoundError:
        print(f"Input file not found: {args.input}")
    except Exception as e:
        print(f"Encounter error for input: {args.input}, err: {e}")

if __name__ == "__main__":
    main()
