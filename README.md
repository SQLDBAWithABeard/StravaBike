# Last Refreshed - 14 August, 2022 at 12:43:58
The Latest Activity was a Ride - 

<b>Sunday morning in the sunshine</b> 

which happened on 14 August, 2022 at 07:25:32 

Which is 0 years, 0 months, 0 days, 5 hours and 18 minutes since the last refresh! 

You can see it here https://www.strava.com/activities/7635100588 

## Number of Rides
How many rides have I done each year?

![Number_of_Rides_each_Year](Number_of_Rides_each_Year.png?raw=true "Number_of_Rides_each_Year")

|   Year |   Rides |   E-Bike |   Virtual |   Total Rides |
|-------:|--------:|---------:|----------:|--------------:|
|   2019 |      36 |        0 |         0 |            36 |
|   2020 |      44 |        0 |       168 |           212 |
|   2021 |     103 |       18 |        95 |           216 |
|   2022 |      26 |       58 |         6 |            90 |

## Distance Travelled

How many miles have I ridden?

![Number_of_Miles_each_Year](Number_of_Miles_each_Year.png?raw=true "Number_of_Miles_each_Year")

|   Year |   Ride Miles |   E-Bike Miles |   Virtual Miles |   Total Miles |
|-------:|-------------:|---------------:|----------------:|--------------:|
|   2019 |       474.41 |           0    |            0    |        474.41 |
|   2020 |       869.54 |           0    |         2004.61 |       2874.15 |
|   2021 |      2317.61 |         349.92 |         1228.45 |       3895.98 |
|   2022 |       558.21 |        1267.24 |           84.08 |       1909.53 |

## Elevation Climbed

How many metres have I climbed?

![Elevation_each_Year](Elevation_each_Year.png?raw=true "Elevation_each_Year")

|   Year |   Ride Elevation |   E-Bike Elevation |   Virtual Elevation |   Total Elevation |
|-------:|-----------------:|-------------------:|--------------------:|------------------:|
|   2019 |          10362   |                0   |                   0 |           10362   |
|   2020 |          17818.3 |                0   |               18937 |           36755.3 |
|   2021 |          43499.4 |             9272.8 |               12630 |           65402.2 |
|   2022 |          10054.2 |            31400.2 |                1821 |           43275.4 |

## Average Bike Speed Outside
How does my average bike speed vary for rides that are outside by distance, by year, and by type of ride?

![Average Bike Speed Outside](AverageSpeedOutSide.png?raw=true "Average Bike Speed Outside")

## Average Bike Speed Wherever
How does my average bike speed vary for rides by distance, by year, and by type of ride?

![AverageSpeed](AverageSpeed.png?raw=true "Average Bike Speed per Distance")

## Average Cadence
How does my average bike cadence vary for rides by distance, by year, and by type of ride?

![AverageCadence](AverageCadence.png?raw=true "Average Cadence per Distance")

## Average Power
How does my average bike power vary for rides by distance, by year, and by type of ride?

![AverageCadence](AveragePower.png?raw=true "Average Power per Distance")

## Outside Rides Distance by day
How far do I ride each day on average?

![DistanceByDayRide](DistanceByDayRide.png?raw=true "DistanceByDayRide")

## Cadence by day
Does my cadence change by the day of the week?

![CadenceByDay](CadenceByDay.png?raw=true "CadenceByDay")

## Rides by day
How far do I ride each day by Ride Type, by year, and by type of ride?

![DistanceByDay](DistanceByDay.png?raw=true "DistanceByDay")

## How Long by How Far
How far do I ride and how long does it take??

![Time_Taken_Distance](Time_Taken_Distance.png?raw=true "Time_Taken_Distance")

## 5 mile buckets
How many times do I ride in each 5 mile bucket for all activities?

![Number_of_Activities_per_Distance](Number_of_Activities_per_Distance.png?raw=true "Number_of_Activities_per_Distance")

## 5 mile buckets outside ?
How many times do I ride in each 5 mile bucket outside??

![Number_of_Rides_per_Distance](Number_of_Rides_per_Distance.png?raw=true "Number_of_Rides_per_Distance")

## Each Week Distance for 2022 ?
How far did I ride each week in 2022 ??

![Distance_per_Week_For_2022](Distance_per_Week_For_2022.png?raw=true "Distance_per_Week_For_2022")

## Each Week Distance for 2021 ?
How far did I ride each week in 2021 ??

![Distance_per_Week_For_2021](Distance_per_Week_For_2021.png?raw=true "Distance_per_Week_For_2021")

## Each Week Distance for 2020 ?
How far did I ride each week in 2020 ??

![Distance_per_Week_For_2020](Distance_per_Week_For_2020.png?raw=true "Distance_per_Week_For_2020")

## Each Week Distance for 2019 ?
How far did I ride each week in 2019 ??

![Distance_per_Week_For_2019](Distance_per_Week_For_2019.png?raw=true "Distance_per_Week_For_2019")

# StravaDataAnalysis
Simple data extract from the Strava API which I forked from here https://github.com/c-wilkinson/StravaDataAnalysis and altered to match what I was interested in as I do Bike Rides and Craig does Running

He said

As I'm sure is obvious, I'm teaching myself python as I go so the code quality is not likely to be great.  Do with it as you wish.

I say - My Python knowledge is even more worserer than my spelling 

1.To use, create an Application on Strava.  This can be done here: https://www.strava.com/settings/api
Give it a name, a website and an "Authorization Callback Domain".  The "Authorization Callback Domain" should be "local host".

2.Copy and paste the following link into your browser, replacing {CLIENTIDHERE} with your numeric Client ID found on your Strava application settings page.
> http://www.strava.com/oauth/authorize?client_id={CLIENTIDHERE}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all

Click authorise when you visit the above link

3.You will go to a 404 not found page with a link that looks like this: -
> http://localhost/exchange_token?state=&code={LONGCODEHERE}&scope=read,activity:read_all,profile:read_all

Copy the code after "&code=" to save for step 4.

4.Open "getTokens.py", paste your code from step 3 to the variable "copied_code".  Add the client_id from your Application on Strava to the client_id variable.  Add the client_secret from your Application on Strava to the client_secret variable.  Save the changes.

5.Run "getTokens.py".  This will create the initial tokens required for the script.

6.Open "refreshTokens.py", add the client_id from your Application on Strava to the client_id variable.  Add the client_secret from your Application on Strava to the client_secret variable.  Save the changes.

Once this has been completed, you can run "getData.py" which uses the tokens to get the data points.  If the access_token has expired, it will use the refresh_token to get a new token.

