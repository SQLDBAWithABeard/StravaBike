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
    print('Starting the produceTimeDistance')
    splits = databaseAccess.getSplits()
    base = datetime.datetime(1970, 1, 1, 0, 0, 0)
    times = [base + datetime.timedelta(seconds=x) for x in splits['elapsed_time']]
    y = matplotlib.dates.date2num(times)
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
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
    matplotlib.pyplot.gcf().set_size_inches(8,6)
    matplotlib.pyplot.savefig('Running_Pace_vs_Total_Distance.png',dpi=300)
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
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(8, 6)
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
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
    matplotlib.pyplot.title('Time Taken Over Distances', fontsize=20)
    matplotlib.pyplot.xticks(fontsize=16)
    matplotlib.pyplot.yticks(fontsize=16)
    matplotlib.pyplot.xlabel('Total Distance (miles)', fontsize=14)
    matplotlib.pyplot.ylabel('Time Taken (hh:mm)', fontsize=14)
    matplotlib.pyplot.grid()
    matplotlib.pyplot.gca().yaxis.set_major_locator(matplotlib.dates.HourLocator(interval = 1))
    matplotlib.pyplot.gca().yaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.savefig('Time_Taken_Distance.png', dpi=300)
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
    AllRidesSince19 = AllOutsideRides[AllOutsideRides['Year'].isin([2019,2020,2021,2022,2023,2024,2025])]
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(12,9 )
    matplotlib.pyplot.tight_layout()
    averageoutside = seaborn.relplot(x='distance_miles', y = 'average_speed_miles_hr', data = AllRidesSince19, hue = 'type', col = 'Year', s=30)
    averageoutside.set_titles("{col_name}")  # use this argument literally
    averageoutside.set_xlabels('Total Distance (miles)', fontsize=18)
    averageoutside.set_ylabels('Average Speed (mph)', fontsize=18)

    # Saving the Seaborn Figure:
    plt.savefig('AverageSpeedOutSide.png')# , dpi=300)

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
    AllRidesSince19 = AllRides[AllRides['Year'].isin([2019,2020,2021,2022,2023,2024,2025])]
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(18.5, 10.5)
    howfast = seaborn.relplot(x='distance_miles', y = 'average_speed_miles_hr', data = AllRidesSince19, hue = 'type', col = 'Year')
    # Adjust title and axis labels directly
    howfast.set_titles("{col_name}")  # use this argument literally
    howfast.set_xlabels('Total Distance (miles)', fontsize=18)
    howfast.set_ylabels('Average Speed (mph)', fontsize=18)
    # Saving the Seaborn Figure:
    plt.savefig('AverageSpeed.png',dpi=300)

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
    AllRidesSince19 = AllRides[AllRides['Year'].isin([2019,2020,2021,2022,2023,2024,2025])]
    # Apply the default theme
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(12,9)
    power = seaborn.relplot(x='distance_miles', y = 'average_watts', data = AllRidesSince19, hue = 'type', col = 'Year',s=150)
    # Adjust title and axis labels directly
    power.set_titles("{col_name}")  # use this argument literally
    power.set_xlabels('Total Distance (miles)', fontsize=18)
    power.set_ylabels('Average Power (watts)', fontsize=18)
    # Saving the Seaborn Figure:
    plt.savefig('AveragePower.png', dpi=300)

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
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(12,9 )
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    matplotlib.pyplot.tight_layout()
    cadence = seaborn.relplot(x='distance_miles', y = 'average_cadence', data = AllRidesSince20, hue = 'type', col = 'Year',s=100)
    # Adjust title and axis labels directly
    cadence.set_titles("{col_name}")  # use this argument literally
    cadence.set_xlabels('Total Distance (miles)', fontsize=18)
    cadence.set_ylabels('Average Cadence', fontsize=18)
    # Saving the Seaborn Figure:
    plt.savefig('AverageCadence.png',dpi=300)

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
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(12,9 )
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    matplotlib.pyplot.tight_layout()
    howfar =  seaborn.catplot(x='start_date_day_of_week', y='distance_miles', kind='strip', data=AllRides, 
                    order=day_of_week_order, col='type', height=9, aspect=1, 
                    palette='pastel',s=10)
    
    howfar.set_titles("{col_name}")  # use this argument literally
    howfar.set_xlabels('Week Day', fontsize=18)
    howfar.set_ylabels('Distance (miles)', fontsize=18)
    howfar.set_xticklabels(rotation=90)

    # Saving the Seaborn Figure:
    plt.savefig('DistanceByDay.png',dpi=300)

