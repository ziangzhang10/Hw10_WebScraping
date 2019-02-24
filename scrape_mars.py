# import beautiful soup
from bs4 import BeautifulSoup as bs

# import Pandas
import pandas as pd

# import splinter for automated browser manipulation
from splinter import Browser

# import request library for http requests
import requests

# import time
import time

def scrape(): 

    # ===========================================
    # declare dictionary for all results
    all_dict = {
        "mars_news_title": "",
        "mars_news_text": "",
        "featured_image_url": "",
        "mars_weather": "",
        "mars_facts": "",
        "hemisphere_list": ""
    }

    # ===========================================
    # Mars news url to be scraped
    mars_news_url = "https://mars.nasa.gov/news/"

    # module to call API
    response = requests.get(mars_news_url)

    # scrape raw text from page
    soup = bs(response.text, "html.parser")

    # print soup
    #print(soup.prettify())

    # get all the responses as an iterable list
    results = soup.find_all('div', class_="slide")

    # print the latest news
    #print(results[0].prettify)

    # get news title
    mars_news_title = results[0].find("div", class_="content_title").find("a").text.strip()
    print(mars_news_title)

    # get news text
    mars_news_text = results[0].find("div", class_="rollover_description_inner").text.strip()
    print(mars_news_text)

    all_dict["mars_news_title"] = mars_news_title
    all_dict["mars_news_text"] = mars_news_text

    # ===========================================
    # open browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit the page for image
    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)

    # find the button to clicked the feature image
    button = browser.click_link_by_partial_text("FULL IMAGE")

    # Otherwise, this code cannot run in one flow; please blame Splinter
    time.sleep(1)

    # get image url
    soup = bs(browser.html, "html.parser")
    whatever = soup.find("img", {"class":"fancybox-image"})
    print(type(whatever))
    featured_image_url = "https://www.jpl.nasa.gov" + whatever["src"]
    print(featured_image_url)

    browser.quit()

    all_dict["featured_image_url"] = featured_image_url

    # ===========================================
    # Mars weather url to be scraped
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"

    # module to call API
    response = requests.get(mars_weather_url)

    # scrape raw text from page
    soup = bs(response.text, "html.parser")

    # print soup
    #print(soup.prettify())

    # get all the responses as an iterable list
    results = soup.find_all('div', class_="js-tweet-text-container")

    # print the latest weather tweet
    # print(results[0].prettify)

    # get tweet text
    for result in results:
        # get rid of the unwanted tail
        trash = result.find("a", class_="twitter-timeline-link")
        _ = trash.extract()
        # now get the "pure" output
        mars_weather = result.find("p", class_="js-tweet-text").text.strip()
        # if it's a valid weather tweet
        if "InSight" in mars_weather:
            print(mars_weather)
            break

    all_dict["mars_weather"] = mars_weather

    # ===========================================
    # Mars facts url to be scraped
    mars_facts_url = "https://space-facts.com/mars/"

    # read table into pandas
    tables = pd.read_html(mars_facts_url)
    table = tables[0]

    # change name of columns
    table.columns = ['Parameter', 'Value']
    #display(table)

    # convert table to html
    mars_facts = table.to_html()
    mars_facts

    all_dict["mars_facts"] = mars_facts

    # ===========================================
    # open browser (if closed already)
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit the page for image
    mars_hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemis_url)


    # find the button to clicked the feature image
    buttons = browser.find_by_css('img[class="thumb"]')
    buttons_length = len(buttons)
    button = buttons[0]

    dict_list = []

    # loop over all the buttons
    for i in range(buttons_length):
        button.click()
        
        #extract elements with beautifulsoup
        soup = bs(browser.html, "html.parser")
        img_title = soup.find('h2', class_="title").text.strip()
        img_url = soup.find('a', target="_blank")['href']
        
        # append list of dictionaries
        this_dict = {
            "title": "",
            "img_url": ""
        }
        this_dict["title"] = img_title
        this_dict["img_url"] = img_url
        dict_list.append(this_dict)

        # go back one level
        browser.back()
        buttons = browser.find_by_css('img[class="thumb"]')
        if i+1 in range(buttons_length):
            button = buttons[i+1]
        else:
            pass
        
    browser.quit()

    all_dict["hemisphere_list"] = dict_list
    print(all_dict)

    return all_dict