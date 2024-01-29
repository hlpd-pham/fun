## Calculate Total Spending from Different Types of Statements

### Prerequisite

`pip3 install PyPDF2`

## Create Report from Amex PDF Statement

`python runner.py -f sample_file.pdf`

## Create Report from CSV


```bash
usage: activity.py [-h] -c CSV -t {amex,chase}

Run spending activity report

options:
  -h, --help            show this help message and exit
  -c CSV, --csv CSV     CSV input file
  -t {amex,chase}, --type {amex,chase}
                        CC provider type
```

