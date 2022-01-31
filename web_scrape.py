import bs4
import requests
import json


class Job:
	def __init__(self,position,company,link,date):
		self.position = position
		self.company = company
		self.link = link
		self.post_date = date
	def __repr__(self):
		return f"Job Title: {self.position}\nCompany: {self.company}\nPosted on: {self.post_date}\n<a href=\"{self.link}\">Click here to Apply</a>"
	def __str__(self):
		return self.__repr__()

def get_results(keywords,num_results=5):
	if num_results > 10: num_results = 10
	if num_results < 1: num_results = 1
	#keywords = "product manager"
	query = f"https://www.linkedin.com/jobs/search/?keywords={keywords.replace(' ','%20')}"
	t = requests.get(query).text
	result = bs4.BeautifulSoup(t,"lxml")
	items = result.find_all('ul')[6]

	all_items = items.find_all('li')

	l = []
	for it in all_items:
		it_ = it.find('div').find('a')
		time = it.find('time')
		time = time['datetime'] + ' (' + time.text.strip() + ')'

		if it_:
			j = Job(it_.text.strip(),
				it.find('h4').text.strip(),
				it_['href'].strip(),
				 time)
			l.append(str(j))
	return '\n\n'.join(l[:num_results])


			#print(j)
		#print()
