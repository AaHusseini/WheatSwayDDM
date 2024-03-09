from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os

# Path to the Chrome WebDriver
chrome_driver_path = '/Applications/chromedriver-mac-x64/chromedriver'

# Initialize Chrome Options
options = Options()
# Uncomment the following line if you want to run Chrome headlessly
#options.add_argument('--headless')
# adding some options to configure the chrome webdriver for automatic downloads 
prefs = {
    "download.default_directory": '/Users/ayahusseini/Project/Database/original_flight_CSV_files',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option('prefs', prefs)

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

login_page_URL = 'https://app.airdata.com/main?a=login'

def get_login_info():
    """Prompt the user for login credentials."""
    usr = input('Username: ')
    pw = input('Password: ')
    return usr, pw

def new_login_to_airdata(driver, login_URL, savecookies=False, cookies_filename='login_cookies.json', login_details= False):
    """Perform a new login to Airdata and optionally save cookies."""
    if not login_details:
        username, password = get_login_info()
    else:
        username, password = login_details
    driver.get(login_URL)
    
    # Enter login credentials and sign in
    username_form = driver.find_element(By.ID, 'email')
    password_form = driver.find_element(By.ID, 'password')
    username_form.send_keys(username)
    password_form.send_keys(password)
    driver.find_element(By.ID, 'submitButton').click()

    # Wait for the login process to complete
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'menu_link_2'))
        )
    except TimeoutException:
        print('Login failed.')

    if savecookies:
        save_cookies(driver, cookies_filename)

def save_cookies(driver, cookies_filename):
    """Save the current session cookies to a file."""
    cookies = driver.get_cookies()
    with open(cookies_filename, 'w') as file:
        json.dump(cookies, file)
    print('Cookies successfully saved.')

def load_cookies(driver, cookies_filename, url_before_loading_cookies):
    """Load cookies from a file into the driver and refresh the page."""
    # Check if the cookies file exists
    if os.path.exists(cookies_filename):
        # Navigate to the domain before setting cookies
        driver.get(url_before_loading_cookies)
        
        with open(cookies_filename, 'r') as file:
            cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
    else:
        print('No such file found.')

