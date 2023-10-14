from flask import Flask, request, jsonify
import transformers
# from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, AutoModel, pipeline
from ctransformers import AutoModelForCausalLM
import torch
import requests

# Flask app setup
app = Flask(__name__)

model_name = "TheBloke/Llama-2-7B-GGUF"
model = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7B-GGUF", model_file="llama-2-7b.q4_K_M.gguf", model_type="llama", gpu_layers=50)

def query_test():
    
    return(jsonify(""))

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
    result = query_test()
    
    # Return the result
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
