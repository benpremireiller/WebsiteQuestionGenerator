import requests
from bs4 import BeautifulSoup, NavigableString
from furl import furl

class WebsiteScraper:

    def __init__(self):
        pass

    def get_website_data(self, user_provided_url, scrape_page_limit = 3) -> list[dict]:
        """Return data about a website by scraping the content passed webpage and related navigation pages"""
        
        content = []
        parsed_url = self.standardize_url(user_provided_url)

        # Access the page the user provided
        try:
            root_response = requests.get(parsed_url)
        except:
            raise Exception('Unable to retrieve data from: ' + parsed_url)
        
        soup = BeautifulSoup(root_response.text, 'html.parser')

        # Get the first navigation anchor tags on the site
        navs = soup.find('nav')
        href_urls = navs.find_all('a', attrs={"href": True}) if navs else [] 
        
        # Add all nav anchors to scrape list
        sites_to_scrape = [parsed_url]
        hrefs = [parsed_url + url.get('href')[1:] if url.get('href')[0] == '/' else parsed_url + url.get('href') for url in href_urls] 
        sites_to_scrape = sites_to_scrape + hrefs
        
        already_scraped = [] # To avoid scraping the same page

        # Scrape up to scrape_page_limit pages on the domain
        i = 0
        while i < min(scrape_page_limit, len(sites_to_scrape)): 
            site = sites_to_scrape[i]
            if site not in already_scraped:
                try:
                    site_data = self.scrape_webpage(site)
                    content.append(site_data)
                    already_scraped.append(site)
                except:
                    print('Unable to scrape site:', site)
            i += 1

        return content


    def scrape_webpage(self, url) -> dict:
        """Scrape a url, trim the response and return the remaining html"""

        # Download the page html
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('title').get_text() if soup.find('title') else []

        # Only keep tags related to headers and paragraphs, plus divs for structure
        tags_to_keep = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']
        content_str = self.strain_soup(soup, tags_to_keep)

        output = {'title': title, 'contents': content_str}

        return output

    def strain_soup(self, soup, tags_to_keep) -> str:
        """Strain or trim soup object to only tags passed in tags_to_keep"""

        # Keep only the tags required
        for tag in soup.find_all():
            if tag.name not in tags_to_keep:
                for element in tag.children:
                    if isinstance(element, NavigableString): # Remove strings that are direct children of tags we want to remove
                        element.extract()
                tag.unwrap()
            else:
                tag.attrs = {}

        # Strip whitespace
        for element in soup.find_all(string=lambda text: not text.strip()):
            element.extract()

        # Flatten structure
        for tag in soup.find_all():
            empty_container = len(list(tag.children)) == 0
            only_same_children = all([element.name == tag.name for element in tag.children])

            if tag.get_text().strip() == '': # No text in any descendents
                tag.extract()

            elif empty_container or only_same_children:
                tag.unwrap()

        return str(soup)
    
    def standardize_url(self, url) -> str:
        """Standardize URLs by adding/modifying protocol and path"""

        f = furl(url)

        # Standardize to http
        if f.scheme != 'http':
            f.scheme = 'http'

        if not f.path:
            f.path = '/'

        return f.url



