import re
import argparse
import pandas as pd

AMEX = 'amex'
CHASE = 'chase'
ALLOWED_CC_TYPES = [AMEX, CHASE]
ROW_SEPARATORS = '------------------------------------------------------------'

def create_amex_report(df):
    pattern = r'MOBILE PAYMENT - THANK YOU'
    mask = df.Description.str.contains(pattern, regex = True)
    df_filtered = df[~mask]
    large = df_filtered[df_filtered.Amount > 300]
    monthly_spend = df_filtered[df_filtered.Amount <= 300]

    print(f'{ROW_SEPARATORS}\nLarge Transactions (> 300): {sum(large.Amount)}')
    print(large)
    print(f'{ROW_SEPARATORS}\nMonthly Spending (<= 300): {sum(monthly_spend.Amount)}')
    print(monthly_spend)


def crease_chase_report(df):
    columns = ['Transaction Date', 'Description', 'Amount']
    df = df[columns]
    df.loc[:, 'Amount'] = df.Amount * -1
    chase_pattern = r'Payment Thank You-Mobile'
    chase_mask = df.Description.str.contains(chase_pattern, regex=True)
    chase_filtered = df[~chase_mask]
    costco_mask = chase_filtered.Description.str.contains("COSTCO")
    costco = chase_filtered[costco_mask]
    amzn = chase_filtered[chase_filtered.Description.apply(lambda x: any(element in x for element in ['AMZN', 'Amazon']))]
    others = chase_filtered[~chase_filtered.Description.apply(lambda x: any(element in x for element in ['AMZN', 'Amazon','COSTCO']))]

    print(f'{ROW_SEPARATORS}\nCOSTCO: {sum(costco.Amount):.2f}')
    print(costco)
    print(f'{ROW_SEPARATORS}\nAMZN: {sum(amzn.Amount):.2f}')
    print(amzn)
    print(f'{ROW_SEPARATORS}\nOthers: {sum(others.Amount):.2f}')
    print(others)



def create_report(csv_file, cc_type):
    df = pd.read_csv(csv_file)
    print('Report Type:', cc_type.upper())
    if cc_type == AMEX:
        create_amex_report(df)
    else:
        crease_chase_report(df)

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Run spending activity report")
    parser.add_argument("-c", "--csv", help="CSV input file", type=str, required=True)
    parser.add_argument("-t", "--type", help="CC provider type", type=str, required=True, choices=ALLOWED_CC_TYPES)
    args = parser.parse_args()

    create_report(args.csv, args.type)
