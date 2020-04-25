
#works in terminal, python3 run and press enter to see other productsn download beautifulsoup and ebaysdp : pip install/pip3 install ebaysdk, BeautifulSoup
from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup

ID_APP = 'AmandaLi-Globesho-PRD-5bcb87b90-5890e4ce'

class API:
	def __init__(self):
		pass
	def findItems(self,keyword):
		api = finding(appid=ID_APP, config_file=None)
		api_request = { 'keywords': keyword }
		response = api.execute('findItemsByKeywords', api_request)
		soup = BeautifulSoup(response.content,'lxml')

		totalentries = int(soup.find('totalentries').text)
		items = soup.find_all('item')
		return items

