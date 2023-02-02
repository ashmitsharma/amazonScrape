#importing required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}
#list to contain all products detail
all_products_details = []
#for loop to go till 20th Page
for i in range(1, 21):
    print(i)
    url = "https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=1675270125&sprefix=ba%2Caps%2C283&ref=sr_pg_2".format(i)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #list that contain all products HTML from a page
    all_products_on_page = soup.findAll("div", class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")
    #loop to get product URL, Title, Price, Rating, Number of Reviews
    for product in all_products_on_page:
        product_detail=[]
        product_url = "https://www.amazon.in" + str(product.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").get('href'))
        title = product.find("a",class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").text
        try:
            price = product.find("span", {'class': 'a-price-whole'}).text
        except:
            price = None
        try:
            rating = product.find("span", class_="a-icon-alt").text
        except:
            rating = None
        try:
            no_of_reviews = product.find("span", {'class': 'a-size-base s-underline-text'}).text
        except:
            no_of_reviews = None
        product_detail.append(product_url)
        product_detail.append(title)
        product_detail.append(price)
        product_detail.append(rating)
        product_detail.append(no_of_reviews)
        all_products_details.append(product_detail)

#This loop will scrape ASIN, Manufacturer, Description and Product Description from URL extracted in previous step
for productDetail in all_products_details:
    url = productDetail[0]
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    index = url.find('dp')
    asin = url[index+3: index +13]

    try:
        if soup.find("div", class_="a-expander-content a-expander-section-content a-section-expander-inner") == None:
            list = soup.find_all("li")
            for li in list:
                if li.text.find("Manufacturer") != -1:
                    manuf = li.text
                    manuf = manuf.replace(" ", "")
                    manuf = manuf.split(':')
                    manufacturer = str(manuf[1])
                    break
        else:
            trs = soup.find_all("tr")
            for tr in trs:
                if tr.text.find("Manufacturer") != -1:
                    manufacturer = tr.find("td", class_="a-size-base prodDetAttrValue").text
                    break
    except:
        manufacturer = None

    try:
        description = soup.find("ul", class_="a-unordered-list a-vertical a-spacing-mini")
        description = description.text
    except:
        description = None

    try:
        product_description = soup.find("div", class_="aplus-v2 desktop celwidget")
        product_description = product_description.text
        product_description = product_description.strip()
        product_description = product_description.replace("\n", "")
    except:
        product_description = None

    productDetail.append(asin)
    productDetail.append(manufacturer)
    productDetail.append(description)
    productDetail.append(product_description)

#empty list of each filed
url = []
title = []
price = []
rating = []
no_of_reviews = []
asin = []
manufacturer = []
description = []
product_description = []
#storing data from all product detail to specific list for easy excel file creation
for product_data in all_products_details:
    url.append(product_data[0])
    title.append(product_data[1])
    price.append(product_data[2])
    rating.append(product_data[3])
    no_of_reviews.append(product_data[4])
    asin.append(product_data[5])
    manufacturer.append(product_data[6])
    description.append(product_data[7])
    product_description.append(product_data[8])

#storing data to excel file
df = pd.DataFrame.from_dict({'URL':url,'Title':title,'Price':price,'Rating':rating,'Number of Reviews':no_of_reviews,'ASIN':asin,'Manufacturer':manufacturer,'Description':description,'Product Description':product_description})
df.to_excel('AmazonData.xlsx', header=True, index=False)