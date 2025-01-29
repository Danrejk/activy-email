import json
import string
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from gpx_processor import refreshAccessToken, getRefreshToken, config
def generateRandomString(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))


def addTokenData(new_data):
    with open('tokens.json', 'r') as file:
        tokens = json.load(file)

    tokens.append(new_data)

    with open('tokens.json', 'w') as file:
        json.dump(tokens, file, indent=4)


mail = input('Enter your email: ')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Register the account
driver.get('https://www.strava.com/register/free')
driver.implicitly_wait(10)
element = driver.find_element(By.ID, 'mobile-email')
element.send_keys(mail)
element = driver.find_element(By.ID, 'mobile-new-password')
element.send_keys(config['accounts_password'])
element.send_keys(Keys.RETURN)
while driver.current_url == 'https://www.strava.com/register/free':
    pass

# Fill the form
element = driver.find_element(By.ID, 'firstName')
element.send_keys(config['accounts_name'])
element = driver.find_element(By.ID, 'lastName')
element.send_keys(generateRandomString())

element = driver.find_element(By.ID, 'react-select-2-input')
element.send_keys('January', Keys.RETURN)
element = driver.find_element(By.ID, 'react-select-3-input')
element.send_keys('1', Keys.RETURN)
element = driver.find_element(By.ID, 'react-select-4-input')
element.send_keys('2000', Keys.RETURN)
element = driver.find_element(By.ID, 'react-select-5-input')
element.send_keys('Man', Keys.RETURN)

element = driver.find_element(By.XPATH, "//div[contains(text(), 'Continue')]")
element.click()

print('Account created successfully!')
print('Email: ' + mail)
print('Password: ' + config['accounts_password'])

time.sleep(2)

# Authorize ur app
authorizeUrl = 'https://www.strava.com/oauth/authorize?client_id=' + config['client_id'] + '&response_type=code&redirect_uri=http://www.franki.ovh/&scope=activity:write'
driver.get(authorizeUrl)
authorize_button = driver.find_element(By.ID, 'authorize')
authorize_button.click()
while driver.current_url == authorizeUrl:
    pass
code = driver.current_url.split('code=')[1].split('&')[0]
print('Code: ' + code)
refreshToken = getRefreshToken(config['client_id'], config['client_secret'], code)
accessToken = refreshAccessToken(config['client_id'], config['client_secret'], refreshToken)[0]
print('Refresh token: ' + refreshToken)
print('Access token: ' + accessToken)


addTokenData({
    "mail": mail,
    "refresh_token": refreshToken,
    "access_token": accessToken,
})

input('Press Enter to close the browser...')
