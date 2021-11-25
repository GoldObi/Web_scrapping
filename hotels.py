#Loop through pagination to scrape hotel listings in Abuja,Nigeria from hotels.ng

from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

 
    
#Creating an empty lists of variables to store values later
hotel_name = []
hotel_price = []
hotel_location = []
hotel_city = []
hotel_address = []
adds = []
new_address = []
new_city = []
exs = []
news = []



# Defining the webscrapper function
def webscrapper(webpage, page_number):
    next_page = webpage + str(page_number)
    response= requests.get(str(next_page))
    soup = BeautifulSoup(response.content,"html.parser")
    soup_hotel= soup.findAll("h2",{"class":"listing-hotels-name"})
    soup_price= soup.findAll("p",{"class":"listing-hotels-prices-discount"})
    soup_location= soup.findAll("p",{"class":"listing-hotels-address color-dark hidden-xs hidden-sm"})
    soup_city = soup.findAll("p",{"class":"listing-hotels-address color-dark hidden-md hidden-lg"})
                          
# Loop through the listings and append values to appropriate list                        
    for x in range(len(soup_hotel)):
        hotel_name.append(soup_hotel[x].text)
        hotel_price.append(int(soup_price[x].text.strip('₦,\navg/night\n').replace(',','')))
        hotel_location.append(soup_location[x].text)
        hotel_city.append(soup_city[x].text)
        hotel_address.append(soup_location[x].text)
    
         
#Generating the next page url
    if page_number < 35:
        page_number = page_number + 1
        webscrapper(webpage, page_number)

webscrapper('https://hotels.ng/hotels-in-abuja/luxury/',0)  

# Seperate city from address and populate list new_city and new_address
countns = 0
countnt = 1    

for i in hotel_address:
    x = i.split('-',1)
    for n in x:
        us = n.strip()
        adds.append(us)
for address in adds:
    if countns < len(adds) > countnt:
        new_city.append(adds[countns])
        new_address.append(adds[countnt])
        countns += 2
        countnt += 2
        
for n in new_city:
    x = n.split(',')
    exs.append(x)
for x in exs:
    news.append(x[1])


# Creating the data frame and populating its data into the csv file
df = pd.DataFrame()
df['Hotel'] = hotel_name
df['Price'] = hotel_price
df['City'] = news
df['Address'] = new_address
df.index += 1
  
# Easily convert dataframe to csv file with pandas#df.to_csv('hotel.csv',index=None)
df.to_excel('hotel_excel.xlsx')
    