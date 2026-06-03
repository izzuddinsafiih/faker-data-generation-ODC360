import pandas as pd
 
def generate_dim_cost_rate():
    print("=== Generating Distinct Dim_Cost_Rate Table ===\n")
    # 1. Base Financial Data (FY26 Target Rates)
    base_band_rates = {
        3: {'GZ': ('CNY', 703), 'SZ': ('CNY', 703), 'MY': ('MYR', 301), 'PH': ('USD', 69), 'HK': ('HKD', 1448), 'SG': ('SGD', 235)},
        4: {'GZ': ('CNY', 945), 'SZ': ('CNY', 1041), 'MY': ('MYR', 554), 'PH': ('USD', 90), 'HK': ('HKD', 1635), 'SG': ('SGD', 265)},
        5: {'GZ': ('CNY', 1190), 'SZ': ('CNY', 1274), 'MY': ('MYR', 593), 'PH': ('USD', 117), 'HK': ('HKD', 1757), 'SG': ('SGD', 285)},
        6: {'GZ': ('CNY', 1461), 'SZ': ('CNY', 1753), 'MY': ('MYR', 748), 'PH': ('USD', 146), 'HK': ('HKD', 2513), 'SG': ('SGD', 407)},
        7: {'GZ': ('CNY', 1916), 'SZ': ('CNY', 2145), 'MY': ('MYR', 1032), 'PH': ('USD', 190), 'HK': ('HKD', 2972), 'SG': ('SGD', 482)},
        8: {'GZ': ('CNY', 2596), 'SZ': ('CNY', 2848), 'MY': ('MYR', 1604), 'PH': ('USD', 314), 'HK': ('HKD', 4346), 'SG': ('SGD', 705)}
    }
 
    exchange_rates = {
        'USD': 1.0, 
        'MYR': 4.09, 
        'CNY': 6.8157, 
        'HKD': 7.8344, 
        'SGD': 1.2712
    }
 
    fiscal_years = {
        'FY25': 0.95, # Simulating FY25 as 5% cheaper than FY26
        'FY26': 1.00, # Base Year
        'FY27': 1.05  # Simulating FY27 as 5% more expensive due to inflation
    }
 
    cost_records = []
    cost_id_counter = 5000 # Starting surrogate key
 
    # 2. Matrix Generation Loop (FY x Band x Region)
    for fy, inflation_multiplier in fiscal_years.items():
        for band, regions in base_band_rates.items():
            for region, (currency, base_local_rate) in regions.items():
                # Apply inflation/deflation based on Fiscal Year
                adjusted_local_rate = round(base_local_rate * inflation_multiplier, 2)
                # Calculate USD conversion
                ex_rate = exchange_rates[currency]
                usd_rate = round(adjusted_local_rate / ex_rate, 2)
                cost_records.append({
                    'Cost_ID': cost_id_counter,
                    'Fiscal_Year': fy,
                    'Region_Code': region,
                    'Lenovo_Band': band,
                    'Local_Currency': currency,
                    'Daily_Rate_Local': adjusted_local_rate,
                    'Exchange_Rate': ex_rate,
                    'Daily_Rate_USD': usd_rate
                })
                cost_id_counter += 1
 
    # 3. Export to CSV
    df_cost = pd.DataFrame(cost_records)
    try:
        df_cost.to_csv('Dim_Cost_Rate.csv', index=False)
        print(f"✅ Dim_Cost_Rate.csv generated successfully with {len(df_cost)} distinct rate profiles.")
    except PermissionError:
        print("❌ ERROR: Please close 'Dim_Cost_Rate.csv' in Excel and try again.")
 
    return df_cost
 
# Run the generator
if __name__ == "__main__":
    df = generate_dim_cost_rate()
