#!/usr/bin/env python
# coding: utf-8

# In[2]:


import argparse
from bank_parser.bank_of_america import parse_bank_of_america

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Process bank statements.')

    # Add an argument for the bank name
    parser.add_argument('bank', type=str, help='Name of the bank to process')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Now, you can access the bank name using args.bank
    bank = args.bank
    
    if bank == "Bank of America":
        parse_bank_of_america()
    elif bank == "PNC Bank":
        pass
    else:
        # Run parse functions of all banks
        parse_bank_of_america()    


if __name__ == "__main__":
    main()


# In[ ]:




