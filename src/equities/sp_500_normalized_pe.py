import matplotlib.pyplot as plt
import pandas as pd


# From https://fred.stlouisfed.org/
m2_data = pd.read_csv('data/M2SL.csv')
m2_data_source = "https://fred.stlouisfed.org/series/M2SL"
dgs10_data = pd.read_csv('data/DGS10.csv')
dgs10_data_source = "https://fred.stlouisfed.org/series/DGS10"

# Macrotrends Data Download

# S&P 500 PE Ratio - 90 Year Historical Chart

# DISCLAIMER AND TERMS OF USE: HISTORICAL DATA IS PROVIDED "AS IS" AND SOLELY
# FOR INFORMATIONAL PURPOSES - NOT FOR TRADING PURPOSES OR ADVICE.
# NEITHER MACROTRENDS LLC NOR ANY OF OUR INFORMATION PROVIDERS WILL BE LIABLE
# FOR ANY DAMAGES RELATING TO YOUR USE OF THE DATA PROVIDED.

# ATTRIBUTION: Proper attribution requires clear indication of the data source as "www.macrotrends.net".
# A "dofollow" backlink to the originating page is also required if the data is displayed on a web page.
sp500_data = pd.read_csv('data/sp-500-pe-ratio-price-to-earnings-chart.csv')
sp500_data_source = "https://www.macrotrends.net/2577/sp-500-pe-ratio-price-to-earnings-chart"

def calculate_sp500_normalized_pe_m2(sp500_data, m2_data):
    """
    Calculate the normalized P/E ratio for the S&P 500 index.

    Parameters:
    sp500_data (pd.DataFrame): A DataFrame containing the S&P 500 index data with columns 'date' and 'value'.
    m2_data (pd.DataFrame): A DataFrame containing the M2 money supply data with columns 'observation_date' and 'M2SL'.

    Returns:
    pd.DataFrame: A DataFrame with columns 'date', 'value', 'M2SL', and 'Normalized_PE'.
    """
    # Convert date columns to datetime for proper matching
    sp500_data['date'] = pd.to_datetime(sp500_data['date'])
    m2_data['observation_date'] = pd.to_datetime(m2_data['observation_date'])
    m2_data["M2SL"] = m2_data["M2SL"] / 1000  # Convert M2SL to trillions for better readability

    # Merge the S&P 500 data with the M2 data on the 'date' column. If there are any missing dates in either DataFrame, they will be excluded from the merged result.
    merged_data = pd.merge(sp500_data, m2_data, left_on='date', right_on='observation_date', how='inner')
    merged_data.drop(columns=['observation_date'], inplace=True)

    # Check if merge was successful
    if merged_data.empty:
        print("Warning: No matching dates found between datasets")
        print(f"SP500 date range: {sp500_data['date'].min()} to {sp500_data['date'].max()}")
        print(f"M2 date range: {m2_data['observation_date'].min()} to {m2_data['observation_date'].max()}")
        return pd.DataFrame(columns=['date', 'value', 'M2SL', 'Normalized_PE'])

    # Calculate the normalized P/E ratio
    merged_data['Normalized_PE'] = merged_data['value'] / merged_data['M2SL']
    merged_data.to_csv('data/sp500_normalized_pe.csv', index=False)

    # Plot the normalized P/E ratio over time
    plt.figure(figsize=(12, 6))
    plt.plot(merged_data['date'], merged_data['Normalized_PE'], label='Normalized P/E Ratio', color='blue')
    plt.title('S&P 500 Normalized P/E Ratio Over Time (Using M2 Money Supply)')
    plt.xlabel('Date')
    plt.ylabel('Normalized P/E Ratio')
    # Add text box with data sources
    textstr = f'Source: {sp500_data_source} & {m2_data_source}'
    plt.gcf().text(0.5, 0.01, textstr, ha='center', fontsize=8)
    plt.legend()
    plt.grid()
    plt.savefig('reports/figures/sp500_normalized_pe.png')

def calculate_sp500_normalized_pe_dgs10(sp500_data, dgs10_data):
    """
    Calculate the normalized P/E ratio for the S&P 500 index using the 10-year Treasury yield.

    Parameters:
    sp500_data (pd.DataFrame): A DataFrame containing the S&P 500 index data with columns 'date' and 'value'.
    dgs10_data (pd.DataFrame): A DataFrame containing the 10-year Treasury yield data with columns 'DATE' and 'DGS10'.

    Returns:
    pd.DataFrame: A DataFrame with columns 'date', 'value', 'DGS10', and 'Normalized_PE'.
    """
    # Convert date columns to datetime for proper matching
    sp500_data['date'] = pd.to_datetime(sp500_data['date'])
    dgs10_data['observation_date'] = pd.to_datetime(dgs10_data['observation_date'])

    # Merge the S&P 500 data with the DGS10 data on the 'date' column.
    # Drop dates from before 1962 to ensure we have overlapping data.
    # If DSG10 data is missing for any date in the S&P 500 data, use the last available DGS10 value (forward fill) to ensure we have a complete dataset for the normalized P/E calculation.
    merged_data = pd.merge(sp500_data, dgs10_data, left_on='date', right_on='observation_date', how='left')
    merged_data.drop(columns=['observation_date'], inplace=True)
    merged_data['DGS10'] = merged_data['DGS10'].fillna(method='ffill')  # Forward fill to handle missing DGS10 values
    # Drop any remaining rows with missing DGS10 values after forward fill
    merged_data.dropna(subset=['DGS10'], inplace=True)

    # Check if merge was successful
    if merged_data.empty:
        print("Warning: No matching dates found between datasets")
        print(f"SP500 date range: {sp500_data['date'].min()} to {sp500_data['date'].max()}")
        print(f"DGS10 date range: {dgs10_data['observation_date'].min()} to {dgs10_data['observation_date'].max()}")
        return pd.DataFrame(columns=['date', 'value', 'DGS10', 'Normalized_PE'])

    # Calculate the normalized P/E ratio
    merged_data['Normalized_PE'] = merged_data['value'] / merged_data['DGS10']
    merged_data.to_csv('data/sp500_normalized_pe_dgs10.csv', index=False)

    # Plot the normalized P/E ratio over time
    plt.figure(figsize=(12, 6))
    plt.plot(merged_data['date'], merged_data['Normalized_PE'], label='Normalized P/E Ratio (DGS10)', color='orange')
    plt.title('S&P 500 Normalized P/E Ratio Over Time (Using DGS10)')
    plt.xlabel('Date')
    plt.ylabel('Normalized P/E Ratio')
    # Add text box with data sources
    textstr = f'Source: {sp500_data_source} & {dgs10_data_source}'
    plt.gcf().text(0.5, 0.01, textstr, ha='center', fontsize=8)
    plt.legend()
    plt.grid()
    plt.savefig('reports/figures/sp500_normalized_pe_dgs10.png')

if __name__ == "__main__":
    calculate_sp500_normalized_pe_m2(sp500_data, m2_data)
    calculate_sp500_normalized_pe_dgs10(sp500_data, dgs10_data)