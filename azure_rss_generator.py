import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime

def get_webpage_content(url):
    response = requests.get(url)
    return response.text

def parse_webpage(content):
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.string if soup.title else "Azure Updates"
    # Find all news items with the class "ms-rte-link"
    news_items = soup.find_all('a', class_='ms-rte-link')
    return title, news_items

def create_rss_feed(title, news_items, url):
    fg = FeedGenerator()
    fg.title(title)
    fg.link(href=url)
    fg.description(f"RSS feed for {url}")

    for item in news_items:
        fe = fg.add_entry()
        item_title = item.text.strip()
        item_link = item['href']
        
        fe.title(item_title if item_title else "No title")
        fe.link(href=f"https://azure.microsoft.com{item_link}" if item_link.startswith('/') else item_link)
        fe.description(item_title)


    return fg

def main():
    url = "https://azure.microsoft.com/en-us/updates/"
    content = get_webpage_content(url)
    title, news_items = parse_webpage(content)
    feed = create_rss_feed(title, news_items, url)
    
    feed.rss_file('azure_updates_feed.xml')
    print("RSS feed has been created and saved as 'azure_updates_feed.xml'")
    print(f"Number of items in feed: {len(news_items)}")

if __name__ == "__main__":
    main()
