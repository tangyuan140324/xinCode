import json

import requests



url_nick = 'http://s.m.taobao.com/search?m=api4h5&n=40&page=2&nick=优衣库官方旗舰店'
url_sellerId = 'http://api.s.m.taobao.com/search.json?m=shopitemsearch&sellerId=263817957&n=40&page=1'
headers = {
            "user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                         "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }

html = requests.get(url_nick,headers = headers).text
print(html)
ta = json.loads(html)
data = ta.get('listItem')
#print(type(data))
print(len(data))
temple ={}
for item in data:
    # temple{
    #     'title': item
    # }
    print(item)
    print(type(item))