def produceDistanceByDayRide():
    AllActivities = databaseAccess.getActivities()
    Ride = AllActivities[AllActivities['type'] == 'Ride']

    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(12,9 )
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    matplotlib.pyplot.tight_layout()
    howfar = seaborn.catplot(x='start_date_day_of_week', y='distance_miles', kind='strip', data=Ride, 
                    order=day_of_week_order, col='type', height=9, aspect=1, 
                    palette='pastel',s=10)
    howfar.set_titles("{col_name}")  # use this argument literally
    howfar.set_xlabels('Week Day', fontsize=18)
    howfar.set_ylabels('Distance (miles)', fontsize=18)
    (howfar.set_axis_labels().set_xticklabels(rotation=30))
    # Saving the Seaborn Figure:
    plt.savefig('DistanceByDayRide.png', dpi=300)

def produceCadenceByDay():
    print('Starting the produceCadenceByDay')
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
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(12,9 )
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    cadence = seaborn.catplot(x='start_date_day_of_week', y='average_cadence', kind='strip', data=AllRides, 
                    order=day_of_week_order, col='type', height=9, aspect=1, 
                    palette='pastel',s= 10)
    cadence.set_titles("{col_name}")  # use this argument literally
    cadence.set_xlabels('Week Day', fontsize=18)
    cadence.set_ylabels('Average Cadence', fontsize=18)
    cadence.set_xticklabels(rotation=90)
    matplotlib.pyplot.tight_layout()
    plt.savefig('CadenceByDay.png', dpi=300)

def GetRideDistanceByWeek(activities): 
    print('Starting the GetRideDistanceByWeek')
    howmany = len(activities.index)
    print('There are {0} activities'.format(howmany))
    # print('There are column names {0}'.format(activities.columns.values))
    # print('The first one is {0}'.format(activities.head(1)))
    
    df = activities.groupby([pandas.Grouper(key='start_date_local', freq='W-MON'),'Year']).agg(

            Ride=('distance_miles_Ride', 'sum'),
            EBike=('distance_miles_EBike', 'sum'),
            VirtualRide=('distance_miles_VirtualRide', 'sum')
    )
    dfm = pandas.melt(df.reset_index(), id_vars=['start_date_local','Year'], value_name='distance',value_vars =['Ride','EBike','VirtualRide'],var_name='Type Of Ride')
    Unique_Year = dfm.Year.unique()[0]
    figure = matplotlib.pyplot.gcf()
    figure.set_size_inches(6, 9)
    seaborn.set_theme()
    seaborn.set(style="darkgrid", context="poster")
    # seaborn.lineplot(data=dfm, x='start_date_local',y='distance',hue='Type Of Ride') #, marker='o')
    # seaborn.barplot(data=dfm, x='distance',y='start_date_local',hue='Type Of Ride', palette='hls') #, marker='o')
    # get first row using head() function
    # print(dfm.head(1))
    dfm["start_date_local"] = dfm["start_date_local"].dt.date
    seaborn.barplot(data=dfm, x='distance',y='start_date_local',hue='Type Of Ride', palette='hls') #, marker='o')
    # print(dfm.head(1))
    #dfm.plot(kind='bar', stacked=True, color=['red', 'skyblue', 'green'])
    matplotlib.pyplot.legend(bbox_to_anchor=(1.05, 0.5), loc='upper left', title="Type Of Ride", fontsize=6, title_fontsize=8)
    matplotlib.pyplot.tight_layout()
    title = 'Distance Per Week for {0}'.format(Unique_Year)
    # matplotlib.pyplot.gca().yaxis.set_major_locator(matplotlib.dates.MonthLocator())
    # matplotlib.pyplot.gca().yaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %Y"))
    matplotlib.pyplot.title(title, fontsize=20 ) #, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=8,rotation=90)
    matplotlib.pyplot.yticks(fontsize=8)
    matplotlib.pyplot.xlabel('Distance (miles)', fontsize=14)
    matplotlib.pyplot.ylabel('Week', fontsize=14)
    # matplotlib.pyplot.show()
    image_name = 'Distance_per_Week_For_{0}.png'.format(Unique_Year)
    matplotlib.pyplot.savefig(image_name,dpi=300)
    matplotlib.pyplot.clf()
    
