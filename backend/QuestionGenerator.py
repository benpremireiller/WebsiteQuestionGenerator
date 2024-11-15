import json
from NvidiaLLM import NvidiaLLM
from Scraper import WebsiteScraper
from functools import wraps


class WebsiteQuestionGenerator:


    def __init__(self, redis_cache, LLM_API_KEY):

        self.NvidiaLLM = NvidiaLLM(LLM_API_KEY)
        self.scraper = WebsiteScraper()
        self.cache = redis_cache

    def cache_decorator(method):
        """Create a wrapper that applies the cache decorator to get_questions_for_site"""

        @wraps(method)
        def wrapped(self, *args, **kwargs):
            
            cached_method = self.cache.cache_response(method)
            return cached_method(self, *args, **kwargs)
        
        return wrapped
    
    @cache_decorator    
    def get_questions_for_site(self, site, question_count=2) -> json:
        """Return n survey questions for the provided website"""

        # Scrape content from website
        website_data = self.scraper.get_website_data(site)

        # Define prompt
        context = 'You are an expert marketing researcher'

        prompt_head= "Given the following array where each element is data from a particular webpage all on the same domain, " +\
                     "infer what the purpose of the website is and create " + str(question_count) + " multiple choice " +\
                     "question(s) with 4 answers which you would ask a user to help classify their intent for visiting the website." +\
                     "The questions should be straightforward and user-friendly, aiming to uncover the user’s intent, such as seeking " +\
                     "information, making a purchase, contacting support, or any other primary actions the website supports."
        prompt_body = str(website_data)
        prompt_tail = 'Respond with ONLY question(s) in the following JSON format: '+\
                      '[{question_text: question_you_devised, response_type: multiple_choice, options: [option1, option2, option3, option4]}]. '+\
                      'Ensure to format your response so a JSON encoder will be able to parse it.'

        prompt = prompt_head + '\n' + prompt_body + '\n' + prompt_tail
        
        # Generate questions from LLM
        llm_response = self.NvidiaLLM.get_LLM_response(context, prompt)

        return json.loads(llm_response)



