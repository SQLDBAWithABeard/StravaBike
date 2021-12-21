import pandas
import dateutil
import datetime
import seaborn
import matplotlib
import matplotlib.pylab
import databaseAccess
import matplotlib.pyplot as plt

# py -c 'import visualiseData; visualiseData.getFastestTimes()'
def getFastestTimes():
    splits = databaseAccess.getSplits()
    activities = splits[['activity_date', 'distance', 'elapsed_time']]
    produceFastest1k(activities)
    months=[]
    max_date = datetime.datetime.strptime((datetime.datetime.strptime(splits['activity_date'].max(),"%Y-%m-%dT%H:%M:%SZ")).strftime('%Y%m'),'%Y%m')
    min_date = datetime.datetime.strptime((datetime.datetime.strptime(splits['activity_date'].min(),"%Y-%m-%dT%H:%M:%SZ")).strftime('%Y%m'),'%Y%m')
    months.append(min_date)
    while min_date <= max_date:
        min_date = min_date + dateutil.relativedelta.relativedelta(months=1)
        months.append(min_date)

def produceFastest1k(activities):
    pandas.options.mode.chained_assignment = None
    activities['activity_date'] = [datetime.datetime.strptime((datetime.datetime.strptime(x,"%Y-%m-%dT%H:%M:%SZ")).strftime('%Y%m'),'%Y%m') for x in activities['activity_date']]
    activities['distance'] = activities['distance'].astype(float)
    activities['elapsed_time'] = activities['elapsed_time'].astype(float)
    activities.set_index(['activity_date'], inplace=True)
    fastestSplits = activities['elapsed_time'].groupby('activity_date').agg(elapsed_time=('min')).reset_index()
    base = datetime.datetime(1970, 1, 1, 0, 0, 0)
    times = [base + datetime.timedelta(seconds=x) for x in fastestSplits['elapsed_time']]
    dates = fastestSplits['activity_date']
    x = matplotlib.dates.date2num(dates)
    y = matplotlib.dates.date2num(times)
    matplotlib.pylab.plot_date(x, y, linestyle='', marker='o', markersize=5, alpha=0.1, color="blue")
    matplotlib.pyplot.title('Fastest 1k Pace over Time', fontsize=18, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=16, rotation='vertical')
    matplotlib.pyplot.yticks(fontsize=16)
    matplotlib.pyplot.xlabel('Month', fontsize=18)
    matplotlib.pyplot.ylabel('Pace (km / hh:mm:ss)', fontsize=18)
    seaborn.regplot(x = x, y = y, scatter=None, data = fastestSplits ,order = 2)
    loc= matplotlib.dates.AutoDateLocator()
    matplotlib.pyplot.gca().xaxis.set_major_locator(loc)
    matplotlib.pyplot.gca().yaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M:%S'))
    matplotlib.pyplot.gca().xaxis.set_major_formatter(matplotlib.dates.AutoDateFormatter(loc))
    matplotlib.pyplot.gcf().autofmt_xdate()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.savefig('Fastest_1k_Pace_over_Time.png')
    matplotlib.pyplot.clf()

# py -c 'import visualiseData; visualiseData.produceTimeElevation()'
def produceTimeElevation():
    splits = databaseAccess.getSplits()
    base = datetime.datetime(1970, 1, 1, 0, 0, 0)
    times = [base + datetime.timedelta(seconds=x) for x in splits['elapsed_time']]
    y = matplotlib.dates.date2num(times)
    matplotlib.pyplot.plot( splits['elevation_difference'], y, linestyle='', marker='o', markersize=5, alpha=0.1, color="blue")
    seaborn.regplot(x = splits['elevation_difference'], y = y, scatter=None, order = 2)
    matplotlib.pyplot.title('Running Pace vs. Elevation Change', fontsize=18, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=16)
    matplotlib.pyplot.yticks(fontsize=16)
    matplotlib.pyplot.xlabel('Elevation Change (m)', fontsize=18)
    matplotlib.pyplot.ylabel('1km Pace (hh:mm:ss)', fontsize=18)
    matplotlib.pyplot.gca().yaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M:%S'))
    matplotlib.pyplot.gcf().autofmt_xdate()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.savefig('Running_Pace_vs_Elevation_Change.png')
    matplotlib.pyplot.clf()

