import json
import os
import sqlite3
import pyAesCrypt
import pandas
from os import stat
from datetime import datetime
import time
import numpy

# Global variables for use by this file
bufferSize = 64*1024
password = os.environ.get('ENCRYPTIONPASSWORD')

# py -c 'import databaseAccess; databaseAccess.reset()'
def reset():
    resetActivities()
    resetSplits()

# py -c 'import databaseAccess; databaseAccess.resetActivities()'
def resetActivities():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS activities;')
    conn.commit()
    conn.close()
    encryptDatabase()

# py -c 'import databaseAccess; databaseAccess.resetSplits()'
def resetSplits():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS splits;')
    conn.commit()
    conn.close()
    encryptDatabase()

def getLastDate():
    print('Getting last date')
    decryptDatabase()
    lastActivityDate = '1970-01-01T00:00:00Z'
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities';")
    result = cur.fetchone()
    if result is not None:
        # There is data, so let's grab the max datetime
        cur.execute("SELECT MAX(start_date_local) FROM activities;")
        result = cur.fetchone()
        if result is not None:
            # Found a max date
            lastActivityDate, = result
    conn.commit()
    conn.close()
    encryptDatabase()
    return lastActivityDate

def setConfig(strava_tokens):
    decryptDatabase()
    print('Lets put the tokens into the database')
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS config;')
    cur.execute('CREATE TABLE config (token_type VARCHAR, access_token VARCHAR, expires_at BIGINT, expires_in INT, refresh_token VARCHAR);')
    cur.execute('INSERT INTO config (token_type, access_token, expires_at, expires_in, refresh_token) values (?, ?, ?, ?, ?);', (strava_tokens['token_type'], strava_tokens['access_token'], strava_tokens['expires_at'], strava_tokens['expires_in'], strava_tokens['refresh_token']))
    conn.commit()
    conn.close()
    encryptDatabase()

def getConfig():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM config')
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    encryptDatabase()
    return json.loads(json.dumps( [dict(ix) for ix in rows] ))[0]

# Must be called to access the database, otherwise it can't be read
# py -c 'import databaseAccess; databaseAccess.decryptDatabase()'
def decryptDatabase():
    if os.path.exists('strava_temp.sqlite'):
        print('Database already decrypted!  Skipping. . .')
    else:
       # print('Looking for database and decrypting')
        if os.path.exists('strava.sqlite'):
            encFileSize = stat('strava.sqlite').st_size
            with open('strava.sqlite', 'rb') as fIn:
                with open('strava_temp.sqlite', 'wb') as fOut:
                    pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
        else:
            print('Unable to find database to decrypt!  Skipping. . .')

# Always call this after you touch the database to re-encrypt it
def encryptDatabase():
    if os.path.exists('strava_temp.sqlite'):
        if os.path.exists('strava.sqlite'):
            os.remove('strava.sqlite')
        with open('strava_temp.sqlite', 'rb') as fIn:
            with open('strava.sqlite', 'wb') as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
        if os.path.exists('strava_temp.sqlite'):
            os.remove('strava_temp.sqlite')
    else:
        print('Unable to find database to encrypt, skipping...')

