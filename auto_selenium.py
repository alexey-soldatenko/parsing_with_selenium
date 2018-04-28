from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import choice
from random import uniform
from bs4 import BeautifulSoup


PROXY_HOST = "97.74.230.16"
PROXY_PORT = 30740

def handle_main_page(main_page, html, first=None):
	#ищем ссылки на объявления
	a_ls = main_page.findAll('a', attrs={'class':'link link_theme_auto \
			listing-item__link link__control i-bem'})	
	links = [a.get('href') for a in a_ls]
		
	return links


profile = webdriver.FirefoxProfile()

#подключаем прокси
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", PROXY_HOST)
profile.set_preference("network.proxy.socks_port", PROXY_PORT)
profile.set_preference("network.proxy.socks_version", 5)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile=profile)


driver.get("https://auto.ru/cars/used/")

time.sleep(uniform(5, 10))


#устанавливаем регион для парсинга
region = "moskovskaya_oblast"
	
#первая страница	
main_link = "https://auto.ru/{0}/cars/used/?beaten=1&\
	customs_state=1&geo_id=1&price_to=200000&dealer_org_type=4&\
	owners_count=1&image=true&sort_offers=fresh_relevance_1-DESC&\
	top_days=off&currency=RUR&output_type=list".format(region)

driver.get(main_link)


html = driver.page_source
main_page = BeautifulSoup(html, 'html.parser')



#обрабатываем первую страницу, получаем ссылки на объявления
links = handle_main_page(main_page, html)


while True:
	
	for link in links:
		#обрабатываем страницу с объявлением в новом окне
		main_window = driver.current_window_handle
		driver.execute_script("window.open('');")
		driver.switch_to_window(driver.window_handles[1])
		driver.get(link)
		
		#ищем кнопку "просмотреть телефон"
		elem = driver.find_element_by_xpath('/html/body/div[6]/div/\
			div[3]/div/div/div[2]/div[4]/div[1]')
											
		elem.click()
		time.sleep(4.0)
		try:
			elem = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME, 
				"call-numbers__phone"))
			)
		except:
			print('no phones')
			
		print(elem.text)
		#закрываем новое окно
		driver.execute_script("window.close('');")

		#переключаемся на основное окно
		driver.switch_to_window(main_window)
		break
	
	
	#ищем кнопку "следующая страница"
	driver.execute_script("window.scrollTo(0, \
			document.body.scrollHeight/1.3);")
	try:
		elem = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 
					".pager__next"))
		)
	except:
		print('no next page')
		break
	class_name = elem.get_attribute('class')

	if class_name.find('disabled') > -1:
		print('Exit/no pages')
		break

	else:
		elem.click()
	
	time.sleep(5.0)
	
	html = driver.page_source
	main_page = BeautifulSoup(html, 'html.parser')



	#обрабатываем первую страницу, получаем ссылки на объявления
	links = handle_main_page(main_page, html)
	
	
time.sleep(2.0)
driver.close()
