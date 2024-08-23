## Calculate Total Spending from Different Types of Statements

### Setup

`python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`

## Create Report from Amex PDF Statement

`python runner.py -f sample_file.pdf`

## Create Report from CSV

```bash
usage: activity.py [-h] -c CSV -t {amex,chase,costco}

Run spending activity report

options:
  -h, --help            show this help message and exit
  -c CSV, --csv CSV     CSV input file
  -t {amex,chase}, --type {amex,chase}
                        CC provider type
```
