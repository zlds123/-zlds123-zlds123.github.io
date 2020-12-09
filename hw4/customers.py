import pandas as pd
import numpy as np
import warnings
from loans import tidy_loans
warnings.filterwarnings('ignore')

def tidy_customer(account, districts, links, cards, transactions, payment_orders, loans):
    loans_tidy = tidy_loans(loans)
    combined1 = pd.merge(account, districts, left_on='district_id', right_on='id', how='left').drop(['id_y'], axis=1)
    combined1.rename(columns={'id_x': 'account_id', 'name': 'district_name', 'date': 'open_date'}, inplace=True)
    combined3 = pd.merge(cards, links, left_on='link_id', right_on='id', how='right')
    combined3.rename(columns={'id_x': 'card_id', 'type_x': 'card_type', 'issue_date': 'card_issue_date', 'type_y': 'card_type'}, inplace=True)
    combined3.drop(['id_y'], axis=1, inplace=True)
    card_account = combined3.groupby(['account_id']).count().reset_index()
    links_account = links.groupby(['account_id']).count().reset_index()
    links_account.rename(columns={'client_id': 'num_customers'}, inplace=True)
    combined2 = pd.merge(combined1, links_account, left_on='account_id', right_on='account_id', how='left')
    combined4 = pd.merge(combined2, card_account, left_on='account_id', right_on='account_id', how='left')
    combined4.rename(columns={'card_id': 'credit_cards'}, inplace=True)
    combined5 = pd.merge(combined4, loans_tidy, left_on='account_id', right_on='account_id', how='left')
    combined5.rename(columns={'id_y': 'loan'}, inplace=True)
    combined5['loan'] = combined5['loan'].apply(lambda x: False if np.isnan(x) else True)
    combined5.rename(columns={'amount': 'loan_amount', 'payments': 'loan_payments', 'term': 'loan_term', 'active_status': 'loan_status'}, inplace=True)
    combined5['loan_default'] = combined5['payment'].apply(lambda x: True if x == 'default' else (False if x in ['full', 'in_progress'] else x))
    max_withdrawal = transactions.groupby(['account_id'])['amount'].agg(max)
    min_withdrawal = transactions.groupby(['account_id'])['amount'].agg(min)  
    combined6 = pd.merge(combined5, max_withdrawal, left_on='account_id', right_on='account_id', how='left')
    combined7 = pd.merge(combined6, min_withdrawal, left_on='account_id', right_on='account_id', how='left')
    combined7.rename(columns={'amount_x': 'max_withdrawal', 'amount_y': 'min_withdrawal'}, inplace=True)
    payment_counts = payment_orders.groupby(['account_id'])['id'].count().reset_index()
    payment_counts.columns = ['account_id', 'cc_payments']
    combined8 = pd.merge(combined7, payment_counts, left_on='account_id', right_on='account_id',how='left')
    max_balance = transactions.groupby(['account_id'])['balance'].agg(max).to_frame().reset_index().rename(columns={'balance': 'max_balance'})
    min_balance = transactions.groupby(['account_id'])['balance'].agg(min).to_frame().reset_index().rename(columns={'balance': 'min_balance'})
    combined9 = pd.concat([combined8, max_balance, min_balance], axis=1)
    final_df = combined9[['account_id', 'district_name', 'open_date', 'statement_frequency', 'num_customers', 'credit_cards', 'loan', 'loan_amount', 'loan_payments', 'loan_term', 'loan_status', 'loan_default', 'max_withdrawal', 'min_withdrawal', 'cc_payments', 'max_balance', 'min_balance']]
    final_df = final_df.iloc[:,2:]
    final_df.to_csv('customers_py.csv')  
    return final_df 
      
if __name__ == '__main__':
    account = pd.read_csv('data/accounts.csv')
    districts = pd.read_csv('data/districts.csv')
    links = pd.read_csv('data/links.csv')
    cards = pd.read_csv('data/cards.csv')
    transactions = pd.read_csv('data/transactions.csv')
    payment_orders = pd.read_csv('data/payment_orders.csv')
    loans = pd.read_csv('data/loans.csv')
    tidy_customer(account, districts, links, cards, transactions, payment_orders, loans)