from flask import Flask, request, jsonify
import transformers
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import requests
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


creativity_map = {
    0: "Not Creative",
    1: "Slightly Creative",
    2: "Moderately Creative",
    3: "Quite Creative",
    4: "Very Creative",
}

tone_map = {
    0: "Formal",
    1: "Slightly Formal",
    2: "Neutral",
    3: "Slightly Casual",
    4: "Casual",
}

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_URI']
inference_header = "Bearer "+ os.environ['INFERENCE_TOKEN']
print(os.environ['POSTGRES_URI'] )
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

print("setting up")

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String, nullable=False)
    creativity_level = db.Column(db.Integer, nullable=False)
    tone = db.Column(db.Integer, nullable=False)
    style = db.Column(db.String, nullable=False)
    keywords = db.Column(db.String, nullable=False)
    feedback = db.Column(db.String, nullable=False)



LLAMA2_MODEL_URL = os.environ['LLAMA2_URL']

headers = {
	"Authorization": inference_header,
	"Content-Type": "application/json"
}


def query(payload):
    response = requests.post(LLAMA2_MODEL_URL, headers=headers, json=payload)
    return response.json()

def generate_prompt(creativityLevel,tone,style,keywords):
    instruction_template = """
        <s>[INST] <<SYS>>
        You are a system designed to come up with one-sentence slogans.
        The slogans you generate must be {} and {} in tone, while still being {}.
        Given the keywords, generate 1 unique sample slogan while keeping the above rules for slogans in mind.
        <</SYS>>
        Keywords: {}

    """
    return instruction_template.format(creativityLevel,tone,style,keywords)

@app.route('/')
def index():
    return "Welcome to Llama 2 AI Model API!"

# Method for evaluating and getting all feedback entries
@app.route('/feedback/entries', methods=['GET'])
def get_all_entries():
    entries = Feedback.query.all()
    output = []

    for entry in entries:
        entry_data = {
            'id': entry.id,
            'sentence': entry.sentence,
            'creativity_level': entry.creativity_level,
            'tone': entry.tone,
            'style': entry.style,
            'keywords': entry.keywords,
            'feedback': entry.feedback
        }
        output.append(entry_data)

    return jsonify(output)

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    data = request.json

    # Generating a feedback entry from the defined class above with
    # all relevant meta-data
    feedback_entry = Feedback(
        sentence=data['sentence'],
        creativity_level=data['creativityLevel'],
        tone=data['tone'],
        style=data['style'],
        keywords=data['keywords'],
        feedback=data['feedback']
    )
    
    db.session.add(feedback_entry)
    db.session.commit()

    return jsonify({"message": "Feedback saved successfully!"})

@app.route('/generate', methods=['POST'])
def generate():
    print(request.json)

    # Structure:
    # {'creativityLevel': 2, 'tone': 2, 'style': 'direct', 'keywords': ''}
    creativityLevel = creativity_map[request.json.get('creativityLevel')]
    tone = tone_map[request.json.get('tone')]
    style = request.json.get('style')
    keywords = request.json.get('keywords')

    if not keywords:
        return jsonify({'sentences': ["INVALID KEYWORDS"]})
    
    # Based on data of response, we will formulate this instrction differently.
    # String proc, prompt engineering, then updating parameters too:
        # Create a sophisticated user interface where they not only input keywords 
        # but also adjust AI parameters like creativity level, tone (e.g., formal, casual),
        # and style (e.g., humorous, direct)
    # NOTE: As is right now, I'm doing glorified prompt engineering with these things.
    # In the future, I might map some of these to temperature, top_k, etc... but for now
    # prompt engineering it is lolol
    instruction = generate_prompt(creativityLevel,tone,style,keywords)
    print(instruction)

    results = []
    # Having to loop cause prompt gens are a bit wonky but 
    # NOTE THIS IS BAD: 3 API CALLS FOR ONE QUERY
    # TODO: Refine prompt engineering and model should generate more efficiently after AWS. will do after i get deployed on AWS tho
    # Another fix would be fine-tuning, see part 3 of the coding assignment

    # This is needed to vary up some generated responses
    temp_list = [0.2,0.5,1.0]
    for i in range(3):
        result = query({
            "inputs": instruction,
            "parameters": {
                "repetition_penalty": 4.0,
                "max_new_tokens": 20,
                "temperature": temp_list[i]
            }
        })
        results.append(result[0]['generated_text'])

    print(results)
    return jsonify({'sentences': results})

if __name__ == '__main__':
    print("FUCK")
    app.run(host='0.0.0.0')