# py -c 'import visualiseData; visualiseData.produceTimeDistance()'
def produceTimeDistance():
    splits = databaseAccess.getSplits()
    base = datetime.datetime(1970, 1, 1, 0, 0, 0)
    times = [base + datetime.timedelta(seconds=x) for x in splits['elapsed_time']]
    y = matplotlib.dates.date2num(times)
    matplotlib.pyplot.plot( splits['total_distance'], y, linestyle='', marker='o', markersize=5, alpha=0.1, color="blue")
    seaborn.regplot(x = splits['total_distance'], y = y, scatter=None, order = 2)
    matplotlib.pyplot.title('Running Pace vs. Total Distance', fontsize=18, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=16)
    matplotlib.pyplot.yticks(fontsize=16)
    matplotlib.pyplot.xlabel('Total Distance (m)', fontsize=18)
    matplotlib.pyplot.ylabel('1km Pace (hh:mm:ss)', fontsize=18)
    matplotlib.pyplot.gca().yaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M:%S'))
    matplotlib.pyplot.gcf().autofmt_xdate()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    matplotlib.pyplot.savefig('Running_Pace_vs_Total_Distance.png')
    matplotlib.pyplot.clf()

# py -c 'import visualiseData; visualiseData.produceActivtyHistogram()'
def produceActivtyHistogram():
    activities = databaseAccess.getActivityDistances()
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    seaborn.catplot(x="nearest_5miles", y="cnt",  data=activities, kind = "bar")
    matplotlib.pyplot.title('Number of Activities per Distance', fontsize=20 ) #, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=8,rotation=90)
    matplotlib.pyplot.yticks(fontsize=8)
    matplotlib.pyplot.xlabel('Distance (miles)', fontsize=14)
    matplotlib.pyplot.ylabel('Count of Activities', fontsize=14)
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(8, 4.5)
    matplotlib.pyplot.savefig('Number_of_Activities_per_Distance.png', dpi=300)
    matplotlib.pyplot.clf()

def produceActivtyRideHistogram():
    Ride = databaseAccess.getActivityRideDistances()
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    seaborn.catplot(x="nearest_5miles", y="cnt",  data=Ride, kind = "bar")
    matplotlib.pyplot.title('Number of Outside Rides per Distance', fontsize=20 ) #, fontweight="bold")
    matplotlib.pyplot.xlabel('Distance (miles)', fontsize=14)
    matplotlib.pyplot.ylabel('Count of Rides', fontsize=14)
    matplotlib.pyplot.xticks(fontsize=8,rotation=90)
    matplotlib.pyplot.yticks(fontsize=8)
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(8, 4.5)
    matplotlib.pyplot.savefig('Number_of_Rides_per_Distance.png', dpi=300)
    matplotlib.pyplot.clf()

# py -c 'import visualiseData; visualiseData.produceTimePace()'
def produceTimePace():
    splits = databaseAccess.getMonthSplits()
    dates = [dateutil.parser.parse(x) for x in splits['activity_month']]
    x = matplotlib.dates.date2num(dates)
    base = datetime.datetime(1970, 1, 1, 0, 0, 0)
    times = [base + datetime.timedelta(seconds=x) for x in splits['elapsed_time']]
    y = matplotlib.dates.date2num(times)
    matplotlib.pylab.plot_date(x, y, linestyle='', marker='o', markersize=5, alpha=0.1, color="blue")
    matplotlib.pyplot.title('Running Pace over Time', fontsize=18, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=16, rotation='vertical')
    matplotlib.pyplot.yticks(fontsize=16)
    matplotlib.pyplot.xlabel('Date', fontsize=18)
    matplotlib.pyplot.ylabel('Pace (km / hh:mm:ss)', fontsize=18)
    seaborn.regplot(x = x, y = y, scatter=None, data = splits ,order = 2)
    loc= matplotlib.dates.AutoDateLocator()
    matplotlib.pyplot.gca().xaxis.set_major_locator(loc)
    matplotlib.pyplot.gca().yaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M:%S'))
    matplotlib.pyplot.gca().xaxis.set_major_formatter(matplotlib.dates.AutoDateFormatter(loc))
    matplotlib.pyplot.gcf().autofmt_xdate()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    matplotlib.pyplot.savefig('Running_Pace_over_Time.png')
    matplotlib.pyplot.clf()

