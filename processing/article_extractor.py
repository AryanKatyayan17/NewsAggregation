from newspaper import Article

def extract_article_content(url):
    try:
        article= Article(url)
        article.download()
        article.parse()

        return {
            "title":article.title,
            "text":article.text,
            "authors":article.authors,
            "publish_date":article.publish_date
        }
    
    except Exception as e:
        return {
            "title":"Extraction Failed",
            "text":f"Could not get the article: {e}",
            "authors":[],
            "publish_date":None
        }