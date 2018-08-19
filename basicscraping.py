import pandas as pd
import requests
import time
from collections import defaultdict
from bs4 import BeautifulSoup

from bs4 import BeautifulSoup

def keyword_query(keyword):
    """

    Takes Indeed parameters, converts, and returns it into appropriate query format.

    """
    url = "http://www.indeed.com/jobs?q="
    for words in keyword:
        for word in words.split():
            url += word + '+'

    url = url + '&l={}&start={}'

    return url


def extract_text(query):
    if query:
        return query.text.strip()
    else:
        return None


def get_title_from_result(div):
    return extract_text(div.find(name='a', attrs={'data-tn-element':'jobTitle'}))


def get_company_from_result(div):
    return extract_text(div.find('span', {'class' : 'company'}))


def get_location_from_result(div):
    return extract_text(div.find('span', {'class' : 'location'}))


def get_summary_from_result(div):
    return extract_text(div.find('span', {'class' : 'summary'}))




def extract_posts_to_df(keyword=[], city_set=[], max_results_per_city=int):


    url = keyword_query(keyword)

    job_post = defaultdict(list)
    for city in city_set:

        for start in range(0, max_results_per_city, 10):
            page = requests.get(url.format(city, start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'html.parser')

            for div in soup.find_all(name='div', attrs={'class':'row'}):
                job_post['city'].append(city)
                job_post['title'].append(get_title_from_result(div))
                job_post['company'].append(get_company_from_result(div))
                job_post['location'].append(get_location_from_result(div))
                job_post['summary'].append(get_summary_from_result(div))

    df = pd.DataFrame.from_records(job_post)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df

def extract_posts_to_csv(keyword=[], city_set=[], max_results_per_city=int, file=0):
"""Extracts city, state, company, summary and title from posts on indeed.
    Writes the posts data to a CSV file  """
    url = keyword_query(keyword)

    for city in city_set:

        for start in range(0, max_results_per_city, 10):
            page = requests.get(url.format(city, start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'html.parser')

            for div in soup.find_all(name='div', attrs={'class':'row'}):
                f.write(str(city)+',')
                f.write(str(get_title_from_result(div))+',')
                f.write(str(get_company_from_result(div))+',')
                f.write(str(get_location_from_result(div))+',')
                f.write(str(get_summary_from_result(div))+'\n')
    return 0



cities = ['los angeles','chicago','san francisco','seattle','new york','austin',
          'philadelphia','atlanta','dallas','portland','phoenix','denver',
          'houston','miami','washington']
f = open('posts.csv','w')
extract_posts_to_csv(keyword=['data scientist'],city_set = cities, max_results_per_city = 1000, file = f)
f.close()
