from time import sleep
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# chromedriver controls the browser on which the website to be scrapped will opened from backend 
# Change this to the system's chromedriver path
chromedriver_path="C:/Users/RITIK AGRAWAL/Desktop/Mtech 1st sem/DPM/dpm project/WEB scrapping/flight_scraper/chromedriver.exe"


def start_kayak(city_from, city_to, date_start, date_end):
    global driver
    driver = webdriver.Chrome(executable_path=chromedriver_path)

    kayak = ('https://www.kayak.com/flights/' + city_from + '-' + city_to +
             '/' + date_start + '-flexible/' + date_end + '-flexible?sort=bestflight_a')
    driver.minimize_window()
    print("\n\n----------------------came into scraping function------------------------\n\n ")
    print("\n\n----------------------Going on sleep for 20 seconds as buffer period such that website loads completely ------------------------\n\n ")
    driver.get(kayak)
    sleep(20)
    print('\n\n--------------------------starting first scrape......................................\n\n')
    df_flights_best = page_scrape()
    df_temp=df_flights_best.copy()
    df_flights_best['Filter'] = 'best'
    sleep(randint(6, 8))
    matrix = driver.find_elements_by_xpath(
        '//*[contains(@id,"FlexMatrixCell")]')
    matrix_prices = [price.text.replace('$', '') for price in matrix]
    matrix_prices = [i for i in matrix_prices if (i != '')]
    matrix_prices = [i.replace(",","") for i in matrix_prices ]
    matrix_prices = list(map(int, matrix_prices))
    matrix_min = min(matrix_prices)
    matrix_avg = sum(matrix_prices)/len(matrix_prices)

    print('switching to cheapest results.....')
    df_flights_cheap = df_temp.sort_values(by=['Price($)'])
    df_flights_cheap['Filter'] = 'cheap'

    print('\n\n--------------------------starting third scrape................................')

    # df_flights_fast = df_flights_best.sort_values(by=['Out Duration'])
    df1 = df_temp["Out Duration"].tolist()
    df1 = [i.replace("h"," ") for i in df1 ] 
    df1 = [i.replace("m","") for i in df1 ] 
    l=[]
    for i in df1:
        print(i)
        l1= i.split()
        print(l1)
        a= int(l1[0])*60 + int(l1[1])
        print(a)
        l.append(a)
    df1= pd.DataFrame(l,columns = ["Duration"])
    df_temp = pd.concat([df_temp,df1], axis =1)
    df_temp = df_temp.sort_values(by=['Duration'])
    df_temp = df_temp.drop("Duration",axis='columns')
    df_flights_fast=df_temp
    df_flights_fast['Filter'] = 'fast'
    final_df = df_flights_cheap.append(df_flights_best).append(df_flights_fast)
    print("\n\n--------------------------Final df:---------------------------------------------------\n\n")
    print(final_df)
    final_df.to_csv('file1.csv')

    xp_loading = '//div[contains(@id,"advice")]'
    loading = driver.find_element_by_xpath(xp_loading).text
    xp_prediction = '//span[@class="info-text"]'
    prediction = driver.find_element_by_xpath(xp_prediction).text
    print("\n\n Rate prediction data scraped from website.")
    print(loading+'\n'+prediction)
    print("\n\n")


    # This is the "weird" symbol used on the website. That's why we are using it here like this.
    weird = '¯\\_(ツ)_/¯'
    if loading == weird:
        loading = 'Not sure'
 
    return [df_flights_best,df_flights_cheap,df_flights_fast]


