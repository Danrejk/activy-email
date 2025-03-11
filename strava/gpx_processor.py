import gpxpy
import random
import datetime
import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def isSunday():
    return datetime.datetime.now().weekday() == 6

def modifyGpx(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    timeMove = datetime.timedelta(random.uniform(0, 0.01))
    # Randomize the time, latitude, longitude and elevation of each point (make it look more realistic)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if not isSunday():
                    point.time += timeMove
                point.latitude += random.uniform(-0.00001, 0.00001)
                point.longitude += random.uniform(-0.00001, 0.00001)
                point.elevation += random.uniform(-0.01, 0.01)
                currentDay = int(datetime.datetime.now().strftime('%d'))
                point.time = point.time.replace(day=currentDay)
                currentMonth = int(datetime.datetime.now().strftime('%m'))
                point.time = point.time.replace(month=currentMonth)
                currentYear = int(datetime.datetime.now().strftime('%Y'))
                point.time = point.time.replace(year=currentYear)
    lastPoint = gpx.tracks[0].segments[-1].points[-1]
    lastPoint.time += datetime.timedelta(random.uniform(0, 0.02))


    with open(gpx_file_path[:-4] + '_modified.gpx', 'w') as gpx_file:
        gpx_file.write(gpx.to_xml())

def getRefreshToken(client_id, client_secret, code):
    url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=payload)
    try:
        return response.json()['refresh_token']
    except:
        return None

def refreshAccessToken(client_id, client_secret, refresh_token):
    url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url, data=payload)
    try:
        return response.json()['access_token'], response.json()['refresh_token']
    except:
        return None



def uploadToStrava(access_token, gpx_file_path):
    url = 'https://www.strava.com/api/v3/uploads'
    headers = {'Authorization': 'Bearer ' + access_token}
    with open(gpx_file_path, 'rb') as gpx_file:
        files = {'file': gpx_file}
        payload = {'data_type': 'gpx',
                   'activity_type': 'ride',
                   'name': '',
                   'commute': 'true'}
        if isSunday():
            payload['commute'] = 'false'
        response = requests.post(url, headers=headers, files=files, data=payload)
    return response.json()

def copyFile(src, dst):
    with open(src, 'rb') as f:
        with open(dst, 'wb') as f2:
            f2.write(f.read())

dataFolder = './data/'

def processTokens(client_id, client_secret, file_path):
    with open(file_path, 'r') as f:
        tokens = json.load(f)
    i = 0
    for token in tokens:
        i += 1
        if 'refresh_token' in token:
            access_token, refresh_token = refreshAccessToken(client_id, client_secret, token['refresh_token'])
            if access_token:
                token['access_token'] = access_token
                token['refresh_token'] = refresh_token
                if isSunday():
                    copyFile('sunday.gpx', dataFolder + str(i) + '/sunday.gpx')
                    modifyGpx(dataFolder + str(i) + '/sunday.gpx')
                else:
                    modifyGpx(dataFolder + str(i) + '/in.gpx')
                    modifyGpx(dataFolder + str(i) + '/out.gpx')
            else:
                print('Failed to refresh token')
    with open(file_path, 'w') as f:
        json.dump(tokens, f, indent=4)

def uploadAll(file_path):
    with open(file_path, 'r') as f:
        tokens = json.load(f)
    i = 0
    for token in tokens:
        i+=1
        if 'access_token' in token:
            print('Uploading ' + token['access_token'])
            if isSunday():
                print(uploadToStrava(token['access_token'], dataFolder + str(i) + '/sunday_modified.gpx'))
            else:
                print(uploadToStrava(token['access_token'], dataFolder + str(i) + '/in_modified.gpx'))
                print(uploadToStrava(token['access_token'], dataFolder + str(i) + '/out_modified.gpx'))
        else:
            print('No access token')

