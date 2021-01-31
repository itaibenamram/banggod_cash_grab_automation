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
game_link = "https://www.banggood.com/Casual-Game-Money-Box.html"

def print_message(message):
    message_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{message_time}: {message}")
    return

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
        print_message("loading cookies...")
        for cookie in cookies:
            driver.add_cookie(cookie)
        return
    except:
        print_message("ERROR - Was not able to load cookies, trying to login")
        return
        
def set_cookie():
    print_message("Trying to get cookie")
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    print_message("Cookie Set")
    return

def login_to_banggood():
    try:
        print_message("Looking for logging element")
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.header-user-title")))
        print_message("Element Found, Logging in")

        # Logging In
        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div[2]/ul/li[1]/div[1]/span/a[2]').click()
        time.sleep(0.5)
        email_input = driver.find_element_by_name("login-email")
        password_input = driver.find_element_by_name("login-pwd")
        email_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        print_message("submitting information")
        driver.find_element_by_name("login-submit").click()
    except:
        print_message("Could not login - continuing")
        return

def find_maxium_deposit():
    maximum_cash_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div/div[2]/div/p[3]")))
    maximum_cash = maximum_cash_element.get_attribute('innerText')[20:]
    print_message(f'Max Cash is:{maximum_cash}')
    return maximum_cash

def repeat_single_daily(daily_element, daily_type, button_xpath, wait_time):
    daily_element = daily_element.get_attribute("innerText")[-4:-1].split("/")
    daily_lower_bound = int(daily_element[0])
    daily_upper_bound = int(daily_element[1])
    print_message(f"{daily_type} count is {daily_lower_bound} out of {daily_upper_bound}")
    if int(daily_lower_bound) < int(daily_upper_bound):
        print_message(f"Starting {daily_type} dailies")
        for i in range(0, (int(daily_upper_bound) - int(daily_lower_bound))*2):
            try:
                button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, button_xpath)))
                print_message(f"Collecting task {daily_lower_bound} out of {daily_upper_bound} | part {i+1} of {(int(daily_upper_bound) - int(daily_lower_bound))*2}")
                button_text = button.get_attribute("innerText")
                if button_text == "GO":
                    button.click()
                    time.sleep(wait_time)
                    driver.get(game_link)
                elif button_text == "GET":
                    button.click()
                    daily_lower_bound += 1
                    time.sleep(wait_time)
            except:
                print_message("Could not find button")

def do_dailies():
    print_message("Checking dailies")
    selected_products_count = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div[3]/div[3]/ul/li/p[3]/span")))
    repeat_single_daily(selected_products_count, "Selected Procuts", "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div[3]/div[3]/ul/li/p[4]/span", 5)
            
    activity_for_15s_count =  WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[3]/ul/li/p[3]/span")))
    repeat_single_daily(activity_for_15s_count, "Activity for 15s", "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[3]/ul/li/p[4]/span", 16)

    print_message("Dailies done.")

def collect_cash():
    maximum_cash = find_maxium_deposit()

    print_message(f'Starting cash detection - will deposit when at {int(maximum_cash)/2}')
    
    failure_counter = 0
    while True:
        try:
            paragraph = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div/div/div[2]/div/p[1]")
            cash = paragraph.get_attribute("innerText")
            if int(cash) >= int(maximum_cash)/2:
                try:
                    print_message(f'Collected {cash}')
                    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div/div/div[2]/div/div").click()
                    break
                except:
                    continue
        except:
            failure_counter += 1
            if failure_counter > 5:
                print_message("ERROR - Lost cash html element - breaking cash grab")
                break
            continue
        time.sleep(10)

def main():

    driver.get("https://www.banggood.com")
    load_cookie()
    driver.refresh()
    time.sleep(5)
    
    # Login to Banggood
    login_to_banggood()
    
    continue_affirmation = input("Are you logged in? y/n  ")
    
    if continue_affirmation == "y":
        set_cookie()
        driver.get(game_link)
        while True:
            do_dailies()
            collect_cash()
            driver.refresh()
            time.sleep(5)
    else:
        driver.quit()

if __name__ == "__main__":
    driver = create_driver()
    main()
