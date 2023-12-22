import numpy as np
from selenium import webdriver
from time import sleep
import random
from random import randint
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-notifications")

# driver = webdriver.Chrome(options=chrome_options)
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")

# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# URL
dates = [f'{str(day).zfill(2)}012024' for day in range(1, 30)]
total_price, carrier_name, flight_numb, depart_airport, arrival_airport ,depart_hour, arrival_hour, depart_date, arrival_date, flight_time, seat_class, plane, cabin_baggage, checked_baggage= [], [], [], [], [], [], [], [], [] ,[], [], [], [], []
for date in dates:
    url = f"https://baydep.vn/flights/PQCSGN{date}/1/0/0?nearby-airport=yes"
    driver.get(url)
    random_sleep = randint(20, 25)
    sleep(random_sleep)

    elems_fare_options = driver.find_elements(By.CSS_SELECTOR, ".fare-option")
    count = 1
    for elems_fare_option in elems_fare_options:
        elems_click = None
        try:
            xpath_expression = f'//*[@id="pnSearchResult"]/div[3]/div[5]/div[{count}]/div[1]/div[1]/div[2]/div[3]/div[4]/a'
            elems_click = elems_fare_option.find_element(By.XPATH, xpath_expression)
        except NoSuchElementException:
            print(f"Không tìm thấy phần tử với flightid = {count}")
        if elems_click:
            elems_click.click()
            sleep(randint(1, 3))

            elems_detail = driver.find_elements(By.CSS_SELECTOR, ".flight-detail-container")
            visible_flight_detail_containers = [elem for elem in elems_detail if "display: block" in elem.get_attribute("style")]
            for flight_detail_container in visible_flight_detail_containers:
            
                elems_carrier = flight_detail_container.find_element(By.CSS_SELECTOR, ".carrier-name")
                carrier_name.append(elems_carrier.get_attribute('innerHTML').strip(" "))
                
                elems_total_price = flight_detail_container.find_elements(By.CSS_SELECTOR, ".total-price strong")
                total_price.append(elems_total_price[1].text)
                
                elems_depart_airport = flight_detail_container.find_element(By.CSS_SELECTOR, ".depart span.airport-code")
                depart_airport.append(elems_depart_airport.text.strip("()"))
                
                elems_arrival_airport = flight_detail_container.find_element(By.CSS_SELECTOR, ".arrival span.airport-code")
                arrival_airport.append(elems_arrival_airport.text.strip("()"))
                
                elems_depart_hour = flight_detail_container.find_element(By.CSS_SELECTOR, ".depart span.hour")
                depart_hour.append(elems_depart_hour.text)
                
                elems_arrival_hour = flight_detail_container.find_element(By.CSS_SELECTOR, ".arrival span.hour")
                arrival_hour.append(elems_arrival_hour.text)
                
                elems_depart_date = flight_detail_container.find_element(By.CSS_SELECTOR, ".depart span.date")
                depart_date.append(elems_depart_date.text)
                
                elems_arrival_date = flight_detail_container.find_element(By.CSS_SELECTOR, ".arrival span.date")
                arrival_date.append(elems_arrival_date.text)
                
                elems_flight_info = flight_detail_container.find_elements(By.CSS_SELECTOR, ".flight-detail-info strong")
                flight_numb.append(elems_flight_info[0].text)
                flight_time.append(elems_flight_info[1].text)
                seat_class.append(elems_flight_info[2].text)
                plane.append(elems_flight_info[3].text)
                
                elems_baggage_info = flight_detail_container.find_elements(By.CSS_SELECTOR, ".baggage-type span.bag-value")
                checked_baggage.append(elems_baggage_info[0].text)
                cabin_baggage.append(elems_baggage_info[1].text)
            elems_click.click()
            sleep(randint(1, 3))
        count += 1

df = pd.DataFrame(list(zip(flight_numb, carrier_name, total_price, depart_airport, arrival_airport, depart_hour, arrival_hour, depart_date, arrival_date, flight_time, seat_class, plane, cabin_baggage, checked_baggage)), columns = ['flight-numb', 'airlines-name', 'price', 'depart-airport','arrival-airport','depart-hour', 'arrival-hour', 'depart-date', 'arrival-date', 'flight-time', 'seat-class', 'plane', 'cabin-baggage', 'checked-baggage'])
df['index_'] = np.arange(1, len(df) + 1)
df1 = df[df['arrival-airport'] == 'SGN']
df1.reset_index(drop=True, inplace=True)

df1.to_csv('data_flight_thang1_(PQC-SGN).csv', index=False)

driver.quit()
