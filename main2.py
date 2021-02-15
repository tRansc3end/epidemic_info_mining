# -*- coding: utf-8 -*-
import requests,random,re
import time
import os
import csv
import sys
import json
import importlib
from fake_useragent import UserAgent
from lxml import etree
importlib.reload(sys)
startTime = time.time() #Record start time

#--------------------------------------------File storage-----------------------------------------------------
path = os.getcwd() + "/weibodata.csv"
csvfile = open(path, 'a', newline='', encoding = 'utf-8')
writer = csv.writer(csvfile)
#csv header
writer.writerow(('话题链接','话题内容','楼主ID', '楼主昵称', '楼主性别','发布日期',
                 '发布时间', '转发量','评论量','点赞量', '评论者ID', '评论者昵称',
                 '评论者性别', '评论日期', '评论时间','评论内容'))

#set headers
headers = {
    "Cookie": '_T_WM=75978789314; SCF=AiOOsAW2Cy8W_lL7g7go7suT-GW58aezrrCGrXeOi97NoZlM5IjeG-yk0lOVqiGUnvaB3RiRHEKJ1AAeuRUY04o.; SUB=_2A25yz7zBDeRhGeFL6lYT9ifPzDWIHXVuM8SJrDV6PUJbktAKLUvakW1NQmRUR3SMHIiDuevyOk7UdZ1SAjKA0bi1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW-zz2CfNGU-JlivKLhBwlG5JpX5K-hUgL.FoMfeKBESo.0S0.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoM0eo24ShqX1K.4; SSOLoginState=1607191698; ALF=1609783698; BAIDU_SSP_lcr=https://login.sina.com.cn/; WEIBOCN_FROM=1110105030; MLOGIN=1; XSRF-TOKEN=5cb0d4; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E5%25AE%2598%25E6%2596%25B9%25E5%259B%259E%25E5%25BA%2594%25E5%258F%25A3%25E7%25BD%25A9%25E8%25BF%259B%25E4%25BB%25B76%25E6%25AF%259B%25E5%258D%25961%25E5%2585%2583%25E8%25A2%25AB%25E7%25BD%259A%2523%25EF%25BC%259A%25E7%25B3%25BB%25E5%258A%25B3%25E4%25BF%259D%25E5%258F%25A3%25E7%25BD%25A9%25EF%25BC%258C%25E5%25B9%25B3%25E6%2597%25B6%25E5%2594%25AE%25E4%25BB%25B7%25E4%25B8%258D%25E8%25B6%2585%25E8%25BF%25875%25E6%25AF%259B%26fid%3D100103type%253D1%2526q%253D%25E5%25AE%2598%25E6%2596%25B9%25E5%259B%259E%25E5%25BA%2594%25E5%258F%25A3%25E7%25BD%25A9%25E8%25BF%259B%25E4%25BB%25B76%25E6%25AF%259B%25E5%258D%25961%25E5%2585%2583%25E8%25A2%25AB%25E7%25BD%259A%2523%25EF%25BC%259A%25E7%25B3%25BB%25E5%258A%25B3%25E4%25BF%259D%25E5%258F%25A3%25E7%25BD%25A9%25EF%25BC%258C%25E5%25B9%25B3%25E6%2597%25B6%25E5%2594%25AE%25E4%25BB%25B7%25E4%25B8%258D%25E8%25B6%2585%25E8%25BF%25875%25E6%25AF%259B%26uicode%3D10000011',
    "User-agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
    "X-Requested-With": 'XMLHttpRequest',
    "Referer": 'https://m.weibo.cn/detail/4471277660537906'
}

#--------Crawl the ID of each topic on the homepage of the epidemic------------------------------------------
comments_ID = []
def get_title_id():
    for page in range(1,20):  #Each page has about 18 topics
        headers = {
            "User-Agent" : UserAgent().chrome #chrome browser random agent
        }
        time.sleep(1)
        #The link is obtained through packet capture
        api_url = 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_7978_-_ctg1_7978&page=' + str(page)
        print(api_url)
        rep = requests.get(url=api_url, headers=headers)
         #Get the ID value and write it into the list comment_ID
        for json in rep.json()["data"]["statuses"]:
            comment_ID = json["id" ]
            comments_ID.append(comment_ID)

    return comments_ID

