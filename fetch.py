
from typing import Dict, Union

import sys
import requests
import json
from bs4 import BeautifulSoup as Soup
import re
from py2neo import Graph,Node,Relationship

douban_movie_graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="guitar"
)

baseurl = "https://movie.douban.com/j/new_search_subjects"

option = {
    'sort': 'u',
    'range': '0,10',
    'tags': '电影',
    'start': 0
    }
useragents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)"
]

url = '{0}?{1}'.format(baseurl, 'sort={}&range={}&tags={}&start={}'.format(
    option['sort'], option['range'], option['tags'], str(option['start'])))

headers = {
    'User-Agent':random.choice(useragents)
}

response = requests.get(url=url,headers=headers)

if not response.text:
    sys.exit(''Did not get proper response, start from:'+ option['start']')

for item in response.json():
    movie_id = item['id']
    movie_name = item['title']
    movie_url = item['url']
#    url = 'https://movie.douban.com/subject/'+str(id)
    headers = {
        'Host': 'movie.douban.com',
        'Referer': url,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    r = requests.get(url=url,headers=headers)
    soup = Soup(r)

    imdb_info = soup.find('a', href = re.compile('imdb'))
    imdb_url = imdb_info['href']
    imdb_id = imdb_info.text

#    director_info = soup.find_all('a', rel = re.compile('directedBy'))
#    directors = {}
#    for director in director_info:
#        directors['name'] = director.text
#        directors['link'] = director['href']
#
#    actor_info = soup.find_all('a', rel = re.compile('starring'))
#    actors = {}
#    for actor in actor_info:
#        actors['name'] = actor.text
#        actors['link'] = actor['href']

    info = json.loads(soup.find('script', type="application/ld+json"))
    directors = info['director']
    authors = info['author']
    actors = info['actor']

# rating process
    rating_everage = soup.find('strong', property="v:average").text
    votes = soup.find('span', property="v:votes").text
    rating_results = soup.find_all('span', class_ = 'rating_per')
    ratings = {}
    stars = 5
    for rating in rating_results:
        ratings[stars] = rating.text
        stars = stars -1

    desc = soup.find('span', property="v:summary").text




