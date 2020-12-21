"""Post Request Example."""

import copy
import time
import requests
from bs4 import BeautifulSoup
from pprint import pprint

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "en-US,en;q=0.5",
	"Connection": "keep-alive",
	"Host": "cses.fi",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0"
}


def get_response(url, session, method_name, headers, payload={}):
	"""
		This function we will make a request and return response if there is no error.
		It handles two type of request which is get and post.
		Headers is required here to replicate the request.
		Timeout is set to 60.
	"""
	try:
		response = ''
		if method_name == 'get':
			response = session.get(url, headers=headers, timeout=60)
		else:
			response = session.post(url, data=payload, headers=headers, timeout=60)
		response.raise_for_status()
		return response
	except requests.RequestException as e:
		print("Exception occured: %s" % e)
		return ''


def main(usernames, passwords):
	"""
		This function take array of usernames and passwords.
		It will process for every index of username and password.
		It will give a dict of usernames which have the result.
		The final response will look something like this
		{
			"username": {
				"name": "Name",
				"country": "User Country",
				"submission_count": "Submission count",
				"first_submission": "First submission",
				"last_submission": "Last submission",
			}
		}
	"""
	result = {}
	url = 'https://cses.fi/login'
	base_url = 'https://cses.fi'
	for i in range(len(usernames)):
		session = requests.Session()
		first_response = get_response(url, session, "get", headers)
		if not first_response or not first_response.text.strip():
			print("First request failed for username-%s" % usernames[i])
			continue
		soup = BeautifulSoup(first_response.text, 'lxml')
		csrf_token = soup.find('input', {'name': 'csrf_token'})
		if not csrf_token or not csrf_token['value']:
			print("Not able to find csrf-token")
			continue
		payload = {
			"csrf_token": csrf_token['value'],
			"nick": usernames[i],
			"pass": passwords[i]
		}
		new_headers = headers.copy()
		new_headers['Content-Type'] = 'application/x-www-form-urlencoded'
		new_headers['Origin'] = 'https://cses.fi'
		new_headers['Referer'] = 'https://cses.fi/login'
		second_response = get_response(url, session, "post", new_headers, payload)
		if not second_response or not second_response.text.strip():
			print("Not able to login please check username and password")
		new_soup = BeautifulSoup(second_response.text, 'lxml')
		find_user_id = new_soup.find('a', {'class': 'account'})
		if not find_user_id or not find_user_id['href']:
			print("Not able to find user")
			continue
		final_url = base_url + find_user_id['href']
		final_resp = get_response(final_url, session, "get", new_headers)
		if not final_resp or not final_resp.text:
			print("Not able to get user details")
			continue
		final_soup = BeautifulSoup(final_resp.text, 'lxml')
		tables = final_soup.find_all('table')
		if len(tables) < 1:
			print("Not able to find user details table")
			continue
		detail_table = tables[0]
		all_td = detail_table.find_all('tr')
		if len(all_td) < 5:
			continue
		ans_dict = {}
		ans_dict['Name'] = all_td[0].find_all('td')[-1].text
		ans_dict['Country'] = all_td[1].find_all('td')[-1].text
		ans_dict['Submission_Count'] = all_td[2].find_all('td')[-1].text
		ans_dict['First_Submission'] = all_td[3].find_all('td')[-1].text
		ans_dict['Last_Submission'] = all_td[4].find_all('td')[-1].text
		result[usernames[i]] = ans_dict
		# To stop frequent request so that it will seems like real requst
		time.sleep(1)
		print("New Request")
	return result



if __name__ == '__main__':
	print("write usernames with space separated")
	username = list(input().split())
	print("print password space separated according to username index")
	password = list(input().split())
	if len(username) != len(password):
		exit(print("Either username is missing or password is missing"))
	result = main(username, password)
	pprint(result)