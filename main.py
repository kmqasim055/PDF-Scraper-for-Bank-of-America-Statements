#!/usr/bin/env python
# coding: utf-8

# In[2]:


import argparse
from bank_parser.bank_of_america import parse_bank_of_america
from bank_parser.capital_one_bank import parse_capital_one_bank

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Process bank statements.')

    # Add an argument for the bank name
    parser.add_argument('bank', nargs='?', type=str, help='Name of the bank to process')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Now, you can access the bank name using args.bank
    bank = args.bank
    
    if bank == "Bank of America" or bank is None:
        parse_bank_of_america()
    if bank == "Capital One Bank" or bank is None:
        parse_capital_one_bank()
    if bank == "PNC Bank" or bank is None:
        pass


if __name__ == "__main__":
    main()
