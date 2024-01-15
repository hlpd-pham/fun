#!/opt/homebrew/bin/python3

import argparse
import traceback

def preprocess(lines):
    games = {}

    def get_cube_count(subsets):
        count = {}
        for s in subsets:
            for item in s:
                item = item.strip()
                cube_count, cube_type = item.split(' ')
                count[cube_type] = count.get(cube_type, 0) + int(cube_count)
        return count

    for line in lines:
        game_info, subsets = line.split(':')
        _, game_id = game_info.split(' ')
        game_id = int(game_id)
        subsets = subsets.strip().split(';')
        subsets = [s.strip().split(',') for s in subsets]
        games[game_id] = get_cube_count(subsets)

    return games

def solve(lines):
    total = 0

    RED, GREEN, BLUE = 'red', 'green', 'blue'
    CUBES_HAVE = set([RED, GREEN, BLUE])
    HAVE = {
        RED: 12,
        GREEN: 13,
        BLUE: 14
    }

    # organize lines into games, which is a hashmap
    games = preprocess(lines)
    for game_id, cube_count in games.items():
        if (cube_count.get(RED, 0) <= HAVE[RED] and 
            cube_count.get(GREEN, 0) <= HAVE[GREEN] and
            cube_count.get(BLUE, 0) <= HAVE[BLUE]):
            total += game_id
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
