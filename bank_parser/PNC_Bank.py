#!/usr/bin/env python
# coding: utf-8

# In[106]:


try:
    import os
    import fitz
    import time
    import pandas as pd
    import re
    from time import sleep
    from decimal import Decimal
    import numpy as np
    import camelot
except:
    get_ipython().system('pip install pymupdf')
    get_ipython().system('pip install pandas')
    get_ipython().system('pip install fitz')
    get_ipython().system('pip install camelot-py[cv]')
    import os
    import fitz
    import time
    import pandas as pd
    import re
    from time import sleep
    from decimal import Decimal
    import numpy as np
    import camelot


# In[107]:


def extract_tables_from_pdf(filepath):
    a = None
    # Extract tables from PDF using camelot
    tables = camelot.read_pdf(filepath, flavor='stream', pages='all', suppress_stdout=True)
    # Iterate through each table
    for i, table in enumerate(tables, start=1):
        # print(table.df)
        for tab in table.df[0]:
            if(tab.find('Deposits and Other Additions') != -1):
                a = table.df[1][len(table.df[1]) -1]
                b = table.df[4][len(table.df[4]) -1]
                break
        if a != None:
            break
    return a, b


# In[120]:


def parse_pnc_bank():
    # Define a regular expression pattern to match amounts
    amount_pattern = re.compile(r'([\d,]+(\.\d{1,2})?)') 
    folder_path = "./data/PNCBANK/input"
    folder_output = "./data/PNCBANK/output"
    
    # Check if the directory exists, and create it if it doesn't
    os.makedirs(folder_output, exist_ok=True)
    date_pattern = r'\d{2}/\d{2}'
    date_pattern2 = r'\b\d{1,2}/\d{1,2}\b'

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
        flag14 = True
        flag15 = True

        beg = ""
        end = ""
        bal = ""
        dep = ""
        witd = ""
        ending_balance = ""
        tot_amount_dep = ""
        tot_amt_wth = ""
        avg_ledj = ""
        tot_list_dep = ""
        sub_card = ""
        tot_list_with = ""
        subtotal = ""
        last_amount = ""

        date_depos = []
        date_with = []
        desc = []
        desc2 = []
        credit = []
        debit = []
        amt = []
        date = []

        ledger_amt = []
        check_num = []
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
                    # print(i)
                    if page_number == 0:
                        if(i.find('For the Period') != -1):
                            beg = (i.split('For the Period')[1].split('to')[0])
                            end = (i.split('For the Period')[1].split('to')[1])
                    if(flag == False):
                        match = amount_pattern.search(i)
                        if match:
                            flag = True
                            bal = i
                            last_amount = bal
                            ending_balance = docs[calc+3]
                            tot_list_dep = docs[calc+1]
                            tot_list_with = docs[calc+2]
                    if(flag2 == False):
                        match = amount_pattern.search(i)
                        if match:
                            flag2 = True
                            avg_ledj = i
                    if(i == 'Balance Summary'):
                        flag = False
                    if(i == 'Average ledger'):
                        flag2 = False
