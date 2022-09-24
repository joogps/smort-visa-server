import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

#driver = webdriver.Safari()

driver.get('https://ais.usvisa-info.com/en-br/niv/users/sign_in')

username = driver.find_element(By.ID, "user_email")
password = driver.find_element(By.ID, "user_password")

username.send_keys("joogps@gmail.com")
password.send_keys("xyFgac-jedwoc-5rarba")

time.sleep(1)

toggle = driver.find_element(By.CLASS_NAME, "icheckbox")
toggle.click()

commit = driver.find_element(By.NAME, "commit")
commit.click()

time.sleep(2)

button = driver.find_element(By.XPATH, "//a[@href='/en-br/niv/schedule/43465551/continue_actions']")
button.click()

time.sleep(2)

button = driver.find_element(By.CLASS_NAME, "fa-calendar-minus")
button.click()

time.sleep(1)

button = driver.find_element(By.XPATH, "//a[@href='/en-br/niv/schedule/43465551/appointment']")
button.click()

time.sleep(2)

commit = driver.find_element(By.NAME, "commit")
commit.click()

time.sleep(2)

picker = driver.find_element(By.ID, "appointments_consulate_appointment_date_input")
picker.click()

available_dates = []
while not available_dates:
    time.sleep(0.2)
    next_button = driver.find_element(By.CLASS_NAME, "ui-datepicker-next")
    next_button.click()
    available_dates = driver.find_elements(By.XPATH, "//td[contains(@class,'undefined') and not(contains(@class,'ui-datepicker-unselectable'))]")

parsed_dates = []
for date in available_dates:
    day = date.text
    month = date.get_attribute("data-month")
    year = date.get_attribute("data-year")

    parsed_dates.append(datetime.date(int(year), int(month) + 1, int(day)))

date = min(parsed_dates)
print(date)