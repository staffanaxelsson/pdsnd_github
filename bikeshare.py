#!/opt/conda/bin/python
import time
import pandas as pd
import numpy as np
import sys

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
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington).
    attempts = 1
    city_dict = {'chi': 'chicago', 'nyc': 'new york city', 'was': 'washington'}

    while attempts <= 3:
        city = input('Would you like to see data for Chicago, New York City, or Washington? [Enter chi/nyc/was or type full name] ').lower()
        if city[:3] in city_dict.keys():
            city = city_dict[city[:3]]
            break
        elif city in city_dict.values():
            break
        else:
            print('Invalid input')
        attempts += 1
    if attempts > 3:
        print('Too many failed attempts. Exiting')
        sys.exit()
    print('')

    month = 'all'
    month_dict = {'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april', 'may': 'may', 'jun': 'june'}
    day = 'all'
    day_dict = {'mon': 'monday', 'tue': 'tuesday', 'wed': 'wednesday', 'thu': 'thursday', 'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday'}

    attempts_two = 1
    while attempts_two <= 3:
        choice_two = input('Would you like to filter by month, day, both, or no filter? [Enter month, day, both or no] ')

        # get user input for month (all, january, february, ... , june)
        if choice_two.lower() == 'month' or choice_two.lower() == 'both':
            print('')
            attempts = 1
            while attempts <= 3:
                month = input('Which month? [enter 3 first characters or full name] ').lower()
                if month[:3] in month_dict.keys():
                    break
                else:
                    print('Invalid input. Type "jan" or "january", for example. Valid month "jan" to "jun"')
                attempts += 1
            if attempts > 3:
                print('Too many failed attempts. Exiting')
                sys.exit()
            month = month_dict[month[:3]]

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        if choice_two.lower() == 'day' or choice_two.lower() == 'both':
            print('')
            attempts = 1
            while attempts <= 3:
                day = input('Which day? [enter 3 first characters or full name] ').lower()
                if day[:3] in day_dict.keys():
                    break
                else:
                    print('Invalid input. Type "mon" or "monday", for example.')
                attempts += 1
            if attempts > 3:
                print('Too many failed attempts. Exiting')
                sys.exit()
            day = day_dict[day[:3]]
            print('')

        if choice_two.lower() in ['month', 'day', 'both', 'no']:
            break
        else:
            print('Invalid input. Type "month", "day", "both" or "no".')
            attempts_two += 1

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_count = df['month'].value_counts().nlargest(1).to_string(index=False)
    print('The most popular month of travel is: {} [counts: {}]'.format(str(popular_month), popular_month_count))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    popular_day_count = df['day_of_week'].value_counts().nlargest(1).to_string(index=False)
    print('The most popular day of week of travel is: ' + str(popular_day) + ' [counts: ' + popular_day_count + ']')

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df['hour'].value_counts().nlargest(1).to_string(index=False)
    print('The most popular hour of week of travel is: ' + str(popular_hour) + ' [counts: ' + popular_hour_count + ']')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df['Start Station'].value_counts().nlargest(1).to_string(index=False)
    print('The most popular start station is: ' + str(popular_start_station) + ' [counts: ' + popular_start_station_count + ']')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df['End Station'].value_counts().nlargest(1).to_string(index=False)
    print('The most popular end station is: ' + str(popular_end_station) + ' [counts: ' + popular_end_station_count + ']')

    # display most frequent combination of start station and end station trip
    popular_start_end_station = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most popular combination of start and end station is: ')
    print(popular_start_end_station.to_string())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total time duration for travel: ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean time duration for travel: ' + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The number of travelers per user type: ')
    print(user_types.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts().to_string()
    else:
        gender_types = 'The data from ' + city + ' did not include this data.'

    print('The number of travelers per gender type: ' + gender_types)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        born_max = str(int(df['Birth Year'].max()))
        born_min = str(int(df['Birth Year'].min()))
        born_mod = str(int(df['Birth Year'].mode()))
    else:
        born_max = born_min = born_mod = 'The data from ' + city + ' did not include this data.'

    print('The oldest traveler was born: ' + born_min)
    print('The youngest traveler was born: ' + born_max)
    print('The most popular birth year of traveler: ' + born_mod)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    viewdata = input('\nWould you like to view the raw data (first 5 rows)? Enter yes or no.\n')
    row = 1
    if viewdata.lower() == 'yes':
        print(df.iloc[row:row+5])
        while True:
            viewdata = input('\nWould you like to view the next 5 rows? Enter yes or no.\n')
            if viewdata.lower() == 'yes':
                row += 5
                print(df.iloc[row:row+5])
            else:
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
