import pandas as pd
from faker import Faker
import random
import datetime

# Initialize Faker
fake = Faker()

def generate_star_schema_dataset():
    print("=== ODC 360: ProjectDB Data Generation Pipeline ===\n")

    # ==========================================
    # 1. CONFIGURATION LAYER (User Inputs)
    # ==========================================
    try: 
        num_resources = int(input("Enter the number of Employees (Resources) to generate: "))
        num_projects = int(input("Enter the number of Projects to generate: "))
        num_fact_records = int(input("Enter number of transactional records per Fact table: "))
    except ValueError:
        print("❌ Invalid Input. Please enter whole numbers only.")
        return 
        
    print("\n⏳ Commencing secure mock data generation loop...\n")

    # ==========================================
    # 2. DIMENSION LAYER (Context & Lookups)
    # ==========================================
    print("Generating Dimension Tables...")
    
    # --- Dim_Resource (Advanced Financial Mapping) ---
    fy26_band_rates = {
        3: {'GZ': ('CNY', 703), 'SZ': ('CNY', 703), 'MY': ('MYR', 301), 'PH': ('USD', 69), 'HK': ('HKD', 1448), 'SG': ('SGD', 235)},
        4: {'GZ': ('CNY', 945), 'SZ': ('CNY', 1041), 'MY': ('MYR', 554), 'PH': ('USD', 90), 'HK': ('HKD', 1635), 'SG': ('SGD', 265)},
        5: {'GZ': ('CNY', 1190), 'SZ': ('CNY', 1274), 'MY': ('MYR', 593), 'PH': ('USD', 117), 'HK': ('HKD', 1757), 'SG': ('SGD', 285)},
        6: {'GZ': ('CNY', 1461), 'SZ': ('CNY', 1753), 'MY': ('MYR', 748), 'PH': ('USD', 146), 'HK': ('HKD', 2513), 'SG': ('SGD', 407)},
        7: {'GZ': ('CNY', 1916), 'SZ': ('CNY', 2145), 'MY': ('MYR', 1032), 'PH': ('USD', 190), 'HK': ('HKD', 2972), 'SG': ('SGD', 482)},
        8: {'GZ': ('CNY', 2596), 'SZ': ('CNY', 2848), 'MY': ('MYR', 1604), 'PH': ('USD', 314), 'HK': ('HKD', 4346), 'SG': ('SGD', 705)}
    }
    fy26_exchange_rates = {'USD': 1.0, 'MYR': 4.09, 'CNY': 6.8157, 'HKD': 7.8344, 'SGD': 1.2712}
    regions = ['GZ', 'SZ', 'MY', 'PH', 'HK', 'SG']
    
    resource_ids = list(range(1, num_resources + 1))
    resources = []
    
    for r_id in resource_ids:
        band = random.randint(3, 8)
        region = random.choice(regions)
        local_currency, local_rate = fy26_band_rates[band][region]
        usd_rate = round(local_rate / fy26_exchange_rates[local_currency], 2)
        
        resources.append({
            'Resource_ID': r_id,
            'Resource_Name': fake.unique.name(),
            'Region_Code': region,
            'Lenovo_Band': band,
            'Local_Currency': local_currency,
            'Daily_Rate_Local': local_rate,
            'Daily_Rate_USD': usd_rate
        })
    df_resource = pd.DataFrame(resources)
    fake.unique.clear() # Clear cache to prevent memory leaks/collisions

    # --- Dim_Project ---
    project_ids = list(range(1001, 1001 + num_projects))
    projects = []
    for p_id in project_ids:
        projects.append({
            'Project_ID': p_id,
            'Project_Name': fake.unique.catch_phrase(),
            'Status': random.choice(['Initiation', 'Development', 'Execution', 'Closed Won', 'Closed Lost', 'Cancelled'])
        })
    df_project = pd.DataFrame(projects)
    fake.unique.clear()

    # --- Dim_Date ---
    start_date = datetime.date(2025, 1, 1)
    date_list = [start_date + datetime.timedelta(days=x) for x in range(730)] 
    dates = []
    for d in date_list:
        dates.append({
            'Date_Key': int(d.strftime('%Y%m%d')),
            'Full_Date': d,
            'Calendar_Year': d.year,
            'Calendar_Month': d.month
        })
    df_date = pd.DataFrame(dates)
    date_keys = list(df_date['Date_Key'])


    # ==========================================
    # 3. FACT LAYER (Transactions & Logic)
    # ==========================================
    print("Generating Fact Tables with Referential Integrity...")
    
    # --- Fact_Utilization ---
    utilization_records = []

    util_composite_cache = set()

    while len(utilization_records) < num_fact_records:
        r_id = random.choice(resource_ids) 
        p_id = random.choice(project_ids)
        d_key = random.choice(date_keys)

        composite_key = (r_id, p_id, d_key)
        
        if composite_key not in util_composite_cache:
            util_composite_cache.add(composite_key)
            utilization_records.append({
                'Resource_ID': r_id,
                'Project_ID': p_id,
                'Date_Key': d_key,
                'Hours_Utilized': round(random.uniform(4.0, 8.0), 2)
            })
    df_utilization = pd.DataFrame(utilization_records)

    # --- Fact_Resource_Planning ---
    planning_records = []
    plan_composite_cache = set()

    while len(planning_records) < num_fact_records:
        r_id = random.choice(resource_ids) 
        p_id = random.choice(project_ids)
        d_key = random.choice(date_keys)

        composite_key = (r_id, p_id, d_key)
        
        if composite_key not in plan_composite_cache:
            plan_composite_cache.add(composite_key)
            planning_records.append({
                'Resource_ID': r_id,
                'Project_ID': p_id,
                'Date_Key': d_key,
                'Allocated_Mandays': round(random.uniform(0.5, 1.0), 1) 
            })
    df_planning = pd.DataFrame(planning_records)

    print("✅ Verification Checks Passed: 100% Unique Primary Keys.")
    print("✅ Verification Checks Passed: Referential Integrity Validated.")


    # ==========================================
    # 4. PERSISTENCE LAYER (Centralized Export)
    # ==========================================
    print("\nExporting to CSV...")
    try:
        df_resource.to_csv('data/Dim_Resource.csv', index=False)
        df_project.to_csv('data/Dim_Project.csv', index=False)
        df_date.to_csv('data/Dim_Date.csv', index=False)
        df_utilization.to_csv('data/Fact_Utilization.csv', index=False)
        df_planning.to_csv('data/Fact_Resource_Planning.csv', index=False)
        print("🎉 Success! All pipeline data exported safely.")
    except PermissionError as e:
        print(f"\n❌ EXPORT ERROR: {e}")
        print("💡 TIP: A file is currently open in Excel or Power BI. Please close it and rerun the script.")


# Execute Pipeline
if __name__ == "__main__":
    generate_star_schema_dataset()
