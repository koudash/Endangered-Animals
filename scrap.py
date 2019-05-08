# dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import os
import time
from splinter import Browser
from urllib.parse import urlsplit
from selenium import webdriver
import requests

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()


    url = "https://www.iucnredlist.org/species/12392/3339343"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    countries = soup.find('p',class_='card__data card__data--std card__data--accent')
    print(countries)

#     # Get the average temps
#     avg_temps = soup.find('div', id='weather')

#     # Get the min avg temp
#     min_temp = avg_temps.find_all('strong')[0].text

#     # Get the max avg temp
#     max_temp = avg_temps.find_all('strong')[1].text

#     # BONUS: Find the src for the sloth image
#     relative_image_path = soup.find_all('img')[2]["src"]
#     sloth_img = url + relative_image_path

    # Store data in a dictionary
    countries_data = {
        "countries": countries
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return countries_data

    from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()


    url = "https://www.iucnredlist.org/species/12392/3339343"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    countries = soup.find('p',class_='card__data card__data--std card__data--accent')
    print(countries)

#     # Get the average temps
#     avg_temps = soup.find('div', id='weather')

#     # Get the min avg temp
#     min_temp = avg_temps.find_all('strong')[0].text

#     # Get the max avg temp
#     max_temp = avg_temps.find_all('strong')[1].text

#     # BONUS: Find the src for the sloth image
#     relative_image_path = soup.find_all('img')[2]["src"]
#     sloth_img = url + relative_image_path

    # Store data in a dictionary
    countries_data = {
        "countries": countries
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return countries_data
