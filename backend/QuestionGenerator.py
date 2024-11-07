from dotenv import load_dotenv
import json
from NvidiaLLM import NvidiaLLM
from Scraper import WebsiteScraper

class WebsiteQuestionGenerator:

    def __init__(self, LLM_API_KEY):

        self.NvidiaLLM = NvidiaLLM(LLM_API_KEY)
        self.scraper = WebsiteScraper()
        
    def get_questions_for_site(self, site, question_count=2):

        website_data = self.scraper.get_website_data(site)

        prompt_head= "Given the following array where each element is data from a particular webpage all on the same domain, " +\
                     "infer what the purpose of the website is and create " + str(question_count) + " multiple choice survey " +\
                     "question with 4 answers which you would ask to a user to engage their interest in the content."
        prompt_body = str(website_data)
        prompt_tail = 'Do not reference the website by name, do not include your reasoning and respond with only question(s) in the following JSON format '+\
                      '[{question_text: question_you_devised, response_type: multiple_choice, options: [option1, option2, option3, option4]}] and nothing else. '+\
                      'Keep your answers short and try to include specific facts, products or events you identified in the data.'
                      
        context = 'You are an expert survey researcher'

        prompt = prompt_head + '\n' + prompt_body + '\n' + prompt_tail
        
        llm_response = self.NvidiaLLM.get_LLM_response(context, prompt)
        
        return json.loads(llm_response)



