# news-feed-analyzer #
A web-app that performs sentiment analysis of web-scrapped industrial news.

## Dependencies ##

 - Some important site-packages required are:
    - nltk==3.7
    - GoogleNews==1.6.4
    - numpy==1.23.0
    - pandas==1.4.3
    - tqdm==4.64.0
    - regex
    - pickle
    - pyodbc==4.0.32
    - sqlalchemy==1.4.38
    - mssql_django==1.1.3
 
 - Libraries:
    - Django v4.0.5
    - Python v3.8.0

## Description ##
- NLP models (using Count Vectorizer, Tf-Idf Vectorizer & Word2Vec) developed for News Sentiment Analysis.
- Web-scraping using GoogleNews, to generate unseen test data.
- Connection with database using pyodbc, create_engine & urllib, to push predicted results into the database managed by Microsoft SSMS 18.
- Deployment using virtualenv, rendered by Django.
- Simplistic UI made using HTML5, bootstrap5 and a little bit of Js.


One can run the scraper from the frontend to create a live news feed, and simultaneously run the model for classifying the news articles. 
Final results can be viewed by selecting options which displays the respective tables.

