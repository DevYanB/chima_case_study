#NOTE: TO BE RUN IN SAGEMAKER NOTEBOOK ONLY

import json
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri

try:
	role = sagemaker.get_execution_role()
except ValueError:
	iam = boto3.client('iam')
	role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']

# Hub Model configuration. https://huggingface.co/models
hub = {
	'HF_MODEL_ID':'daryl149/llama-2-7b-chat-hf',
	'SM_NUM_GPUS': json.dumps(1)
}

huggingface_model = HuggingFaceModel(
	image_uri=get_huggingface_llm_image_uri("huggingface",version="1.1.0"),
	env=hub,
	role=role, 
)

# This is the deploy step; allocating the instance_type is what took me too long.
predictor = huggingface_model.deploy(
	initial_instance_count=1,
	instance_type="ml.g5.2xlarge",
	container_startup_health_check_timeout=300,
  )
  
# Sample request send
predictor.predict({
	"inputs": "My name is Julien and I like to",
})