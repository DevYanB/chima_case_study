from flask import Flask, request, jsonify
import transformers
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import requests

# Flask app setup
app = Flask(__name__)

LLAMA2_MODEL_URL = "https://avdizq4m0s7moy4d.us-east-1.aws.endpoints.huggingface.cloud"
# LLAMA2_MODEL_URL = "https://eb0cex2kcbk94qi5.us-east-1.aws.endpoints.huggingface.cloud"

headers = {
	"Authorization": "Bearer wbSiYmyZFBAcLEMgFIGGIDRvtMAZDIbkvNSgPlKzrIIucGwHfSGeblMJdGJYRLDtsvOZuCRxTavrauchfgLXQsdYKxarfWFVQEpbaNvUThlvGSkBetigQvLtxrUSPzSd",
	"Content-Type": "application/json"
}


def query(payload):
    response = requests.post(LLAMA2_MODEL_URL, headers=headers, json=payload)
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

    print(data)
    instruction = f""

    # Pass data to the model and get the result
    result = query({
        "inputs": data,
         "parameters": {
            "repetition_penalty": 4.0,
            "max_length": 128
        }
    })
    
    # Return the result
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
