# TODO's:
- Llama2 hosting through AWS Sagemaker
    - Blocked by API endpoint request for hosting, will be working on implementations after
    - Sample of what this code may look like can be found in deploy_model.py
- Appllication deployment and security, scaling, and resilience features needed
    - Blocked by Docker frontend issues
    - Blocked by AWS sagemaker role enablement
- Application payment
    - Did not research
- LLlama2-specific prompt engineering
    - This would require refinid the existing promt (see prompt template) giventhe meta/llama2 model needed.

# Fine-tuning
The fine-tuning process would be relatively straightforward once the Sagemaker instance of the model was deployed on a notebook. For several open source models of llama2, we can run data-proc on our feedback files, using the original prompt with keywords and the ranking (in this case thumbs up ie like or thumbs down ie dislike) to begin the fitting process of the model to fine tune the os model.

This would require a notebook instance to periodically run, implementing the following type of flow for text-gen, for example. One way I would likely do this is top expose this functionality on sagemaker and design a basic API to prompt this run on my own running flask server: https://huggingface.co/daryl149/llama-2-7b-chat-hf?sagemaker_train=true

This would also allow me to pass the feedback data to the API. Of course, if deployed to a container running on an EC2 instance, I could simply use a bucket to store said feedback or smth and poll when this process was initiated. Some data proc would need to be done, which can be as straightforward as mapping keywords and creativity, style, and tone to liked and non-liked variants.

# Errors List

This will contain a summary of the errors and problems I am running into as I get to them 
with a tag relating what area of errors this one applies to. Here's the potential tags:

[A]Challenges related specifically to integrating and fine-tuning the generative AI
[B]Considerations for handling large-scale user interactions with the AI model
[C]Proposals for leveraging user feedback for continuous AI improvement

I will also make a not of if they're fixed or not and, if there is a fix, will update
the solution underneath it.


[A] __Inability to get access to meta-llama/Llama-2-7b__
Okay, this one is a bit annoying. Huggingface makes it super easy to use their in-built transformers class to call their models. BUT, meta won't give me access until 1-2 days, which I probably don't have time for. So, my temporary fix is to simply use a different, maybe more janky, open-source model and embed it here.

The one I'm using: [daryl149/llama-2-7b-chat-hf](https://huggingface.co/daryl149/llama-2-7b-chat-hf) (praise him lol)

[A] __How to set this up to allow for param adjust on the fly__
Yeah, so I'm debating using either the in-built pipeline in huggingface or just loading the models direct. Rn, imma do pipeline since it's easier and more efficient to spin up, but if it ends up not scaling well I might have to switch it up. If I do need to switch it up, I'll start with these 2:
1. https://stackoverflow.com/questions/76051807/automodelforcausallm-for-extracting-text-embeddings
2. https://huggingface.co/docs/transformers/quicktour
___NOTE___, link 2 could also be useful for the implementing or designing the feedback based fine-tuning and saving process

[A] __Issues with one potential solution model__

Had some issues getting daryl149 model running locally, had to `pip install accelerate` and had to follow this tutorial :https://huggingface.co/blog/accelerate-large-models
In the end, this is showing me it might be really inefficient without meta's llama2 to try and get this working local at all. So, I'm gonna deploy this model to Sagemaker and see if that helps fix some issues with the two factors and, if not, welp let's see what happens.

[A] __Issue with using an async endpoint in sagemaker:__ https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference-create-invoke-update-delete.html to allow it to run efficiently and scale better

[A] __My instance type didn't support the model I found__
botocore.errorfactory.ResourceLimitExceeded: An error occurred (ResourceLimitExceeded) when calling the CreateEndpoint operation: The account-level service limit 'ml.g5.2xlarge for endpoint usage' is 0 Instances, with current utilization of 0 
This is because, well, I haven't allocated this resource yet...
While waiting for that, I'm gonna try inference endpoints on huggingface itself
__NOTE__: Inference Endpoint for this particular model is PRICEY, 1.6 an HOUR. Not worth it for ANY scaling purposes.

[A] __Need to setup ml.g5.2xlarge for endpoint__ AND training if I eventually want to be able to run fine-tuning on this deployment of AWS Sagemaker as well. This is needed for [decapoda-research/llama-7b-hf](https://huggingface.co/decapoda-research/llama-7b-hf) too, which I'm gonna try to use instead of the previous one since this is just basic ass text gen.

[B] This is the main one. I wasn't able to implement pipelining or sequencing through huggingface for the open sourced models. Additionally, I needed to acquisition particular resources for async endpoints for the deployed model on sagemaker, which would make this much more scalable: 
https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html
https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html

[C] This step was blocked by the AWS sagemaker allocation

# NEXT STEPS
I need to end-to-end test the feedback loop and do some data proc before storing
I need to enable message queueing and load balancing on a deployed version of the backend
I need to fix the dockerization of the frontend and ensure end-to-end works
I need to integrate payment loop
I also need to integrate more security features agains promt injection, as well as sustainability and cleanliness with inputs from frontend
Lastly, I need to deploy the Llama2 meta model to sagemaker (blocked by my waiting on both meta approval and on AWS allocation for model size)
