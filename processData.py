import visualiseData
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Commenting out for now as we're not using the new version of this yet
# import dataPredication
import databaseAccess
import pandas
from tabulate import tabulate

# py -c 'import processData; processData.generateReadme()'
def generateReadme():
    lastActivity = databaseAccess.getlastActivity()
    lastActivityDate = datetime.strptime(lastActivity[0], "%Y-%m-%dT%H:%M:%SZ")
    lastActivityDateFormat = lastActivityDate.strftime("%d %B, %Y at %H:%M:%S")
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
    AllRides19 = AllRides[AllRides['Year'].isin([2019])]
    AllRides20 = AllRides[AllRides['Year'].isin([2020])]
    AllRides21 = AllRides[AllRides['Year'].isin([2021])]
    AllRides22 = AllRides[AllRides['Year'].isin([2022])]
    AllRides23 = AllRides[AllRides['Year'].isin([2023])]
    RidesandDistances = visualiseData.GetRideDistanceByYear(AllRidesSince19)
    Elevation = visualiseData.GetRideElevationByYear(AllRidesSince19)
    visualiseData.produceAverageSpeedOutside()
    visualiseData.produceAverageSpeed()
    visualiseData.produceAverageCadence()
    visualiseData.produceAveragePower()
    visualiseData.produceDistanceByDay()
    visualiseData.produceDistanceByDayRide()
    visualiseData.produceCadenceByDay()
    visualiseData.produceElapsedTimeDistance()
    visualiseData.produceActivtyRideHistogram()
    visualiseData.produceActivtyHistogram()
    # visualiseData.GetRideDistanceByWeek(AllRides19)
    # visualiseData.GetRideDistanceByWeek(AllRides20)
    # visualiseData.GetRideDistanceByWeek(AllRides21)
    visualiseData.GetRideDistanceByWeek(AllRides22)
    visualiseData.GetRideDistanceByWeek(AllRides23)

    now = datetime.now()
    now_string = now.strftime("%d %B, %Y at %H:%M:%S")
    delta = relativedelta(datetime.now(), lastActivityDate )
    if os.path.exists('README.md'):
        os.remove('README.md')
    with open('README.md', 'w') as handle:
        handle.write('# Last Refreshed - {0}\n'.format(now_string))
        handle.write('The Latest Activity was a {0} - \n\n'.format( lastActivity[2]))
        handle.write('<b>{0}</b> \n\n'.format( lastActivity[1]))
        handle.write('which happened on {0} \n\n'.format( lastActivityDateFormat))
        handle.write('Which is {0} years, {1} months, {2} days, {3} hours and {4} minutes since the last refresh! \n\n'.format( delta.years, delta.months, delta.days, delta.hours, delta.minutes))    
        handle.write('You can see it here https://www.strava.com/activities/{0} \n\n'.format( lastActivity[3] ))
        handle.write('## Number of Rides\n')
        handle.write('How many rides have I done each year?\n\n')
        handle.write('![Number_of_Rides_each_Year](Number_of_Rides_each_Year.png?raw=true "Number_of_Rides_each_Year")\n\n')
        RidesandDistances[1].to_markdown(buf=handle)
        handle.write('\n\n')
        handle.write('## Distance Travelled\n\n')
        handle.write('How many miles have I ridden?\n\n')
        handle.write('![Number_of_Miles_each_Year](Number_of_Miles_each_Year.png?raw=true "Number_of_Miles_each_Year")\n\n')
        RidesandDistances[0].to_markdown(buf=handle)
        handle.write('\n\n')
        handle.write('## Elevation Climbed\n\n')
        handle.write('How many metres have I climbed?\n\n')
        handle.write('![Elevation_each_Year](Elevation_each_Year.png?raw=true "Elevation_each_Year")\n\n')
        Elevation.to_markdown(buf=handle)
        handle.write('\n\n')
        handle.write('## Average Bike Speed Outside\n')
        handle.write('How does my average bike speed vary for rides that are outside by distance, by year, and by type of ride?\n\n')
        handle.write('![Average Bike Speed Outside](AverageSpeedOutSide.png?raw=true "Average Bike Speed Outside")\n\n')
        handle.write('## Average Bike Speed Wherever\n')
        handle.write('How does my average bike speed vary for rides by distance, by year, and by type of ride?\n\n')
        handle.write('![AverageSpeed](AverageSpeed.png?raw=true "Average Bike Speed per Distance")\n\n')
        handle.write('## Average Cadence\n')
        handle.write('How does my average bike cadence vary for rides by distance, by year, and by type of ride?\n\n')
        handle.write('![AverageCadence](AverageCadence.png?raw=true "Average Cadence per Distance")\n\n')
        handle.write('## Average Power\n')
        handle.write('How does my average bike power vary for rides by distance, by year, and by type of ride?\n\n')
        handle.write('![AverageCadence](AveragePower.png?raw=true "Average Power per Distance")\n\n')
        handle.write('## Outside Rides Distance by day\n')
        handle.write('How far do I ride each day on average?\n\n')
        handle.write('![DistanceByDayRide](DistanceByDayRide.png?raw=true "DistanceByDayRide")\n\n')
        handle.write('## Cadence by day\n')
        handle.write('Does my cadence change by the day of the week?\n\n')
        handle.write('![CadenceByDay](CadenceByDay.png?raw=true "CadenceByDay")\n\n')
        handle.write('## Rides by day\n')
        handle.write('How far do I ride each day by Ride Type, by year, and by type of ride?\n\n')
        handle.write('![DistanceByDay](DistanceByDay.png?raw=true "DistanceByDay")\n\n')
        handle.write('## How Long by How Far\n')
        handle.write('How far do I ride and how long does it take??\n\n')
        handle.write('![Time_Taken_Distance](Time_Taken_Distance.png?raw=true "Time_Taken_Distance")\n\n')
        handle.write('## 5 mile buckets\n')
        handle.write('How many times do I ride in each 5 mile bucket for all activities?\n\n')
        handle.write('![Number_of_Activities_per_Distance](Number_of_Activities_per_Distance.png?raw=true "Number_of_Activities_per_Distance")\n\n')
        handle.write('## 5 mile buckets outside ?\n')
        handle.write('How many times do I ride in each 5 mile bucket outside??\n\n')
        handle.write('![Number_of_Rides_per_Distance](Number_of_Rides_per_Distance.png?raw=true "Number_of_Rides_per_Distance")\n\n')
        handle.write('## Each Week Distance for 2023 ?\n')
        handle.write('How far did I ride each week in 2023 ??\n\n')
        handle.write('![Distance_per_Week_For_2023](Distance_per_Week_For_2023.png?raw=true "Distance_per_Week_For_2023")\n\n')
        handle.write('## Each Week Distance for 2022 ?\n')
        handle.write('How far did I ride each week in 2022 ??\n\n')
        handle.write('![Distance_per_Week_For_2022](Distance_per_Week_For_2022.png?raw=true "Distance_per_Week_For_2022")\n\n')
        handle.write('## Each Week Distance for 2021 ?\n')
        handle.write('How far did I ride each week in 2021 ??\n\n')
        handle.write('![Distance_per_Week_For_2021](Distance_per_Week_For_2021.png?raw=true "Distance_per_Week_For_2021")\n\n')
        handle.write('## Each Week Distance for 2020 ?\n')
        handle.write('How far did I ride each week in 2020 ??\n\n')
        handle.write('![Distance_per_Week_For_2020](Distance_per_Week_For_2020.png?raw=true "Distance_per_Week_For_2020")\n\n')
        handle.write('## Each Week Distance for 2019 ?\n')
        handle.write('How far did I ride each week in 2019 ??\n\n')
        handle.write('![Distance_per_Week_For_2019](Distance_per_Week_For_2019.png?raw=true "Distance_per_Week_For_2019")\n\n')
        handle.write('# StravaDataAnalysis\n')
        handle.write("Simple data extract from the Strava API which I forked from here https://github.com/c-wilkinson/StravaDataAnalysis and altered to match what I was interested in as I do Bike Rides and Craig does Running\n\n")
        handle.write("He said\n\n")
        handle.write("As I'm sure is obvious, I'm teaching myself python as I go so the code quality is not likely to be great.  Do with it as you wish.\n\n")
        handle.write("I say - My Python knowledge is even more worserer than my spelling \n\n")
        handle.write('1.To use, create an Application on Strava.  This can be done here: https://www.strava.com/settings/api\n')
        handle.write('Give it a name, a website and an "Authorization Callback Domain".  The "Authorization Callback Domain" should be "local host".\n\n')
        handle.write('2.Copy and paste the following link into your browser, replacing {CLIENTIDHERE} with your numeric Client ID found on your Strava application settings page.\n')
        handle.write('> http://www.strava.com/oauth/authorize?client_id={CLIENTIDHERE}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all\n\n')
        handle.write('Click authorise when you visit the above link\n\n')
        handle.write('3.You will go to a 404 not found page with a link that looks like this: -\n')
        handle.write('> http://localhost/exchange_token?state=&code={LONGCODEHERE}&scope=read,activity:read_all,profile:read_all\n\n')
        handle.write('Copy the code after "&code=" to save for step 4.\n\n')
        handle.write('4.Open "getTokens.py", paste your code from step 3 to the variable "copied_code".  Add the client_id from your Application on Strava to the client_id variable.  Add the client_secret from your Application on Strava to the client_secret variable.  Save the changes.\n\n')
        handle.write('5.Run "getTokens.py".  This will create the initial tokens required for the script.\n\n')
        handle.write('6.Open "refreshTokens.py", add the client_id from your Application on Strava to the client_id variable.  Add the client_secret from your Application on Strava to the client_secret variable.  Save the changes.\n\n')
        handle.write('Once this has been completed, you can run "getData.py" which uses the tokens to get the data points.  If the access_token has expired, it will use the refresh_token to get a new token.\n\n')

if __name__ == '__main__':
    generateReadme()