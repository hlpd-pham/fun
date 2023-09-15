import argparse
import math
import json

def validate_creator_mapping(creator_mapping):
    """
    Validate that creator percentages sum to 1.
    """
    mapping_sum = sum(creator_mapping.values())
    if not math.isclose(mapping_sum, 1, rel_tol=1e-9):
        raise ValueError(f"Creator mapping does not sum to 1: {creator_mapping}\nSum: {mapping_sum}")


def allocate_budget(budget, creator_mapping):
    '''
    Allocate a budget to creators based on their percentages.
    Returns a dictionary with the allocated amounts.
    '''

    validate_creator_mapping(creator_mapping)
    allocations = {}

    for creator_name, percentage in creator_mapping.items():
        allocation = budget * percentage
        allocations[creator_name] = allocation

    return allocations

def handle_error(err, input_json):
    print(f"Encounter error for input: {input_json}, err: {err}")

def main():
    parser = argparse.ArgumentParser(description='Allocate a budget to creators.')
    parser.add_argument('-i', '--input', required=True, help='JSON file containing budget and distribution for creators')
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as input_file:
            input_json = json.load(input_file)
            budget, distribution = input_json['budget'], input_json['distribution']

            allocations = allocate_budget(budget, distribution)
            print(f"Budget: ${budget}")
            for creator, allocation in allocations.items():
                print(f"Creator: {creator}, budget: ${allocation:.2f}")
    except ValueError as ve:
        handle_error(ve, input_json)
    except TypeError as te:
        handle_error(te, input_json)
    except FileNotFoundError:
        print(f"Input file not found: {args.input}")
    except Exception as e:
        handle_error(e, input_json)

if __name__ == "__main__":
    main()