def setActvities(activities):
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS activities (id BIGINT, name NVARCHAR, upload_id BIGINT, type VARCHAR, distance NUMERIC, moving_time INT, average_speed NUMERIC, max_speed NUMERIC, total_elevation_gain NUMERIC, start_date_local DATETIME, average_cadence NUMERIC, average_watts NUMERIC, average_heartrate NUMERIC, UNIQUE(id));')
    conn.commit()
    for _, currentActivity in activities.iterrows():
        acitivityName = currentActivity['name']
        activityId = currentActivity['id']
        print(f'Insert activity id [{activityId}], [{acitivityName}] to database')
        cur.execute('INSERT OR IGNORE INTO activities (id, name, upload_id, type, distance, moving_time, average_speed, max_speed, total_elevation_gain, start_date_local, average_cadence, average_watts, average_heartrate) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (activityId, acitivityName, currentActivity['upload_id'], currentActivity['type'], currentActivity['distance'], currentActivity['moving_time'], currentActivity['average_speed'], currentActivity['max_speed'], currentActivity['total_elevation_gain'], currentActivity['start_date_local'], currentActivity['average_cadence'], currentActivity['average_watts'], currentActivity['average_heartrate']))
        conn.commit()
        print(f'[{acitivityName}] done. . .')
    conn.close()
    encryptDatabase()

def setSplits(splits):
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS splits (split_id INT, activity_id BIGINT, activity_date DATETIME, average_speed NUMERIC, distance NUMERIC, elapsed_time INT, elevation_difference NUMERIC, moving_time INT, pace_zone INT, split INT, average_grade_adjusted_speed NUMERIC, average_heartrate NUMERIC, UNIQUE(split_id, activity_id));')
    conn.commit()
    for index, row in splits.iterrows():
        cur.execute('INSERT OR IGNORE INTO splits (split_id, activity_id, activity_date, average_speed, distance, elapsed_time, elevation_difference, moving_time, pace_zone, split, average_grade_adjusted_speed, average_heartrate) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (index, row['id'], row['date'], row['average_speed'], row['distance'], row['elapsed_time'], row['elevation_difference'], row['moving_time'], row['pace_zone'], row['split'], row['average_grade_adjusted_speed'], row['average_heartrate']))
        conn.commit()
    conn.close()
    encryptDatabase()

def getActvitiesMissingSplits():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='splits';")
    result = cur.fetchone()
    storedActivities = pandas.DataFrame()
    if result is not None:
        storedActivities = pandas.read_sql_query('SELECT * FROM activities WHERE id NOT IN (SELECT activity_id FROM splits)', conn)
    else:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='splits';")
        result = cur.fetchone()
        if result is not None:
            storedActivities = pandas.read_sql_query('SELECT * FROM activities', conn)
    conn.commit()
    conn.close()
    encryptDatabase()
    return storedActivities

def deleteActvitiesMissingSplits():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='splits';")
    result = cur.fetchone()
    if result is not None:
        cur = conn.cursor()
        cur.execute('DELETE FROM activities WHERE id NOT IN (SELECT activity_id FROM splits)')
    conn.commit()
    conn.close()
    encryptDatabase()

def getSplits():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='splits';")
    result = cur.fetchone()
    storedSplits = pandas.DataFrame()
    if result is not None:
        storedSplits = pandas.read_sql_query('SELECT s.split_id, s.activity_id, s.activity_date, s.average_speed, s.distance, s.elapsed_time, s.elevation_difference, s.moving_time, s.pace_zone, s.split, s.average_grade_adjusted_speed, s.average_heartrate, a.name, a.upload_id, a.type, a.distance AS total_distance, a.moving_time AS total_moving_time, a.average_speed AS total_average_speed, a.max_speed, a.total_elevation_gain, a.start_date_local, a.average_cadence FROM splits s INNER JOIN activities a ON a.id = s.activity_id', conn)
    conn.commit()
    conn.close()
    encryptDatabase()
    return storedSplits

def getMonthSplits():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='splits';")
    result = cur.fetchone()
    storedSplits = pandas.DataFrame()
    if result is not None:
        storedSplits = pandas.read_sql_query('SELECT split_id, activity_id, STRFTIME("%Y-%m", activity_date) AS activity_month, activity_date, average_speed, distance, elapsed_time, elevation_difference, moving_time, pace_zone, split, average_grade_adjusted_speed, average_heartrate FROM splits', conn)
    conn.commit()
    conn.close()
    encryptDatabase()
    return storedSplits

def getActivityDistances():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities';")
    result = cur.fetchone()
    activityCount = pandas.DataFrame()
    if result is not None:
       activityCount = pandas.read_sql_query("SELECT COUNT(*) AS cnt, CAST(CAST(nearest_5miles AS INT) AS VARCHAR(1000)) || ' < ' || CAST(CAST(nearest_5miles + 5 AS INT) AS VARCHAR(1000)) AS nearest_5miles FROM (SELECT id,  ROUND((distance* 0.000621371)/5,0)*5 AS nearest_5miles FROM activities) a GROUP BY nearest_5miles", conn)
    conn.commit()
    conn.close()
    encryptDatabase()
    return activityCount

def getActivityRideDistances():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities';")
    result = cur.fetchone()
    activityCount = pandas.DataFrame()
    if result is not None:
       activityCount = pandas.read_sql_query("SELECT COUNT(*) AS cnt,distance, CAST(CAST(nearest_5miles AS INT) AS VARCHAR(1000)) || ' < ' || CAST(CAST(nearest_5miles + 5 AS INT) AS VARCHAR(1000)) AS nearest_5miles FROM (SELECT id,distance,type, ROUND((distance* 0.000621371)/5,0)*5 AS nearest_5miles FROM activities WHERE type = 'Ride') a GROUP BY nearest_5miles,type ORDER BY distance", conn)
    conn.commit()
    conn.close()
    encryptDatabase()
    return activityCount

# py -c 'import databaseAccess; databaseAccess.getLastRun()'
def getlastActivity():
    decryptDatabase()
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities';")
    result = cur.fetchone()
    startDateTime = datetime.strptime('Jan 1 1970', '%b %d %Y')
    if result is not None:
        cur = conn.cursor()
        cur.execute("SELECT start_date_local FROM activities ORDER BY start_date_local DESC LIMIT 1;")
        row = cur.fetchone()
        cur.execute("SELECT start_date_local,name,type,id FROM activities ORDER BY start_date_local DESC LIMIT 1;")
        lastActivity = cur.fetchone()
    conn.commit()
    conn.close()
    encryptDatabase()
    return lastActivity

def getActivities():
    decryptDatabase()
    print('Getting Activities')
    conn = sqlite3.connect('strava_temp.sqlite')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities';")
    result = cur.fetchone()
    storedActivities = pandas.DataFrame()
    if result is not None:
        storedActivities = pandas.read_sql_query('SELECT * FROM activities;', conn)
    else:
        storedActivities = ''
    conn.commit()
    conn.close()
    encryptDatabase()
    #print('Adding some calulated columns')
    storedActivities['start_date_local'] = pandas.to_datetime(storedActivities['start_date_local'],errors='coerce')
    storedActivities['start_time'] = storedActivities['start_date_local'].dt.time
    storedActivities['start_date'] = storedActivities['start_date_local'].dt.date
    storedActivities['start_date_month'] = storedActivities['start_date_local'].dt.month
    storedActivities['start_date_day'] = storedActivities['start_date_local'].dt.day
    storedActivities['start_date_day_of_week'] = storedActivities['start_date_local'].dt.day_name()
    storedActivities['Year'] = storedActivities['start_date_local'].dt.year
    storedActivities['distance_km'] = storedActivities['distance']/1000
    storedActivities['distance_miles'] = storedActivities['distance_km']*0.621371
    storedActivities['distance_miles'] = storedActivities['distance_miles'].round(2)
    storedActivities['distance_miles_Ride'] = storedActivities['distance_miles'].where(storedActivities['type'] == 'Ride', 0)
    storedActivities['distance_miles_EBike'] = storedActivities['distance_miles'].where(storedActivities['type'] == 'EBikeRide', 0)
    storedActivities['distance_miles_VirtualRide'] = storedActivities['distance_miles'].where(storedActivities['type'] == 'VirtualRide', 0)
    storedActivities['elevation_Ride'] = storedActivities['total_elevation_gain'].where(storedActivities['type'] == 'Ride', 0)
    storedActivities['elevation_EBike'] = storedActivities['total_elevation_gain'].where(storedActivities['type'] == 'EBikeRide', 0)
    storedActivities['elevation_VirtualRide'] = storedActivities['total_elevation_gain'].where(storedActivities['type'] == 'VirtualRide', 0)
    storedActivities['IsVirtualRide'] = numpy.where(storedActivities['type'] == 'VirtualRide',True,False)
    storedActivities['IsOutsideRide'] = numpy.where(storedActivities['type'] == 'Ride',True,False)
    storedActivities['IsEBikeRide'] = numpy.where(storedActivities['type'] == 'EBikeRide',True,False)
    storedActivities['IsARide'] = numpy.where(storedActivities['type'].isin(['EBikeRide','Ride','VirtualRide']),True,False)
    # Max km/h speed original value is m/s
    # divide by 3600/1000
    storedActivities['max_speed_km_hr'] = storedActivities['max_speed'] *3.6
    storedActivities['average_speed_km_hr'] = storedActivities['average_speed'] *3.6
    storedActivities['average_speed_miles_hr'] = storedActivities['average_speed'] *3.6*0.621371
    storedActivities['max_speed_miles_hr'] = storedActivities['max_speed'] *3.6*0.621371
    #print('Returning Some data')
    return storedActivities