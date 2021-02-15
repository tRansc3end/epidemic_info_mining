# -*- coding: utf-8 -*-

import requests
import json
import re
import time
import random

start_time=time.time()
headers = {
    "Cookie": '_T_WM=75978789314; SCF=AiOOsAW2Cy8W_lL7g7go7suT-GW58aezrrCGrXeOi97NoZlM5IjeG-yk0lOVqiGUnvaB3RiRHEKJ1AAeuRUY04o.; SUB=_2A25yz7zBDeRhGeFL6lYT9ifPzDWIHXVuM8SJrDV6PUJbktAKLUvakW1NQmRUR3SMHIiDuevyOk7UdZ1SAjKA0bi1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW-zz2CfNGU-JlivKLhBwlG5JpX5K-hUgL.FoMfeKBESo.0S0.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoM0eo24ShqX1K.4; SSOLoginState=1607191698; ALF=1609783698; BAIDU_SSP_lcr=https://login.sina.com.cn/; WEIBOCN_FROM=1110105030; MLOGIN=1; XSRF-TOKEN=5cb0d4; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E5%25AE%2598%25E6%2596%25B9%25E5%259B%259E%25E5%25BA%2594%25E5%258F%25A3%25E7%25BD%25A9%25E8%25BF%259B%25E4%25BB%25B76%25E6%25AF%259B%25E5%258D%25961%25E5%2585%2583%25E8%25A2%25AB%25E7%25BD%259A%2523%25EF%25BC%259A%25E7%25B3%25BB%25E5%258A%25B3%25E4%25BF%259D%25E5%258F%25A3%25E7%25BD%25A9%25EF%25BC%258C%25E5%25B9%25B3%25E6%2597%25B6%25E5%2594%25AE%25E4%25BB%25B7%25E4%25B8%258D%25E8%25B6%2585%25E8%25BF%25875%25E6%25AF%259B%26fid%3D100103type%253D1%2526q%253D%25E5%25AE%2598%25E6%2596%25B9%25E5%259B%259E%25E5%25BA%2594%25E5%258F%25A3%25E7%25BD%25A9%25E8%25BF%259B%25E4%25BB%25B76%25E6%25AF%259B%25E5%258D%25961%25E5%2585%2583%25E8%25A2%25AB%25E7%25BD%259A%2523%25EF%25BC%259A%25E7%25B3%25BB%25E5%258A%25B3%25E4%25BF%259D%25E5%258F%25A3%25E7%25BD%25A9%25EF%25BC%258C%25E5%25B9%25B3%25E6%2597%25B6%25E5%2594%25AE%25E4%25BB%25B7%25E4%25B8%258D%25E8%25B6%2585%25E8%25BF%25875%25E6%25AF%259B%26uicode%3D10000011',
    "User-agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
    "X-Requested-With": 'XMLHttpRequest',
    "Referer": 'https://m.weibo.cn/detail/4471277660537906'
}

# 抓取数据并获得数据
# 1.获得主页所有的新闻标题(网址)
# 新浪战役请的主页

#======获取新闻id======
def get_news_id():
    news_id=[]
    for i in range(20): #这里调节爬的信息多少
        url1 = 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_7978_-_ctg1_7978&page=' + str(i)
        respond=requests.get(url1,headers=headers)
        for j in respond.json()['data']['statuses']:
            news_id.append(j['id'])
            #news_id = json['id']
        time.sleep(0.5)
    return str(news_id)

def get_news(newsid):
    ls = []
    page = {}
    count = 1
    for id in newsid:
        print('正在爬取第{}个微博信息,共{}个'.format(count,len(newsid)))
        count += 1
        url2 = 'https://m.weibo.cn/detail/'+id
        html = requests.get(url2,headers=headers).text
        #微博正文
        wb = re.findall('.*?"text":(.*?),.*?',html)[0]
        weibo = re.sub('<S*?>[^>]*>.*?|<.*?>','',wb).replace('"','').replace(',',' ').replace('↵','').replace('\n','') #过滤标签
        #发布时间,并转化格式
        ct = re.findall('.*?"created_at":(.*?),.*?',html)[0].split(' ')
        if 'Mar' in ct:
            created_at = "{}/{}/{} {}".format(ct[-1].replace('"',''), '03', ct[3], ct[-3])
        elif 'Feb' in ct:
            created_at = "{}/{}/{} {}".format(ct[-1].replace('"',''), '02', ct[3], ct[-3])
        elif 'Jan' in ct:
            created_at = "{}/{}/{} {}".format(ct[-1].replace('"',''), '01', ct[3], ct[-3])
        elif 'Apr' in ct:
            created_at = "{}/{}/{} {}".format(ct[-1].replace('"',''), '04', ct[3], ct[-3])
        elif 'May' in ct:
            created_at = "{}/{}/{} {}".format(ct[-1].replace('"',''), '05', ct[3], ct[-3])
        else:
            created_at=''
        #楼主id
        title_user_id = re.findall('.*?"id":(.*?),.*?', html)[1]
        ##楼主昵称
        title_user_name = re.findall('.*?"screen_name": (.*?),.*?',html)[0]
        #楼主性别
        title_user_gender = re.findall('.*?"gender":(.*?),.*?', html)
        #楼主粉丝数
        title_user_followscount = re.findall('.*?"followers_count":(.*?),.*?', html)
        #发过微博数
        title_user_statusescount = re.findall('.*?"statuses_count":(.*?),.*?', html)
        #转发数
        reposts_count = re.findall('.*?"reposts_count":(.*?),.*?', html)
        #评论数
        comments_count = re.findall('.*?"comments_count":(.*?),.*?', html)
        #点赞数
        attitudes_count = re.findall('.*?"attitudes_count":(.*?),.*?', html)
        l = [id]+[weibo]+[created_at]+[title_user_id]+[title_user_name]+title_user_gender+title_user_followscount+title_user_statusescount+reposts_count+comments_count+attitudes_count
        ls.append(l)
        page[id] = int(comments_count[0])//20
        time.sleep(random.randint(3,7)/10)
    return ls,page

