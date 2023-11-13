#!/usr/bin/env python
# coding: utf-8

# In[102]:


try:
    import os
    import fitz
    import time
    import pandas as pd
    import re
    from time import sleep
    from decimal import Decimal
except:
    get_ipython().system('pip install pymupdf')
    get_ipython().system('pip install pandas')
    get_ipython().system('pip install fitz')
    import os
    import fitz
    import time
    import pandas as pd
    import re
    from time import sleep   


# In[103]:


def parse_CITIBANK():
    folder_path = "./data/CITIBANK/input"
    folder_output = "./data/CITIBANK/output"
    
    # Check if the directory exists, and create it if it doesn't
    os.makedirs(folder_output, exist_ok=True)
    date_pattern = r'\d{2}/\d{2}'
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
        flag14 = True
        flag15 = True
        flag16 = True

        beg = ""
        end = ""
        bal = ""
        dep = ""
        witd = ""
        ending_balance = ""
        tot_amount_dep = 0
        tot_amt_wth = 0
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
                        if(flag == False):
                            beg = (i.split('-')[0]) + "," + (i.split(',')[1])
                            end = (i.split('-')[1])
                            flag = True
                            # print(beg, end)
                        if(i.find('Statement Period') != -1):
                            flag = False
                        if(flag2 == False):
                            flag2 = True
                            bal = i
                            last_amount = bal
                            # print(bal)
                        if(flag3 == False):
                            flag3 = True
                            ending_balance = i
                            # print(ending_balance)
                        if(i.find('Beginning Balance:') != -1):
                            flag2 = False
                        if(i.find('Ending Balance:') != -1):
                            flag3 = False
# #                     #####################################################################################################
                    if(flag13 == False):
                        flag13 = True
                        tot_list_dep = (i)
                        
                    if(flag12 == False):
                        tot_list_with = (i)
                        flag12 = True
                        flag13 = False
                        
                    if(i.find('Total Debits/Credits') != -1):
                        flag12 = False
                        flag16 = False
                        
                    if(i == 'Total'):
                        flag10 = False
                        
                    if(flag4 == False):
                        matches = re.findall(date_pattern, i)
                        if (matches and len(i.split()) ==1) or (i.find('Total Debits/Credits') != -1) or cur_page !=page_number:
                            flag4 = True
                            if(flag9 == False):
                                flag9 = True
                                desc.append(s)
                            else:
                                desc2.append(s)
                        else:
                            s+=i+' '
                            
                    if(flag8 == False):
                        flag8 = True
                        if Decimal(last_amount.replace('$', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '')) + Decimal(amt[len(amt) -1].replace('$', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '')) == Decimal(i.replace('$', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '')):
                            debit.append(amt[len(amt) -1])
                            #desc.append(s)
                            date_depos.append(date[len(date) -1])
                            tot_amount_dep+=1
                            cur_page = page_number
                            flag4 = False
                            flag9 = False
                        else:
                            credit.append(amt[len(amt) -1])
                            #desc2.append(s)
                            date_with.append(date[len(date) -1])
                            tot_amt_wth+=1
                            flag4 = False
                            
                        last_amount = i
                    if(flag7 == False):
                        try:
                            if((i[0].isdigit() and len(i.split()) == 1)): #or (i[1].isdigit() and i[0] == '-' and len(i.split()) == 1)):
                                flag7 = True
                                amt.append(i)
                                flag8 = False
                            else:
                                s+=i+' '
                        except:
                            pass
                    if(flag6 == False and flag16 == True):
                        matches = re.findall(date_pattern, i)
                        if matches and len(i.split()) ==1:
                            date.append(matches[0])
                            flag7 = False
                            s = ""
                    if(i.find('Balance') != -1):
                        flag6 = False
                    if(flag15 == False):
                        ledger_amt.append(i)
                        flag15 = True
                    if(flag14 == False):
                        matches = re.findall(date_pattern2, i)
                        if matches and len(i.split()) ==1:
                            date3.append(matches[0])
                            check_num.append(docs[calc-1])
                            # print(i)
                            flag15 = False
                    if(i.find('Checks Paid') != -1):
                        flag14 = False
                    calc+=1

            deposits_items = []
            
            
            # Remove redundant spaces from the beginning and end
            beg = beg.strip()
            end = end.strip()
            bal = bal.strip()
            dep = dep.strip()
            witd = witd.strip()
            ending_balance = ending_balance.strip()
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
            ending_balance = float(ending_balance.replace('$', '').replace(',', ''))
            try:
                subtotal = float(subtotal.replace('$', '').replace(',', ''))
            except:
                pass
            tot_list_dep  = float(tot_list_dep.replace('$', '').replace(',', ''))
            tot_list_with = float(tot_list_with.replace('$', '').replace(',', ''))

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
                # print(len(desc2), len(credit), len(date_with))
                entry = {
                    "date": date_with[i],
                    "Description": desc2[i],
                    "amount": credit[i]
                }
                withdrawal_items.append(entry)

            daily_ledger_balances = []

            for i in range(len(date3)):
                entry = {
                    "Check No.": check_num[i],
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
    # print(date),print(debit), print(desc), print(date_depos), print(credit), print(desc2), print(date_with)


# In[ ]:




