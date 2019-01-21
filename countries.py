"""This is my first project"""


from urllib.request import urlopen, Request

url = 'http://example.webscraping.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
request = Request(url, headers=headers)
response = urlopen(request).read().decode('utf-8')
response = str(response)

while '<a href="/places/default/view/' in response:
    tag = response.find('png" />')
    start = tag + len('png" />')
    country = ''
    for chair in response[start:]:
        if chair != '<':
            country += chair
        else:
            print(country)
            break
    response = response[response.find(country):]
