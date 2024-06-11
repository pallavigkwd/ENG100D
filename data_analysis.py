import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# plot the reasons for ending charging
def reasons_end_charging(viasatCharging_df):
    # Convert NaN values to 'Unknown' and the column to string type
    viasatCharging_df['Ended By'] = viasatCharging_df['Ended By'].fillna('Unknown').astype(str)

    plt.figure(figsize=(10, 6))
    plt.hist(viasatCharging_df['Ended By'])
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.xlabel('Ended By')
    plt.ylabel('Frequency')
    plt.title('Histogram of reasons for ending charging')
    plt.show()

# Convert 'Total Duration (hh:mm:ss)' to total hours
def convert_to_hours(duration):
    hours, minutes, seconds = map(int, duration.split(':'))
    total_hours = hours + minutes / 60 + seconds / 3600
    return total_hours

# plot the total
def total_duration(viasatCharging_df):
    viasatCharging_df['Charging Time (hours)'] = viasatCharging_df['Charging Time (hh:mm:ss)'].apply(convert_to_hours)

    # Define bins for grouping (1-hour increments)
    bins = range(0, int(viasatCharging_df['Charging Time (hours)'].max()) + 1, 1)

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(viasatCharging_df['Charging Time (hours)'], bins=bins)
    plt.xlabel('Charging Time (hours)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Total Duration (1-hour increments)')
    plt.xticks(bins)
    plt.show()

def start_times_grouped_by_hours(viasatCharging_df):
    # Convert "Start Time" to datetime
    viasatCharging_df['Start Time'] = pd.to_datetime(viasatCharging_df['Start Time'], format='%H:%M:%S')

    # Extract the hour from "Start Time"
    viasatCharging_df['Start Hour'] = viasatCharging_df['Start Time'].dt.hour

    # Group by the extracted hour
    start_times_grouped = viasatCharging_df.groupby('Start Hour').size().reset_index(name='Count')

    # Plot the grouped data
    plt.figure(figsize=(10, 6))
    plt.bar(start_times_grouped['Start Hour'], start_times_grouped['Count'])
    plt.xlabel('Hour of the Day')
    plt.ylabel('Start Time Events')
    plt.title('Count of Start Time Events by Hour')
    plt.xticks(start_times_grouped['Start Hour'])
    plt.show()

def end_times_grouped_by_hours(viasatCharging_df):
    # Convert "End Time" to datetime
    viasatCharging_df['End Time'] = pd.to_datetime(viasatCharging_df['End Time'], format='%H:%M:%S')

    # Extract the hour from "End Time"
    viasatCharging_df['End Hour'] = viasatCharging_df['End Time'].dt.hour

    # Group by the extracted hour
    end_times_grouped = viasatCharging_df.groupby('End Hour').size().reset_index(name='Count')

    # Plot the grouped data
    plt.figure(figsize=(10, 6))
    plt.bar(end_times_grouped['End Hour'], end_times_grouped['Count'])
    plt.xlabel('Hour of the Day')
    plt.ylabel('End Time Events')
    plt.title('Count of End Time Events by Hour')
    plt.xticks(end_times_grouped['End Hour'])
    plt.show()

