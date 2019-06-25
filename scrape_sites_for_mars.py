from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path":r"C:\Users\Mrinalini\Desktop\MarkDowns\Web scraping Document DBs\mission_to_mars\chromedriver_win32}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_Data = {}

    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(2)

    html = browser.html
    soup = bs(html,"html.parser")

    #latest news about mars from  site
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    mars_Data['news_title'] = news_title
    mars_Data['news_paragraph'] = news_paragraph 
    
    #featured image of Mars
    nasa_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(nasa_image)
    time.sleep(2)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(nasa_image))
    
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[3]/a/div/div[2]/img"

    #click on the mars featured image using splinter for full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    time.sleep(2)
    
    #image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = base_url + img_url
    mars_Data["featured_image"] = full_img_url
    
   
    #get mars weather's latest tweet from twitter
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_Data["mars_weather"] = mars_weather

    # mars facts

    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)
    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_Data["mars_facts_table"] = mars_html_table

    # mars hemisperes

    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    # base url
    hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
    hemisphere_img_urls = []
    hemisphere_img_urls


    # Image Url of Cerberus Hemisphere from astrogeology.usgs.gov

    hemisphere_img_urls = []
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
    time.sleep(2)
    cerberus_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    cerberus_image = browser.html
    soup = bs(cerberus_image, "html.parser")
    cerberus_url = soup.find("img", class_="wide-image")["src"]
    cerberus_img_url = hemisphere_base_url + cerberus_url
    cerberus_title = soup.find("h2",class_="title").text
    cerberus = {"image title":cerberus_title, "image url": cerberus_img_url}
    hemisphere_img_urls.append(cerberus)


    # Image Url of Valles Marineris Hemisphere from astrogeology.usgs.gov 
    browser.visit(url_hemisphere)
    
    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
    time.sleep(2)
    valles_marineris_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    valles_marineris_image = browser.html
    soup = bs(valles_marineris_image, "html.parser")
    valles_marineris_url = soup.find("img", class_="wide-image")["src"]
    valles_marineris_img_url = hemisphere_base_url + valles_marineris_url
    valles_marineris_title = soup.find("h2",class_="title").text
    valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_img_url}
    hemisphere_img_urls.append(valles_marineris)

    
    # Image Url of Syrtis Major Hemisphere from astrogeology.usgs.gov 
    browser.visit(url_hemisphere)
    
    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
    time.sleep(2)
    syrtis_major_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    syrtis_major_image = browser.html
    soup = bs(syrtis_major_image, "html.parser")
    syrtis_major_url = soup.find("img", class_="wide-image")["src"]
    syrtis_major_img_url = hemisphere_base_url + syrtis_major_url
    syrtis_major_title = soup.find("h2",class_="title").text
    syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_img_url}
    hemisphere_img_urls.append(syrtis_major)


    # Image Url of Schiaparelli Hemisphere from astrogeology.usgs.gov  
    browser.visit(url_hemisphere)

    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
    time.sleep(2)
    schiaparelli_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    schiaparelli_image = browser.html
    soup = bs(schiaparelli_image, "html.parser")
    schiaparelli_url = soup.find("img", class_="wide-image")["src"]
    schiaparelli_img_url = hemisphere_base_url + schiaparelli_url
    schiaparelli_title = soup.find("h2",class_="title").text
    schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_img_url}
    hemisphere_img_urls.append(schiaparelli)


    mars_Data["hemisphere_img_url"] = hemisphere_img_urls

    

    return mars_Data