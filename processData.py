import visualiseData
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Commenting out for now as we're not using the new version of this yet
# import dataPredication
import databaseAccess

# py -c 'import processData; processData.generateReadme()'
def generateReadme():
    visualiseData.produceAverageSpeedOutside()
    visualiseData.produceAverageSpeed()
    visualiseData.produceAverageCadence()
    visualiseData.produceAveragePower()
    visualiseData.produceDistanceByDay()
    visualiseData.produceDistanceByDayRide()
    visualiseData.produceCadenceByDay()
    visualiseData.produceElapsedTimeDistance()
    lastActivity = databaseAccess.getlastActivity()
    lastActivityDate = datetime.strptime(lastActivity[0], "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now()
    now_string = now.strftime("%d %B, %Y at %H:%M:%S")
    delta = relativedelta(datetime.now(), lastActivityDate )
    if os.path.exists('README.md'):
        os.remove('README.md')
    with open('README.md', 'w') as handle:
        handle.write('# Generated From Strava - Last Refreshed - {0}\n'.format(now_string))
        handle.write('The Latest Activity was a {0} called {1} which happened on {2} \n\n'.format( lastActivity[2],lastActivity[1],lastActivity[0]))
        handle.write('Which is {0} years, {1} months, {2} days, {3} hours and {4} minutes since the last refresh! \n\n'.format( delta.years, delta.months, delta.days, delta.hours, delta.minutes))
        handle.write('You can see it here https://www.strava.com/activities/{0} \n\n'.format( lastActivity[3] ))
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