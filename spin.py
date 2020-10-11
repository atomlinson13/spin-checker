import time
from selenium import webdriver
from twilio.rest import Client

def send_text():
    account_sid = 'acct_id'
    auth_token = 'auth'
    client = Client(account_sid, auth_token)

    numbers_to_message = ['num1', 'num2']
    for number in numbers_to_message:
        client.messages.create(
            body = 'SPIN CLASSES ARE POSTED!',
            from_ = 'num',
            to = number
        )

def check_if_schedule_empty():
    driver.switch_to_frame(driver.find_element_by_id("sf-frame"))
    time.sleep(2)
    driver.find_element_by_id("scheduleNextArrow").click()
    driver.find_element_by_id("scheduleNextArrow").click()
    time.sleep(2)
    isEmpty = driver.execute_script('return document.getElementsByClassName("wppc-most-recent-val")[1].innerHTML.trim()  === "";')
    return isEmpty

url = "https://stridespinstudio.com/schedule/"
DRIVER_PATH = ''
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(url)


isEmpty = True
while(isEmpty):

    isEmpty = check_if_schedule_empty()

    if not isEmpty:
        send_text()
        break
    else:
        time.sleep(30)
        driver.refresh()