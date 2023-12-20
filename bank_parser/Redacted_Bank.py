#!/usr/bin/env python
# coding: utf-8

# In[264]:


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


# In[270]:


def extract_tables_from_pdf(filepath):
    # Extract tables from PDF using camelot
    tables = camelot.read_pdf(filepath, flavor='stream', pages='all', suppress_stdout=True)

    # Lists to store data
    dates = []
    descriptions = []
    column3_values = []
    column4_values = []

    date_pattern2 = r'\b\d{1,2}/\d{1,2}\b'

    c = 0

    # Iterate through each table
    for i, table in enumerate(tables, start=1):

        #print(f"\nTable {i} Columns:", table.df.columns)
        # Print headers
        #print("Headers:", list(table.df.columns))
    #     try:
    #         print(table.df[2][2], '*', table.df[3][2],"*", table.df[0])
    #     except:
    #         pass

        # Initialize variables to store row data
        current_date = None
        current_description = ""
        current_column3 = None
        current_column4 = None

        if table.df[0][0] == 'Transaction history':
            c+=1

        if c > 1:
            break

        flag = True
        flag2 = True

        # Process each row in the table
        for index, row in table.df.iterrows(): 
            try:
                if 'description' in table.df[1][2].lower() or flag == True:
                    for iterate in table.df[2]:
                        if 'Deposits/' in iterate:
                            # print("dep yes 1")
                            flag = False
                            break
                    for iterate in table.df[3]:
                        if 'Withdrawals/' in iterate:
                            # print("With yes 1")
                            flag2 = False
                            break
                    if flag == False and flag2 == False:
                        date_value = row[0]
                        description_value = row[1]
                        column3_value = row[2]
                        column4_value = row[3]
                elif 'description' in table.df[2][2].lower() or flag == True:
                    for iterate in table.df[3]:
                        if 'Deposits/' in iterate:
                            flag = False
                            # print("dep yes")
                            break
                    for iterate in table.df[4]:
                        if 'Withdrawals/' in iterate:
                            # print("With yes")
                            flag2 = False
                            break
                    if flag == False and flag2 == False:
                        date_value = row[0]
                        description_value = row[2] 
                        column3_value = row[3]
                        column4_value = row[4]
                else:
                    break
            except:
                break

            # Skip if date is None
            if date_value is None:
                continue

            matches = re.findall(date_pattern2, date_value)
            # Check if the date is not nan
            if matches and len(date_value.split()) == 1:
                # Append values to lists
                dates.append(current_date)
                descriptions.append(current_description)
                column3_values.append(current_column3)
                column4_values.append(current_column4)

                # Update current date and reset accumulated data
                current_date = date_value
                current_description = description_value
                current_column3 = column3_value
                current_column4 = column4_value
            else:
                # Append description if date is nan
                try:
                    current_description += " " + str(description_value)
                except:
                    pass

        # Append the last accumulated data for the table
        if current_date is not None:
            dates.append(current_date)
            descriptions.append(current_description)
            column3_values.append(current_column3)
            column4_values.append(current_column4)
        # break

    # Print or use the separated lists as needed
    # print("Date:", dates)
    # print("Description:", descriptions)
    # print("Deposits:", column3_values)
    # print("Withdrawals:", column4_values)
    # Create a DataFrame
    data = {'Date': dates, 'Description': descriptions, 'Deposits': column3_values, 'Withdrawals': column4_values}
    df = pd.DataFrame(data)

    # Drop rows with None in the 'Date' column
    df = df.dropna(subset=['Date'])
    deposits_df = df[df['Deposits'].notna() & (df['Deposits'] != '')]
    withdrawals_df = df[df['Withdrawals'].notna() & (df['Withdrawals'] != '')]

    return deposits_df[['Date', 'Description', 'Deposits']], withdrawals_df[['Date', 'Description', 'Withdrawals']]


# In[271]:


def parse_redacted_bank():
    folder_path = "./data/REDACTED/input"
    folder_output = "./data/REDACTED/output"
    
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
                    if(flag == False and flag2 == True):
                        beg = i
                        flag2 = False
                        flag = True
                    if(flag3 == False and flag5 == True):
                        ending_balance = i
                        flag3 = True
                    if(i.find('Ending balance on') != -1):
                        end = i.split('Ending balance on')[1]
                        flag3 = False
                    if(i.find('balance') != -1):
                        flag = False
                    #####################################################################################################
                    if(flag11 == False):
                        flag11 = True
                        tot_list_with = (i)
                    if(flag10 == False):
                        tot_list_dep = (i)
                        flag11 = False
                        flag10 = True
                        flag5 = False
                    if(i == 'Totals ' and flag5 == True):
                        flag10 = False
                        flag5 = True
                    if(i.find("Gap in check sequence") != -1 and flag12 == False):
                        flag15 = False
                    if(flag13 == False):
                        ledger_amt.append(i)
                        flag13 = True
                    if(flag12 == False and flag15 == True):
                        matches = re.findall(date_pattern2, i)
                        if matches and len(i.split()) ==1:
                            date3.append(matches[0])
                            check_num.append(docs[calc-1])
                            flag13 = False
                    if(i.find('Summary of checks written') != -1):
                        flag12 = False
                    calc+=1
            if(max(Decimal(tot_list_dep.replace('$', '').replace(',', '')), Decimal(tot_list_with.replace('$', '').replace(',', ''))) == Decimal(tot_list_dep.replace('$', '').replace(',', ''))):
                bal= max(Decimal(tot_list_dep.replace('$', '').replace(',', '')), Decimal(tot_list_with.replace('$', '').replace(',', ''))) - min(Decimal(tot_list_dep.replace('$', '').replace(',', '')), Decimal(tot_list_with.replace('$', '').replace(',', ''))) - Decimal(ending_balance.replace('$', '').replace(',', ''))
            else:
                bal= max(Decimal(tot_list_dep.replace('$', '').replace(',', '')), Decimal(tot_list_with.replace('$', '').replace(',', ''))) - min(Decimal(tot_list_dep.replace('$', '').replace(',', '')), Decimal(tot_list_with.replace('$', '').replace(',', ''))) + Decimal(ending_balance.replace('$', '').replace(',', ''))
            
            bal = abs(bal)
            beg = end.split('/')[0] + '/1'
            # Call the function to extract tables and process data row by row
            table_depos, table_with = extract_tables_from_pdf(file_path)
            tot_amount_dep = len(table_depos['Deposits'].tolist())
            debit = table_depos['Deposits'].tolist()
            desc = table_depos['Description'].tolist()
            date_depos = table_depos['Date'].tolist()
            
            tot_amt_wth = len(table_with['Withdrawals'].tolist())
            credit = table_with['Withdrawals'].tolist()
            desc2 = table_with['Description'].tolist()
            date_with = table_with['Date'].tolist()
            deposits_items = []
            
            # Remove redundant spaces from the beginning and end
            beg = beg.strip()
            end = end.strip()
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
            # tot_amt_wth = float(tot_amt_wth.replace('$', '').replace(',', ''))
            # avg_ledj = float(avg_ledj.replace('$', '').replace(',', ''))
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
                "beginning_balance": float(bal),
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


