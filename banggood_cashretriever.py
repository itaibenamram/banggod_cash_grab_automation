from decouple import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import time
import datetime
import pyautogui

# Setting environement variables
USERNAME = config('API_USERNAME')
PASSWORD = config('API_PASSWORD')
WEB_DRIVER = config('API_DRIVER')

def find_maxium_deposit():
    maximum_cash_text = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div/div[2]/div/p[3]")))
    maximum_cash = maximum_cash_text.get_attribute('innerText')[20:]
    print(f'Max Cash is:{maximum_cash}')
    return maximum_cash

def main():
    # Navigating to game machine page
    driver.get("https://www.banggood.com/Casual-Game-Money-Box.html?utmid=15618&bid=41104")
    print("Looking for element")
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.header-user-title")))
    print("Element Found, Logging in")

    # Logging In
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div[2]/ul/li[1]/div[1]/span/a[2]').click()
    time.sleep(0.5)
    email_input = driver.find_element_by_name("login-email")
    password_input = driver.find_element_by_name("login-pwd")
    email_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    print("submitting information")
    driver.find_element_by_name("login-submit").click()

    # Looking for maximum cash ammount
    maximum_cash = find_maxium_deposit()
    print(f'Starting cash detection - will deposit when at {maximum_cash}')

    # Time logging
    start_time = datetime.datetime.now()
    print(f'Time collection start: {start_time.strftime("%H:%M:%S")}')

    failure_counter = 0
    while True:
        try:
            paragraph = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div/div/div[2]/div/p[1]")
            cash = paragraph.get_attribute("innerText")
        except:
            failure_counter += 1
            if failure_counter > 5:
                break
            continue
        if int(cash) >= int(maximum_cash)/2:
            try:
                current_time = datetime.datetime.now()
                print(f'Collected {cash} at {current_time.strftime("%H:%M:%S")}')
                print(f'Current deposit took: {current_time - start_time} ')
                start_time = current_time
                driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div/div/div[2]/div/div").click()
            except:
                continue
        time.sleep(10)

def create_driver():
    user_input = WEB_DRIVER.lower()
    if user_input == "chrome":
        return webdriver.Chrome()
    elif user_input == "edge":
        return webdriver.Edge()
    else:
        return webdriver.Firefox()


if __name__ == "__main__":
    driver = create_driver()
    main()    
