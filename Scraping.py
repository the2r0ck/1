import pymysql
from bs4 import BeautifulSoup
import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = 'https://coinmarketcap.com/?page='
coins_data = []


def db_connect(user, host, password, db_name):
	try:
		connection = pymysql.connect(
				host = config.host,
				user = config.user,
				database = config.db_name,
				password = config.password
			)
		print("Successfuly connected...")

	except Exception as e:
		print("Connection refused...")
		print(e)

	cursor = connection.cursor()
	return cursor


def get_driver(user_agent, driver_location):	
	options = webdriver.ChromeOptions()
	options.add_argument("user-agent=" + user_agent)
	options.add_argument('--disable-blink-features=AutomationControlled')
	options.headless = True


	driver = webdriver.Chrome(options=options, executable_path=driver_location)
	return driver


driver = get_driver(user_agent=config.user_agent, driver_location=config.driver_location)
try:
	for i in range(1, 62):
		driver.get(url + str(i))
		for i in range(20):
			driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_DOWN)
			time.sleep(0.5)

		src = driver.page_source	
		soup = BeautifulSoup(src, 'lxml')

		table = soup.find('tbody')
		table_rows = table.find_all('tr')

		for item in table_rows:
			table_column = item.find_all('td')[2]
			coin_data = []
			
			top = table_column.find(class_='etWhyV').text
			coin_data.append(top)

			long_name = table_column.find(class_='iJjGCS').text
			coin_data.append(long_name)

			short_name = table_column.find(class_='gGIpIK').text
			coin_data.append(short_name)

			link = 'https://coinmarketcap.com' + table_column.find('a').get('href')
			coin_data.append(link)

			coins_data.append(coin_data)


except Exception as e:
	print(e)
finally:
	driver.close()
	driver.quit()


for item in coins_data:
	with open('coin_data.txt', 'a') as file:
		file.write(str(item) + '\n')