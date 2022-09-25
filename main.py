import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import os
import requests
import random

def get_driver(): 
    if "GOOGLE_CHROME_BIN" in os.environ:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    else:
        return webdriver.Safari()

def send_notification(title, body):
    url = 'https://fcm.googleapis.com/fcm/send'

    server_key = "AAAAI-h238w:APA91bFEbTW5GG-s-7elcTGdN5cdqmgbIgJnvP-VRXzzFTViVdXH6SCuSGWTvJ6a41iu9SiQKcbDiWARm2lz9k95mjYCz53Etv8xW__Xcvjh4daP1HqsveDfRO8wnvnfTBqVNncRBdH4"
    device_fcm = "cR1gkwwosEmTvRx6lTWQPU:APA91bFSAYWgXf5zi5AwvT3Lxv5Dn-RyO2TLyjkfInIqYkmUesL2fmSuw1BSboSCYDqzeIbhnCZ1DbcP_F6pRltGScJ-RcYl8p39sOByPiI7zRiMachXC0QqxBvEEuAOcVN99ezaXjTG"

    headers = {"Content-Type": "application/json", "Authorization": f"key={server_key}"}

    json = {
        "to": device_fcm,
        "notification": {
        "title": title,
        "body": body,
        "mutable_content": "true",
        "sound": "Tri-tone"
        },
    "data": {
        }
    }

    response = requests.post(url, headers=headers, json=json)
    print("Message sent: ", response.text)

def send_date_notification(date):
    send_notification("⚠️ Nova data disponível", date.strftime('%d/%m/%Y'))

def fetch_date():
    driver = get_driver()
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
    
    driver.close()
    return min(parsed_dates)

send_notification("🎉 Sistema inicializado", "Tudo em cima.")

while True:
    successes = 0
    errors = 0

    for x in range(60):
        try:
            date = fetch_date()
            print("Got date: ", date)
            if date < datetime.date(2022, 6, 1):
                send_date_notification(date)
                break
            successes+= 1
        except Exception as e:
            print("Error: ", e)
            errors+= 1
            time.sleep(60*10)

        number = random.uniform(3, 12)
        time.sleep(60*number)
    
    send_notification("⚙️ Sistema rodando", f"Nas últimas verificações, houveram {successes} sucessos e {errors} erros.")