from dotenv import load_dotenv
import os
from NvidiaLLM import NvidiaLLM
from Scraper import WebsiteScraper

class WebsiteQuestionGenerator:

    def __init__(self, LLM_API_KEY):

        self.NvidiaLLM = NvidiaLLM(LLM_API_KEY)
        self.scraper = WebsiteScraper()
        
    def get_questions_for_site(self, site):

        website_data = self.scraper.get_website_data(site)

        prompt_head= """Given the following array where each element is data from a particular webpage all on the same domain,  
                        and each element's data includes a webpage title and counts of the most common words in the headers and paragraphs, 
                        infer what the purpose of the website is and create one multiple choice survey question with 4 answers which 
                        you would ask to a user to gauge their interest in the content."""
        prompt_body = str(website_data)
        prompt_tail = 'Do not reference the website by name, do not include any text formatting and respond with only one question and nothing else.'
        
        prompt = prompt_head + '\n' + prompt_body + '\n' + prompt_tail
        
        llm_response = self.NvidiaLLM.get_LLM_response(prompt)
        
        return llm_response



api_key = os.getenv("NIM_KEY")
chatBot = NvidiaLLM(api_key)
prompt = 'Tell me a one sentence joke about surveys'
response = chatBot.get_LLM_response(prompt)
print(response)

api_key = os.getenv("NIM_KEY")
generator = WebsiteQuestionGenerator(api_key)
answer = generator.get_questions_for_site('https://techcrunch.com')
print(answer)