# py -c 'import visualiseData; visualiseData.produceElapsedTimeDistance()'
def produceElapsedTimeDistance():
    splits = databaseAccess.getSplits()
    splits = pandas.merge(splits, splits.groupby(['activity_id'])[['elapsed_time']].agg('sum'), on=["activity_id", "activity_id"])
    splits['total_distance'] = splits['total_distance']* 0.000621371
    base = datetime.datetime(1970, 1, 1, 0, 0, 0)
    times = [base + datetime.timedelta(seconds=x) for x in splits['elapsed_time_y']]
    y = matplotlib.dates.date2num(times)
    max_distance = int(round(splits['total_distance'].max()))
    max_time = max(times)
    if max_distance < 100:
        # Assume we want to extend for a century
        max_distance = 100
        # Since we haven't been that far, assume we can finish  in under 8 hours
        max_time = datetime.datetime(1970, 1, 1, 10, 0, 0)
    _, axes = matplotlib.pyplot.subplots()
    xlim = [0,max_distance]
    axes.set_xlim(xlim)
    ylim = [0,max_time]
    axes.set_ylim(ylim)
    matplotlib.pyplot.plot( splits['total_distance'], y, linestyle='', marker='o', markersize=3, alpha=0.1, color="orange")
    seaborn.regplot(x = splits['total_distance'], y = y, scatter=None, data = splits ,order = 2, ax = axes, truncate = False)
    matplotlib.pyplot.title('Time Taken Over Distances', fontsize=18, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=16)
    matplotlib.pyplot.yticks(fontsize=16)
    matplotlib.pyplot.xlabel('Total Distance (miles)', fontsize=18)
    matplotlib.pyplot.ylabel('Time Taken (hh:mm)', fontsize=18)
    matplotlib.pyplot.grid()
    matplotlib.pyplot.gca().yaxis.set_major_locator(matplotlib.dates.HourLocator(interval = 1))
    matplotlib.pyplot.gca().yaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    matplotlib.pyplot.savefig('Time_Taken_Distance.png')
    matplotlib.pyplot.clf()
def produceAverageSpeedOutside():
    AllActivities = databaseAccess.getActivities()
    NightWalk = AllActivities[AllActivities['type'] == 'Night Walk']
    Walk = AllActivities[AllActivities['type'] == 'Walk']
    Run = AllActivities[AllActivities['type'] == 'Run']
    EBikeRide = AllActivities[AllActivities['type'] == 'EBikeRide']
    VirtualRide = AllActivities[AllActivities['type'] == 'VirtualRide']
    Ride = AllActivities[AllActivities['type'] == 'Ride']

    frames = [EBikeRide, VirtualRide, Ride]
    AllRides = pandas.concat(frames)

    frames = [EBikeRide, Ride]
    AllOutsideRides = pandas.concat(frames)
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    seaborn.relplot(x='distance_miles', y = 'average_speed_miles_hr', data = AllOutsideRides, hue = 'type', col = 'Year')
    matplotlib.pyplot.xlabel('Total Distance (miles)', fontsize=18)
    matplotlib.pyplot.ylabel('Average Speed (mph)', fontsize=18)
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    # Saving the Seaborn Figure:
    plt.savefig('AverageSpeedOutSide.png')