#-----Crawl the details page of each topic of the coronavirus epidemic------------------------------------------
def spider_title(comments_ID):
    #count=1
    #page = {}
    for comment_ID in comments_ID:
        #count+=1
        #print('共{}个'.format(len(comment_ID)))
        #try:
        article_url = 'https://m.weibo.cn/detail/'+comment_ID
        print ("article_url = ", article_url)
        html_text = requests.get(url=article_url, headers=headers).text
        #Topic content
        find_title = re.findall('.*?"text": "(.*?)",.*?', html_text)[0]
        title_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', find_title)
        print ("title_text = ", title_text)
        #user_id
        title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]
        print ("title_user_id = ", title_user_id)
        #title_user_NicName
        title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]
        print ("title_user_NicName = ", title_user_NicName)
        #Original gender
        title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]
        print ("title_user_gender = ", title_user_gender)
        #Forwarding volume
        reposts_count = re.findall('.*?"reposts_count": (.*?),.*?', html_text)[0]
        print ("reposts_count = ", reposts_count)
        #Comments
        comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[0]
        print ("comments_count = ", comments_count)
        #Likes
        attitudes_count = re.findall('.*?"attitudes_count": (.*?),.*?', html_text)[0]
        print ("attitudes_count = ", attitudes_count)
        comment_count = int(int(comments_count) / 20) #每个ajax一次加载20条数据
        position1 = (article_url, title_text, title_user_id, title_user_NicName,title_user_gender, reposts_count, comments_count, attitudes_count, " ", " ", " ", " "," ", " ")
        #data input
        writer.writerow((position1))
        return comment_count

#------------------Crawling comment information---------------------------------------------------
#comment_ID Topic ID
def get_page(comment_ID, max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }
    url = ' https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id'.format(comment_ID, comment_ID)
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)
        pass

#------------------Crawl the maximum value of comment item---------------------------------------------------
def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
        item_max_id['max_id_type'] = items['max_id_type']
        return item_max_id

#-------------------Crawl comment information---------------------------------------------------
def write_csv(jsondata):
    for json in jsondata['data']['data']:
        #User ID
        user_id = json['user']['id']
        # User's Nickname
        user_name = json['user']['screen_name']
        # User gender, m means male, f means female
        user_gender = json['user']['gender']
        #Get comments
        comments_text = json['text']
        comment_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', comments_text) #Regular match off html tags
        # Comment time
        created_times = json['created_at'].split(' ')
        created_time = created_times[3] # Comment time hour minutes and seconds
        #if len(comment_text) != 0:
        position2 = (" ", " ", " ", " "," ", " ", " ", " ", " ", " ", user_id, user_name, user_gender, created_time, comment_text)
        writer.writerow((position2)) #Write data

#-----------------------Main function---------------------------------------------------
def main():
    count_title = len(comments_ID)
    for count, comment_ID in enumerate(comments_ID):
        print ("number %s topic is being crawled, a total of %s topics are found and need to be crawled"%(count+1, count_title))
        #maxPage Get the maximum number of comments returned
        maxPage = spider_title(comments_ID)
        print ('maxPage = ', maxPage)
        m_id = 0
        id_type = 0
        if maxPage != 0: # Less than 20 comments do not need to loop
            try:
                #Custom Function-Fetch web comment information
                for page in range(0, maxPage):
                    #Custom Function-Fetch web comment information
                    jsondata = get_page(comment_ID, m_id, id_type)

                    #Custom function-write CSV file
                    write_csv(jsondata)

                    #Custom function-Get the maximum value of comment
                    results = parse_page(jsondata)
                    time.sleep(1)

                    m_id = results['max_id']               #marker input id manually
                    id_type = results['max_id_type']
            except:
                pass
        print ("--------------------------separator---------------------------")
    csvfile.close()

if __name__ == '__main__':

    #Get topic ID
    get_title_id()

    #Main function operation
    main()

    #Calculate usage time
    endTime = time.time()
    useTime = (endTime-startTime) / 60
    print("total time spent %s minutes"%useTime)

#Running results
