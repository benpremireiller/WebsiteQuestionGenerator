import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import spacy

nlp = spacy.load("en_core_web_sm")

class WebsiteScraper:

    def __init__(self):
        pass

    def get_website_data(self, home_page_url, page_limit = 7):
        
        content = []
        try:
            root_response = requests.get(home_page_url)
        except:
            raise Exception('Unable to retrieve data from: ' + home_page_url)
        
        root_soup = BeautifulSoup(root_response.text, 'html.parser')

        stripped_home_page_url = home_page_url[:-1] if home_page_url[-1] == '/' else home_page_url # Remove ending slash if exists
        
        # Get the first navigation page anchor tags on the site
        navs = root_soup.find('nav')
        href_urls = navs.find_all('a', attrs={"href": True}) if navs else [] 
        
        sites_to_scrape = [home_page_url] + [stripped_home_page_url + url.get('href') for url in href_urls] 
        
        already_scraped = set() # To avoid scraping the same site

        i = 0
        while i < min(page_limit, len(sites_to_scrape)): 
            site = sites_to_scrape[i]
            if site not in already_scraped:
                try:
                    site_data = self.scrape_url(site)
                except:
                    print('Scrape failed for site:', site)
                    i += 1
                    continue

                compressed_data = self.compress_site_data(site_data)
                content.append(compressed_data)
                already_scraped.add(site)
            i += 1

        return content


    def scrape_url(self, url):

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('title').get_text() if soup.find('title') else []
        headers = [h.get_text().replace('\n', '').replace('\t', '') for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])]
        paragraphs = [p.get_text().replace('\n', '').replace('\t', '') for p in soup.find_all('p')]
        # TODO Add text from <a> and maybe <div> tags

        output = {'title': title, 'headers': headers, 'paragraphs': paragraphs}

        return output

    def compress_site_data(self, site_data):

        title = site_data['title']
        headers = site_data['headers']
        paragraph_text = ' '.join(site_data['paragraphs'])
        
        compressed_paragraphs = self.get_most_frequent_words(paragraph_text, 50)

        compressed_site_data = {'title': title, 'headers': headers, 'paragraphs': compressed_paragraphs}

        return compressed_site_data


    def get_most_frequent_words(self, text, n):
        
        doc = nlp(text)

        focused_word_counts = defaultdict(int)
        POS_tags_to_keep = ['NOUN', 'VERB', 'PROPN']

        for token in doc:
            if token.pos_ in POS_tags_to_keep and not token.is_stop:
                focused_word_counts[token.lower_] += 1

        highest_n_occurences = sorted(focused_word_counts.items(), key=lambda x: x[1], reverse=True)[:min(n, len(focused_word_counts))]
        return highest_n_occurences




