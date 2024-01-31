import time
import pandas as pd
import numpy as np

CITY_NAME = {
    "chicago": "chicago.csv",
    "new_york_city": "new_york_city.csv",
    "washington": "washington.csv",
}


# ------------------------------------------------------------------------------------------
# additional
def data_cleaning(df):
    """cleans data, remove errors, add columns in dataframe"""

    # rename columns
    df.rename(columns={"Unnamed: 0": "id"}, inplace=True)

    # add month, days, and hour columns
    startDate = pd.to_datetime(df["Start Time"])
    df["Month"] = startDate.dt.month
    df["Month Name"] = startDate.dt.strftime("%B")
    df["Day"] = startDate.dt.strftime("%A")
    df["Hour"] = startDate.dt.hour

    return df


# ------------------------------------------------------------------------------------------


# additional
def month_filter():
    """
    filters Month

    month- a return value to get the filtered month
    """
    month = 0
    while True:
        try:
            month_num = int(
                input(
                    """
                    Which month?
                        1.	Jan
                        2.	Feb
                        3.	Mar
                        4.	Apr
                        5.	May
                        6.	Jun 
                        7.  All

                """
                )
            )
        except ValueError:
            print("It's NOT a number! Try again!")
            continue
        else:
            if month_num in range(1, 8):
                month = month_num
            else:
                print("Wrong number! Try again!")
                continue
        break
    return month


# --------------------------------------------------------------------------------------
# additional
def day_filter():
    """
    filters Day

    day- a return value to get the filtered month
    """
    day = 0
    while True:
        try:
            day = int(
                input(
                    """
                    Which day?
                        1.	Sat
                        2.	Sun
                        3.	Mon
                        4.	Tue
                        5.	Wed
                        6.	Thru
                        7.	Fri
                        8.	All

                """
                )
            )

        except ValueError:
            print("It's NOT a number! Try again!")
            continue
        else:
            if day not in range(1, 9):
                print("Wrong number! Try again!")
                continue
            else:
                break

    return day


# --------------------------------------------------------------------------------------
# additional
def city_filter():
    """
    filters City

    city- a return value to get the filtered month
    """
    while True:
        try:
            city_num = int(
                input(
                    """ 
                    Would you like to see data for?
                        1.	Chicago
                        2.	New York
                        3.	Washington

                """
                )
            )
        except ValueError:
            print("It's NOT a number! Try again!")
            continue
        else:
            if city_num == 1:
                city = "chicago"
            elif city_num == 2:
                city = "new_york_city"
            elif city_num == 3:
                city = "washington"
            else:
                print("Wrong number! Try again!")
                continue
        break

    return city


# --------------------------------------------------------------------------------------
# additional
def by_filter():
    """
    specifies chosed filter

    filter_by- a return value to get the chosed filter
    """
    while True:
        try:
            filter_by_num = int(
                input(
                    """
                Would you like to filter data by?
                    1.	Month
                    2.	Day
                    3.	Both
            """
                )
            )
        except ValueError:
            print("It's NOT a number! Try again!")
            continue
        else:
            if filter_by_num == 1:
                filter_by = "month"
            elif filter_by_num == 2:
                filter_by = "day"
            elif filter_by_num == 3:
                filter_by = "both"
            else:
                print("Wrong number! Try again!")
                continue

        break
    return filter_by


