from flask import Flask, request, jsonify
from QuestionGenerator import WebsiteQuestionGenerator
import os
from dotenv import load_dotenv

path_to_env = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(path_to_env)
generator = WebsiteQuestionGenerator(os.getenv("NIM_KEY"))
app = Flask(__name__)

@app.route('/api/questions', methods = ['GET'])
def send_survey_questions():
    """Serve survey questions to frontend"""

    url = request.args.get('url')
    if url is not None:
        answer = generator.get_questions_for_site(url)
        print('Sending:', answer)
        return jsonify(answer)

    return jsonify(response='No URL passed')
    
if __name__ == '__main__':
    app.run(debug=True)