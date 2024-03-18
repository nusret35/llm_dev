'''
from langchain.chat_models import ChatOpenAI
from langchain.llms import llamacpp

"""
    To use, you should have the llama-cpp-python library installed, and provide the
    path to the Llama model as a named parameter to the constructor.
    Check out: https://github.com/abetlen/llama-cpp-python

    Example:
        .. code-block:: python

            from langchain.llms import LlamaCpp
            llm = LlamaCpp(model_path="/path/to/llama/model")
"""

llama_adapter = llamacpp()
'''

import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Replicate

load_dotenv()

api_key = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = api_key

llm = Replicate(
    model="andreasjansson/llama-2-70b-chat-gguf:51b87745820e6a8de6ad7bceb340bb6ba85f7ba6dab8e02bb7e2de0853425f4c",
    model_kwargs={"top_k": 50, "top_p": 0.95, "max_tokens": 500, "temperature": 0.8},
)

prompt = """
Answer the question and explain: Can a dog drive a car?

Respond with json that adheres to the following jsonschema:

{jsonschema}
"""
response = llm(prompt)
print(response)