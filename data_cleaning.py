import pandas as pd
from datetime import datetime
import os

def clean_data(input_file, year):
    # Load the raw dataset
    viasatCharging_df_raw = pd.read_csv(input_file)

    # Create a copy of the dataset to clean
    viasatCharging_df = viasatCharging_df_raw.copy()

    # Remove irrelevant columns
    viasatCharging_df = viasatCharging_df.drop(columns=[
        'Address 2',
        'Start SOC',
        'End SOC',
        'OnRamp ID Tag',
        'Payment Terminal Session ID',
        'Org Name',
        'Currency',
        'Fee',
        'Transaction Date (Pacific Time)',
        'Start Time Zone',
        'End Time Zone',
        'County'
    ])

    if 'Vehicle MAC ID' in viasatCharging_df.columns:
        viasatCharging_df = viasatCharging_df.drop(columns=[
        'Vehicle MAC ID'
    ])

    # Only keep information for California
    viasatCharging_df = viasatCharging_df[viasatCharging_df['State/Province'] == 'California']

    # Remove rows with null end date values
    viasatCharging_df = viasatCharging_df[viasatCharging_df['End Date'].notna()]

    # Separating start date and end date into date and time columns
    start_dates = viasatCharging_df['Start Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M').date())
    start_times = viasatCharging_df['Start Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M').time())
    end_dates = viasatCharging_df['End Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M').date())
    end_times = viasatCharging_df['End Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M').time())

    viasatCharging_df = viasatCharging_df.drop(columns=[
        'Start Date',
        'End Date'
    ])

    viasatCharging_df['Start Date'], viasatCharging_df['Start Time'] = start_dates, start_times
    viasatCharging_df['End Date'], viasatCharging_df['End Time'] = end_dates, end_times

    # Convert 'Charging Time (hh:mm:ss)' to timedelta
    viasatCharging_df['Charging Time'] = pd.to_timedelta(viasatCharging_df['Charging Time (hh:mm:ss)'])

    # Filter out rows where charging time is 0
    viasatCharging_df = viasatCharging_df[viasatCharging_df['Charging Time'] != pd.Timedelta(0)]

    # Convert 'Start Date' and 'End Date' back to datetime objects to filter by year
    viasatCharging_df['Start Date'] = pd.to_datetime(viasatCharging_df['Start Date'])
    viasatCharging_df['End Date'] = pd.to_datetime(viasatCharging_df['End Date'])

    # Filter the DataFrame for entries in the desired year
    viasatCharging_df = viasatCharging_df[viasatCharging_df['Start Date'].dt.year == year]

    output_path = f"clean_data/viasatChargingDataClean{year}.csv"
    # Output the cleaned DataFrame to a CSV file

    # Check if the output file already exists
    if os.path.exists(output_path):
        # If the file exists, read the existing data and append the new data
        existing_data = pd.read_csv(output_path)
        combined_data = pd.concat([existing_data, viasatCharging_df], ignore_index=True)
        combined_data.to_csv(output_path, index=False)
    else:
        # If the file does not exist, write the new data to a new file
        viasatCharging_df.to_csv(output_path, index=False)
    viasatCharging_df.to_csv(output_path, index=False)
    
def combine_datasets():
    all_files = [file for file in os.listdir("clean_data") if file.endswith('.csv')]
    combined_df = pd.DataFrame()
    
    for file in all_files:
        df = pd.read_csv(os.path.join("clean_data", file))
        
        # Exclude empty or all-NA columns before concatenating
        non_empty_columns = df.columns[df.notna().any()]
        df = df[non_empty_columns]

        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    # Reset index
    combined_df.reset_index(drop=True, inplace=True)
    
    return combined_df
