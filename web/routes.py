from newspaper import Article
from flask import Flask, url_for, request, \
         render_template, redirect, flash, session, Response
from time import sleep

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
import argparse
import pickle
from Topics import Topics
from Reader import Reader
from Processor import Processor

app = Flask(__name__)
with open('secret_key.txt','rb') as f:
    app.secret_key = f.read()

com_list = pickle.load(open('valid_list.pkl','rb'))
topics = pickle.load(open('topics_obj_300_2000_40_500.pkl','rb'))

def make_links(companies):
    # fetch the links
    base_str = "https://www.google.com/search?q={}"
    links = [base_str.format(c + ' ticker') for c in companies]
    return links

@app.route('/')
def index():
   return render_template('index.html') 

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def get_companies():    
    article_url = request.args.get('request_url')
    try:
        article = Article(article_url)
        article.download()
        article.parse()
        article_text = article.text
    except Exception as e:
        flash('Unable to parse news article, please provide another link')
        return redirect(url_for('index'))

    company_names = topics.get_top_companies(article_text)
    if len(company_names) == 0:
        flash("Couldn't match any companies to the article provided, please try a different article")
        return redirect(url_for('index'))
    
    # fetch company links and return to user
    links =  make_links(company_names)
    return render_template('results.html',company_names=company_names,links=links)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-p',dest='prod',action='store_true')
    parser.add_argument('--port',dest='port',type=int,default=5000)
    args = parser.parse_args()
    if args.prod:
        print('running in production')
        enable_pretty_logging()
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(args.port)
        IOLoop.instance().start()
    else:
        print('running in debug')
        app.debug = True
        app.run(port=args.port,host = '0.0.0.0')

