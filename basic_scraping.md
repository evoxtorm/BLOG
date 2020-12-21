# Scraping using Request library and BeautifulSoup

- [Summary](#summary)
- [HTTP Get Request](#http-get-request)
- [Get Values Using BeautifulSoup](#get-values-using-beautifulsoup)
- [End Notes](#end-notes)

## Summary

This blog will contain how to use `Python request library` to make HTTP requests and getting data from various websites and, we will use another python library called`BeautifulSoup`. It will help us to extract data from web pages. BeautifulSoup provides the various parsers for searching and iterating through the HTML Dom tree.

## HTTP Get Request

Here, we will start with basic **HTTP** get request and extracting some of the basic values from the web page. Let start with a basic example of an HTTP get request.

```
requests.get(url, params=None, **kwargs)
```
Here above, it is just the representation of how we can make a `get request`. Here the First parameter is the URL, without this, you can't request so it should be there. The second param is query string parameters for the URL. The second parameter is optional. Third, we have `kwargs` so in this we can include `headers, timeout, cookies, etc`.

When a call is made to `request.get` basically two major things that we are doing. First, we are constructing the `requests` object which will be sent to the server to request some resource. Second, a `Response` object will be generated once the request will be completed or we get a response from the server. The Response object contains all the information which we will get from the server and we also have the `request` object which we have created and sent to the server. 


First of all, we have to install the requests library and import. So, we can use this. Then we have to make an `HTTP get request`. In getting a request we have passed a website URL so that we can get the response from that website or any `API` which will return some response. **Get** request also has various parameters like `params, headers, timeout` etc. We will discuss this eventually.

In this blog, we will scrap basic details from [CSES](https://cses.fi/problemset/). If you click this URL, you will find programming questions and their statics related to it. So, we will try to extract the Question name and their statics and URL for the questions. You can check the website and get the basic idea.


```
import requests
response = requests.get('https://cses.fi/problemset/')
```

Here we know that we will get the response object from the server let's check what we have in `response` object.

```
response.
response.apparent_encoding      response.elapsed                response.is_redirect            response.next                   response.request
response.close(                 response.encoding               response.iter_content(          response.ok                     response.status_code
response.connection             response.headers                response.iter_lines(            response.raise_for_status(      response.text
response.content                response.history                response.json(                  response.raw                    response.url
response.cookies                response.is_permanent_redirect  response.links                  response.reason                 

```

Here I've used the python terminal and where I've used `tab` after writing `response.`. Now we get lots of values here but here we're looking only for `response.text`. But if you want to know more about this you can read it [here](https://requests.kennethreitz.org/en/master/api/#requests.Response).

So, we have now made an **HTTP request**. Let see, what we get as a response. If we print the `response` variable which is holding the result we get from the request. 

```
print(response)
<Response [200]>
```

So, here response shows like this. So what this mean?
Here it shows the **HTTP response status code**. From 200-299, these all are successful responses that mean we can make requests properly without any error. We also have various other HTTP response status codes. You can read about all the code [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

One more **status code** is `404`. Whenever you encountered this status code there is any typo or the server is not able to find the requested resource.

So, what does the `404` error means?

This status code is often returned by the server whenever the page is moved or deleted to another URL. Like you have a Domain name for a particular URL and then it will try to find the IP address associated with it. But if the `404 status code` is returned by the server it is not able to find it. So, you've needed to check for `404 code`.

Here's an example for it.

```
import requests
url = "https://www.transfermarkt.com/jumplist/startseite/wettbewerb/GB1"
ans = requests.get(url)
ans
<Response [404]>
``` 

Here you can see we are not getting any exception but, we got a response `404`. That's why we need to check for it.

Now, how we will extract the data from the response. So, it can be achieved by this.

We can get the content of the response using `response.content` or `response.text`. I will explain later what is the difference between `response.text` and `response.content`. For now, I will stick to `response.text`. If we print this.

 ```
print(response.text)
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
                <a class="account" href="/login">Login</a>
        <span>&mdash;</span>
                        <a href="/darkmode" title="Toggle dark mode" onclick="return toggle_theme()"><i class="fas fa-adjust"></i><span>Dark mode</span></a>
              </div>
 ............................................................................................................................. 
   </html>
```

So, here we get the response in the form of `HTML text`. It can be varied to `XML` or `JSON`. Depend on the website and their use-cases.
Now we will learn how we can get the values from the HTML text using `BeautifulSoup`.


## Get Values Using BeautifulSoup

![alt text](https://github.com/evoxtorm/BLOG/blob/main/Images/example_one.jpg "Example One")

Here is the screenshot which is taken from [CSES](https://cses.fi/problemset/). I've highlighted the screenshot where we will try to get the question name which is in the left and, the stats about it in the right.

First of all, let's know a little about `BeautifulSoup`. From their official documentation, we have "Beautiful Soup is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. It commonly saves programmers hours or days of work."

In simple words, it helps to find the data in the HTML dom tree and provides some method which will help us to find data using `id, class, etc.`. With the help of BeautifulSoup, we can find nested data easily or find a data in particular HTML tag which has some id or having any class or iterate through various tags to collect the data.

BeautifulSoup uses various parsers to parse the `HTML`. We have three popular parsers.
	* `html.parser`
	* `lxml`
	* `html5lib`

I will try to explain these parsers in another blog. But for now, we will stick to `lxml`.

![alt text](https://github.com/evoxtorm/BLOG/blob/main/Images/example2.jpg "Example Two")

First, we need to check where we can find the tag or location of the text we want to extract. Here, in the above screenshot. I've marked highlighted the HTML tag where we want to go and get the data. So, now we know the exact location where we get the data and, from there, we will extract the data.

```
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')
print(soup)
<html>
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<link href="/cses.css?2" id="styles" rel="stylesheet " type="text/css"/>
<link href="/cses-dark.css?2" id="styles-dark" rel="stylesheet alternate" type="text/css"/>
<meta content="white" id="theme-color" name="theme-color"/>
<script id="darkmode-enabled" type="application/json">false</script>
<script src="/ui.js"></script>
<link href="/lib/fontawesome/css/all.min.css" rel="stylesheet" type="text/css"/>
</head>
<body class=" ">
<div class="header">
<div>
<a class="logo" href="/"><img alt="CSES" src="/logo.png?1"/></a>
<a class="menu-toggle" onclick="document.body.classList.toggle('menu-open');">
<i class="fas fa-bars"></i>
</a>
<div class="controls">
<a class="account" href="/login">Login</a>
<span>—</span>
<a href="/darkmode" onclick="return toggle_theme()" title="Toggle dark mode"><i class="fas fa-adjust"></i><span>Dark mode</span></a>
</div>
</div>
</div>
<div class="skeleton">
<div class="navigation">
<div class="title-block">
<h1>CSES Problem Set</h1>
<ul class="nav">
<li><a href="/problemset/list">Tasks</a></li>
<li><a href="/problemset/stats">Statistics</a></li>
</ul>
</div>
<div class="sidebar"></div>
</div>
<div class="content-wrapper">
<div class="content">
<title>CSES - CSES Problem Set - Tasks</title><h2>General</h2><ul class="task-list"><li class="text"><a href="/problemset/text/1810">Introduction</a></li><li class="link"><a href="https://cses.fi/register/?open">Create new account</a></li><li class="link"><a href="https://cses.fi/problemset/stats/">Statistics</a></li></ul><h2>Introductory Problems</h2>
..............................................
</html>
```

Here in the above code snippet, we have seen how we will use BeautifulSoup to make the response parsable and we have used `lxml parser` here.

Now we will extract data that is useful to us. So, for example, we want to see data in a structure like this.

```
{
	"Problem Name": ["Statics", "Problem Url"]
}
```

So, to achieve the basic data structure we defined above, we will use BeautifulSoup inbuilt methods which, will make our work easy with more efficiently.

```
# So using BeautifulSoup we are extracting all the li tag which has class equal to task
data_tag = soup.findAll('li', {'class': 'task'})
print(data_tag[0])
<li class="task"><a href="/problemset/task/1068">Weird Algorithm</a><span class="detail">17382 / 18110</span> <span class="task-score icon "></span></li>

```

Here I've used a method called `findAll` which, will give all the li tags which have a class task and, from there, we can make our data.

```
final_result = {}
# For now I've only used starting 5 tags
for tag in data_tag[:5]:
	url_link =  tag.find('a')
	span = tag.find('span', {'class': 'detail'})
	key_name = url_link.text
	url = url_link['href']
	details = span.text
	data[key_name] = [url, details]
print(data)
{'Increasing Array': ['/problemset/task/1094', '11906 / 12457'],
 'Missing Number': ['/problemset/task/1083', '14543 / 15518'],
 'Permutations': ['/problemset/task/1070', '10576 / 10962'],
 'Repetitions': ['/problemset/task/1069', '12881 / 13632'],
 'Weird Algorithm': ['/problemset/task/1068', '17382 / 18110']
}
```

In the above snippet, we are able to get the data in the desired form. Here in the above code, we have extracted the nested data which is present inside the li tag in the form of `span` and `a` tag. We searched and get the data and save it to the dictionary. Here one more thing to learn where I've used `.text` we can also use `get_text()` here but the text is an extension to it and you can pass other parameters to the `get_text()` method which are `(separator, strip, types)`. Here we don't need this so we are not using it.


## End Notes

In this blog, we have learned how to make a get request and get a response. Extract all the required data with the help of BeautifulSoup. In the next blog. I will try to explain more advanced methods using request and will know what other things we can achieve. The next part of this blog is [here](https://github.com/evoxtorm/BLOG/blob/main/basic_scraping_two.md).