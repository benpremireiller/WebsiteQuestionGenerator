from dotenv import load_dotenv
import json
from NvidiaLLM import NvidiaLLM
from Scraper import WebsiteScraper

class WebsiteQuestionGenerator:

    def __init__(self, LLM_API_KEY):

        self.NvidiaLLM = NvidiaLLM(LLM_API_KEY)
        self.scraper = WebsiteScraper()
        
    def get_questions_for_site(self, site, question_count=2) -> json:
        """Return n survey questions for the provided website"""

        website_data = self.scraper.get_website_data(site)

        context = 'You are an expert marketing researcher'

        prompt_head= "Given the following array where each element is data from a particular webpage all on the same domain, " +\
                     "infer what the purpose of the website is and create " + str(question_count) + " multiple choice " +\
                     "question(s) with 4 answers which you would ask a user to help classify their intent for visiting the website." +\
                     "The questions should be straightforward and user-friendly, aiming to uncover the user’s intent, such as seeking " +\
                     "information, making a purchase, contacting support, or any other primary actions the website supports."
        prompt_body = str(website_data)
        prompt_tail = 'Respond with ONLY question(s) in the following JSON format: '+\
                      '[{question_text: question_you_devised, response_type: multiple_choice, options: [option1, option2, option3, option4]}]. '+\
                      'Do not include any special characters.'

        prompt = prompt_head + '\n' + prompt_body + '\n' + prompt_tail
        
        llm_response = self.NvidiaLLM.get_LLM_response(context, prompt)

        return json.loads(llm_response)



