This will contain a summary of the errors and problems I am running into as I get to them 
with a tag relating what area of errors this one applies to. Here's the potential tags:

[A]Challenges related specifically to integrating and fine-tuning the generative AI
[B]Considerations for handling large-scale user interactions with the AI model
[C]Proposals for leveraging user feedback for continuous AI improvement

I will also make a not of if they're fixed or not and, if there is a fix, will update
the solution underneath it.


# Errors List

[A] __Inability to get access to meta-llama/Llama-2-7b__
Okay, this one is a bit annoying. Huggingface makes it super easy to use their in-built transformers class to call their models. BUT, meta won't give me access until 1-2 days, which I probably don't have time for. So, my temporary fix is to simply use a different, maybe more janky, open-source model and embed it here.

The one I'm using: [daryl149/llama-2-7b-chat-hf](https://huggingface.co/daryl149/llama-2-7b-chat-hf) (praise him lol)

[A] __How to set this up to allow for param adjust on the fly__
Yeah, so I'm debating using either the in-built pipeline in huggingface or just loading the models direct. Rn, imma do pipeline since it's easier and more efficient to spin up, but if it ends up not scaling well I might have to switch it up. If I do need to switch it up, I'll start with these 2:
1. https://stackoverflow.com/questions/76051807/automodelforcausallm-for-extracting-text-embeddings
2. https://huggingface.co/docs/transformers/quicktour
___NOTE___, link 2 could also be useful for the implementing or designing the feedback based fine-tuning and saving process

[A] Had some issues getting daryl149 model running locally, had to `pip install accelerate` and had to follow this tutorial:https://huggingface.co/blog/accelerate-large-models
In the end, this is showing me it might be really inefficient without meta's llama2 to try and get this working.