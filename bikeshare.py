import time
import math
import pandas as pd
import numpy as np


"""
FUNCTIONS
"""

def get_user_choice(allowed_choices, prompt):
    """
    Gets and validates user choice from a list of allowed choices. Attempts match of any non-zero-size string from user.

        IN:
           (list) allowed_choices                   - all choices allowed for user input
           (str)  prompt                            - prompt for user choice

        OUT:
           (str)  allowed_choices[user_input_index] - item from allowed_choices list matching user choice 
    """

    user_input_index = 0

    # Repeat until user enters correct response and confirms choice
    while True:
        try:
            # Get user input
            user_input = input(prompt).lower()
            # Match test list string sizes to size of user input
            test_list = list((val[:len(user_input)] for val in allowed_choices))

            # Find index from list if user input in list
            # Otherwise except
            if user_input in test_list :
                for i, test_list_val in enumerate(test_list): 
                    if user_input == test_list_val:
                        user_input_index = i
                        break
            else:
                raise ValueError("That is not a valid response.")
            
            # Confirm user choice    
            # If user input is exact match, skip
            if user_input != allowed_choices[user_input_index]:
                if input("Do you mean " + allowed_choices[user_input_index].title() + "? ")[0].lower() != 'y':
                    raise ValueError("Sorry, let's try again.")
            break
        except ValueError as error:
            print(error)

    # Return allowed choice matching user choice
    return allowed_choices[user_input_index]


def get_user_num(num_range, prompt):
    """
    Gets a number from the user and validates it against a certain range

        IN:
           (list) num_range                         - range of allowed inputs, [min, max] - range is inclusive
           (str)  prompt                            - prompt for user choice

        OUT:
           (str)  user_input                        - user input once valid
    """
    while True:
        try:
            # Get user input
            user_input = input(prompt)
            # If user enters all, assign user input to max value, else cast as correct type
            if user_input.lower() == 'all':
                user_input = num_range[1]
                user_input = type(num_range[1])(user_input)
            else:
                user_input = type(num_range[1])(user_input)
                # Check if in valid range
                if user_input < num_range[0] or user_input > num_range[1]:
                    raise ValueError("Value entered is out of range, please try again.")
            break
        except ValueError as error:
            print(error)
    
    return user_input


"""Returns most commonly occurring item in a column"""
def most_common(df, col):
    return df[col].mode()[0]


def count_all(df, col):
    """Prints counts of occurrances for each item in a column"""

    # Print column count if column exists
    if col in df.columns:
        print("Printing " + col + " data:")
        return df[col].dropna(axis = 0).groupby(df[col]).size().reset_index(name='count')
    else:
        print("There is no " + col + " data in this file")


def first_last_common(df, col):
    """Returns a list of first item, last item, most common item from a numerical column"""
    return [df[col].min(), df[col].max(), most_common(df, col)]



"""DATA AND ALLOWED VALUES"""
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


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

    # Get city from user
    city = get_user_choice(list(CITY_DATA.keys()), "Input a city: ")

    # get user input for month (all, january, february, ... , june)
    month = get_user_choice(months, "Input a month between january and june or input all for all months: ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_choice(days, "Input a day of the week or input all for all days: ")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def view_raw_data(df):
    """Asks user if they want to see the raw data and by how many rows"""
    
    if input("Would you like to see the raw data? ")[0].lower() == 'y':
        max_rows = df.shape[0]
        num_rows = get_user_num([1,max_rows], "How many rows would you like to view? (Choose 1 to {}): ".format(max_rows))
        print(df.rename(columns = {'Unnamed: 0' : 'IDs'}).head(num_rows))

def get_time():
    return time.time()

def time_diff(time_start, time_end):
    return time_end - time_start


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = get_time()

    # display the most common month
    print("The most common month for bikeshare is: {}".format(most_common(df, 'month')))

    # display the most common day of week
    print("The most common day of the week for bikeshare is: {}".format(most_common(df, 'day_of_week')))

    # display the most common start hour
    print("The most common hour for bikeshare is: {}".format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time_diff(start_time, get_time())))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = get_time()

    # display most commonly used start station
    print("The most common start station for bikeshare is: {}".format(most_common(df, 'Start Station')))

    # display most commonly used end station
    print("The most common end station for bikeshare is: {}".format(most_common(df, 'End Station')))

    # display most frequent combination of start station and end station trip
    df2 = pd.DataFrame(df.groupby(['Start Station', 'End Station']).size().nlargest(1).reset_index(name = 'Count'))
    print("The most common combination of start and end stations is {} (start) and {} (end)".format(df2['Start Station'][0], df2['End Station'][0]))

    print("\nThis took %s seconds." % (time_diff(start_time, get_time())))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = get_time()

    # display total travel time
    pd.set_option('precision', 2)
    
    print("Total travel time is : {} minutes".format(int(math.ceil(df['Trip Duration'].sum() / 60))))

    # display mean travel time
    print("Mean travel time is : {} minutes".format(int(math.ceil(df['Trip Duration'].mean() / 60))))

    # pd.set_option('precision', 0)


    print("\nThis took %s seconds." % (time_diff(start_time, get_time())))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = get_time()

    # Display counts of user types
    print(count_all(df, 'User Type'))

    print('\n')
    # Display counts of gender
    print(count_all(df, 'Gender'))

    print('\n')
    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        # Function returns earliest, latest, mode - in that order
        birth_list = first_last_common(df, 'Birth Year')
        print("The earliest birth year: {}".format(int(birth_list[0])))
        print("The most recent birth year: {}".format(int(birth_list[1])))
        print("The most common birth year: {}".format(int(birth_list[2])))
    else:
        print("There is no Birth Year data in this file")




    print("\nThis took %s seconds." % (time_diff(start_time, get_time())))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        view_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower()[0] != 'y':
            break


if __name__ == "__main__":
	main()
