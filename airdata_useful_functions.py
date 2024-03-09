flight_log_URL = 'https://app.airdata.com/flight/last' 

def get_flight_information(driver, flight_log_page_url):
    driver.get(flight_log_page_url)