#!/opt/homebrew/bin/python3

import argparse

def solve(lines):
    pass

def main():
    parser = argparse.ArgumentParser(description='Advent of code day x part x')
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
