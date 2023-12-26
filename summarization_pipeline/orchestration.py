import replicate
import json
import time



# Greenness approach trial by changing the parameters of the model

class Extractor:
    def __init__(self,model,top_k=50,top_p=1.0,temperature=0.5,max_new_tokens=500):
        model_dict = {
            '70B':{'model':'meta/llama-2-70b-chat', 'version':'02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3'},
            '13B': {'model':'meta/llama-2-13b-chat','version':'f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d'}
        }
        self.top_k = top_k
        self.top_p = top_p
        self.time = 0.0
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        self.log = {
            'model':model,
            'top_k':self.top_k,
            'top_p':self.top_p,
            'temperature':self.temperature,
            'max_new_tokens':self.max_new_tokens
        }
        if model in model_dict:
            self.model = model_dict[model]
        else:
            self.model = model_dict['70B']

    def send_prompt(self, prompt, sys_prompt):
        rep = replicate.Client(api_token='r8_6sb3qvFAQAmMLpoRSoIXUvUKkQ3Wjbq3UsxLe')
        print('\nSending prompt...')
        model = rep.models.get(self.model['model'])
        version = model.versions.get(self.model['version'])
        prediction = rep.predictions.create( 
            
            version=version,input={
            "debug": False,
            "top_k": self.top_k, # reduced from 50
            "top_p": self.top_p, # reduced from 1
            "prompt": prompt,
            "temperature": self.temperature,
            "system_prompt": sys_prompt,
            "max_new_tokens": self.max_new_tokens, # reduced from 1000
            "min_new_tokens": -1
        })
        prediction.wait()
        output = prediction.output
        metrics = prediction.metrics
        print('Response received.')
        print(metrics)
        self.time += metrics['predict_time']
        response = ""
        for item in output:
            response += item
        return response

    # Below are the methods that are defined for processes within our pipeline 
    # that send prompt to LLaMA 2 70B model

    """
    Method for sending prompt to the LLaMA 2 70B model to
    summarize an article given the section names and section texts
    """
    def summarize(self, section_name, section_text):
        summarize_sys_prompt = 'You are a tool that summarizes the given text. The given text is a section of an article. Give a concise summary of the section text to include only the most important information.'
        prompt = section_name + ": " + section_text
        output = self.send_prompt(prompt, summarize_sys_prompt)
        self.log[f"summarize {section_name}"] = output
        return output
    
    """
    Method for sending prompt to the LLaMA 2 70B model to
    enrich the abstract given the section texts and abstract
    """
    def enrich_abstract(self, sections, abstract):
        enrich_sys_prompt = 'Using the section texts you are given, enlarge the abstract to get a longer and more comprehensive summary of the article. While enlarging the abstract, integrate key information, findings, and implications from the given sections. Avoid any repetition of information.'
        prompt = "Section texts: " + sections + "Abstract: " + abstract + "Enriched abstract: "
        output = self.send_prompt(prompt, enrich_sys_prompt)
        self.log["enrich abstract"] = output
        return output

    """
    Method for sending prompt to the LLaMA 2 70B model to
    extract insights from an article given the important article sections
    """
    def extract_insights(self, input):
        insights_sys_prompt = 'You are a tool that extracts key insights from an article. You will be provided with article sections. As an output, you should provide concise insights about the given article in bulletpoints.'
        prompt = input
        output = self.send_prompt(prompt, insights_sys_prompt)
        self.log['insights'] = output
        return output

    """s
    Method for sending prompt to the LLaMA 2 70B model to
    generate a title for the chat interface given the extracted insights
    """
    def generate_title(self, insights):
        find_title_sys_prompt = "From the given insights, provide a title. Output should be in the following format: Title. Just give one title."
        prompt = "Extracted insights: " + insights + "Title: "
        output = self.send_prompt(prompt, find_title_sys_prompt)
        self.log['generate title'] = output
        return output

    """
    Method for sending prompt to the LLaMA 2 70B model to
    choose the most important images in an article given the image titles
    """
    def choose_images(self, insights, image_titles):
        choose_images_sys_prompt = "Given the image titles, choose the most important 3 images of the article based on the insights extracted from the article. Output should be in the following format: Image title (Page: Page number) - Explanation"
        prompt = "Extracted insights: " + insights + "Image titles: " + image_titles + "Important sections: "
        output = self.send_prompt(prompt, choose_images_sys_prompt)
        self.log['choose images'] = output
        return output
    
    """
    Method for logging the model results to the logs.json file
    """
    def close(self):
        self.log['runtime (s)'] = self.time
        json_file_name = "logs_w_time.json"
        # Read the existing JSON data from the file
        with open(json_file_name, 'r') as json_file:
            existing_data = json.load(json_file)

        # Append the new dictionary to the existing list
        existing_data.append(self.log)
        print(self.log)

        # Write the updated list back to the JSON file
        with open(json_file_name, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)
        
        