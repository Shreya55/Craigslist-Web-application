from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from . import models
from requests.compat import quote_plus 



BASE_CRAIGSLIST_URL = 'https://delhi.craigslist.org/search/?query={}' #dynamically generated query
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'  #alternate for no image

def basic(request):
    return render(request, 'myapp/basic.html')


def home(request):
    return render(request, 'myapp/base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search)) #joing the BASE_CRAIGSLIST_URL and the word that you search
    response = requests.get(final_url) #using bs4 requests that is imported which stores the final_url in var response
    data = response.text #converting that url html to text
    soup = BeautifulSoup(data, features='html.parser') #parsing and create bs4 object in a variable soup
    

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text #finds all items with class 'result-title'
        post_url = post.find('a').get('href') #finds all items with link to that item

#if a post has a price then print its price else print N/A
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

#if post has an image display it else display a peace sign image
#logic to grab image of posts-> bs4 cant grab images through direct img names but through data ids so
#data ids have been parsed and splitted and then grabbed

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

#creating a tuple of post's title,url,price,image so that it is visible on frontent by accessing through its indices
        final_postings.append((post_title, post_url, post_price, post_image_url))




    print(search)
    stuff_for_frontend = {
        'search' : search,
        'final_postings': final_postings,
    } 
    return render(request, 'myapp/new_search.html', stuff_for_frontend)