# Scraping Using Requests and BeautifulSoup (Advance)

- [Summary](#summary)
- [Http Post Request](#http-post-request)
- [Use of Headers](#use-of-headers)
- [Exception Handling](#exception-handling)
- [Final Enhancement](#final-enhancement)
- [End Notes](#end-notes)

## Summary

This blog will contain Advance techniques related to the `Requests` library. Like what is the use of `headers`, how to make a post request, use of `session`. All these things will be covered in detail.


## Http Post Request

```
requests.post(url, data=None, json=None, **kwargs)
```
That is how we can make a `post` request. The first parameter is URL without this we cannot proceed further.  

The second parameter is `data` which is also optional but when we have to send a specific parameter to the server to get a filtered or tailored response. We can send `Dictionary, list of tuples, bytes, or file-like object`.

The third parameter is `JSON` so if we have to send a `JSON` object as a body of the request so we will send this. This can also be done with `data` which is the second parameter so in `data` we have to use something like this `data=json.dumps(payload)`. Here, JSON library is used, and in some cases, with `data` we also have to send headers like `'Content-type': 'application/JSON'` in `headers`. But with the help of `JSON`, we can directly send a `dict with values` in `JSON`.

The fourth parameter is `kwargs` so it contains lots of other values like `headers, timeout, cookies, etc`.

Here, we will learn about how we can make a post request. Post requests are used when we submit a form or sending multiple values to the backend to get the specific response or it can also be used at the time of authentication where you send your `username` and `password` and sometimes other values like `csrf-token`. If you don't know about **CSRF-TOKEN** you can read it [here](https://stackoverflow.com/questions/5207160/what-is-a-csrf-token-what-is-its-importance-and-how-does-it-work). Here we will use a series of the request so we will use `session`. You can read the basics about the session [here](https://github.com/evoxtorm/Scraping-Blog-Private/blob/main/small_articles.md#requests-session).

In this blog we will make request to `CSES` website. It will be a post request. Here, we are not extractig data as a end result but we will extract some values which will be necessary to make a login post request and therefore we will be using `get request` first.

We are using a series of requests because first, we will get the `csrfToken` then we will proceed further.

![alt text](https://github.com/evoxtorm/Scraping-Blog-Private/blob/main/Images/login_payload.jpg "Payload")

So, for a login request, we need `username` and `password` to login. But if we check the request and its payload then we will get to know it also sending a `csrfToken`.


Here in the above screenshot, we are seeing three parameters. So, let's start with `get request` and get the `csrfToken`.

```
import requests
from bs4 import BeautifulSoup

# Session object is intialized
session = requests.Session()

url = 'https://cses.fi/login'

first_response = session.get(url)
soup = BeautifulSoup(first_response.text, 'lxml')
csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
```

Here, in the above code snippet, we made a get `request` to the login URL so that we can fetch `csrf_token`. We don't have `csrf_token` we will not able to sign in. So, we have used `BeautifulSoup` for extracting the csrf_token. 

If you inspect the page using `developer tools` and search for `csrf_token` you will see something like this `<input type="hidden" name="csrf_token" value="some-value">`.
So, by using `BeautifulSoup` we are using the `find` method which will find the `input` HTML tag with `name:csrf_token`. From here, we can get the `csrf_token` now we need to make a post request.

Next, we will declare a `dict` name as a payload which will hold the values.

```
payload = {
    "csrf_token": csrf_token,
    "nick": "username",
    "pass": "password"
}

```

Here payload will consist of three values that are needed to log in. We get the `csrf_token` from the previous request and we know our `username` which is represented by key `nick`, the next parameter is `pass` which represents the `password`. So, for now, you can hardcode these values for now. 

```
final_response = session.post(url, data=payload)
print(final_response.text)
```

Here, we have made the final request. So if we check what we get in response.

```
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet " type="text/css" href="/cses.css?2" id="styles">
  <link rel="stylesheet alternate" type="text/css" href="/cses-dark.css?2" id="styles-dark">
  <meta name="theme-color" content="white" id="theme-color">
  <script type="application/json" id="darkmode-enabled">false</script>
  <script src="/ui.js"></script>
  <link rel="stylesheet" type="text/css" href="/lib/fontawesome/css/all.min.css">
</head>
<body class=" ">
  <div class="header">
    <div>
      <a href="/" class="logo"><img src="/logo.png?1" alt="CSES"></a>
      <a class="menu-toggle" onclick="document.body.classList.toggle('menu-open');">
        <i class="fas fa-bars"></i>
      </a>
      <div class="controls">
                <a class="account" href="/user/number">User Name</a>
        <span>&mdash;</span>
                        <a href="/darkmode" title="Toggle dark mode" onclick="return toggle_theme()"><i class="fas fa-adjust"></i><span>Dark mode</span></a>
                <a href="/logout" title="Log out"><i class="fas fa-sign-out-alt"></i><span>Log out</span></a>
              </div>
    </div>
  </div>
  <div class="skeleton">
  <div class="navigation">
    <div class="title-block">
      <h1>Code Submission Evaluation System</h1>
<ul class="nav">
<li><a href="/" class="current">Home</a></li>
<li><a href="/courses" >Courses</a></li>
<li><a href="/contests" >Contests</a></li>
<li><a href="/stats" >Statistics</a></li>
<li><a href="/about" >About</a></li>
</ul>
    </div>
  </div>
  
  <div class="content-wrapper">
  <div class="content">

<title>CSES</title><div class="boxes">
<div><b>CSES Problem Set</b><br />
</div></div>
```

Here's the response. Here If you search `<a class="account" href="/user/number">User Name</a>` this in response text. You will see you're 
`username` and `number` which is their inside href. So, how you can make an `HTTP post request`.



## Use of Headers

Headers let the `client` or `server` to send some additional information with the `HTTP request or response.` Headers consist of multiple parameters like `Accept, Cookie, User-Agent, Referer, etc.` You can read about headers in detail [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).

So, why we are talking about `headers`. Headers play a very important role in any HTTP request. So, we do not replicate the whole request then we are not able to request properly in some cases. You can send the request without headers also but it increases the risk of blocking by the servers or you miss any important header which is required by the website.

Let see this in an example. We will request a `URL` where we will not send headers but let's see if there any default headers sent the by `requests` library.

```
import requests
response = requests.get('https://cses.fi/')
print(response.request.headers)
{'User-Agent': 'python-requests/2.21.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
```

Yes, the `requests` library sent some default headers with requests and, it will send it with every request if you don't use any headers. So, what happens if we make multiple requests to the server without using headers our chance of getting blocked by the server is increase as you will see the `User-Agent` is `'python-requests/2.21.0'`, which is telling it is coming from a python script. So, here the chance of getting blocked or blacklisting is high. So we can replicate the headers as well.

You can replicate the headers in two ways. First, you can go to the website and inspect in developer tools and get the parameters. Second, you can do with the `requests library`.

So, let's see how we can do this.

```
import requests
headers = requests.head('https://cses.fi/')
print(headers.headers)
# Here I've changed the values of the headers to some value you can check the values either in their webiste of using this code
{
	'Date': 'Some value',
	'Server': 'Some value',
	'Set-Cookie': 'Some value',
	'Expires': 'Some value',
	'Cache-Control': 'Some value',
	'Keep-Alive': 'Some value',
	'Connection': 'Some value',
	'Content-Type': 'Some value'
}
```

So, here we make made a `head` request which will return us headers from the requests. So, if we are making a single get the request for extracting the data then it is fine to use this method but if you are making some request in sequence using session then this method is not that effective because every URL have to make a `head` request in that case you can directly inspect to the website request and can copy the parameters.

If you are making some continuous requests, you should use headers it will help you make the request identical to the browser request.


## Exception Handling

An unexcepted event that occurs during the execution of the code can be called an exception. Exception handling is used whenever you are not sure about unexpected events so exception handling is used there. You can read more about exception handling [here](https://docs.python.org/3/tutorial/errors.html).

Here, why it is important because if let we assume we are doing everything right but here we are depending on another source so there can be an error from the server or while requesting to the server.

So, here we will handling `request exceptions`. So, that if any unexcepted thing occurs at least we get to know or we stop making the further request.

So, let's see a basic exception handled code.

```
try:
	print(any_variable)
except Exception as e:
	print(e)
name 'any_variable' is not defined
print("This is working fine")
This is working fine
```

As you can see, we have not defined the variable `any_variable`. So, it goes to the exception part and prints the exception then it executes the next line of code. [Here's](https://stackoverflow.com/questions/30507358/python-time-a-try-except) the explanation of why we can't use exception handling everywhere. In simple words, it's a heavy process and it will take extra time if there will be any exception.
If making a huge number of requests if there will be more exceptions so it will make more time. So, making a code efficient and using exception handling where it is needed necessary.

```
import requests
from bs4 import BeautifulSoup

def get_response(url, session, method_name):
	try:
		response = ''
		if method_name == 'get':
			response = session.get(url)
		else:
			response = session.post(url, data=payload)
		response.raise_for_status()
		return response
	except requests.RequestException as e:
		print("Exception occured: %s" % e)
		return ''


def main():
	url = 'https://cses.fi/login'
	session = requests.Session()
	first_response = get_response(url, session, "get")
	soup = BeautifulSoup(first_response.text, 'lxml')
	csrf_token = soup.find('input', {'name': 'csrf_token'})
	payload = {
	    "csrf_token": csrf_token['value'],
	    "nick": "username",
	    "pass": "password"
	}
	final_response = get_response(url, session, "post")
	print(final_response.text)

if __name__ == '__main__':
	main()
```

Here, we had to make functions for their specific tasks. The central function is the `main` function which will be called at the starting of the script. The `main` function is calling another function `get_response` where we are making the `get and post` request based on `method_name`. 

Let's first discuss about `get_response` function. In this function, we have three parameters `URL, session, method_name`. Url is the website URL from which we want to fetch something. A session is for maintaining `cookies` and other things throughout the series of requests. The method name (method_name variable) is for what type of request we want forex `get or post` (in our case we are only making two types of requests). 

In the `get_response` function first, we are wrapping the whole request code inside the `try-except` block from where we are requesting to the website and extracting the content. So, we are making a `get or post` request. Here we have noticed something new `raise_for_status`. This method is also there with the response object we get from the server. It tells us whether any HTTP Error occurred during the process of requesting to the server. If any error happens it will raise the request exception and it will automatically go to the `exception` block where we simply print the exception which is occurred during this process.


## Final Enhancement

Till now we have learned about `post request, headers and exception handling`. Now we will learn how we can use all these things together and also add some other things which will make scraping efficient and less time taking.

Let's talk about what we will be doing and our end goal or result. 

So, we will log in to [CSES](https://cses.fi/), and then we will extract the stats of the user. 

![alt text](https://github.com/evoxtorm/Scraping-Blog-Private/blob/main/Images/profile_details.png "Profile details")

We have a user profile that looks like this (above screenshot). Here we have various information about the user like name, country, submission count, etc.

So the result will look something like this.

```
{
	"username": {
		"name": "Name",
		"country": "User Country",
		"submission_count": "Submission count",
		"first_submission": "First submission",
		"last_submission": "Last submission",
	}
}

```


Here, We will have a `dict` which have various `username` as key and details as value.

Now, we will stitch all the above steps and make it into a single file.

For the first step, we will make a basic structure of the file and get the usernames and passwords.

```
import requests
from bs4 import BeautifulSoup

def get_response(url, session, method_name, headers, payload={}):
	return ''

def main(usernames, passwords):
	pass


if __name__ == '__main__':
	print("write usernames with space separated")
	usernames = input().split()
	print("print password space separated according to username index")
	passwords = input().split()
	if len(username) != len(password):
		exit(print("Either username is missing or password is missing"))
	main(usernames, passwords)
```

In the above code, we are making a basic structure of the file where we have two functions one is the `main` function and the other is `get_response`. The first function name says it all it's the main function where we will do all the scraping and parsing part and the other function is a helper function that will give us a response for that particular request.

Let talk about the parameters of these function. For the first function i.e. `main`, we have two parameters` usernames passwords`. So, this the array of usernames and passwords for multiple people. Another function is `get_response` which has four parameters `URL, session,method_name, headers, and payload`. So `url` is any URL we are requesting, `session` for maintaining the session between two consecutive requests, `method_name` is for what type of request we are making like the post, get, etc., next is headers which are `dict` and contain all the headers so that we replicate the request properly and last is the payload which helps to send the data which is required for a request.

So, next, we will write code inside these functions so that they can get the data and get the work done.

Let's work on the `main` function.

```
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
```

Above we have the fully functional code for getting the result which we want to extract.

So, we have `main` in which all major things are happening. Let's walk through the code. First, we are looping to the length of `usernames` then we are making a session. So, we will make a unique session for every username.

**Why we are making a new session here?**

So, the answer for this is that if you log in a new user every time then the browser will create a new session for every user every time so we are trying to do this. Then we are requesting to get a response so that we can extract `csrf_token`.

In `get_response` we have new parameter called `timeout`. You can read it [Here](https://github.com/evoxtorm/Scraping-Blog-Private/blob/main/small_articles.md#requests-timeouts).

After extracting `csrf_token` we made a login request. After login to the website, we extracted the user detail URL from its response. Then we made a last request so that we can extract all the things which we want to extract from the website.

At last, we have attached the details in result `dict` which key is username and value is `ans_dict`. After this `time.sleep` is used so that we don't have that frequent requests in real scenarios it will take some time to do all these things. You can use this after every request for real-world problems but for now, it's ok.

You can run this file to test this code. [Here's](https://github.com/evoxtorm/Scraping-Blog-Private/blob/main/scripts/post_request.py) the file.



## End Notes

Here we have learned more advanced concepts about the `requests` library and see how useful it is for scraping and extracting the data.