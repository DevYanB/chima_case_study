from flask import Flask, request, jsonify
import transformers
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import requests
from flask_cors import CORS

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

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# LLAMA2_MODEL_URL = "https://avdizq4m0s7moy4d.us-east-1.aws.endpoints.huggingface.cloud"
LLAMA2_MODEL_URL = "https://eb0cex2kcbk94qi5.us-east-1.aws.endpoints.huggingface.cloud"

headers = {
	"Authorization": "Bearer wbSiYmyZFBAcLEMgFIGGIDRvtMAZDIbkvNSgPlKzrIIucGwHfSGeblMJdGJYRLDtsvOZuCRxTavrauchfgLXQsdYKxarfWFVQEpbaNvUThlvGSkBetigQvLtxrUSPzSd",
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
    # NOTE THIS IS FUCKING HELL 3 API CALLS FOR ONE QUERY
    # TODO: Refine prompt engineering and model should generate more efficiently after AWS. will do after i get deployed on AWS tho
    # Another fix would be fine-tuning, see part 3 of the coding assignment
    for i in range(3):
        # Pass data to the model and get the result
        # result = query({
        #     "inputs": instruction,
        #     "parameters": {
        #         "repetition_penalty": 4.0,
        #         "max_new_tokens": 20
        #     }
        # })
        # results.append(result[0]['generated_text'])
        results.append("Garbage " + str(i))

    print(results)
    return jsonify({'sentences': results})

if __name__ == "__main__":
    app.run(debug=True)
