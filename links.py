import requests,time
import fake_useragent
#from fake_useragent import UserAgent
#print(fake_useragent.VERSION)

comment_urls = []
def get_title_id():

    #craw for IDs on search page
    for page in range(1,3):
        headers = {
            "User-Agent" : UserAgent().chrome
        }
        time.sleep(2)

        # links obtrained through packet capture
        api_url = 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_7978_-_ctg1_7978page=' + str(page)
        print (api_url)
        rep = requests.get(url=api_url, headers=headers)
        for json in rep.json()['data']['statuses']:
            comment_url = 'https://m.weibo.cn/detail/' + json['id']
            print (comment_url)
            comment_urls.append(comment_url)
get_title_id()

#extracting topic links