# --------------------------------------------------------------------------------------


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    print("Please Enter Numbers!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    # restart = True
    # while restart:
    city = city_filter()
    # -----------------------------------------------------------

    # filtering
    filter_by = by_filter()

    # Initializing variables
    month = 0
    day = 0

    # get user input for month (all, january, february, ... , june)
    if filter_by == "month":  # month = num and day = 0
        month = month_filter()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif filter_by == "day":  # month = 0 and day = num
        day = day_filter()

    elif filter_by == "both":  # month = num and day = num
        month = month_filter()
        day = day_filter()

    print("-" * 40)
    print(f"\n\tFiltered by: {filter_by}")
    return city, month, day


# ------------------------------------------------------------------------------------------


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

    # open file
    city_df = pd.read_csv(CITY_NAME[city])
    df = data_cleaning(city_df)

    # Day name
    if day in range(1, 7):
        if day == 1:
            day_name = "Sat"
        elif day == 2:
            day_name = "Sun"
        elif day == 3:
            day_name = "Mon"
        elif day == 4:
            day_name = "Tue"
        elif day == 5:
            day_name = "Wed"
        elif day == 6:
            day_name = "Thu"
        elif day == 7:
            day_name = "Fri"

    # filtering
    # month = num
    if month:
        # all months
        if month == 7:
            return df
        # no day
        elif not day or day == 8:
            df = df[(df["Month"] == month)]
        # day in 1 :
        elif day:
            df = df[(df["Month"] == month) & (df["Day"].str.slice(0, 3) == day_name)]
    # no month
    elif not month:
        #  no day or all days
        if not day or day == 8:
            return df
        elif day:
            df = df[(df["Day"].str.slice(0, 3) == day_name)]

    # to print multiple specific columns
    # print(df[["Month", "Day"]])

    return df


# ------------------------------------------------------------------------------------------
# additional
def popular_used(df, *popular_thing):
    """
    gets the frequent value with number of occurrence

    returns variables
    maxValue - number of occurrence
    maxName - the value (in the row)
    """
    things = []
    for thing in popular_thing:
        things.append(thing)

    thingCount = df.groupby(things)["id"].count()
    maxValue = thingCount.max()
    maxName = thingCount.index[thingCount.eq(maxValue)][0]
    return maxValue, maxName


# ------------------------------------------------------------------------------------------


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    maxMonthValue, maxMonthName = popular_used(df, "Month Name")
    print(f"Month: {maxMonthName}, Count: {maxMonthValue}")

    # display the most common day of week
    maxDayValue, maxDayName = popular_used(df, "Day")
    print(f"Day: {maxDayName}, Count: {maxDayValue}")

    # display the most common start hour
    maxHourValue, maxHourName = popular_used(df, "Hour")
    print(f"Start hour: {maxHourName}, Count: {maxHourValue}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


# ------------------------------------------------------------------------------------------


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    maxStartStaionValue, maxStartStaionName = popular_used(df, "Start Station")
    print(f"Start Staion: {maxStartStaionName}, Count: {maxStartStaionValue}")

    # display most commonly used end station
    maxEndStaionValue, maxEndStaionName = popular_used(df, "End Station")
    print(f"End Staion: {maxEndStaionName}, Count: {maxEndStaionValue}")

    # display most frequent combination of start station and end station trip
    maxStaionsValue, maxStaionsName = popular_used(df, "Start Station", "End Station")
    print(
        f"Combination of\n\t Start station: {maxStaionsName[0]} \n\t\tand\n\t End station: {maxStaionsName[1]} trip "
    )
    # print(f"\t{maxStaionsName[0]} (start station)")
    # print(f"\t{maxStaionsName[1]} (end station)")
    print(f"\t Count: {maxStaionsValue}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


# ------------------------------------------------------------------------------------------


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    totalTime = df["Trip Duration"].sum()
    totalcount = df["id"].count()
    print(f"Total time: {totalTime}\nCounts: {totalcount}")

    # display mean travel time
    meanTime = df["Trip Duration"].mean()
    print(f"AVG time: {meanTime}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


# ------------------------------------------------------------------------------------------


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    typeCounts = df.groupby(["User Type"])["id"].count()
    print("\tUser Type")
    for value in typeCounts:
        print(f"{typeCounts.index[typeCounts.eq(value)][0]}: {value}")

    # Display counts of gender
    genderCounts = df.groupby(["Gender"])["id"].count()
    print("\n\tGender")
    for value in genderCounts:
        print(f"{genderCounts.index[genderCounts.eq(value)][0]}: {value}")

    # Display earliest, most recent, and most common year of birth
    minBY = df["Birth Year"].min()
    maxBY = df["Birth Year"].max()
    commonYearValue, commonYearNum = popular_used(df, "Birth Year")

    print("\n\tYear of birth")
    print(f"Earliest: {int(minBY)}")
    print(f"Recent: {int(maxBY)}")
    print(f"Common: {int(commonYearNum)}, Count: {commonYearValue}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


# ------------------------------------------------------------------------------------------


def get_data(df):
    """asks the user if want to show individual data
    prints a random row of a df
    """
    while True:
        getData = input("\n\nWould you like to get individual data? Enter yes or no.\n")
        if getData.lower() != "yes":
            break

        print(df.iloc[np.random.randint(1, len(df))].to_dict())


# ------------------------------------------------------------------------------------------


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        get_data(df)

        restart = input("\n\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


# ------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
