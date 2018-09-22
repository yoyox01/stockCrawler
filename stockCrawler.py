
# coding: utf-8

# In[1]:


import requests
import json
import csv
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}


# In[2]:


def Crawler(stockID):
    url = 'https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID='+stockID
    result = requests.get(url, headers=headers)
    result.encoding = 'utf8'
    #print("encoding: %s" % result.encoding)
    #print("content: \n%s" % result.text)
    soup = BeautifulSoup(result.text,'html.parser')
    table_tags = soup.select('nobr a.link_blue')
    info_tags = soup.select('table.solid_1_padding_4_0_tbl tr td')
    
    return table_tags, info_tags

def StoreInfo(years_of_data, info_tags):
    del info_tags[0:41]
    Stock_info = []
    for i in range(0,int(years_of_data)):
        tmp = []
        tmp.append(stock_name)
        tmp.append(info_tags[0+26*i].text)
        tmp.append(info_tags[3+26*i].text)
        tmp.append(info_tags[6+26*i].text)
        tmp.append(info_tags[7+26*i].text)
        if i==0:
            tmp.append(None)
            tmp.append(None)
        else:
            tmp.append(info_tags[22+26*(i-1)].text)
            tmp.append(info_tags[25+26*(i-1)].text)
        tmp.append(info_tags[15+26*i].text)
        tmp.append(info_tags[16+26*i].text)
        tmp.append(info_tags[17+26*i].text)
        Stock_info.append(tmp)
    
    return Stock_info

def WriteJson(filename, Stock_info):
    with open(filename, 'w') as outfile:
        json.dump(Stock_info, outfile)
    
def ReadJson(filename):
    with open(filename) as infile:  
        data = json.load(infile)
        for p in data:
            print(p)

def WriteCsv(filename, Stock_header, Stock_info):
    outfile = open(filename,'a', newline='')
    writeCSV = csv.writer(outfile)
    writeCSV.writerow(Stock_header)
    writeCSV.writerows(Stock_info)
    writeCSV.writerow([])
    outfile.close()
    print('The data above have been written into', filename,'successfully!')


# In[3]:


###### key in the stock ID and years  of data you want to crawl
stockID = input("Stock ID :")
years_of_data = input("Years of data :")

###### start crawling, and store the results in lists
table_tags, info_tags = Crawler(stockID)
stock_name = table_tags[4].text.replace(u'\xa0', u' ')
print(stock_name)


# In[4]:


###### store the filtered informations in list of lists
Stock_header = ['年度','現金股利','股票股利','每股盈餘','EPS','盈配率','最高','最低','平均','備註']
Stock_header.insert( 0, stock_name)
Stock_info = StoreInfo(years_of_data, info_tags)


# In[5]:


###### write json file
WriteJson('stock_data.json', Stock_info)

###### read json file
ReadJson('stock_data.json')

###### write csv file
save = input('Do you want to save it? (y/n)')
if (save=='y') or (save=='Y'):
    WriteCsv('stocks_info.csv', Stock_header, Stock_info)
else:
    print('The data above is not saved.')

