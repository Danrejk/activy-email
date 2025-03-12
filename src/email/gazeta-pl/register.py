from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

driver = webdriver.Chrome()

driver.get("https://konto.gazeta.pl/konto/szybka-rejestracja.servlet?back=https%3A%2F%2Fpoczta.gazeta.pl")

try:
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    accept_button.click()
except:
    pass

radio_button = driver.find_element(By.CSS_SELECTOR, "input[type='radio'][name='accountType'][value='0']")
radio_button.click()

name = "Adam"
surname = "Pluta"

driver.find_element(By.ID, "login").send_keys(name + surname  + str(random.randint(100, 999)))

password = "Password" + str(random.randint(1000, 9999))
driver.find_element(By.ID, "pass").send_keys(password)

driver.find_element(By.ID, "emailPassRecovery").send_keys("foyjames34@gmail.com")

birth_year = random.randint(1980, 2006)
birth_month = random.randint(1, 12)
birth_day = random.randint(1, 28)  # Simplified to avoid invalid dates
birth_date = f"{birth_day:02d}{birth_month:02d}{birth_year:04d}"
driver.find_element(By.ID, "birthDate").send_keys(birth_date)

driver.find_element(By.ID, "acceptEmailAccountTermsGazeta").click()

driver.find_element(By.ID, "accountRegister-rec3btn").click()

time.sleep(5)

driver.quit()