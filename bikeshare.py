import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ('chicago', 'new york city', 'washington')
    global city
    while True:
        city = input("Which city would you like to see data for: Chicago, New York City, or Washington? ").lower()
        if city in cities:
            print("Okay, let's look at the data for {}.".format(city.title()))
            break
        elif city not in cities:
            print("Invalid entry. Please enter Chicago, New York City, or Washington.")
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    while True:
        month = input("Which month(s) would you like to see data for: All or a month from January through June? ").lower()
        if month in months:
            print("Okay, let's look at the data for {}.".format(month.title()))
            break
        elif month not in months:
            print("Invalid entry. Please enter a valid month.")
            continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    while True:
        day = input("Which day(s) would you like to see data for: All or a day from Monday through Sunday? ").lower()
        if day in days:
            print("Okay, let's look at the data for {}.".format(day.title()))
            break
        elif day not in days:
            print("Invalid entry. Please enter a valid day of the week.")
            continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    # Create a dictionary with month numbers as keys
    month_dict = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
    }
    # Find the common month using the mode and the dictionary
    common_month = month_dict[df['Month'].mode()[0]]
    print("The most common month is {}.".format(common_month))

    # TO DO: display the most common day of week
    common_day = df['Day'].mode()[0]
    print("The most common day of the week is {}.".format(common_day))

    # TO DO: display the most common start hour
    # extract the start hour as a new column
    df['Start Hour'] = df['Start Time'].dt.hour
    # Create a dictionary with hour numbers as keys
    hour_dict = {
    0: "12:00 AM", 1: "1:00 AM", 2: "2:00 AM", 3: "3:00 AM", 4: "4:00 AM", 5: "5:00 AM", 
    6: "6:00 AM", 7: "7:00 AM", 8: "8:00 AM", 9: "9:00 AM", 10: "10:00 AM", 11: "11:00 AM",
    12: "12:00 PM", 13: "1:00 PM", 14: "2:00 PM", 15: "3:00 PM", 16: "4:00 PM", 17: "5:00 PM",
    18: "6:00 PM", 19: "7:00 PM", 20: "8:00 PM", 21: "9:00 PM", 22: "10:00 PM", 13: "11:00 PM"
    }
    common_hour = hour_dict[df['Start Hour'].mode()[0]]
    print("The most common start hour is {}.".format(common_hour))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("The most common start station is {}.".format(start_station))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("The most common end station is {}.".format(end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combo'] = "starting at " + df['Start Station'] + "\nand ending with " + df['End Station']
    combo = df['Station Combo'].mode()[0]
    print("The most frequent station combination is {}.".format(combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # Convert columns to datetime format and then extract the hours and minutes and add them
    df['End Time'] = pd.to_datetime(df['End Time'])
    end_time = (df['End Time'].dt.hour * 60) + df['End Time'].dt.minute
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    st_time = (df['Start Time'].dt.hour * 60) + df['Start Time'].dt.minute
    # Calculate the sum of each column and then calculate the total time in hours
    total_time = abs(sum(st_time) - sum(end_time)) / 60
    print("Total travel time was {} hours.".format(total_time))

    # TO DO: display mean travel time
    mean_time = total_time / df['End Time'].count()
    print("The mean travel time was {} hours.".format(mean_time))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User type counts:")
    print(user_types)
    print("\n")
    
    # Create an if statement to skip the following sections if Washington is selected
    invalid_cities = ('washington')
    if city in invalid_cities:
        print("Sorry, gender and birth year data are not available for Washington.")
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        return
            
    # TO DO: Display counts of gender
    gender_types = df['Gender'].value_counts()
    print("Gender counts:")
    print(gender_types)
    print("\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    min_yr = int(df['Birth Year'].min())
    max_yr = int(df['Birth Year'].max())
    common_yr = int(df['Birth Year'].mode())
    print("Birth year data:")
    print("The earliest birth year is {}.".format(min_yr))
    print("The most recent birth year is {}.".format(max_yr))
    print("The most common birth year is {}.".format(common_yr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    # Instructor recommendation to implement: move this function out of main()
    def display_raw_data(df):
        """Displays raw data on bikeshare users and their trips."""
        # Create a variable to track the row index
        x = 0
        print("\nRaw Data Display Option")
        print("NOTE: if you have filtered the data to a specific month and/or day, the displayed data\nwill skip rows to only show the data for the selected time period.")
        # Determine if the user wants to see raw data on trips from the city selected
        raw = input("\nWould you like to view individual trip data? Enter yes or no: ").lower()
        pd.set_option('display.max_columns',200)
        # Create a while loop with logic to determine if the data should be displayed and to increment the data shown
        # Instructor recommendation: Add check for invalid entry (i.e. 'ye')
        while True:
            if raw == 'no':
                break
            elif raw == 'yes':
                print(df.iloc[x:x + 5])
                raw = input("\nWould you like to view more individual trip data? Enter yes or no: ").lower()
                x += 5
                continue
            else:
                raw = input("\nYour input is invalid. Please enter only 'yes' or 'no': ").lower()
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input("\nWould you like to restart? Enter yes or no: ")
        if restart.lower() != 'yes':
            break
            

if __name__ == "__main__":
	main()