def produceAverageSpeed():
    AllActivities = databaseAccess.getActivities()
    NightWalk = AllActivities[AllActivities['type'] == 'Night Walk']
    Walk = AllActivities[AllActivities['type'] == 'Walk']
    Run = AllActivities[AllActivities['type'] == 'Run']
    EBikeRide = AllActivities[AllActivities['type'] == 'EBikeRide']
    VirtualRide = AllActivities[AllActivities['type'] == 'VirtualRide']
    Ride = AllActivities[AllActivities['type'] == 'Ride']

    frames = [EBikeRide, VirtualRide, Ride]
    AllRides = pandas.concat(frames)

    frames = [EBikeRide, Ride]
    AllOutsideRides = pandas.concat(frames)
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    seaborn.relplot(x='distance_miles', y = 'average_speed_miles_hr', data = AllRides, hue = 'type', col = 'Year')
    matplotlib.pyplot.xlabel('Total Distance (miles)', fontsize=18)
    matplotlib.pyplot.ylabel('Average Speed (mph)', fontsize=18)
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    # Saving the Seaborn Figure:
    plt.savefig('AverageSpeed.png')

def produceAveragePower():
    AllActivities = databaseAccess.getActivities()
    NightWalk = AllActivities[AllActivities['type'] == 'Night Walk']
    Walk = AllActivities[AllActivities['type'] == 'Walk']
    Run = AllActivities[AllActivities['type'] == 'Run']
    EBikeRide = AllActivities[AllActivities['type'] == 'EBikeRide']
    VirtualRide = AllActivities[AllActivities['type'] == 'VirtualRide']
    Ride = AllActivities[AllActivities['type'] == 'Ride']

    frames = [EBikeRide, VirtualRide, Ride]
    AllRides = pandas.concat(frames)

    frames = [EBikeRide, Ride]
    AllOutsideRides = pandas.concat(frames)
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    seaborn.relplot(x='distance_miles', y = 'average_watts', data = AllRides, hue = 'type', col = 'Year')
    matplotlib.pyplot.xlabel('Total Distance (miles)', fontsize=18)
    matplotlib.pyplot.ylabel('Average Power (watts)', fontsize=18)
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    # Saving the Seaborn Figure:
    plt.savefig('AveragePower.png')

def produceAverageCadence():
    AllActivities = databaseAccess.getActivities()
    NightWalk = AllActivities[AllActivities['type'] == 'Night Walk']
    Walk = AllActivities[AllActivities['type'] == 'Walk']
    Run = AllActivities[AllActivities['type'] == 'Run']
    EBikeRide = AllActivities[AllActivities['type'] == 'EBikeRide']
    VirtualRide = AllActivities[AllActivities['type'] == 'VirtualRide']
    Ride = AllActivities[AllActivities['type'] == 'Ride']

    frames = [EBikeRide, VirtualRide, Ride]
    AllRides = pandas.concat(frames)
    AllRidesSince20 = AllRides[AllRides['Year'].isin([2020,2021,2022,2023,2024,2025])]
    frames = [EBikeRide, Ride]
    AllOutsideRides = pandas.concat(frames)
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    seaborn.relplot(x='distance_miles', y = 'average_cadence', data = AllRidesSince20, hue = 'type', col = 'Year')
    matplotlib.pyplot.xlabel('Total Distance (miles)', fontsize=18)
    matplotlib.pyplot.ylabel('Average Cadence', fontsize=18)
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    # Saving the Seaborn Figure:
    plt.savefig('AverageCadence.png')

def produceDistanceByDay():
    AllActivities = databaseAccess.getActivities()
    NightWalk = AllActivities[AllActivities['type'] == 'Night Walk']
    Walk = AllActivities[AllActivities['type'] == 'Walk']
    Run = AllActivities[AllActivities['type'] == 'Run']
    EBikeRide = AllActivities[AllActivities['type'] == 'EBikeRide']
    VirtualRide = AllActivities[AllActivities['type'] == 'VirtualRide']
    Ride = AllActivities[AllActivities['type'] == 'Ride']

    frames = [EBikeRide, VirtualRide, Ride]
    AllRides = pandas.concat(frames)
    AllRidesSince20 = AllRides[AllRides['Year'].isin([2020,2021,2022,2023,2024,2025])]
    frames = [EBikeRide, Ride]
    AllOutsideRides = pandas.concat(frames)
    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
    
    g = seaborn.catplot(x='start_date_day_of_week', y='distance_miles', kind='strip', data=AllRides, 
                    order=day_of_week_order, col='type', height=9, aspect=1, 
                    palette='pastel')
    
    (g.set_axis_labels("Week day", "Distance (miles)")
      .set_titles("Activity type: {col_name}")
      .set_xticklabels(rotation=30));
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    # Saving the Seaborn Figure:
    plt.savefig('DistanceByDay.png')

