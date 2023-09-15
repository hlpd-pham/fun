import PyPDF2
import re
import argparse

def get_charges_from_page(page):
    page_content = page.extract_text().split('\n')
    return [l for l in page_content if 'THANK YOU' not in l and '-$' not in l and '$' in l]

def calculate_total_spent(pdf_pages):
    first_page_charges = get_charges_from_page(pdf_pages[0])

    # find where the first line of payment and charges
    for idx, line in enumerate(first_page_charges):
        if 'DATE STATUS DESCRIPTION AMOUNT' in line:
            first_page_charges = first_page_charges[idx+1:]
            break

    charges = first_page_charges[6:]

    if len(pdf_pages) == 1:
        remaining_pages = []
    else:
        remaining_pages = pdf_pages[1:]

    for p in remaining_pages:
        charges.extend(get_charges_from_page(p))

    total = 0

    for c in charges:
        label, amount = c.split('$')
        amount = re.sub('[^\d\.]', '', amount)
        total += float(amount)
        print(f"{label.ljust(55)}{amount.rjust(7)}")

    print('----------------------------------------')
    print(f"Total: {total:.2f}")

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Calculate monthly statement an AMEX PDF file.")
    parser.add_argument("-f", "--file", help="Path to the PDF file.", type=str, required=True)
    args = parser.parse_args()

    # Create a PDF reader object
    reader = PyPDF2.PdfReader(args.file)

    # Calculate total spent
    calculate_total_spent(reader.pages)

