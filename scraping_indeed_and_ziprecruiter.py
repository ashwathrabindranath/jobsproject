import pandas as pd
import requests
import time
from collections import defaultdict
from bs4 import BeautifulSoup

from bs4 import BeautifulSoup

def key_query_indeed(keyword):
    """

    Takes Indeed parameters, converts, and returns it into appropriate query format.

    """
    url = "http://www.indeed.com/jobs?q="
    for words in keyword:
        for word in words.split():
            url += word + '+'

    url = url + '&l={}&start={}'

    return url

def key_query_ziprecruiter(keyword):

    """
    Takes Ziprecruiter parameters, converts, and returns it into appropriate query format.
    """
    url = "https://www.ziprecruiter.com/candidate/search?form=jobs-landing&search="
    for words in keyword:
        for word in words.split():
            url+=word + '%20'
        url = url + '&radius=5&location={}&page={}'
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





def extract_indeed_posts_to_df(keyword=[], city_set=[], max_results_per_city=int):


    url = key_query_indeed(keyword)

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

def extract_ziprecruiter_posts_to_df(keyword=[], city_set=[], max_results_per_city=int):


    url = key_query_ziprecruiter(keyword)

    job_post = defaultdict(list)
    for city in city_set:

        for start in range(0, max_results_per_city, 10):
            page = requests.get(url.format(city, start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'html.parser')

            for div in soup.find_all(name='div', class_='job_content'):
                job_post['city'].append(city)
                job_post['title'].append(extract_text(div.find('span',class_='just_job_title')))
                job_post['company'].append(extract_text(div.find('a',class_='t_org_link name')))
                job_post['location'].append(extract_text(div.find('a',class_='t_location_link location')))
                job_post['summary'].append(extract_text(div.find('p',class_='job_snippet')))

    df = pd.DataFrame.from_records(job_post)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def extract_indeed_posts_to_csv(keyword=[], city_set=[], max_results_per_city=int, file=0):
    """Extracts city, state, company, summary and title from posts on indeed.
    Writes the posts data to a CSV file  """
    url = key_query_indeed(keyword)

    for city in city_set:

        for start in range(0, max_results_per_city, 10):
            page = requests.get(url.format(city, start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'html.parser')

            for div in soup.find_all(name='div', attrs={'class':'row'}):
                f.write(str(city)+',')
                f.write('\"'+str(get_title_from_result(div))+'\"'+',')
                f.write('\"'+str(get_company_from_result(div))+'\"'+',')
                f.write('\"'+str(get_location_from_result(div))+'\"'+',')
                f.write('\"'+str(get_summary_from_result(div))+'\"'+'\n')
    return 0

def extract_ziprecruiter_posts_to_csv(keyword=[], city_set=[], max_results_per_city=int, file = 0):


    url = key_query_ziprecruiter(keyword)

    job_post = defaultdict(list)
    for city in city_set:

        for start in range(0, max_results_per_city, 10):
            page = requests.get(url.format(city, start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'html.parser')

            for div in soup.find_all(name='div', class_='job_content'):
                f.write(str(city)+",")
                f.write('\"'+ str(extract_text(div.find('span',class_='just_job_title')))+'\"'+",")
                f.write('\"'+str(extract_text(div.find('a',class_='t_org_link name')))+'\"'+",")
                f.write('\"'+str(extract_text(div.find('a',class_='t_location_link location')))+'\"'+",")
                f.write('\"'+str(extract_text(div.find('p',class_='job_snippet')))+'\"'+'\n')

    df = pd.DataFrame.from_records(job_post)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


cities = ['los angeles','chicago','san francisco','seattle','new york','austin',
          'philadelphia','atlanta','dallas','portland','phoenix','denver',
          'houston','miami','washington']
f = open('indeed_posts.csv','w')
extract_indeed_posts_to_csv(keyword=['data scientist'],city_set = cities, max_results_per_city = 1000, file = f)
f.close()
g = open('ziprecruiter_posts.csv','w')
extract_ziprecruiter_posts_to_csv(keyword=['data scientist'],city_set = cities, max_results_per_city = 1000, file = g)
g.close()
