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

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter the name of the city to analyze:\n").lower()
    while city not in CITY_DATA:
        print("Warrning: Wrong City Input! Please try again.")
        city = input("Please enter the name of the city to analyze:\n").lower()
    print('The city you have entered is ', city.title())


    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june','all']
    month = input("Please enter a month filter from January to June, or 'all' for no filter:\n").lower()
    while month not in months:
        print("Warrning: Wrong Month Input! Please try again.\n")
        month = input("Please enter the month you want to analyze, or 'all' for no filter:\n").lower()
    if month ==  'all':
        print("You did not enter any filter.")
    else:
        print('The month you have entered is ', month.title())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday','all']
    day = input("Please enter a day filter from Monday to Sunday, or 'all' for no filter:\n").lower()
    while day not in day_of_week:
        print("Warrning: Wrong Day Input! Please try again.\n")
        day = input("Please enter a day filter from Monday to Sunday, or 'all' for no filter:\n").lower()
    if day ==  'all':
        print("You did not enter any filter.")
    else:
        print('The day you have entered is ', day.title())


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
    # load data file into a dataframe by city
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common start hour
    df['hours'] = df['Start Time'].dt.hour
    print('The most common hour is {}.'.format(df['hours'].mode()[0]))
    print('The most common hour count: {}'.format(df['hours'].value_counts().max()))

    # display the earliest Start Time and the latest End Time
    print('The earliest Start Time: {}'.format(df['Start Time'].min()))
    print('The latest End Time: {}'.format(df['End Time'].max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most start station is {}.'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most end station is {}.'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip: From {} to {}'.format(df[['Start Station','End Station']].mode()['Start Station'][0] , df[['Start Station','End Station']].mode()['End Station'][0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    count_duration = df['Trip Duration'].count()
    print('Total Duration: {}\tCount: {}'.format(total_duration,count_duration))
    # display mean travel time
    avg_duration = total_duration / count_duration
    print('Avg Duration: {}'.format(avg_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts().unique()
    print('Subscribers: {}, Customers: {}, Others: {}\n'.format(user_types_count[0],user_types_count[1],user_types_count[2:].sum()))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts().unique()
        print('Male: {}, Female: {}\n'.format(gender_count[0],gender_count[1]))
    except:
        print('No Gender column in this dataset.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        common_birth  = df['Birth Year'].value_counts().index[0]
        print('The earliest year of birth: {}\nThe most recent year of birth: {}\nThe most common year of birth: {}'.format(earliest_birth,most_recent_birth,common_birth))
    except:
        print('No Birth Year column in this dataset.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def df_display(df):
    """Displays rows of df as users want."""

    display = input("Do you want to see some rows in the DataFrame? Enter 'Yes' or 'No'.\n").lower()
    while display != 'yes' and display != 'no':
        display = input("Wrong Input. Enter 'Yes' or 'No'.\n").lower()
    if display == 'yes':
        while True:
            try:
                row_numbers = int(input('how many rows you would like to display each time? Please enter an integer (e.g. 10)\n' ))
                i = row_numbers
                break
            except:
                print('You have enter a wrong input. Please enter an integer!')

        pd.set_option('display.max_columns',200)
        print(df.iloc[:row_numbers])
        while True:
            display_more = input("Do you want more rows to be displayed? Enter 'Yes' or 'No'.\n").lower()
            while display_more != 'yes' and display_more != 'no':
                display_more = input("Wrong Input. Enter 'Yes' or 'No': ").lower()
            if display_more == 'yes':
                less_row_numbers = row_numbers
                row_numbers += i
                print(df.iloc[less_row_numbers:row_numbers])
            else:
                break





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        df_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for using US bikeshare analyzing system!")
            break


if __name__ == "__main__":
	main()
