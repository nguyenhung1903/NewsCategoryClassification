import warnings
warnings.filterwarnings("ignore")

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os
import argparse

from tqdm import tqdm

def getHTMLdocument(url):
    """
        getHTMLdocument(url) -> _type_
    Args:
        url (str): URL of the website

    Returns:
        str: HTML document of the website
    """
    response = requests.get(url)
    return response.text


class DanTriArticle:
    """
        DanTriArticle(url, OUT_DIR) -> _type_
    Args:
        url (str): URL of the website
        OUT_DIR (str): Output directory
    """
    def __init__(self, url, OUT_DIR):
        self.url = url
        self.OUT_DIR = OUT_DIR

    def get_categories(self, categories = ["Thế giới", "Thể thao", "Giáo dục", "Pháp luật", "Sức khỏe", "Du lịch", "Đời sống", "Giải trí"]):
        html_document = getHTMLdocument(self.url)
        soup = BeautifulSoup(html_document, 'html.parser')

        categories_link = []

        for x in soup.find_all('ol', {'class': 'nf-menu'})[0].find_all('li'):
            category = x.find('a').text.strip()
            if (category in categories):
                categories_link.append({"category": category, "link": x.find('a').get('href')})

        return categories_link

    def get_articles(self, category, page = 10):
        name = category['link'].split('.')[0].replace('/', '_')
        f = open(f"{self.OUT_DIR}/url{name}.txt", "w")

        for i in range(1, page + 1):
            sub_url = f"{self.url}{category['link'].split('.')[0]}/trang-{i}.htm"
            print(sub_url)
            soup = BeautifulSoup(getHTMLdocument(sub_url), 'html.parser')
            for e in soup.find_all("a", {'class': "dt-text-black-mine"}):
                f.write(f"{e.text.strip()}\t{e.get('href')}\n")
        f.close()

    def get_article(self, url):
        soup = BeautifulSoup(getHTMLdocument(f"{self.url}{url}"), 'html.parser')
        article = soup.find("article")
        if article is None:
            return None

        # print(f"link: {url}")

        # get article's content
        type_article = soup.find("div", {"class":"emagazine-category"})
        # print(f"Type article: {type_article}")
        if type_article is None:
            # Normal news
            time = article.find("time", {"class": "author-time"}).get("datetime")
            title = article.find("h1", {"class": "title-page detail"}).text.strip()
            description = article.find("h2", {"class": "singular-sapo"}).text.strip()
            content = article.find("div", {"class": "singular-content"}).text.strip()

            if article.find("div", {"class": "author-name"}) is None:
                author = ""
                author_link = ""
            else:
                author = article.find("div", {"class": "author-name"}).text.strip()
                author_link = article.find("div", {"class": "author-name"}).find("a").get("href")

            return {"title": title, "description": description, "content": content, "author": author, "author_link": author_link, "time": time}

        else:
            type_article = type_article.find("img").get("alt")
            if type_article == "DNews":
                # DNews
                time = article.find("time", {"class": "author-time"}).get("datetime")
                title = article.find("h1", {"class": "e-magazine__title"}).text.strip()
                description = article.find("h2", {"class": "e-magazine__sapo"}).text.strip()
                content = article.find("div", {"class": "e-magazine__body dnews__body"}).text.strip()

                if article.find("div", {"class": "author-name"}) is None:
                    author = ""
                    author_link = ""
                else:
                    author = article.find("div", {"class": "author-name"}).text.strip()
                    author_link = article.find("div", {"class": "author-name"}).find("a").get("href")

                return {"title": title, "description": description, "content": content, "author": author, "author_link": author_link, "time": time}

            elif type_article == "PhotoStory":
                # Photo story
                time = article.find("time", {"class": "e-magazine__meta-item"}).get("datetime")
                title = article.find("h1", {"class": "e-magazine__title"}).text.strip()
                description = article.find("h2", {"class": "e-magazine__sapo sapo-top"}).text.strip()
                content = article.find("div", {"class": "e-magazine__body"}).text.strip()

                if article.find("div", {"class": "e-magazine__meta"}) is None:
                    author = ""
                    author_link = ""
                else:
                    author = article.find("div", {"class": "e-magazine__meta"}).text.strip()
                    author_link = article.find("div", {"class": "e-magazine__meta"}).find("a").get("href")

                return {"title": title, "description": description, "content": content, "author": author, "author_link": author_link, "time": time}
            
            
if __name__=="__main__":
    
    args = argparse.ArgumentParser()
    args.add_argument("--url", type=str, default="https://dantri.com.vn", help="URL of the website")
    args.add_argument("--out_dir", type=str, default="dantri_test", help="Output directory")
    args.add_argument("--page", type=int, default=10, help="Number of pages to scrape")
    args = args.parse_args()
    
    url_to_scrape = args.url
    OUT_DIR = args.out_dir
    
    os.makedirs(OUT_DIR, exist_ok=True)
    
    dantri_article = DanTriArticle(url_to_scrape, OUT_DIR)

    categories = dantri_article.get_categories()
    
    # get articles and save the title and url to file for each category
    for category in categories:
        dantri_article.get_articles(category, args.page)
    
    # read the data from the file
    special_links = []
    for c in categories:
        df_output = pd.DataFrame(columns=['time', 'title', 'description','content', 'author', 'author_link', 'category', 'link'])
        name = c["category"]
        data = pd.read_csv(f'{OUT_DIR}/url{c["link"].split(".")[0].replace("/", "_")}.txt', sep='\t', header=None)
        
        print(f"Category: {name}")
        for i in tqdm(range(len(data))):
            _, link = data.iloc[i]
            
            try:
                article = dantri_article.get_article(link)
                df_output = df_output._append({"time": article["time"], "title": article["title"], "description": article["description"], "content": article["content"], "author": article["author"], "author_link": article["author_link"], "category": name, "link": link}, ignore_index=True)
            except Exception as e:
                print(f"Error: {e}")
                special_links.append(link)
                print(f"Special link: {link}")
            
        df_output.to_csv(f"{OUT_DIR}/{c['link'].split('.')[0]}.csv", index=False)
        
    
    f = open(f"{OUT_DIR}/special_links.txt", "w")
    for link in special_links:
        f.write(f"{link}\n")
    f.close()
    
    print("concatenate all csv files")
    all_files = [f"{OUT_DIR}/{c['link'].split('.')[0]}.csv" for c in categories]
    df = pd.concat([pd.read_csv(f) for f in all_files])
    df.to_csv(f"{OUT_DIR}/dantri.csv", index=False)
    
    print("Done!")
    
# python craw_data.py --url "https://dantri.com.vn" --out_dir "dantri_test" --page 10