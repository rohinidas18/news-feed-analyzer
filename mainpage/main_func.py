# -*- coding: utf-8 -*-

"""Sentiment Analysis of News Feed"""
"""Original file is located at https://colab.research.google.com/drive/11COiitL3bpQqlsUYwDa40b0FVFG5MNXs"""

# -----------------------------------------------------------------------------------------------------

def main_func():
    
    #import necessary libraries
    import nltk
    from sqlalchemy import create_engine
    import urllib
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    nltk.download('stopwords')
    nltk.download('omw-1.4')
    nltk.download('punkt')
    nltk.download('wordnet')
    from GoogleNews import GoogleNews
    import pandas as pd
    from tqdm import tqdm
    import regex as re
    import pickle
    
    """ Connect to SQLDatabase """
    
    SERVER = 'LAPTOP-OU080Q7K'
    DATABASE = 'newsDB'
    USERNAME = ''
    PASSWORD = ''    
    params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+PASSWORD)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)    
    connection = engine.connect() #checking the connection
    
    
    """Data Clean-up for NLP Sentiment Analysis"""

    def cleanup(news_titles):
      # all news headlines to lower case
      news_titles = news_titles.apply(lambda x: " ".join(x.lower() for x in str(x).split()))
      # remove non-alpha characters
      news_titles = news_titles.apply(lambda x: " ".join([re.sub('[^A-Za-z]+','', x) for x in nltk.word_tokenize(x)]))
      # remove stop words
      news_titles = news_titles.apply(lambda x: " ".join([x for x in x.split() if x not in stopwords.words('english')]))
      # perform lemmatization
      news_titles = news_titles.apply(lambda x: " ".join([WordNetLemmatizer().lemmatize(w) for w in nltk.word_tokenize(x)]))
      return news_titles


    """ **Testing on Scrapped Dataset** - Extracting Web-Scrapped Dataset"""

    #list of keywords
    keyword_list = [ 'HERO MOTOCORP LTD.', 'Srikalahasthi Pipes Limited', 'FORCE MOTORS LTD.', 'HINDUSTAN CONSTRUCTION CO.LTD.',
                    'ABB India Limited', 'KINETIC ENGINEERING LTD', 'USHA MARTIN LTD.', 'MAHINDRA & MAHINDRA LTD.',
                    'MAHARASHTRA SEAMLESS LTD.', 'BHARAT HEAVY ELECTRICALS LTD.', 'LML LTD.', 'ELECTROTHERM (INDIA) LTD.',
                    'MARUTI SUZUKI INDIA LTD.', 'NCC Limited', 'THERMAX LTD.', 'MAJESTIC AUTO LTD.', 'MSP STEEL & POWER LTD.',
                    'BEML LTD.', 'JINDAL SAW LTD.', 'ATLAS CYCLES (HARYANA) LTD.']
    
    
    # function to scrape news and then clean it, returns a list
    def get_news(word):
        gn = GoogleNews(lang='en',region='IN')
        gn.get_news(word)
        tlist = []
        tlist = gn.get_texts()

        tfinal = []
        for ele in tlist:
            if '-' in ele:
                temp_list = re.split(' - ', ele)
            else:
                temp_list = re.split(' [|] *', ele)
            tfinal.append(temp_list[0])
    
        return tfinal


    # create a dataframe for each list and append it to a final dataframe
    def get_dataframe():
        final_df = pd.DataFrame()
        
        for kw in tqdm(keyword_list):
            nlist = get_news(kw)
            cname = [kw for i in range(len(nlist))]
            df = pd.DataFrame(list(zip(cname, nlist[0:42])), columns=['company_name', 'news'])
            final_df = final_df.append(df, ignore_index=True)
            
        #final_df.reset_index(drop=True)
        return final_df



    """Preprocessing and clean-up of the scrapped Dataset"""
    news_df = get_dataframe()
    news_df["r_title"] = cleanup(news_df["news"])

    """Load the Vectorizers and the Models"""
    
    # load the tf-idf sentiment vectorizer from the file
    tfidf_vectorizer = pickle.load(open(r"C:\Users\Rohini\Desktop\news_feed\mainpage\tfidf_vectorizer.pkl", 'rb'))
    tf_x_test = tfidf_vectorizer.transform(news_df['r_title']).toarray()
    
    # loading saved sentimental model to test on extracted data
    tfidf_sentiment_model = pickle.load(open(r"C:\Users\Rohini\Desktop\news_feed\mainpage\sentiment-model_tfidf.pkl", 'rb'))
    
    # prediction on the scrapped dataset
    result_sentiment_tfidf = tfidf_sentiment_model.predict(tf_x_test)
    news_df["Sentiment_TfIdf"] = result_sentiment_tfidf
    del news_df["r_title"]
    
    """push dataframe to database"""
    
    try:
        news_df.to_sql("final_table", if_exists='replace', con=engine, chunksize=500)
        connection.close()
        return True
    except:
        return False
        
# ---------------------------------------------------------------------------------

def pick_up(company):
    from sqlalchemy import create_engine
    import urllib
    import pandas as pd
    
    SERVER = 'LAPTOP-OU080Q7K'
    DATABASE = 'newsDB'
    USERNAME = ''
    PASSWORD = ''    
    params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+PASSWORD)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)    
    connection = engine.connect()

    ndf = pd.read_sql_query(f"SELECT * FROM final_table WHERE company_name='{company}'", connection)
    connection.close()
    del ndf['index']
    return ndf

# -----------------------------------------------------------------------------------------

def jsonify_df(df): #function for turning a dataframe into an array
    import json
    json_records=df.reset_index().to_json()
    arr=[]
    arr=json.loads(json_records)
    return arr

# -----------------------------------------------------------------------------------------

