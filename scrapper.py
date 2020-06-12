from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from IPython.core.display import clear_output
from time import time
from warnings import warn
import pandas as pd
import os

def url(page_count = "51", country_code="us"):
     #returns url with the inputed query params
    #skips first page 
    if int(page_count) < 51:
        #if first page
        return "https://www.imdb.com/search/title/?title_type=movie&countries="+country_code
        
    return "https://www.imdb.com/search/title/?title_type=movie&countries="+country_code +"&start="+ page_count +"&ref_=adv_nxt"

def get_pages(pages_number):
    #returns list of the pages 
    pages = []
    page_count = 51
    pages.append(url(0,"us"))

    for i in range(1,pages_number):
        page_count = page_count + 50
        pages.append(url(str(page_count),"us"))
    return pages

pages = get_pages(8)
titles =  []
years =   []
genres =  []

requests = 0
start_time = time()

# For every page in the interval 1-4
for page in pages:

    # Make a get request
    response = get(page, headers = {"Accept-Language": "en-US, en;q=0.5"})

    # Pause the loop
    sleep(randint(10,15))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)

    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if requests > 72:
        warn('Number of requests was greater than expected.')
        break
    
    page_html =  BeautifulSoup(response.text, 'html.parser')
    movie_containers = page_html.find_all('div', class_ = 'lister-item-content')
    for container in movie_containers:
        titles.append(container.h3.a.text)
        #year
        years.append(container.find("span", class_="lister-item-year text-muted unbold").text)
        #genre
        if container.find("span", class_="genre") is not None:
            genres.append(container.find("span", class_="genre").text)
        else:
            genres.append("/")

    

#make a data frame
movie_ratings = pd.DataFrame({'movie': titles,
"years": years,
"genres": genres
})


#save the data frame as a csv to our current dir
movie_ratings.to_csv("movies", encoding='utf-8', index=False)

#lister-item-content