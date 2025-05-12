import argparse

import numpy as np
import pandas as pd

AMEX = "amex"
CHASE = "chase"
CITI = "citi"
ALLOWED_CC_TYPES = [AMEX, CHASE, CITI]
ROW_SEPARATORS = "------------------------------------------------------------"


def print_df(df, cols):
    longest_row = np.max(df.apply(lambda row: len(row["Description"]), axis=1))
    for _, row in df.iterrows():
        for c in cols:
            if c == "Description":
                print(f"{row[c]:<{longest_row}}", end=" ")
            else:
                print(row[c], end=" ")
        print()


def create_amex_report(df):
    pattern = r"MOBILE PAYMENT - THANK YOU"
    mask = df.Description.str.contains(pattern, regex=True)
    columns = ["Date", "Description", "Amount"]
    df_filtered = df[~mask]
    large = df_filtered[df_filtered.Amount > 300]
    monthly_spend = df_filtered[df_filtered.Amount <= 300]

    print(f"{ROW_SEPARATORS}\nLarge Transactions (> 300): {sum(large.Amount)}")
    print_df(large, columns)
    print(f"{ROW_SEPARATORS}\nMonthly Spending (<= 300): {sum(monthly_spend.Amount)}")
    print_df(monthly_spend, columns)


def create_chase_report(df):
    columns = ["Transaction Date", "Description", "Amount"]
    df = df[columns]
    df.loc[:, "Amount"] = df.Amount * -1
    chase_pattern = r"Payment Thank You-Mobile"
    chase_mask = df.Description.str.contains(chase_pattern, regex=True)
    chase_filtered = df[~chase_mask]
    costco_mask = chase_filtered.Description.str.contains("COSTCO")
    costco = chase_filtered[costco_mask]
    amzn = chase_filtered[
        chase_filtered.Description.apply(
            lambda x: any(element in x for element in ["AMZN", "Amazon", "AMAZON"])
        )
    ]
    others = chase_filtered[
        ~chase_filtered.Description.apply(
            lambda x: any(
                element in x for element in ["AMZN", "Amazon", "COSTCO", "AMAZON"]
            )
        )
    ]

    print(f"{ROW_SEPARATORS}\nCOSTCO: {sum(costco.Amount):.2f}")
    print_df(costco, columns)
    print(f"{ROW_SEPARATORS}\nAMZN: {sum(amzn.Amount):.2f}")
    print_df(amzn, columns)
    print(f"{ROW_SEPARATORS}\nOthers: {sum(others.Amount):.2f}")
    print_df(others, columns)


def create_citi_report(df):
    columns = ["Date", "Description", "Debit"]
    df = df[columns]
    citi_pattern = r"ONLINE PAYMENT, THANK YOU"
    citi_mask = df.Description.str.contains(citi_pattern, regex=True)
    citi_filtered = df[~citi_mask]

    costco_mask = citi_filtered.Description.str.contains("COSTCO")
    costco = citi_filtered[costco_mask]
    others = citi_filtered[~costco_mask]

    print(f"{ROW_SEPARATORS}\nCOSTCO: {sum(costco.Debit):.2f}")
    print_df(costco, columns)
    print(f"{ROW_SEPARATORS}\nOthers: {sum(others.Debit):.2f}")
    print_df(others, columns)


def create_report(csv_file, cc_type):
    function_map = {
        AMEX: create_amex_report,
        CHASE: create_chase_report,
        CITI: create_citi_report,
    }
    df = pd.read_csv(csv_file)
    print("Report Type:", cc_type.upper())
    if cc_type not in function_map:
        raise Exception(
            f"cc_type {cc_type} is not valid, allow types: {ALLOWED_CC_TYPES}"
        )

    function_map[cc_type](df)


if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Run spending activity report")
    parser.add_argument("-c", "--csv", help="CSV input file", type=str, required=True)
    parser.add_argument(
        "-t",
        "--type",
        help="CC provider type",
        type=str,
        required=True,
        choices=ALLOWED_CC_TYPES,
    )
    args = parser.parse_args()

    create_report(args.csv, args.type)