#                     #####################################################################################################
                    if i == "Checks and Other Deductions" and flag6 == False:
                        flag15 = False
                    if(flag7 == False):
                        try:
                            matches = re.findall(date_pattern2, i)
                            if flag6 == False:
                                if ((matches and len(i.split()) ==1) or i.find('continued on next page') != -1 or i.find('ATM Deposits and Additions') != -1 or i.find('ACH Additions') != -1 or i.find('Other Additions') != -1 or i.find('Fee Refunds') != -1 or flag15 == False):
                                    desc.append(s)
                                    flag7 = True
                                else:
                                    match = amount_pattern.search(i)
                                    if match and len(i.split()) == 1 and re.match(r'^[0-9,]*\.[0-9]+$', i):
                                        amt.append(i)
                                        debit.append(i)
                                    else:
                                        s+=i+' '
                            else:
                                if ((matches and len(i.split()) ==1) or i.find('continued on next page') != -1 or i.find('POS Purchases') != -1 or i.find('ACH Deductions') != -1 or i.find('Service Charges and Fees') != -1 or i.find('Other Deductions') != -1 or i.find('Page') != -1 or i.find('ATM/Misc. Debit Card Transactions') != -1 or i.find('Detail of Services Used During Current Period') != -1 or flag15 == False):
                                    desc2.append(s)
                                    flag7 = True
                                    if(len(desc2) != len(credit)):
                                        print("Here --> ", len(desc2), len(credit), desc2, credit)
                                else:
                                    match = amount_pattern.search(i)
                                    if match and len(i.split()) == 1 and re.match(r'^[0-9,]*\.[0-9]+$', i):
                                        amt.append(i)
                                        credit.append(i)
                                    else:
                                        s+=i+' '
                        except:
                            pass
                    if((flag6 == False or flag5 == False) and flag15 == True):
                        matches = re.findall(date_pattern2, i)
                        if matches and len(i.split()) ==1:
                            date.append(matches[0])
                            if flag6 == False:
                                date_depos.append(matches[0])
                            else:
                                date_with.append(matches[0])
                            flag7 = False
                            s = ""
                    if(i.find('Activity Detail') != -1):
                        flag6 = False
                        flag9 = False
                        flag12 = True
                    if(i == 'Debit Card Purchases' and flag9 == False):
                        flag5 = False
                        flag15 = True
                        flag6 = True
                    if(i.find('Detail of Services Used During Current Period') != -1):
                        flag5 = True
                    if(flag13 == False):
                        ledger_amt.append(i)
                        flag13 = True
                    if(flag12 == False):
                        matches = re.findall(date_pattern2, i)
                        if matches and len(i.split()) ==1:
                            date3.append(matches[0])
                            flag13 = False
                    if(i == 'Daily Balance'):
                        flag12 = False
                    calc+=1

            deposits_items = []
            
            tot_amount_dep, tot_amt_wth = extract_tables_from_pdf(file_path)
            
#             print(beg, end, bal, ending_balance, tot_amount_dep, tot_amt_wth, avg_ledj)
#             print('**************************************')
#             print(date_depos, debit, desc)
#             print("**************************************")
#             print(date_with, credit, desc2)
#             print(len(date_with), len(credit), len(desc2))
            
            
            # Remove redundant spaces from the beginning and end
            beg = beg.strip()
            end = end.strip()
            bal = bal.strip()
            dep = dep.strip()
            witd = witd.strip()
            ending_balance = ending_balance.strip()
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
            check_num = [item.strip() for item in check_num]
            
            
            # Remove dollar signs and commas, then convert to float
            bal = float(bal.replace('$', '').replace(',', ''))
            try:
                dep = float(dep.replace('$', '').replace(',', ''))
            except:
                pass
            try:
                witd = float(witd.replace('$', '').replace(',', ''))
            except:
                pass
            try:
                tot_amount_dep = float(tot_amount_dep.replace('$', '').replace(',', ''))
            except:
                pass
            tot_amt_wth = float(tot_amt_wth.replace('$', '').replace(',', ''))
            # avg_ledj = float(avg_ledj.replace('$', '').replace(',', ''))
            ending_balance = float(ending_balance.replace('$', '').replace(',', ''))
            try:
                subtotal = float(subtotal.replace('$', '').replace(',', ''))
            except:
                pass
            tot_list_dep  = float(tot_list_dep.replace('$', '').replace(',', ''))
            tot_list_with = float(tot_list_with.replace('$', '').replace(',', ''))
            avg_ledj = float(avg_ledj.replace('$', '').replace(',', ''))

            # Assuming 'amt' and 'amt2' are lists of strings
            # Remove dollar signs and commas, then convert each element to float
            amt = [float(amount.replace('$', '').replace(',', '')) for amount in amt]
            # amt2 = [float(amount.replace('$', '').replace(',', '')) for amount in amt2]

            # Assuming 'ledger_amt' is a list of strings
            # Remove dollar signs and commas, then convert each element to float
            ledger_amt = [float(amount.replace('$', '').replace(',', '')) for amount in ledger_amt]

            for i in range(len(date_depos)):
                entry = {
                    "date": date_depos[i],
                    "Description": desc[i],
                    "amount": debit[i]
                }
                deposits_items.append(entry)

            withdrawal_items = []

            for i in range(len(date_with)):
                entry = {
                    "date": date_with[i],
                    "Description": desc2[i],
                    "amount": credit[i]
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
                "begin_date": beg,
                "end_date": end,
                "beginning_balance": bal,
                "ending_balance": ending_balance,
                "total_withdrawals": witd,
                "total_deposits": tot_amount_dep,
                "total_withdrawals": tot_amt_wth,
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


# In[122]:


# parse_pnc_bank() 


# In[ ]:




