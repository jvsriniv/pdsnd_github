import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}

DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city
    city = ''
    i = 0
    while city not in CITY_DATA.keys() and i <= 3:
        print("\nPlease enter a city [Allowed cities are : Chicago, New York City, Washington]:")
        city = input().lower()
        i = i + 1
        if city not in [cty.lower() for cty in CITY_DATA.keys()]:
            if i >= 3:
                print("\nYou exceeded maximum trails. Please retry running the program.")
                sys.exit()
            print("\nPlease check your input. Allowed cities are: Chicago, New York City, Washington.")
            print("Restarting...")

    # get user input for month
    month = ''
    i = 0
    while month not in MONTH_DATA.keys() and i <= 3:
        print("\nPlease enter a month [Allowed months are : January to June, ALL for all months]:")
        month = input().lower()
        i = i + 1
        if month not in [mnth.lower() for mnth in MONTH_DATA.keys()]:
            if i >= 3:
                print("\nYou exceeded maximum trails. Please retry running the program.")
                sys.exit()
            print("\nPlease check your input. Allowed months are: ALL, January to June.")
            print("Restarting...")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    i = 0
    while day not in DAY_LIST and i <= 3:
        print("\nPlease enter a day [Allowed days are : Sunday to Saturday, ALL]:")
        day = input().lower()
        i = i + 1
        if day not in [dy.lower() for dy in DAY_LIST]:
            if i >= 3:
                print("\nYou exceeded maximum trails. Please retry running the program.")
                sys.exit()
            print("\nPlease check your input. Allowed days are : Sunday to Saturday, ALL")
            print("Restarting...")

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month = MONTH_DATA[month]
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]
#        TODO: may be using .title() on RHS improves performance(?)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    print('The most common month:', list(MONTH_DATA.keys())[list(MONTH_DATA.values()).index(most_common_month)].title())

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of the week:', most_common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:',  most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    trips = df.groupby(['Start Station', 'End Station'])
    most_frequent_trip = trips.size().nlargest(1)
    print('The most frequent combination of start station and end station trip:\n', most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel duration is', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel duration is', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('The counts of user types are as below:\n', user_types_counts)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\nThe counts of gender are as below:\n', gender_counts)
    else:
        print('\nThere is no gender information in the data for this city.')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_yob = df['Birth Year'].min()
        print('\nThe earliest year of birth is', earliest_yob)
        recent_yob = df['Birth Year'].max()
        print('The most recent year of birth is', recent_yob)
        most_common_yob = df['Birth Year'].mode()[0]
        print('The most common year of birth is', most_common_yob)
    else:
        print('\nThere is no birth year information in the data for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays data based on user's response."""
    raw_data_index = 0
    response = input('Would you like to view 5 rows of the trip data? Yes or No').lower()
    while True:
        if response not in ['yes', 'no']:
            response = input('You provided an invalid input. Please type Yes or No.').lower()
        elif response == 'no':
            return
        elif response == 'yes':
            print(df.iloc[raw_data_index : raw_data_index + 5])
            raw_data_index += 5
        response = input('Would you like to 5 more rows?  Yes or No').lower()





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
