import requests
import json

class NvidiaLLM:

    def __init__(self, API_key, model = "nvidia/llama-3.1-nemotron-70b-instruct"):

        self.api_key = API_key
        self.url = 'https://integrate.api.nvidia.com/v1/chat/completions'
        self.model  = model

    def get_LLM_response(self, context, prompt) -> str:
        """Return a response from the LLM using context and a prompt"""
        
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "stream": False,
            "temperature": 0.8, # Higher 'creativity' seems to generate better responses
            "top_p": 1,
            "stop": None,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "seed": 0,
            "messages": [
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer " + self.api_key
        }

        try:
            http_response = requests.post(self.url, json=payload, headers=headers, timeout=30)
        except:
            raise Exception("No response from NIMs")
        
        if http_response.status_code == 200:
            json_content = json.loads(http_response.content.decode('utf-8'))
            LLM_response = json_content['choices'][0]['message']['content'].strip('"')
            return LLM_response
        
        raise Exception("HTTP response not OK")