# 2.获取每个新闻下的评论单页的json
def get_json(url,max_id,max_id_type):
    params = {'max_id' : max_id,
              'max_id_type' : max_id_type}
    respond = requests.get(url,params = params,headers = headers)
    try:
        if respond.status_code == 200:
            return respond.json()
    except requests.ConnectionError as e:
        print('error',e.args)
        pass

# 获取评论及评论者信息
def get_comment(jsdt):
    ls2=[]
    for data in jsdt['data']['data']:

        # 评论正文
        t=data['text']
        t1=re.sub('<S*?>[^>]*>.*?|<.*?>','',t).replace(',',' ').replace('↵','').replace('\n','')# 去除表情
        # 评论点赞数
        t2=str(data['like_count'])
        # 评论昵称
        t3=data['user']['screen_name']
        # id
        t4=str(data['user']['id'])
        # 性别
        t5=data['user']['gender']
        # 时间日期
        tt=data['created_at'].split(' ')
        if 'Mar' in tt:
            t6 = "{}/{}/{} {}".format(tt[-1], '03', tt[2],tt[-3])#格式:年/月/日
        elif 'Feb' in tt:
            t6 = "{}/{}/{} {}".format(tt[-1], '02', tt[2],tt[-3])
        elif 'Jan' in tt:
            t6 = "{}/{}/{} {}".format(tt[-1], '01', tt[2],tt[-3])
        elif 'Apr' in tt:
            t6 = "{}/{}/{} {}".format(tt[-1], '04', tt[2],tt[-3])
        elif 'May' in tt:
            t6 = "{}/{}/{} {}".format(tt[-1], '05', tt[3],tt[-3])
        # 粉丝数
        t7 = str(data['user']['followers_count'])

        ls2.append([t1]+[t2]+[t3]+[t4]+[t5]+[t6]+[t7])

    return ls2
# 主函数
def main():
    newsid=get_news_id()
    print('完成newid获取共',len(newsid))
    ls,page=get_news(newsid)
    col='新闻id,正文,发布时间,作者id,昵称,性别,粉丝数,共发过微博数,转发数,评论数,点赞数'
    f=open('weiboNews.csv','a',encoding='utf-8')
    f.write(col+'\n')
    for i in ls:
        f.write(','.join(i)+'\n')
    f.close()
    print('已保存weiboNews.csv')
    col1='评论正文,评论点赞数,评论昵称,id,性别,时间日期,粉丝数,新闻id'+'\n'
    ff = open('weiboComment.csv','a',encoding='utf-8')
    ff.write(col1)

    for n in range(len(newsid)):
        print('正在爬取{}的评论'.format(n))
        max_id = 0
        max_id_type = 0
        try:
            if page[n] == 0:
                url = 'https://m.weibo.cn/comments/hotflow?id='+n+'&mid='+n+'&max_id_type=0'
                jsdt = get_json(url,max_id,max_id_type)
                list1 = get_comment(jsdt)
                for i in list1:
                    ff.write(','.join(i+[n])+'\n')
            else:
                for j in range(page[n]):#一个评论页的评论
                    url = 'https://m.weibo.cn/comments/hotflow?id='+n+'&mid='+n+'&max_id_type=0'
                    jsdt=get_json(url,max_id,max_id_type)
                    max_id = jsdt['data']['max_id']
                    max_id_type=jsdt['data']['max_id_type']
                    list1 = get_comment(jsdt)
                    for i in list1:
                        ff.write(','.join(i+[n])+'\n')
            print('完成')
        except:
            print('暂无评论')
        pass
        time.sleep(random.randint(3,7)/10)
    ff.close()
    print('全部完毕')
    return newsid

main()
end_time=time.time()
use_time=end_time-start_time
print('用时%s秒' %use_time)
