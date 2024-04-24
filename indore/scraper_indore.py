from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://web.archive.org/web/20191218101945/https://housing.com/price-trends/property-rates-for-buy-in-indore_madhya_pradesh-P3fo3o3llgtfbceum'



import requests
from bs4 import BeautifulSoup

# importing the csv module
import csv


response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

# loc = soup.find_all('span',class_='css-1y6emt2')
# avg_price = soup.find_all('span',class_='css-q3ye0i')
loc = []
avg_price=[]
for i in soup.find_all('span',class_='css-1y6emt2'):
    if i.text != 'Locality':

        loc.append(i.text)

for i in soup.find_all('span',class_='css-q3ye0i'):
    if i.text == 'avg_price' : 
        print()
    elif i.text == 'Avg. Price / Sqft':
        print()
    else:
        avg_price.append(i.text)
    
filename = "university_records.csv"
 
data = {'location':loc,'avg_price':avg_price}

# print(data)

df1 = pd.DataFrame(data)
print(df1.head())