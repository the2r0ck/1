import requests
import pymysql
from config import user, host, password, db_name
from bs4 import BeautifulSoup

try:
	connection = pymysql.connect(
			host = host,
			user = user,
			database = db_name,
			password = password
		)
	print("Successfuly connected...")

except Exception as e:
	print("Connection refused...")
	print(e)

cursor = connection.cursor()

url = "https://coinmarketcap.com"

headers = {
	"Accept": "application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8",
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
}

req = requests.get(url, headers=headers)

src = req.text
# print(src)

with open("coinmarketcap.html", 'w') as file:
	file.write(src)

# with open("coinmarketcap.html") as file:
# 	src = file.read()
# print(src)
soup = BeautifulSoup(src, "lxml")

coins = soup.find("tbody").find_all("tr")
db_data = [[] for i in range(len(coins[0:10]))]

for item in coins[0:10]:
	element = coins[coins.index(item)].find_all("td")
	
	#top
	top = element[1].text
	db_data[coins.index(item)].append(top)

	#name
	long_short_name = element[2].find_all('p')
	name = long_short_name[0].text
	db_data[coins.index(item)].append(name)

	#short_name
	short_name = long_short_name[1].text
	db_data[coins.index(item)].append(short_name)

	#price
	price = element[3].text
	db_data[coins.index(item)].append(price)

	#24_hours
	h24_ = element[4].find('span', class_=["sc-15yy2pl-0 hzgCfk", "sc-15yy2pl-0 kAXKAX"])
	if len(h24_.find_all(class_="icon-Caret-down")) == 1:
		h24 = '-' + h24_.text
	else:
		h24 = '+' + h24_.text
	db_data[coins.index(item)].append(h24)
	
	#7_days
	d7_ = element[5].find('span', class_=["sc-15yy2pl-0 hzgCfk", "sc-15yy2pl-0 kAXKAX"])
	if len(h24_.find_all(class_="icon-Caret-down")) == 1:
		d7 = '-' + d7_.text
	else:
		d7 = '+' + d7_.text
	db_data[coins.index(item)].append(d7)

for item in db_data:
	execute = f"INSERT INTO crypto (id, name,	short_name, price, change_in_24_hours, change_in_7_days) VALUES('{item[0]}', '{item[1]}', '{item[2]}', '{item[3]}', '{item[4]}', '{item[5]}')"
	cursor.execute(execute)
connection.commit()
