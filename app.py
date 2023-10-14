from flask import Flask, request, jsonify
import transformers
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import requests

# Flask app setup
app = Flask(__name__)

headers = {
	"Authorization": "Bearer wbSiYmyZFBAcLEMgFIGGIDRvtMAZDIbkvNSgPlKzrIIucGwHfSGeblMJdGJYRLDtsvOZuCRxTavrauchfgLXQsdYKxarfWFVQEpbaNvUThlvGSkBetigQvLtxrUSPzSd",
	"Content-Type": "application/json"
}


def query(payload):
    response = requests.post("https://ng8bhe1yz4nw8gsv.us-east-1.aws.endpoints.huggingface.cloud", headers=headers, json=payload)
    return response.json()


@app.route('/')
def index():
    return "Welcome to Llama 2 AI Model API!"

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from POST request
    data = request.json.get('data')
    
    # Based on data of response, we will formulate this instrction differently.
    # String proc, prompt engineering, then updating parameters too:
        # Create a sophisticated user interface where they not only input keywords 
        # but also adjust AI parameters like creativity level, tone (e.g., formal, casual),
        # and style (e.g., humorous, direct)

    instruction = f""

    # Pass data to the model and get the result
    result = query({
        "inputs": data,
        "parameters": {"max_new_tokens": 150},
    })
    
    # Return the result
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
