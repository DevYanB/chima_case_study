from flask import Flask, request, jsonify
import transformers
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Flask app setup
app = Flask(__name__)


# Basic shit to init the model and tokenizer direct
# model_name = "daryl149/llama-2-7b-chat-hf"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# # model = AutoModelForCausalLM.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(
#     model_name, device_map="auto", offload_folder="offload", offload_state_dict = True, torch_dtype=torch.float16
# )
# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model,
#     torch_dtype=torch.float16,
#     device_map="auto",
# )


def llama_2_model(data):
    # sequences = pipeline(
    #     data,
    #     do_sample=True,
    #     top_k=10,
    #     num_return_sequences=1,
    #     eos_token_id=tokenizer.eos_token_id,
    #     max_length=200,
    # )
    # for seq in sequences:
    #     print(f"Result: {seq['generated_text']}")
    return f"Model output for: {data}"

@app.route('/')
def index():
    return "Welcome to Llama 2 AI Model API!"

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from POST request
    data = request.json.get('data')
    
    # Pass data to the model and get the result
    result = llama_2_model(data)
    
    # Return the result
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
