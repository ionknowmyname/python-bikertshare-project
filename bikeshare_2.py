import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA.keys():     
        city = input("Would you like to see data for Chicago, New York or Washington? ").lower()

        if city not in CITY_DATA.keys():
            print("\nPlease try again with an accepted input.")

    print("You chose {} city".format(city))
    
    # get user input for month (all, january, february, ... , june)
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month =''

    while month not in month_list:
        month = input("Choose between January to june, or All to select all months: ").lower()

        if month not in month_list:
            print("\nPlease try again with an accepted input.")

    print("You chose {} month".format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''

    while day not in day_list:
        day = input("Choose between Monday to Sunday, or All to select all days: ").lower()

        if day not in day_list:
            print("\nPlease try again with an accepted input.")

    print("You chose {} day".format(day))
    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    print("Testing if csv is selected: ", CITY_DATA[city])
    print("month from getfilter: ", month)
    print("day from getfilter: ", day)

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    print("testing month output: ", df['month'].head())

    df['day_of_week'] = df['Start Time'].dt.dayofweek   # returns 0 for Monday- 6 for sunday # day_name, weekday_name
    # print("testing day output: ", df['day_of_week'].head())

    df['hour'] = df['Start Time'].dt.hour

    print("df from load_data(): ", df.head(10))

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        print("month index in load_data(): ", month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        print("print df after filtering by month: ",  df.head())

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        print("day index in load_data(): ", day)

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    print("df to return from load_data()", df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    # df['Start Time'] = pd.to_datetime(df['Start Time'])
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    
    # display the most common month

    # df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0] # axis='index'; axis=0
    print("Most Common Month: ", common_month)

    # display the most common day of week

    # df['day_of_week'] = df['Start Time'].dt.day_name 
    common_day = df['day_of_week'].mode()[0]
    print("Most Common day: ", common_day)

    # display the most common start hour
    # df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most Common start hour: ", common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most Common start station: ", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most Common end station: ", common_end_station)

    # display most frequent combination of start station and end station trip

    # use str.cat to join start & stop stations together into a new column
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    start_to_end = df['Start To End'].mode()[0]
    print("Most frequent combination of start & stop stations: ", start_to_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print("Total trip duration in seconds: ", total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("Average travel duration: ", mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    # print("User types: \n", user_types)
    print("User types: ", user_types)

    # Display counts of gender

    # try block for if no gender column
    try:
        gender = df['Gender'].value_counts()
        print("Users by gender: \n", gender)
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Display earliest, most recent, and most common year of birth
    try:
        early = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth: {}\nThe most recent year of birth: {}\nThe most common year of birth: {}".format(early, recent, most_common))
    except:
        print("There are no birth year column in this file.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    response_list = ['yes', 'no']
    start_loc = 0
    ans = ''

    while ans not in response_list:
        ans = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()

        if ans == "yes":
            print(df.head())
        elif ans not in response_list:
            print("Input does not seem to match any of the accepted responses.")
    
    while (ans == 'yes'):
        ans = input("Do you wish to continue?: ").lower()
        start_loc += 5

        if ans == "yes":
            print(df.iloc[start_loc:start_loc+5])
        elif ans != "yes":
            break
        
        
        

def main():
    while True:
        city, month, day = get_filters()
        print("from get_filters() in main(): {}, {}, {}".format(city, month, day))
        df = load_data(city, month, day)
        # df=load_data('new york','march','monday').shape[0]
        print("df in main(): ", df.head(10))

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
