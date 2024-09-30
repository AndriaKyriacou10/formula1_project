from flask import Blueprint, request, render_template, redirect, flash, url_for
import re
import datetime

from .helpers import *
from .models import *
from . import db

news = Blueprint('news', __name__)

API_KEY # Add you own API KEY from newsapi
query = "\"Formula 1\" OR \"F1\" -NASCAR -football -soccer -Premier -league -MotoGP -F2 -F3 -WEC -WRC"
language = 'en'
domains = 'autosport.com'
limit = 4

@login_required
@news.route('/news')
def get_news():
    
    if 'page' not in request.args:
        # Redirect to /news?page=1 if 'page' parameter is missing
        return redirect(url_for('news.get_news', page=1))
    try:
        page = request.args.get('page', 1, type=int)
        page_size = 4  # Number of articles per page
        
        page_num = (page-1 if page%page_size==0 else page)
        start_page = (page_num // page_size)*page_size + 1
        end_page = (page_num // page_size)*page_size + 4
        num_pages = [i for i in range(start_page,end_page+1)]


        url = f"https://newsapi.org/v2/everything?q={query}&language={language}&sortBy=publishedAt&domains={domains}&pageSize={limit}&page={page}&apiKey={API_KEY}"
        response = requests.get(url).json()

        news = response['articles'] 
        
        total_results = response.get('totalResults', 0)
        total_pages = (total_results // limit) + (1 if total_results%page_size > 0 else 0)
        print(total_pages)
    except:
        print(f"Got exception")
        page=1
        total_pages = 1    
        news = []
     
    return render_template('news.html', news=news, page = page, total_pages = total_pages, num_pages = num_pages)