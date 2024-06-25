import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

# BeautifulSoup
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US,es-ES;q=0.9,es;q=0.8,de;q=0.7",
}

response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers)
zillow_web_page = response.text
soup = BeautifulSoup(zillow_web_page, "html.parser")

# Create a list of links for all the listings scraped
houses = soup.find_all(class_="ListItem-c11n-8-84-3-StyledListCardWrapper")
link_list = [house.a.get("href")for house in houses]
print(link_list)

# Create a list of prices for all the listings you scraped.
prices = soup.find_all(attrs={"data-test": "property-card-price"})
price_list = [price.getText().strip("+/mo" "+ 1bd") for price in prices]
print(price_list)

# Create a list of addresses for all the listings you scraped.
addresses = soup.find_all(attrs={"data-test": "property-card-addr"})
address_list = [add.getText().strip(" \n|").replace(" | ", ", ") for add in addresses]

# Create a Google Form with 3 questions and pass each of the items in each list as an answer.
# Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://docs.google.com/forms/d/1QnlWhzvSdIuHqUYXleRnBbA8XEMVE7Jbb4VvHFAr4E8/edit")
driver.maximize_window()
time.sleep(2)

for index in range(len(link_list)):
    what_address = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/'
                                                       'div/div/div[2]/div/div[1]/div/div[1]/input')
    what_price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/'
                                                     'div[2]/div/div[1]/div/div[1]/input')
    what_link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/'
                                                    'div[2]/div/div[1]/div/div[1]/input')
    send_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    time.sleep(2)

    try:
        what_address.send_keys(address_list[index], Keys.ENTER)
        what_price.send_keys(price_list[index], Keys.ENTER)
        what_link.send_keys(link_list[index], Keys.ENTER)
        send_button.click()
        time.sleep(2)
        driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
    except StaleElementReferenceException as e:
        print(f"Error: {e}")

time.sleep(2)