# In[168]:


# def extract_tables_from_pdf(filepath):
#     # Read PDF file and extract tables
#     tables = tabula.read_pdf(filepath, pages='all', multiple_tables=True)

#     # Lists to store data
#     dates = []
#     descriptions = []
#     column3_values = []
#     column4_values = []

#     # Iterate through each table
#     for i, table in enumerate(tables, start=1):
#         try:
#             if(table.columns[0] == 'Number'):
#                 break
#             # Print column names
#             print(f"\nTable {i} Column Names: {list(table.columns)}")

#             # Initialize variables to store row data
#             current_date = None
#             current_description = ""
#             current_column3 = None
#             current_column4 = None

#             row_first = 0
#             # Process each row in the table
#             for index, row in table.iterrows():

#                 if(row_first == 0):
#                     row_first = 1
#                     if(table.columns[1] == 'Unnamed: 0' or len(table.columns) == 6):
#                         # Extract data from each column
#                         date_value = table.columns[0]
#                         description_value = table.columns[2]
#                         column3_value = table.columns[3]
#                         column4_value = table.columns[4]
#                     else:
#                         # Extract data from each column
#                         date_value = table.columns[0]
#                         description_value = table.columns[1]
#                         column3_value = table.columns[2]
#                         column4_value = table.columns[3]

#                     # Check if the date is not nan
#                     if pd.notna(date_value):
#                         # Update current date and reset accumulated data
#                         current_date = date_value
#                         current_description = description_value
#                         current_column3 = column3_value
#                         current_column4 = column4_value
#                     else:
#                         # Append description if date is nan
#                         try:
#                             current_description += " " + str(description_value)
#                         except:
#                             pass
#                     index = 0

#                 if(table.columns[1] == 'Unnamed: 0' or len(table.columns) == 6):
#                     # Extract data from each column
#                     date_value = row[0]
#                     description_value = row[2]
#                     column3_value = row[3]
#                     column4_value = row[4]
#                 else:
#                     # Extract data from each column
#                     date_value = row[0]
#                     description_value = row[1]
#                     column3_value = row[2]
#                     column4_value = row[3]

#                 # Check if the date is not nan
#                 if pd.notna(date_value):
#                     # Append values to lists
#                     dates.append(current_date)
#                     descriptions.append(current_description)
#                     column3_values.append(current_column3)
#                     column4_values.append(current_column4)

#                     # Update current date and reset accumulated data
#                     current_date = date_value
#                     current_description = description_value
#                     current_column3 = column3_value
#                     current_column4 = column4_value
#                 else:
#                     # Append description if date is nan
#                     try:
#                         current_description += " " + str(description_value)
#                     except:
#                         pass

#             # Append the last accumulated data for the table
#             if current_date is not None:
#                 dates.append(current_date)
#                 descriptions.append(current_description)
#                 column3_values.append(current_column3)
#                 column4_values.append(current_column4)
#         except:
#             pass


#     # Print or use the separated lists as needed
# #     print("Date:", dates)
# #     print("Description:", descriptions)
# #     print("deposits:", column3_values)
# #     print("withdrawals:", column4_values)
    
#      # Create a DataFrame
#     data = {'Date': dates, 'Description': descriptions, 'Deposits': column3_values, 'Withdrawals': column4_values}
#     df = pd.DataFrame(data)
    
#     # Replace 'Unnamed: 0' with NaN in both 'Deposits' and 'Withdrawals' columns
#     df['Deposits'] = df['Deposits'].replace('Unnamed: 0', 'Unnamed: 1').replace('Unnamed: 1', 'Unnamed: 2').replace('Unnamed: 2', pd.NA)
#     df['Withdrawals'] = df['Withdrawals'].replace('Unnamed: 0', 'Unnamed: 1').replace('Unnamed: 1', 'Unnamed: 2').replace('Unnamed: 2', pd.NA)

#     # Separate dataframes without NaN values
#     deposits_df = df.dropna(subset=['Deposits'])
#     withdrawals_df = df.dropna(subset=['Withdrawals'])
    
#     return deposits_df[['Date', 'Description', 'Deposits']], withdrawals_df[['Date', 'Description', 'Withdrawals']]

