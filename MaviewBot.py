import requests
import json

class MaviewBot:
	def __init__(self):
		self.last_updated = 0
		self.request_headers = {
			'Accept' : 'application/json',
			'Accept-Encoding' : 'gzip, deflate, sdch',
			'Accept-Language' : 'ko',
			'Connection' : 'keep-alive',
			'DNT' : '1',
			'Host' : 'maview.nexon.com',
			'Referer' : 'http://maview.nexon.com/',
			'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
			'X-Requested-With' : 'XMLHttpRequest'
			'Cookie' 'PCID=14944728485621834338678; A2SK=act02:15960043732999717153; A2SR=http%253A%252F%252Fmaview.nexon.com%252F%3A1494472911435%3A0; _ga=GA1.2.285890743.1494472850; _gid=GA1.2.73831708.1494472912; IsMobile=; TweetsSearchTime=; _gat=1; NXGID=9C0187ACD1D497880B395933E97A01CB; NXLW=SID=D47E9EEE9CA83EF02DA4377C5C5AA334&PTC=http:&DOM=maview.nexon.com&ID=&CP=; NXPID=9FE7C248108465868BA58C1045406103; HENC='
		}
		self.url = None

	def fetch_json(self):
		try:
			res = requests.get(self.url, headers = self.request_headers)
			res_json = json.loads(res.content.decode('utf-8'))
			res_json = list(filter(lambda item: int(item['time']) > self.last_updated, res_json))
		except:
			print ("Failed to fetch new items")
			return []

		if len(res_json) > 0:
			self.last_updated = int(res_json[-1]['time'])
		return res_json
