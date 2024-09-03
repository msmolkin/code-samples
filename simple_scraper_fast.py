import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import markdownify
from concurrent.futures import ThreadPoolExecutor

# All comments are things you might want to edit

# Set the base URL
base_url = "https://developer.usajobs.gov"
visited_urls = set()

def save_as_markdown(html_content, url):
    # Convert HTML to Markdown
    markdown_content = markdownify.markdownify(html_content, heading_style="ATX")
    
    # Create a filename based on the URL
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/').replace('/', '_') + '.md'
    if not path:
        path = 'index.md'
    
    # Save the content to a markdown file
    with open(path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)

def scrape_page(url):
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Scraping {url}")
    
    # Find the main content area and save it as markdown
    main_content = soup.find(id="main-content")
    if main_content:
        save_as_markdown(str(main_content), url)
    
    # Find all internal links
    internal_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            internal_links.append(full_url)

    # Use ThreadPoolExecutor to scrape pages in parallel
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        executor.map(scrape_page, internal_links)

# Start scraping from the base URL
os.chdir(os.path.dirname(os.path.abspath(__file__)))
scrape_page(base_url)