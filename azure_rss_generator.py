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
    
    print(f"Page title: {title}")

    # Find all layout containers
    layout_containers = soup.find_all('div', class_='layout-container')
    print(f"Number of layout containers found: {len(layout_containers)}")

    news_items = []
    for i, container in enumerate(layout_containers):
        print(f"\nAnalyzing container {i+1}:")
        date_div = container.find('div', class_='areaheading')
        article_div = container.find('div', class_='richtext')
        
        if date_div and article_div:
            date_text = date_div.find('div', {'data-automation-test-id': lambda x: x and x.startswith('AreaheadingDesctext-areaheading-')})
            article_link = article_div.find('a', class_='ms-rte-link')
            
            if date_text and article_link:
                news_items.append({
                    'date': date_text.text.strip(),
                    'title': article_link.text.strip(),
                    'link': article_link['href']
                })
                print(f"  Item added: {date_text.text.strip()} - {article_link.text.strip()[:50]}...")

    print(f"\nTotal news items found: {len(news_items)}")
    return title, news_items

def create_rss_feed(title, news_items, url):
    fg = FeedGenerator()
    fg.title(title)
    fg.link(href=url)
    fg.description(f"RSS feed for {url}")
    
    for item in news_items:
        fe = fg.add_entry()
        fe.title(item['title'])
        fe.link(href=item['link'] if item['link'].startswith('http') else f"https://azure.microsoft.com{item['link']}")
        fe.description(item['title'])
        
        try:
            date_str = item['date']
            item_date = datetime.datetime.strptime(date_str, '%b %d')
            current_year = datetime.datetime.now().year
            item_date = item_date.replace(year=current_year, tzinfo=datetime.timezone.utc)
            fe.published(item_date)
            print(f"RSS item added: {item['title']}, Date: {item_date}")
        except ValueError:
            print(f"Date parsing failed for item: {item['title']}, Date string: {date_str}")
    
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
