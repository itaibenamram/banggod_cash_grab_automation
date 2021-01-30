from decouple import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import pickle
import urllib.request
import time
import datetime
import pyautogui

# Setting environement variables
USERNAME = config('API_USERNAME')
PASSWORD = config('API_PASSWORD')
CHROME_PATH = config('CHROME_PATH')
game_link = "https://www.banggood.com/Casual-Game-Money-Box.html?utmid=15618&bid=41104"

def create_driver():
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(options=options, executable_path=CHROME_PATH)
    return driver

def load_cookie():
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        print("loading cookies...")
        print(type(cookies))
        for cookie in cookies:
            driver.add_cookie(cookie)
        
    except:
        print("Was not able to load cookies, trying to login")
        
def set_cookie():
    print("Trying to get cookie")
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    print("Cookie Set")

def login_to_banggood():
    try:
        print("Looking for logging element")
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
    except:
        print("Could not login - continuing")
        return

def find_maxium_deposit():
    maximum_cash_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div/div[2]/div/p[3]")))
    maximum_cash = maximum_cash_element.get_attribute('innerText')[20:]
    print(f'Max Cash is:{maximum_cash}')
    return maximum_cash

def repeat_single_daily(daily_element, daily_type, button_xpath, wait_time):
    daily_element = daily_element.get_attribute("innerText")[-4:-1].split("/")
    daily_lower_bound = int(daily_element[0])
    daily_upper_bound = int(daily_element[1])
    print(f"{daily_type} count is {daily_lower_bound} out of {daily_upper_bound}")
    if int(daily_lower_bound) < int(daily_upper_bound):
        print(f"Starting {daily_type} dailies")
        for i in range(int(daily_lower_bound), int(daily_upper_bound)):
            try:
                button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, button_xpath)))
                print("Detected daily task button")
                button_text = button.get_attribute("innerText")
                print(f"Collecting task {i} out of {daily_upper_bound} - button_text")
                if button_text == "GO":
                    button.click()
                    time.sleep(wait_time)
                    driver.get(game_link)
                elif button_text == "GET":
                    button.click()
            except:
                print("Could not find button")

def do_dailies():
    print("Checking dailies")
    selected_products_count = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div[3]/div[3]/ul/li/p[3]/span")))
    repeat_single_daily(selected_products_count, "Selected Procuts", "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div[3]/div[3]/ul/li/p[4]/span", 10)
            
    activity_for_15s_count =  WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[3]/ul/li/p[3]/span")))
    repeat_single_daily(activity_for_15s_count, "Activity for 15s", "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[3]/ul/li/p[4]/span", 16)

    print("Finished Dailies")

def collect_cash(maximum_cash):
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
                break
            except:
                continue
        time.sleep(10)

def main():

    driver.get("http://www.banggood.com")
    load_cookie()
    driver.refresh()
    time.sleep(5)
    
    # Login to Banggood
    login_to_banggood()
    
    continue_affirmation = input("Are you logged in? y/n  ")
    
    if continue_affirmation == "y":
        set_cookie()
        driver.get(game_link)
        # Looking for maximum cash ammount
        maximum_cash = find_maxium_deposit()
        print(f'Starting cash detection - will deposit when at {int(maximum_cash)/2}')
        while True:
            do_dailies()
            collect_cash(maximum_cash)
    else:
        driver.quit()

if __name__ == "__main__":
    driver = create_driver()
    main()