def GetRideDistanceByYear(activities): 
    print('Starting the GetRideDistanceByYear')
    howmany = len(activities.index)
    print('There are {0} activities'.format(howmany))
    # print('There are column names {0}'.format(activities.columns.values))
    df = activities.groupby('Year').agg(
            NoOutsideRides=('IsOutsideRide', 'sum'),
            Ride_Miles=('distance_miles_Ride', 'sum'),
            NoEBikes=('IsEBikeRide', 'sum'),
            EBike_Miles=('distance_miles_EBike', 'sum'),
            NoVirtual=('IsVirtualRide', 'sum'),
            VirtualRide_Miles=('distance_miles_VirtualRide', 'sum'),
            AllMiles=('distance_miles',sum),
            AllRides=('IsARide',sum)
            
    )

    df.reset_index().plot(x='Year', y=['Ride_Miles','VirtualRide_Miles','EBike_Miles'], kind='bar',legend=False,width=1)
    matplotlib.pyplot.legend(bbox_to_anchor=(1.05, 0.5), loc='upper left', title="Number of Miles", fontsize=6, title_fontsize=8)
    matplotlib.pyplot.title('')#Number of Miles each Year', fontsize=20 ) #, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=14,rotation=0)
    matplotlib.pyplot.yticks(fontsize=8)
    matplotlib.pyplot.ylabel('Distance (miles)', fontsize=10)
    matplotlib.pyplot.xlabel('', fontsize=14)
    matplotlib.pyplot.gcf().set_size_inches(8, 4)
    matplotlib.pyplot.tight_layout()
    #matplotlib.pyplot.show()#avefig('Number_of_Activities_and_Type_per_Distance.png')
    matplotlib.pyplot.savefig('Number_of_Miles_each_Year.png', dpi=300)
    matplotlib.pyplot.clf()
    df.reset_index().plot(x='Year', y=['NoOutsideRides','NoVirtual','NoEBikes'], kind='bar',legend=False,width=1)
    matplotlib.pyplot.legend(bbox_to_anchor=(1.05, 0.5), loc='upper left', title="Number of Rides", fontsize=6, title_fontsize=8)
    matplotlib.pyplot.title('Number of Rides each Year', fontsize=20 ) #, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=14,rotation=0)
    matplotlib.pyplot.yticks(fontsize=8)
    matplotlib.pyplot.xlabel('', fontsize=14)
    matplotlib.pyplot.gcf().set_size_inches(8, 4)
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.subplots_adjust(top=0.85)     # Add space at top
    #matplotlib.pyplot.show()#avefig('Number_of_Activities_and_Type_per_Distance.png')
    matplotlib.pyplot.savefig('Number_of_Rides_each_Year.png', dpi=300)
    matplotlib.pyplot.clf()
    df.reset_index().plot(x='Year', y=['AllRides'], kind='bar',legend=False,width=1)
    matplotlib.pyplot.title('Number of Rides each Year', fontsize=20 ) #, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=14,rotation=0)
    matplotlib.pyplot.yticks(fontsize=8)
    matplotlib.pyplot.gcf().set_size_inches(8, 4)
    matplotlib.pyplot.tight_layout()
    #matplotlib.pyplot.show()#avefig('Total_Number_of_Rides_each_Year.png')
    matplotlib.pyplot.savefig('Total_Number_of_Rides_each_Year.png', dpi=300)
    matplotlib.pyplot.clf()
    df.reset_index().plot(x='Year', y=['AllMiles'], kind='bar',legend=False,width=1)
    matplotlib.pyplot.title('Number of Miles each Year', fontsize=18 ) #, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=14,rotation=0)
    matplotlib.pyplot.yticks(fontsize=8)
    matplotlib.pyplot.ylabel('Distance (miles)', fontsize=10)
    matplotlib.pyplot.xlabel('', fontsize=18)
    matplotlib.pyplot.gcf().set_size_inches(8, 4)
    matplotlib.pyplot.tight_layout()
    #matplotlib.pyplot.show()#avefig('Number_of_Activities_and_Type_per_Distance.png')
    matplotlib.pyplot.savefig('Total_Number_of_Miles_each_Year.png', dpi=300)
    matplotlib.pyplot.clf()
    miles = df[[
            'Ride_Miles',
            'EBike_Miles',
            'VirtualRide_Miles',
            'AllMiles'
    ]]
    miles.rename(columns={'Ride_Miles' : 'Ride Miles', 'EBike_Miles' : 'E-Bike Miles', 'VirtualRide_Miles' : 'Virtual Miles', 'AllMiles' : 'Total Miles'}, inplace=True)
    rides = df[[
            'NoOutsideRides',
            'NoEBikes',
            'NoVirtual',
            'AllRides'
    ]]
    rides.rename(columns={'NoOutsideRides' : 'Rides', 'NoEBikes' : 'E-Bike', 'NoVirtual' : 'Virtual', 'AllRides' : 'Total Rides'}, inplace=True)
    return miles,rides

