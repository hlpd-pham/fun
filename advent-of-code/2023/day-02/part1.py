#!/opt/homebrew/bin/python3

import argparse
import traceback
import re

def solve(lines):
    '''
    get all lines, stripped, check if each turn has more than the amount of cubes we have from threshold,
    exit if we do, increment the total if we exit inner loop normally
    '''
    total = 0
    threshold = {'red': 12, 'green': 13, 'blue': 14}
    for id, game in enumerate(lines, start=1):
        for n, color in re.findall(r'(\d+) (red|green|blue)', game):
            if threshold[color] < int(n):
                break
        else:
            total += id
    return total
        

def main():
    parser = argparse.ArgumentParser(description='Advent of code day 2 part 1')
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as input_file:
            lines = [line.strip() for line in input_file]
            print(solve(lines))
    except FileNotFoundError:
        print(f"Input file not found: {args.input}")
    except Exception:
        stacktrace = traceback.format_exc()
        print(f"Encounter error for input: {args.input}, err: {stacktrace}")

if __name__ == "__main__":
    main()
