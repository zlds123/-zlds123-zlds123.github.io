import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def tidy_district(df):
    # Create 4 separate columns from municipality_info
    df['num_municipality_with_population_<500'] = df['municipality_info'].apply(lambda x: int(x.split(",")[0][1:]))
    df['num_municipality_with_population_500-1999'] = df['municipality_info'].apply(lambda x: int(x.split(",")[1]))
    df['num_municipality_with_population_2000-9999'] = df['municipality_info'].apply(lambda x: int(x.split(",")[2]))
    df['num_municipality_with_population_>10000'] = df['municipality_info'].apply(lambda x: int(x.split(",")[3][:-1]))
    # Create 2 separate columns for unemployment rate
    df['unemployment_rate_95'] = df['unemployment_rate'].apply(lambda x: x.split(",")[0][1:])
    df['unemployment_rate_96'] = df['unemployment_rate'].apply(lambda x: x.split(",")[1][:-1])
    # Create 2 separate columns for crime rate
    df['crime_rate_95'] = df['commited_crimes'].apply(lambda x: x.split(",")[0][1:])
    df['crime_rate_96'] = df['commited_crimes'].apply(lambda x: x.split(",")[1][:-1])
    # Drop the municiplality info, unemployment rate and commited crimes
    df = df.drop(['unemployment_rate', 'commited_crimes', 'municipality_info'],axis=1)
    # Convert data type
    df['unemployment_rate_95'] = df['unemployment_rate_95'].apply(lambda x: float(x) if x != 'NA' else np.nan)
    df['unemployment_rate_96'] = df['unemployment_rate_96'].apply(lambda x: float(x) if x != 'NA' else np.nan)
    df['crime_rate_95'] = df['crime_rate_95'].apply(lambda x: float(x) if x != 'NA' else np.nan)
    df['crime_rate_96'] = df['crime_rate_96'].apply(lambda x: float(x) if x != 'NA' else np.nan)
    df.to_csv("district_py.csv")
    return df

if __name__ == '__main__':
    districts = pd.read_csv("data/districts.csv")
    tidy_district(districts)