def produceDistanceByDayRide():
    AllActivities = databaseAccess.getActivities()
    Ride = AllActivities[AllActivities['type'] == 'Ride']

    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
    
    g = seaborn.catplot(x='start_date_day_of_week', y='distance_miles', kind='strip', data=Ride, 
                    order=day_of_week_order, col='type', height=9, aspect=1, 
                    palette='pastel')
    
    (g.set_axis_labels("Week day", "Distance (miles)")
      .set_titles("Activity type: {col_name}")
      .set_xticklabels(rotation=45));
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    # Saving the Seaborn Figure:
    plt.savefig('DistanceByDayRide.png')

def produceCadenceByDay():
    AllActivities = databaseAccess.getActivities()
    NightWalk = AllActivities[AllActivities['type'] == 'Night Walk']
    Walk = AllActivities[AllActivities['type'] == 'Walk']
    Run = AllActivities[AllActivities['type'] == 'Run']
    EBikeRide = AllActivities[AllActivities['type'] == 'EBikeRide']
    VirtualRide = AllActivities[AllActivities['type'] == 'VirtualRide']
    Ride = AllActivities[AllActivities['type'] == 'Ride']

    frames = [EBikeRide, VirtualRide, Ride]
    AllRides = pandas.concat(frames)
    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]

    g = seaborn.catplot(x='start_date_day_of_week', y='average_cadence', kind='strip', data=AllRides, 
                    order=day_of_week_order, col='type', height=9, aspect=1, 
                    palette='pastel')

    (g.set_axis_labels("Week day", "Average Cadence")
      .set_titles("Activity type: {col_name}")
      .set_xticklabels(rotation=45));

      # Saving the Seaborn Figure:
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    plt.savefig('CadenceByDay.png')

def GetRideDistanceByWeek(activities): 
    print('Starting the GetRideDistanceByWeek')
    howmany = len(activities.index)
    print('There are {0} activities'.format(howmany))
    # print('There are column names {0}'.format(activities.columns.values))
    df = activities.groupby([pandas.Grouper(key='start_date_local', freq='W-MON'),'Year']).agg(

            Ride=('distance_miles_Ride', 'sum'),
            EBike=('distance_miles_EBike', 'sum'),
            VirtualRide=('distance_miles_VirtualRide', 'sum')
    )
    dfm = pandas.melt(df.reset_index(), id_vars=['start_date_local','Year'], value_name='distance',value_vars =['Ride','EBike','VirtualRide'],var_name='Type Of Ride')
    Unique_Year = dfm.Year.unique()[0]
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(12, 5)
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    matplotlib.pyplot.gca().xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    matplotlib.pyplot.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %Y"))
    seaborn.lineplot(data=dfm, x='start_date_local',y='distance',hue='Type Of Ride', marker='o')
    title = 'Distance Per Week for {0}'.format(Unique_Year)
    matplotlib.pyplot.title(title, fontsize=18 ) #, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=12,rotation=90)
    matplotlib.pyplot.yticks(fontsize=12)
    matplotlib.pyplot.ylabel('Distance (miles)', fontsize=18)
    matplotlib.pyplot.show()#avefig('Number_of_Activities_and_Type_per_Distance.png')
    image_name = 'Distance_per_Week_For_{0}.png'.format(Unique_Year)
    matplotlib.pyplot.savefig(image_name,dpi=100)
    matplotlib.pyplot.clf()