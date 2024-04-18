import os.path
import json
from dotenv import load_dotenv
from langchain.llms import Replicate
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from .article_parser import shorten_text
from datetime import datetime
import time

class LLMModel():
    def __init__(self):
        pass

    def to_serializable(self):
        return self.__str__()
    
class LLAMA2(LLMModel):
    def __init__(self):
        pass

class LLAMA2_70B(LLAMA2):
    def __init__(self):
        pass

    def __str__(self):
        return "meta/llama-2-70b-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48"

class LLAMA2_13B(LLAMA2):
    def __init__(self):
        pass
    
    def __str__(self):
        return "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d"

class GPT(LLMModel):
    def __init__(self):
        pass
    
class GPT3_5(GPT):
    def __init__(self):
        pass

    def __str__(self):
        return "gpt-3.5-turbo"
    
class GPT4(GPT):
    def __init__(self):
        pass
    
    def __str__(self):
        return "gpt-4-turbo"
        

class Langchain_Extractor:
    def __init__(self, model:LLMModel, top_p=0.95, temperature=0.5, max_new_tokens=500, min_new_tokens=-1, repetition_penalty=1.15):
        self.model = model
        self.top_p = top_p
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        self.min_new_tokens = min_new_tokens
        self.repetition_penalty = repetition_penalty
        self.time = 0.0

        self.log = {
            'model':model.to_serializable(), # Store model as a serializable string
            'top_p':self.top_p,
            'temperature':self.temperature,
            'max_new_tokens':self.max_new_tokens,
            'min_new_tokens':self.min_new_tokens,
            'repetition_penalty':self.repetition_penalty
        }
        # Add a timestamp to the log
        self.log['timestamp'] = self.get_timestamp()
    

    def get_timestamp(self):
        # Generate a timestamp in the format "DD/MM/YYYY HH:MM"
        return datetime.now().strftime("%d/%m/%Y %H:%M")

        
    def send_prompt(self, prompt, max_new_token=500,callback=None):
        load_dotenv()
        llm = None
        if isinstance(self.model,LLAMA2):
            llm = Replicate(
                model=str(self.model),
                model_kwargs={"top_p": self.top_p, "max_tokens": max_new_token, "temperature": self.temperature, "min_new_tokens": self.min_new_tokens, "repetition_penalty": self.repetition_penalty}
            )
        elif isinstance(self.model,GPT):
            llm = LLMChain(llm=OpenAI(model=str(self.model)))

        assert llm != None
        
        start_time = time.perf_counter()
        response = llm(prompt)
        end_time = time.perf_counter()
        runtime = end_time - start_time
        self.time += runtime

        if callback:
            callback(response)

        return response
    
    
    def summarize(self, section_text):
        prompt = f"""
            Provide a summary of the text which is a section of an article. This is the section text:
            {section_text}
        """
        try :
            response = self.send_prompt(prompt)
        except:
            # Summary is too long. Exclude the last sentence
            shortened = shorten_text(section_text)

            # Recursively call the function until it fits the token size
            response = self.summarize(shortened)
        return response
    
    
    def generate_title(self, insights, user_persona, user_purpose, callback=None):
        max_new_token_for_title = 100
        prompt = f"""
            From the given insights,
            {insights}
            provide a title. Generate this title to be used for {user_purpose} by a/an {user_persona}.

            Output should be in the following format: 
            {{
                "title": "title string"
            }}
        """
        response = self.send_prompt(prompt, max_new_token=max_new_token_for_title, callback=callback)
        self.log['title'] = response
        return response
    
    
    def choose_images(self, insights, image_titles, user_persona, user_purpose):
        max_new_token_for_images = 500
        assert image_titles != ""
        prompt = f"""
            Choose the most important 3 images of the article using the image titles in the article and generated insights about the article. This is the image titles:
            {image_titles}
            
            This is the insights:
            {insights}

            Do not include any introductory sentence.

            Select these important images to be used for {user_purpose} by a/an {user_persona}.

            Give the descriptions of the selected images in the given JSON format. Always include the commas:
            {{
                "Fig./Table 1. Title": "string explanation",
                "Fig./Table 2. Title": "string explanation",
                "Fig./Table 3. Title": "string explanation"
            }}
        """
        response = self.send_prompt(prompt, max_new_token=max_new_token_for_images)
        self.log['image_selection'] = response
        return response
    

    def extract_insights(self, section_summaries, user_persona, user_purpose, regeneration, reason_for_regeneration, callback=None):
        max_new_token_for_insights = 500
        prompt = f"""
            Provide insights about the article from the given summaries for each section of the article. This is the section summaries:
            {section_summaries}

            Do not include any introductory sentence. Do not include incomplete sentences.

            Generate these insights to be used for {user_purpose} by a/an {user_persona}.

            Give the insights in the following format:

            * insight 1 
            * insight 2 
            * insight 3 
            * insight 4
            ...
        """
        #system_prompt = "You are a tool that generates insights."
        assert section_summaries != ""
        response = self.send_prompt(prompt, max_new_token=max_new_token_for_insights, callback=callback)
        self.log['extract_insights'] = response
        return response
    

    """
    Method for logging the model results to the logs.json file
    """
    def close(self):
        self.log['runtime (s)'] = self.time
        self.log['closing_timestamp'] = self.get_timestamp()
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../../greenness_test.json")

        # Read the existing JSON data from the file
        with open(path, 'r') as json_file:
            existing_data = json.load(json_file)

        # Append the new dictionary to the existing list
        existing_data.append(self.log)

        # Write the updated list back to the JSON file
        with open(path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)
