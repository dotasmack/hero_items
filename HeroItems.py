from bs4 import BeautifulSoup
import  requests
import csv
s = requests.Session()
user_agent = {'User-agent': 'Mozilla/5.0'}
base_link = "https://www.dotabuff.com/"



final = {}
all_items=['Hero']

def all_heroes():
    global heros
    heros = {}
    url = 'https://www.dotabuff.com/heroes/played?date=week'
    response=s.get(url,headers=user_agent)
    data=response.text

    soup=BeautifulSoup(data,"lxml")
    records = soup.find("table",class_="sortable")
    records = records.find("tbody")
    records = records.findAll("tr")
    for hero in records:
        hero_name = hero.findAll("td")[1].text
        matches_played = hero.findAll("td")[2].text
        heros[hero_name] = matches_played.replace(',', '')
        final[hero_name] = {}
        
    
        
all_heroes()

url="https://www.dotabuff.com/items"
response=s.get(url,headers=user_agent)
data=response.text
soup=BeautifulSoup(data,"lxml")
itemstable = soup.find("table",class_="sortable")
itemstable = itemstable.find("tbody")
items = itemstable.findAll("tr")

i=0
for item in items:
 
    alldata = item.findAll("td")[1]
    item_name = item.findAll("td")[1].text
    link = base_link+alldata.find("a")['href']
   
    all_items.append(item_name+" %")
    
    
    response=s.get(link,headers=user_agent)
    data=response.text
    soup2=BeautifulSoup(data,"lxml")
    
    records = soup2.find("table",class_="sortable")
    records = records.find("tbody")
    records = records.findAll("tr")


    for hero in records:
        hero_name = hero.findAll("td")[1].text
        
        matches_played = (hero.findAll("td")[2].text).replace(',', '')
        
        a = heros[hero_name]

        percentage = float(matches_played)/float(a) * 100
        final[hero_name][item_name] = "{:.2f}".format(round(percentage,2))


    



for key,value in final.items():
	print(key)

	for key,value in value.items():
		print(key)
		print(value)
		
		
	
print(all_items)
with open('dota_data.csv', mode='w',newline='') as csv_file:
    
    writer = csv.writer(csv_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(all_items)
    
   
    for key,value in final.items():
    	present_row = []
    	present_row.append(key)
    	for key,value in value.items():
    		present_row.append(value)
    	writer.writerow(present_row)
  