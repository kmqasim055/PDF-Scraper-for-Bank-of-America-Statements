#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import fitz
import time
import pandas as pd
import re
from time import sleep
import sys


# In[25]:


def parse_bank_of_america():
    folder_path = "./data/Bank of America/input"
    folder_output = "./data/Bank of America/output"
    
    # Check if the directory exists, and create it if it doesn't
    os.makedirs(folder_output, exist_ok=True)
    date_pattern = r'\d{2}/\d{2}/\d{2}'
    date_pattern2 = r'\d{2}/\d{2}'

    for filename in os.listdir(folder_path):
        flag = True
        flag2 = True
        flag3 = True
        flag4 = True
        flag5 = True
        flag6 = True
        flag7 = True
        flag8 = True
        flag9 = True
        flag10 = True
        flag11 = True
        flag12 = True
        flag13 = True

        acc = ""
        beg = ""
        end = ""
        bal = ""
        dep = ""
        witd = ""
        end_bal = ""
        tot_amount_dep = ""
        tot_amt_wth = ""
        avg_ledj = ""
        tot_list_dep = ""
        sub_card = ""
        tot_list_with = ""
        subtotal = ""

        date = []
        desc = []
        amt = []

        date2 = []
        desc2 = []
        amt2 = []

        ledger_amt = []
        date3 = []
        ####################################################################################################
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            # Open the PDF file
            doc = fitz.open(file_path)
            page_count = doc.page_count
            time.sleep(0.25)
            total_pages = len(doc)
            print("Current PDF Processing: ", file_path)
            for page_number in range(0, total_pages):
                current_page = doc[page_number]
                docs = current_page.get_text().split('\n')
                tour = False
                calc = 0
                for i in docs:
                    #print(i)
                    if page_number == 0:
                        if(i.find('Account number:') != -1):
                            acc = (i.split('Account number:')[1])
                        if(i.find('for') != -1 and i.find('Preferred') == -1 and flag == False):
                            flag = True
                            beg = (i.split('for')[1].split('to')[0])
                            end = (i.split('for')[1].split('to')[1])
                        if(flag2 == False):
                            flag2 = True
                            bal = (i)
                        if(flag3 == False):
                            flag3 = True
                            dep = (i)
                        if(flag4 == False):
                            flag4 = True
                            witd = (i)
                        if(flag5 == False):
                            flag5 = True
                            end_bal = (i)
                        if(i.find('# of deposits') != -1):
                            tot_amount_dep = (i.split(':')[1])
                        if(i.find('# of withdrawals') != -1):
                            tot_amt_wth = (i.split(':')[1])
                        if(i.find('Average ledger balance') != -1):
                            avg_ledj = (i.split(':')[1])      
                        if(i.find('Preferred Rewards') != -1 or i.find('Your Business Advantage') != -1):
                            flag = False
                        if(i.find('Beginning balance') != -1):
                            flag2 = False
                        if(i.find('Deposits') != -1):
                            flag3 = False
                        if(i.find('Withdrawals') != -1):
                            flag4 = False
                        if(i.find('Ending balance') != -1):
                            flag5 = False
                    #####################################################################################################
                    if(flag8 == False):
                        tot_list_dep = (i)
                        flag12 = False
                        flag8 = True
                    if(flag9 == False):
                        tot_list_with = (i)
                        flag9 = True
                    if(flag13 == False):
                        subtotal = (i)
                        # print('njjn')
                        flag13 = True
                    if(i.find('Total withdrawals and other debits') != -1):
                        flag9 = False
                    if(i.find('Total deposits and other credits') !=-1):
                        flag8 = False
                    if(i.find('Subtotal for card account') != -1):
                        flag13 = False
                        # print(';;wd')
                    if(flag7 == False):
                        try:
                            if((i[0].isdigit() and len(i.split()) == 1) or (i[1].isdigit() and i[0] == '-' and len(i.split()) == 1)):
                                flag7 = True
                                if(flag12 == False):
                                    desc2.append(s)
                                    amt2.append(i)
                                else:
                                    desc.append(s)
                                    amt.append(i)
                            else:
                                s+=i+' '
                        except:
                            pass
                    if(flag6 == False and tot_list_with ==""):
                        matches = re.findall(date_pattern, i)
                        if matches and len(i.split()) ==1:
                            if(flag12 == False):
                                date2.append(matches[0])
                            else:
                                date.append(matches[0])
                            # print(i)
                            flag7 = False
                            s = ""

                    if(i.find('Amount') != -1):
                        flag6 = False

                    if(flag11 == False):
                        ledger_amt.append(i)
                        flag11 = True
                    if(flag10 == False):
                        matches = re.findall(date_pattern2, i)
                        if matches and len(i.split()) ==1:
                            date3.append(matches[0])
                            # print(i)
                            flag11 = False
                    if(i.find('Daily ledger balances') != -1):
                        flag10 = False

            deposits_items = []
            
            
            # Remove redundant spaces from the beginning and end
            acc = acc.strip()
            beg = beg.strip()
            end = end.strip()
            bal = bal.strip()
            dep = dep.strip()
            witd = witd.strip()
            end_bal = end_bal.strip()
            tot_amount_dep = tot_amount_dep.strip()
            tot_amt_wth = tot_amt_wth.strip()
            avg_ledj = avg_ledj.strip()
            tot_list_dep = tot_list_dep.strip()
            sub_card = sub_card.strip()
            tot_list_with = tot_list_with.strip()
            subtotal = subtotal.strip()
            
            # Remove redundant spaces from the beginning and end of each string in the list
            desc = [item.strip() for item in desc]
            desc2 = [item.strip() for item in desc2]
            ledger_amt = [item.strip() for item in ledger_amt]
            
            
            # Remove dollar signs and commas, then convert to float
            bal = float(bal.replace('$', '').replace(',', ''))
            dep = float(dep.replace('$', '').replace(',', ''))
            witd = float(witd.replace('$', '').replace(',', ''))
            end_bal = float(end_bal.replace('$', '').replace(',', ''))
            tot_amount_dep = float(tot_amount_dep.replace('$', '').replace(',', ''))
            tot_amt_wth = float(tot_amt_wth.replace('$', '').replace(',', ''))
            avg_ledj = float(avg_ledj.replace('$', '').replace(',', ''))
            try:
                subtotal = float(subtotal.replace('$', '').replace(',', ''))
            except:
                pass
            tot_list_dep  = float(tot_list_dep.replace('$', '').replace(',', ''))
            tot_list_with = float(tot_list_with.replace('$', '').replace(',', ''))

            # Assuming 'amt' and 'amt2' are lists of strings
            # Remove dollar signs and commas, then convert each element to float
            amt = [float(amount.replace('$', '').replace(',', '')) for amount in amt]
            amt2 = [float(amount.replace('$', '').replace(',', '')) for amount in amt2]

            # Assuming 'ledger_amt' is a list of strings
            # Remove dollar signs and commas, then convert each element to float
            ledger_amt = [float(amount.replace('$', '').replace(',', '')) for amount in ledger_amt]

            for i in range(len(date)):
                entry = {
                    "date": date[i],
                    "Description": desc[i],
                    "amount": amt[i]
                }
                deposits_items.append(entry)

            withdrawal_items = []

            for i in range(len(date2)):
                entry = {
                    "date": date2[i],
                    "Description": desc2[i],
                    "amount": amt2[i]
                }
                withdrawal_items.append(entry)

            daily_ledger_balances = []

            for i in range(len(date3)):
                entry = {
                    "date": date3[i],
                    "Balance": ledger_amt[i]
                }
                daily_ledger_balances.append(entry)
            
            
            # Create the result dictionary
            result = {
                "title": None,
                "account_number": acc,
                "begin_date": beg,
                "end_date": end,
                "beginning_balance": bal,
                "total_deposits": dep,
                "total_withdrawals": witd,
                "ending_balance": end_bal,
                "total_amount_deposits": tot_amount_dep,
                "total_amount_withdrawals": tot_amt_wth,
                "average_ledger_balance": avg_ledj,
                "deposits_items": deposits_items,
                "total_list_deposits": tot_list_dep,
                "subtotal_for_card_account": subtotal,
                "withdrawal_items": withdrawal_items,
                "total_list_withdrawals": tot_list_with,
                "daily_ledger_balances": daily_ledger_balances
            }

            # Create the final dictionary
            ledger_data = {
                "message": "success",
                "result": result
            }

            # Save as JSON
            import json

            # Assuming 'filename' is defined somewhere
            with open(os.path.join(folder_output, filename + '.json'), 'w') as json_file:
                json.dump(ledger_data, json_file, indent=3)


# In[ ]:




