import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def tidy_loans(df):
    non_status_fields = ['id', 'account_id', 'date', 'amount', 'payments']
    status_fields = [e for e in df.columns.tolist() if e not in non_status_fields]
    binary_status_fields = df[status_fields].replace('X', 1).replace('-', 0)
    loans2 = pd.concat([df[non_status_fields], binary_status_fields],axis=1)
    melted = loans2.melt(id_vars=non_status_fields)
    loans3 = melted[melted['value'] == 1]
    loans3['term'] = loans3['variable'].apply(lambda x: int(x.split("_")[0]))
    loans3['status'] = loans3['variable'].apply(lambda x: x.split("_")[1])
    loans3['active_status'] = loans3['status'].apply(lambda x: 'expired' if x in ['A','B'] else 'current')
    loans3['payment'] = loans3['status'].apply(lambda x: 'full' if x == 'A' else ('in_progress' if x == 'C' else 'default'))
    loans4 = loans3.drop(['variable', 'value','status'], axis=1)
    loans4.reset_index(drop=True, inplace=True)
    loans4.to_csv('loans_py.csv')
    return loans4

if __name__ == '__main__':
    loans = pd.read_csv('data/loans.csv')
    tidy_loans(loans)