def GetRideElevationByYear(activities): 
    print('Starting the GetRideElevationByYear')
    howmany = len(activities.index)
    print('There are {0} activities'.format(howmany))
    # print('There are column names {0}'.format(activities.columns.values))
    df = activities.groupby('Year').agg(
            Elevation_Ride=('elevation_Ride', 'sum'),
            Elevation_EBike=('elevation_EBike', 'sum'),
            Elevation_VirtualRide=('elevation_VirtualRide', 'sum'),
            AllElevation=('total_elevation_gain',sum),
    )

    df.reset_index().plot(x='Year', y=['Elevation_Ride','Elevation_EBike','Elevation_VirtualRide'], kind='bar',legend=False,width=1)
    matplotlib.pyplot.legend(bbox_to_anchor=(1.05, 0.5), loc='upper left', title="Elevation", fontsize=6, title_fontsize=8)
    matplotlib.pyplot.title('')#Number of Miles each Year', fontsize=20 ) #, fontweight="bold")
    matplotlib.pyplot.xticks(fontsize=14,rotation=0)
    matplotlib.pyplot.yticks(fontsize=8)
    matplotlib.pyplot.ylabel('Elevation (metres)', fontsize=10)
    matplotlib.pyplot.xlabel('', fontsize=14)
    matplotlib.pyplot.gcf().set_size_inches(8, 4)
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.show()#avefig('Number_of_Activities_and_Type_per_Distance.png')
    matplotlib.pyplot.savefig('Elevation_each_Year.png', dpi=300)
    matplotlib.pyplot.clf()
    
    elevation = df[[
            'Elevation_Ride',
            'Elevation_EBike',
            'Elevation_VirtualRide',
            'AllElevation'
    ]]
    elevation.rename(columns={'Elevation_Ride' : 'Ride Elevation', 'Elevation_EBike' : 'E-Bike Elevation', 'Elevation_VirtualRide' : 'Virtual Elevation', 'AllElevation' : 'Total Elevation'}, inplace=True)
    
    return elevation

