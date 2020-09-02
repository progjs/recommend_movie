#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(1)
date = yesterday.strftime('%Y%m%d')

print(date)

# # 1. 영화랭킹(평점순)에서 장르별 30개씩 스크래핑하기

# In[63]:


# 랭킹 1~50위까지 영화제목, 상세페이지 크롤링
import requests
from bs4 import BeautifulSoup
import bs4
from urllib.parse import urljoin
import re

main_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + date

movie_list = []
# for i in [1, 2, 4, 5, 6, 7, 11, 13, 15, 16, 18, 19]:

for page_num in [1, 2]:
    movie_genre_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + str(date) + '&tg=' + str(
        1) + '&page=' + str(page_num)
    html = requests.get(movie_genre_url).text
    soup = BeautifulSoup(html, 'html.parser')

    a_tag_list = soup.select('div .tit5 a[href*="basic.nhn"]')

    for idx, a_tag in enumerate(a_tag_list, 1):
        if idx > 50:
            break
        movie_dict = {}
        title = a_tag.text.strip()
        link = urljoin(main_url, a_tag['href'])

        movie_dict['genre_code'] = 1
        movie_dict['id'] = idx
        movie_dict['title'] = title
        movie_dict['url'] = link
        # scorre_url 은 평점을 스크래핑하기 위한 페이지
        movie_dict['score_url'] = link.replace('basic', 'pointWriteFormList')
        movie_list.append(movie_dict)
        # print(idx, title, link)

print(len(movie_list))
movie_list

# In[64]:


movie_code_list = []
# for i in [1, 2, 4, 5, 6, 7, 11, 13, 15, 16, 18, 19]:
for page_num in [1, 2]:
    movie_genre_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + str(date) + '&tg=' + str(
        1) + '&page=' + str(page_num)
    html = requests.get(movie_genre_url).text
    soup = BeautifulSoup(html, 'html.parser')

    a_tag_list = soup.select('div .tit5 a[href*="basic.nhn"]')

    for idx, a_tag in enumerate(a_tag_list, 1):
        if idx > 50:
            break
        movie_code = re.findall("\d+", a_tag['href'])

        for movie in movie_code:
            movie_code_list.append(movie)

print(len(movie_code_list))
movie_code_list

# In[65]:


movie_info_lists = []

for movie in movie_list:
    html = requests.get(movie['url']).text
    soup = BeautifulSoup(html, 'html.parser')

    movie_info_dict = {}

    # 타이틀
    title = soup.select_one('h3.h_movie a[href*="basic.nhn"]')
    if title == None:
        movie_info_dict['title'] = None
    else:
        movie_info_dict['title'] = title.text.strip().replace(',', '')

    # 네티즌 평점
    score = soup.select_one('div.netizen_score .star_score em')
    if score == None:
        movie_info_dict['score'] = None
    else:
        movie_info_dict['score'] = score.text.strip()

    # 개봉국가
    nation = soup.select_one('dl.info_spec span a[href*="nation"]')
    if nation == None:
        movie_info_dict['nation'] = None
    else:
        movie_info_dict['nation'] = nation.text.strip()

    # 감독
    director = soup.select_one('dl.info_spec a[href*="code"]')
    if director == None:
        movie_info_dict['director'] = None
    else:
        movie_info_dict['director'] = director.text.strip()

    # 누적관객수 
    audience = soup.select_one('p.count')
    if audience == None:
        movie_info_dict['audience'] = None
    else:
        movie_info_dict['audience'] = re.sub(r"(명)\([^()]*\)", "", audience.text.strip()).replace(',', '')

    # 관람객 평점 건수
    comment_count = soup.select_one('div.netizen_score .user_count em')
    if comment_count == None:
        movie_info_dict['comment_count'] = None
    else:
        movie_info_dict['comment_count'] = comment_count.text.strip().replace(',', '')

    # 개봉일자
    release_year = soup.select_one('dl.info_spec a[href*="open"]')
    if release_year == None:
        movie_info_dict['release_year'] = None
    else:
        movie_info_dict['release_year'] = release_year.text.strip()

    # 평점
    movie_info_dict['score_sum'] = 0

    # 줄거리
    plot = soup.select_one('.con_tx')
    if plot == None:
        movie_info_dict['plot'] = None
    else:
        movie_plot = " ".join(re.sub('|  |\t|\r|\n|', '', plot.text).split())
        movie_info_dict['plot'] = movie_plot.replace(',', "")

    movie_info_lists.append(movie_info_dict)

print(len(movie_info_lists))
print(movie_info_lists)

# ## 2.1. movieapp_movie 테이블

# In[67]:


import numpy as np
import pandas as pd

data_df = pd.DataFrame(
    columns=['title', 'score', 'nation', 'director', 'audience', 'plot', 'score_sum', 'comment_count', 'release_year'])

for data in movie_info_lists:
    series_obj = pd.Series(data)
    data_df = data_df.append(series_obj, ignore_index=True)

# 인덱스를 1부터 시작하는 방법
data_df.index = np.arange(1, len(data_df) + 1)

data_df

# ## 2.2. movieapp_genre 테이블

# In[68]:

#
# movie_genre_lists = []
# for movie in movie_list:
#     movie_genre_dict = {}
#
#     html = requests.get(movie['url']).text
#     soup = BeautifulSoup(html, 'html.parser')
#
#     title = soup.select_one('h3.h_movie a[href*=basic.nhn]')
#     if title == None:
#         movie_genre_dict['title'] = None
#     else:
#         movie_genre_dict['title'] = soup.select_one('h3.h_movie a[href*=basic.nhn]').text.strip().replace(',', '')
#
#     genre = soup.select_one('dl.info_spec span')
#     if genre == None:
#         movie_genre_dict['genre'] = None
#     else:
#         movie_genre_dict['genre'] = re.sub(r"\s+", "", genre.text.strip())
#
#     movie_genre_lists.append(movie_genre_dict)
#
# print(len(movie_genre_lists))
#
# for movie_genre in movie_genre_lists:
#     print(movie_genre)
#
# # In[69]:
#
#
# final_genre_list = []
#
# for idx, movie_genre in enumerate(movie_genre_lists, 1):
#     if movie_genre['genre'] == None:
#         movie_genre['genre'] = '로그인 필요(19금)'
#     else:
#         genres = movie_genre['genre'].split(',')
#
#     for genre in genres:
#         genre_dict = {}
#         genre_dict['movie_id'] = idx
#         genre_dict['genre'] = genre
#         final_genre_list.append(genre_dict)
#
# final_genre_list
#
# # In[70]:
#
#
# import numpy as np
# import pandas as pd
#
# genre_data_df = pd.DataFrame(columns=['genre', 'movie_id'])
# for final_genre in final_genre_list:
#     series_obj = pd.Series(final_genre)
#     genre_data_df = genre_data_df.append(series_obj, ignore_index=True)
#
# # 인덱스를 1부터 시작하는 방법
# genre_data_df.index = np.arange(1, len(genre_data_df) + 1)
# genre_data_df
#
# # ### 2.3. movieapp_actor 테이블
#
# # In[72]:
#
#
# movie_actor_list = []
# for movie in movie_list:
#     movie_actor_dict = {}
#     # print(movie)
#     html = requests.get(movie['url']).text
#     soup = BeautifulSoup(html, 'html.parser')
#
#     actor = soup.find('dl', attrs={"class": "info_spec"})
#     if actor == None:
#         movie_actor_dict['actor'] = None
#     else:
#         movie_actor_dict['actor'] = re.sub(r'\([^)]*\)', '', actor.find_all("dd")[2].text.replace('더보기', ''))
#
#     movie_actor_list.append(movie_actor_dict)
#
# print(len(movie_actor_list))
#
# for movie_actor in movie_actor_list:
#     print(movie_actor)
#
# # In[74]:
#
#
# final_actor_list = []
#
# for idx, movie_actor in enumerate(movie_actor_list, 1):
#     if movie_actor['actor'] == None:
#         movie_actor['actor'] = None
#     else:
#         actors = movie_actor['actor'].split(', ')
#
#     for actor in actors:
#         actor_dict = {}
#         actor_dict['movie_id'] = idx
#         actor_dict['actor'] = actor
#         final_actor_list.append(actor_dict)
#
# final_actor_list
#
# # In[75]:
#
#
# import numpy as np
# import pandas as pd
#
# actor_data_df = pd.DataFrame(columns=['actor', 'movie_id'])
# for final_actor in final_actor_list:
#     series_obj = pd.Series(final_actor)
#     actor_data_df = actor_data_df.append(series_obj, ignore_index=True)
#
# # 인덱스를 1부터 시작하는 방법
# # 인덱스 값 변겅
# actor_data_df.index = np.arange(1, len(actor_data_df) + 1)
# actor_data_df
#
# # ## 2.3. movieapp_comment 테이블 (미완성)
#
# # In[76]:
#
#
# comment_list = []
# data = datetime.datetime.now()
# data.strftime('%Y-%m-%d %H:%M:%S.%f')
#
# for idx, movie_code in enumerate(movie_code_list, 1):
#     comment_url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' + movie_code + '&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page='
#
#     for i in range(1, 11):
#         comment_detail_urls = comment_url + str(i)
#         html = requests.get(comment_detail_urls).text
#         soup = BeautifulSoup(html, 'html.parser')
#         comment_tag_list = soup.select('span[id^=_filtered_ment_]')
#         # print(comment_tag_list)
#
#         for comment_tag in comment_tag_list:
#             space_comment = comment_tag.text.strip()
#             no_space_comment = re.sub('|  |\t|\n', '', space_comment)
#             # print(no_space_comment)
#
#             comment_dict = {}
#             comment_dict['movie_id'] = idx
#             comment_dict['comment'] = no_space_comment.replace(',', '')
#             comment_dict['published_date'] = data.strftime('%Y-%m-%d %H:%M:%S.%f')
#             comment_dict['comment_score'] = 0
#             comment_dict['user_id'] = 0
#             comment_list.append(comment_dict)
#
#             if len(comment_tag_list) != 10:
#                 break;
#
# comment_list
#
# # In[78]:
#
#
# import numpy as np
# import pandas as pd
#
# comment_data_df = pd.DataFrame(columns=['comment', 'published_date', 'movie_id', 'comment_score', 'user_id'])
# for comment in comment_list:
#     series_obj = pd.Series(comment)
#     comment_data_df = comment_data_df.append(series_obj, ignore_index=True)
#
# # 인덱스를 1부터 시작하는 방법
# # 인덱스 값 변겅
# comment_data_df.index = np.arange(1, len(comment_data_df) + 1)
# comment_data_df

# # 3. 판다스 데이터프레임 CSV 파일로 export하기

# In[79]:


data_df.to_csv('C:/mypython/test/testcomplete.csv', index=True, header=False, encoding='utf-8-sig')
# genre_data_df.to_csv('C:/mypython/test/movieapp_genre.csv', index=True, header=False, encoding='utf-8-sig')
# actor_data_df.to_csv('C:/mypython/test/movieapp_actor.csv', index=True, header=False, encoding='utf-8-sig')
# comment_data_df.to_csv('C:/mypython/test/movieapp_comment.csv', index=True, header=False,
#                        encoding='utf-8-sig')
