from flask import Flask, request, jsonify
from QuestionGenerator import WebsiteQuestionGenerator
import os
from dotenv import load_dotenv
import redis
from backend.RedisCache import APICache 

# Load env variables
path_to_env = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(path_to_env)

# Create cache 
cache_client = redis.Redis(host='localhost', port=6379, db=0)
cache = APICache(cache_client)

# Create question generator
generator = WebsiteQuestionGenerator(cache_client, os.getenv("NIM_KEY"))

app = Flask(__name__)

# Serve endpoint
@app.route('/api/questions', methods = ['GET'])
def send_survey_questions():
    """Serve survey questions to frontend"""

    url = request.args.get('url')
    print('Received request for:', url)

    if url is not None:
        answer = generator.get_questions_for_site(url)
        print('Sending:', answer)
        return jsonify(answer)

    return jsonify(response='No URL passed')
    
if __name__ == '__main__':
    app.run(debug=True)