def page_scrape():
    global driver
    xp_sections = '//*[@class="section duration allow-multi-modal-icons"]'
    sections = driver.find_elements_by_xpath(xp_sections)
    sections_list = [value.text for value in sections]
    section_a_list = sections_list[::2]
    section_b_list = sections_list[1::2]
    if section_a_list == []:
        raise SystemExit
    a_duration = []
    a_section_names = []
    for n in section_a_list:
        a_section_names.append(''.join(n.split()[2:5]))
        a_duration.append(''.join(n.split()[0:2]))
    b_duration = []
    b_section_names = []
    for n in section_b_list:
        b_section_names.append(''.join(n.split()[2:5]))
        b_duration.append(''.join(n.split()[0:2]))

    xp_dates = '//div[@class="section date"]'
    dates = driver.find_elements_by_xpath(xp_dates)
    dates_list = [value.text for value in dates]
    a_date_list = dates_list[::2]
    b_date_list = dates_list[1::2]

    a_day = [value.split()[0] for value in a_date_list]
    a_weekday = [value.split()[1] for value in a_date_list]
    b_day = [value.split()[0] for value in b_date_list]
    b_weekday = [value.split()[1] for value in b_date_list]

    xp_prices = '//span[@class="price-text"]'
    prices = driver.find_elements_by_xpath(xp_prices)

    prices_list = [price.text.replace('$', '')
                   for price in prices if price.text != '']

    prices_list = [price.replace(',', '')
                   for price in prices_list]

    prices_list = list(map(int, prices_list))

    xp_stops = '//span[contains(@class,"stops-text")]'
    stops = driver.find_elements_by_xpath(xp_stops)
    stops_list = [stop.text[0].replace('n', '0') for stop in stops]

    a_stop_list = stops_list[::2]
    b_stop_list = stops_list[1::2]

    xp_stops_cities = '//span[@class="js-layover"]'

    stops_cities = driver.find_elements_by_xpath(xp_stops_cities)
    try:

        stops_cities_list = [stop.text for stop in stops_cities]

    except:
        pass
    a_counter = 0
    b_counter = 0
    stops_cities_list_a = []
    stops_cities_list_b = []
    stops_cities_list_counter = 0
    if (len(stops_cities_list) == 0):
        stops_cities_list_a = ["-"]*len(a_stop_list)
        stops_cities_list_b = ["-"]*len(b_stop_list)
    else:
        while (b_counter < len(b_stop_list)):
            l1 = []

            for _ in range(int(a_stop_list[a_counter])):
                l1.append(stops_cities_list[stops_cities_list_counter])
                stops_cities_list_counter += 1
            a_counter += 1
            if (len(l1) != 0):
                stops_cities_list_a.append("&".join(l1))
            else:
                stops_cities_list_a.append("-")

            l2 = []

            for _ in range(int(b_stop_list[b_counter])):
                l2.append(stops_cities_list[stops_cities_list_counter])
                stops_cities_list_counter += 1
            if (len(l2) != 0):
                stops_cities_list_b.append("&".join(l2))
            else:
                stops_cities_list_b.append("-")

            b_counter += 1

    xp_schedule = '//div[@class="section times"]'
    schedules = driver.find_elements_by_xpath(xp_schedule)
    hours_list = []
    carrier_list = []
    for schedule in schedules:
        hours_list.append(schedule.text.split('\n')[0])
        carrier_list.append(schedule.text.split('\n')[1])

    a_hours = hours_list[::2]
    a_carrier = carrier_list[::2]
    b_hours = hours_list[1::2]
    b_carrier = carrier_list[1::2]
    #printing the length of each data columns for debugging
    print(len(a_duration))
    print(len(a_section_names))
    print(len(a_stop_list))
    print(len(a_hours))
    print(len(a_carrier))
    print(len(b_duration))
    print(len(b_section_names))
    print(len(b_stop_list))
    print(len(b_hours))
    print(len(b_carrier))
    print(len(prices_list))
    print(len(stops_cities_list_a))
    print(len(stops_cities_list_b))
    cols = (['Out Date', 'Out Day', "Out Duration", 'Out Cities', '#Out Stops', 'Out Stop Cities', 'Out Time', 'Out Airline', 'Return Date', 'Return Day', 'Return Duration', 'Return Cities', '#Return Stops', 'Return Stop Cities',
             'Return Time', 'Return Airline', 'Price($)'])

    flights_df = pd.DataFrame({
        'Out Date': a_day,
        'Out Day': a_weekday,
        'Out Duration': a_duration,
        'Out Cities': a_section_names,
        '#Out Stops': a_stop_list,
        'Out Stop Cities': stops_cities_list_a,
        'Out Time': a_hours,
        'Out Airline': a_carrier,
        'Return Date': b_day,
        'Return Day': b_weekday,
        'Return Duration': b_duration,
        'Return Cities': b_section_names,
        '#Return Stops': b_stop_list,
        'Return Stop Cities': stops_cities_list_b,
        'Return Time': b_hours,
        'Return Airline': b_carrier,
        'Price($)': prices_list})[cols]

    return flights_df
