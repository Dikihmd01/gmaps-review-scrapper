from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time
import pandas as pd

chrome_service = Service('/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=chrome_service, options=options)

def get_page_content(url, scroll_limit=5):
    number = 0
    last_height = driver.execute_script('return document.body.scrollHeight')

    btn_sort_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button'
    newest_list_item_xpath = '//li[@data-index="1"]'
    scroll_element_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
    gooegle_review_section_path = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]'

    # Get URL to access Google Maps Review
    driver.get(url)
    time.sleep(3)
    # Click sort button and choose Newst list item
    driver.find_element(By.XPATH, btn_sort_xpath).click()
    time.sleep(1)
    driver.find_element(By.XPATH, newest_list_item_xpath).click()
    time.sleep(5)

    # Get scroll height
    while True:
        number += 1
        scroll_elemet = driver.find_element(By.XPATH, scroll_element_xpath)
        driver.execute_script('arguments[0].scrollBy(0, 5000);', scroll_elemet)
        time.sleep(scroll_limit)

        # Calculate new scroll height
        scroll_elemet = driver.find_element(By.XPATH, scroll_element_xpath)
        new_height = driver.execute_script('return arguments[0].scrollHeight', scroll_elemet)

        if number == scroll_limit:
            break

        if new_height == last_height:
            break

        last_height = new_height
    
    raw_data = driver.find_elements(By.XPATH, gooegle_review_section_path)
    list_data = [data.text for data in raw_data]
    data = [data.split('\n') for data in list_data]
    time.sleep(3)

    return raw_data

def get_review(page_content):
    usernames = []
    reviews = []

    for content in page_content:
        button = content.find_elements(By.TAG_NAME, 'button')
        for more in button:
            if more.text == 'Lainnya':
                more.click()
        time.sleep(5)

        list_names = content.find_elements(By.CLASS_NAME, 'd4r55')
        list_review = content.find_elements(By.CLASS_NAME, 'MyEned')

        for name, review in zip(list_names, list_review):
            if review.text != '':
                usernames.append(name.text)
                reviews.append(review.text)

    data = {
        'username': usernames,
        'review': reviews
    }
    return data

def to_dataframe(data):
    df_review = pd.DataFrame(data)
    return df_review
