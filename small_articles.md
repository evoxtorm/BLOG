# Extra Articles related to Scraping Techniques

- [Requests Session](#requests-session)
- [Requests Timeouts](#requests-timeouts)


## Requests Session

Sessions are used to persist certain parameters across requests like the use of **cookies** across all the requests. If you are making several requests to the same host and the **TCP connection** will be reused and, it will help to increase your performance throughout all the requests. 

```
import requests
# intialized session object
session = requests.Session()
session.get('https://httpbin.org/cookies/set/sessioncookie/this-is-session-cookie')
r = session.get('https://httpbin.org/cookies')
print(r.text)
{
  "cookies": {
    "sessioncookie": "this-is-session-cookie"
  }
}

```

Here in the above code snippet, we set the session cookie and then when we make a new request to the cookies URL. We get the cookie that we have set in the first URL. Like this example, we can get the same certain parameters in the next requests.

If you want to know what more things you can do with sessions, you can read it [here](https://requests.kennethreitz.org/en/master/api/#sessionapi).


## Requests Timeouts

We can tell `request` to stop waiting for the response after a given time (in seconds). So if don't receive any bytes of response before the timeout it will raise an exception i.e `requests.exceptions.Timeout`. One important thing is that timeout also doesn't limit the response it will give the exception. So, the major advantage of using timeout is that you can save time whenever a website is not working or any other problem request is facing so it will stop the request after sometimes but if you don't use timeout request will not be terminated until the website gives the error response.

Let's quickly check how we can use this.


```
import requests
requests.get('https://google.com/', timeout=0.001)
requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='google.com', port=443): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<urllib3.connection.VerifiedHTTPSConnection object at 0x7f11824fd470>, 'Connection to google.com timed out. (connect timeout=0.001)'))
```

So, if we run this code you will get a large exception here I've shown the last part in which we get the exceptions name and timed out time. Like this, we can set a max time of the request so that it can fetch some bytes in that time.