def energy_consumption_by_month(viasatCharging_df):
    viasatCharging_df['Start Date'] = pd.to_datetime(viasatCharging_df['Start Date'])

    viasatCharging_df['Month'] = viasatCharging_df['Start Date'].dt.month

    kwh_per_month = viasatCharging_df.groupby('Month')['Energy (kWh)'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    plt.bar(kwh_per_month['Month'], kwh_per_month['Energy (kWh)'])
    plt.title('Energy Consumed By Month')
    plt.xlabel('Month')
    plt.ylabel('Energy (kWh)')
    plt.show()
    print('Average:', kwh_per_month['Energy (kWh)'].mean())

def charging_trends_per_month(viasatCharging_df):
    dailyTotalEnergy = viasatCharging_df.groupby('Start Date')['Energy (kWh)'].sum().reset_index()
    # Plotting the energy spent by date
    plt.figure(figsize=(12, 6))
    plt.plot(dailyTotalEnergy['Start Date'], dailyTotalEnergy['Energy (kWh)'])
    plt.title('Energy Spent by Date')
    plt.xlabel('Date')
    plt.ylabel('Energy (kWh)')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.show()

def charging_events_per_month_per_year(viasatCharging_df):
    # To be able to work with the data
    viasatCharging_df['Start Date'] = pd.to_datetime(viasatCharging_df['Start Date'])

    # Extract year from 'Start Date'
    viasatCharging_df['Year'] = viasatCharging_df['Start Date'].dt.year

    # Group by year and month to count the number of charging events per month
    charging_per_month = viasatCharging_df.groupby([viasatCharging_df['Year'], viasatCharging_df['Start Date'].dt.month]).size()

    # Unstack the dataframe to have separate columns for each year
    charging_per_month_unstacked = charging_per_month.unstack(level=0)

    # Plotting
    charging_per_month_unstacked.plot(kind='bar', figsize=(10, 6))
    plt.xlabel('Month')
    plt.ylabel('Number of Charging Events')
    plt.title('Number of Charging Events per Month (over the years)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Year')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Define a function to format timedelta to 'hh:mm:ss'
def format_timedelta(td):
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

def daily_data_table(viasatCharging_df):
    # Convert 'Charging Time (hh:mm:ss)' to timedelta
    viasatCharging_df['Charging Time'] = pd.to_timedelta(viasatCharging_df['Charging Time (hh:mm:ss)'])
    viasatCharging_df['Energy (kWh)'] = pd.to_numeric(viasatCharging_df['Energy (kWh)'])

    # Create daily DataFrame
    daily_data = viasatCharging_df.groupby('Start Date').agg(
        total_charging_time=pd.NamedAgg(column='Charging Time', aggfunc='sum'),
        avg_charging_time=pd.NamedAgg(column='Charging Time', aggfunc='mean'),
        max_charging_time=pd.NamedAgg(column='Charging Time', aggfunc='max'),
        min_charging_time=pd.NamedAgg(column='Charging Time', aggfunc='min'),
        total_energy=pd.NamedAgg(column='Energy (kWh)', aggfunc='sum'),
        avg_energy=pd.NamedAgg(column='Energy (kWh)', aggfunc='mean'),
        max_energy=pd.NamedAgg(column='Energy (kWh)', aggfunc='max'),
        min_energy=pd.NamedAgg(column='Energy (kWh)', aggfunc='min')
    ).reset_index()

    # Format timedelta columns in the daily DataFrame
    daily_data['avg_charging_time'] = daily_data['avg_charging_time'].apply(format_timedelta)
    daily_data['max_charging_time'] = daily_data['max_charging_time'].apply(format_timedelta)
    daily_data['min_charging_time'] = daily_data['min_charging_time'].apply(format_timedelta)

    return daily_data

def monthly_data_table(viasatCharging_df):
    # Create monthly DataFrame
    viasatCharging_df['Start Date'] = pd.to_datetime(viasatCharging_df['Start Date'])
    viasatCharging_df['Month'] = viasatCharging_df['Start Date'].dt.month
    viasatCharging_df['Year'] = viasatCharging_df['Start Date'].dt.year

    monthly_data = viasatCharging_df.groupby(['Year', 'Month']).agg(
        total_charging_time=pd.NamedAgg(column='Charging Time', aggfunc='sum'),
        avg_charging_time=pd.NamedAgg(column='Charging Time', aggfunc='mean'),
        max_charging_time=pd.NamedAgg(column='Charging Time', aggfunc='max'),
        min_charging_time=pd.NamedAgg(column='Charging Time', aggfunc='min'),
        total_energy=pd.NamedAgg(column='Energy (kWh)', aggfunc='sum'),
        avg_energy=pd.NamedAgg(column='Energy (kWh)', aggfunc='mean'),
        max_energy=pd.NamedAgg(column='Energy (kWh)', aggfunc='max'),
        min_energy=pd.NamedAgg(column='Energy (kWh)', aggfunc='min')
    ).reset_index()

    # Format timedelta columns in the daily DataFrame
    monthly_data['avg_charging_time'] = monthly_data['avg_charging_time'].apply(format_timedelta)
    monthly_data['max_charging_time'] = monthly_data['max_charging_time'].apply(format_timedelta)
    monthly_data['min_charging_time'] = monthly_data['min_charging_time'].apply(format_timedelta)

    return monthly_data

def average_total_energy_per_day(viasatCharging_df):
    # Create daily data table
    daily_data = daily_data_table(viasatCharging_df)
    
    # Calculate the mean of the 'total_energy' column
    average_energy_per_day = daily_data['total_energy'].mean()
    
    return average_energy_per_day

def average_energy_per_charge_per_day(viasatCharging_df):
    # Create daily data table
    daily_data = daily_data_table(viasatCharging_df)

    # Calculate the number of charges per day
    daily_data['charge_count'] = viasatCharging_df.groupby('Start Date').size().reset_index(name='count')['count']
    
    # Calculate the average energy per charge per day
    daily_data['avg_energy_per_charge'] = daily_data['total_energy'] / daily_data['charge_count']
    
    # Calculate the overall average of avg_energy_per_charge
    overall_avg_energy_per_charge_per_day = daily_data['avg_energy_per_charge'].mean()
    
    return overall_avg_energy_per_charge_per_day

def average_energy_per_charge_per_day(viasatCharging_df, energy_threshold=0.1, duration_threshold=0.0833):
    # Ensure 'Charging Time (hh:mm:ss)' is converted to hours
    viasatCharging_df.loc[:, 'Charging Time (hours)'] = viasatCharging_df['Charging Time (hh:mm:ss)'].apply(convert_to_hours)
    
    # Filter out negligible charges
    filtered_df = viasatCharging_df[
        (viasatCharging_df['Energy (kWh)'] >= energy_threshold) & 
        (viasatCharging_df['Charging Time (hours)'] >= duration_threshold)
    ].copy()  # Use .copy() to avoid the SettingWithCopyWarning
    
    # Convert 'Charging Time (hh:mm:ss)' to timedelta
    filtered_df.loc[:, 'Charging Time'] = pd.to_timedelta(filtered_df['Charging Time (hh:mm:ss)'])
    filtered_df.loc[:, 'Energy (kWh)'] = pd.to_numeric(filtered_df['Energy (kWh)'])

    # Create daily data table
    daily_data = daily_data_table(filtered_df)

    # Calculate the number of charges per day
    daily_data['charge_count'] = filtered_df.groupby('Start Date').size().reset_index(name='count')['count']
    
    # Calculate the average energy per charge per day
    daily_data['avg_energy_per_charge'] = daily_data['total_energy'] / daily_data['charge_count']
    
    # Calculate the overall average of avg_energy_per_charge
    overall_avg_energy_per_charge_per_day = daily_data['avg_energy_per_charge'].mean()
    
    return overall_avg_energy_per_charge_per_day
