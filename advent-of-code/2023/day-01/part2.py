#!/opt/homebrew/bin/python3

'''
Your calculation isn't quite right_index. It looks like some of the digits 
are actually spelled out with letters: one, two, three, four, five, 
six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real 
first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. 
Adding these together produces 281.

approach:
    - first check if letter is a digit
    - then build a trie to see if the cut off is in word set
'''

import argparse

DIGIT_MAP = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

key_lengths = set([len(k) for k in DIGIT_MAP.keys()])

def get_digit(start_index, line):
    if line[start_index].isdigit():
        return line[start_index]

    
    for k in key_lengths:
        if (
                start_index + k - 1 < len(line) and 
                line[start_index:start_index+k] in DIGIT_MAP
        ):
            return DIGIT_MAP[line[start_index:start_index+k]]

    return None


def solve(lines):
    total = 0
    for l in lines:
        start_digit, end_digit = None, None

        # get start digit
        for left_index in range(len(l)):
            start_digit = get_digit(start_index=left_index, line=l)
            if start_digit:
                break

        if not start_digit:
            raise Exception(f"there was not anything digit in line {l}")

        for right_index in range(len(l) - 1, -1, -1):
            end_digit = get_digit(start_index=right_index, line=l)
            if end_digit:
                break

        total += int(start_digit + end_digit)
    return total


def main():
    parser = argparse.ArgumentParser(description='Advent of code day 1 part 2')
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
