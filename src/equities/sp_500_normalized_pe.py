import matplotlib.pyplot as plt
import pandas as pd


# Macrotrends Data Download

# S&amp;P 500 PE Ratio - 90 Year Historical Chart

# DISCLAIMER AND TERMS OF USE: HISTORICAL DATA IS PROVIDED "AS IS" AND SOLELY
# FOR INFORMATIONAL PURPOSES - NOT FOR TRADING PURPOSES OR ADVICE.
# NEITHER MACROTRENDS LLC NOR ANY OF OUR INFORMATION PROVIDERS WILL BE LIABLE
# FOR ANY DAMAGES RELATING TO YOUR USE OF THE DATA PROVIDED.

# ATTRIBUTION: Proper attribution requires clear indication of the data source as "www.macrotrends.net".
# A "dofollow" backlink to the originating page is also required if the data is displayed on a web page.

def calculate_sp500_normalized_pe(sp500_data, m2_data):
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
    plt.title('S&P 500 Normalized P/E Ratio Over Time')
    plt.xlabel('Date')
    plt.ylabel('Normalized P/E Ratio')
    plt.legend()
    plt.grid()
    plt.savefig('reports/sp500_normalized_pe.png')
    plt.show()

    return merged_data[['date', 'value', 'M2SL', 'Normalized_PE']]

if __name__ == "__main__":

    # Example usage
    sp500_data = pd.read_csv('data/sp-500-pe-ratio-price-to-earnings-chart.csv')
    print(sp500_data.head())

    m2_data = pd.read_csv('data/M2SL.csv')

    result = calculate_sp500_normalized_pe(sp500_data, m2_data)
    print(result)