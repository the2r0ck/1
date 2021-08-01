import requests
from bs4 import BeautifulSoup

url = "https://coinmarketcap.com/"

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


top10_coins = [[] for i in range(11)]

coins = soup.find_all('tr')

for i in range(11):
	if i == 0:
		pass
	else:
		
		top = coins[i].find('p', class_="sc-1eb5slv-0 etpvrL")
		top10_coins[i].append(top.text)

		
		name = coins[i].find('p', class_="sc-1eb5slv-0 iJjGCS")
		top10_coins[i].append(name.text)

		
		short_name = coins[i].find('p', class_="sc-1eb5slv-0 gGIpIK coin-item-symbol")
		top10_coins[i].append(short_name.text)

		
		price = coins[i].find_all('a', class_="cmc-link")
		top10_coins[i].append(price[1].text)

		
		h24_day7 = coins[i].find_all('span', class_=["sc-15yy2pl-0 hzgCfk", "sc-15yy2pl-0 kAXKAX"])

		if str(h24_day7[0].next_element) == "<span class=\"icon-Caret-down\"></span>":
			top10_coins[i].append("-" + h24_day7[0].text)
		else:
			top10_coins[i].append("+" + h24_day7[0].text)
		
		if str(h24_day7[1].next_element) == "<span class=\"icon-Caret-down\"></span>":
			top10_coins[i].append("-" + h24_day7[1].text)
		else:
			top10_coins[i].append("+" + h24_day7[1].text)

		

print(top10_coins)