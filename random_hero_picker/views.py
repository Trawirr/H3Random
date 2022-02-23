from django.shortcuts import render
from django.http import HttpResponse
import bs4
import requests
import numpy as np

def say_hello(request):
    f = open('random_hero_picker\heroes.txt', 'r')
    heroes = f.readlines()
    f.close()
    heroes = [h.replace('\n', '') for h in heroes]
    page_hero = f'https://heroes.thelazy.net/index.php/{heroes[np.random.randint(len(heroes))]}'
    page = requests.get(page_hero)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    # fixing images' sources
    for img in soup.findAll('img'):
        img_urls = img['src']
        img_urls = img_urls.replace("/images", "https://heroes.thelazy.net/images")
        img['src'] = img_urls

    # removing all <a> tags
    for img in soup.findAll('a', href=True):
        img_urls = img['href']
        img_urls = img_urls.replace("/index", "https://heroes.thelazy.net/index")
        img['href'] = img_urls
    
    invalid_tags = ['a']
    for tag in invalid_tags: 
        for match in soup.findAll(tag):
            match.replaceWithChildren()

    tables = soup.findAll('table')[2]
    page_txt = str(tables)

    #return HttpResponse(page_txt)
    return render(request, 'roller.html')