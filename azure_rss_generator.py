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
    # Finding all news items with the class "ms-rte-link"
    news_items = soup.find_all('a', class_='ms-rte-link')
    return title, news_items

def create_rss_feed(title, news_items, url):
    fg = FeedGenerator()
    fg.title(title)
    fg.link(href=url)
    fg.description(f"RSS feed for {url}")

    for item in news_items:
        item_title = item.text.strip()
        item_link = item['href']
        
        date_div = item.find_parent('div', class_='row')
        if date_div:
            date_p = date_div.find('div', attrs={'data-oc-token-text': ''}).find('p')
            if date_p:
                date_str = date_p.text.strip()
                item_date = datetime.datetime.strptime(date_str, '%b %d')
                current_year = datetime.datetime.now().year
                item_date = item_date.replace(year=current_year, tzinfo=datetime.timezone.utc)
                
                fe = fg.add_entry()
                fe.title(item_title if item_title else "No title")
                fe.link(href=f"https://azure.microsoft.com{item_link}" if item_link.startswith('/') else item_link)
                fe.description(item_title)
                fe.published(item_date)
                print(f"Item added: {item_title}, Date: {item_date}")
            else:
                print(f"Date not found for item: {item_title}")
        else:
            print(f"Date div not found for item: {item_title}")

    return fg

def main():
    url = "https://azure.microsoft.com/en-us/updates/"
    content = get_webpage_content(url)
    title, news_items = parse_webpage(content)
    feed = create_rss_feed(title, news_items, url)
    
    feed.rss_file('azure_updates_feed.xml')
    print("RSS feed has been created and saved as 'azure_updates_feed.xml'")
    print(f"Number of items in feed: {len(feed.entry())}")

if __name__ == "__main__":
    main()
