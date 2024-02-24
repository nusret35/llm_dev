import replicate
import json
import time
from datetime import datetime

# Greenness approach trial by changing the parameters of the model

class Extractor:
    def __init__(self, model,top_k=50, top_p=1.0, temperature=0.5, max_new_tokens=500):
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
        # Add a timestamp to the log
        self.log['timestamp'] = self.get_timestamp()
        if model in model_dict:
            self.model = model_dict[model]
        else:
            self.model = model_dict['70B']
    
    def get_timestamp(self):
        # Generate a timestamp in the format "DD/MM/YYYY HH:MM"
        return datetime.now().strftime("%d/%m/%Y %H:%M")

    def send_prompt(self, prompt, sys_prompt):

        rp_client = replicate.Client(api_token='r8_96G04GwgDPZDSpzHD9iP38oLQiy7cjJ0dz6RN')
        print('\nSending prompt...')

        model = rp_client.models.get(self.model['model'])
        version = model.versions.get(self.model['version'])
        prediction = rp_client.predictions.create( 
            version=version,input={
            "debug": False,
            "top_k": self.top_k, 
            "top_p": self.top_p, 
            "prompt": prompt,
            "temperature": self.temperature,
            "system_prompt": sys_prompt,
            "max_new_tokens": self.max_new_tokens, 
            "min_new_tokens": -1
        })
        prediction.wait()
        if prediction.error != None:
            print(f"Error occured: {prediction.error}")
        else:
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
    def summarize(self, section_name, section_text, max_tokens):
        summarize_sys_prompt = 'You are a tool that summarizes the given text. The given text is a section of an article. Give a concise summary of the section text to include only the most important information. Give the output using maximum of ' + str(int(4/3*max_tokens)) + ' words. The sentences should not be left unfinished.'
        prompt = section_name + ": " + section_text
        print("Summarization prompt\n" + summarize_sys_prompt + "\n")
        output = self.send_prompt(prompt, summarize_sys_prompt)
        self.log[f"summarize {section_name}"] = output
        return output
    
    """
    Method for sending prompt to the LLaMA 2 70B model to
    enrich the abstract given the section texts and abstract
    """
    def enrich_abstract(self, sections, abstract, max_tokens):
        enrich_sys_prompt = 'Using the section texts you are given, enlarge the abstract to get a longer and more comprehensive summary of the article. While enlarging the abstract, integrate key information, findings, and implications from the given sections. Avoid any repetition of information. Give the output using maximum of ' + str(int(4/3*max_tokens)) + ' words. The sentences should not be left unfinished.'
        prompt = "Section texts: " + sections + "Abstract: " + abstract + "Enriched abstract: "
        print("Abstract enrichment prompt\n" + enrich_sys_prompt + "\n")
        output = self.send_prompt(prompt, enrich_sys_prompt)
        self.log["enrich abstract"] = output
        return output

    """
    Method for sending prompt to the LLaMA 2 70B model to
    extract insights from an article given the important article sections
    In this method, prompt is made unique based on user persona and user's purpose for using the insights 
    """
    def extract_insights(self, input, max_tokens, user_persona, user_purpose, regeneration, reason_for_regeneration):
        insights_sys_prompt = 'You are a tool that extracts key insights from an article. You will be provided with article sections. As an output, you should provide concise insights about the given article in bulletpoints (ex. * Bulletpoint 1). Give the insights using maximum of ' + str(int(4/3*max_tokens)) + ' words. The sentences should not be left unfinished.'
        if regeneration:
            process_name = "insights extraction"
            new_insights_sys_prompt = self.prompt_regeneration(process_name, insights_sys_prompt, reason_for_regeneration)
            insights_sys_prompt = new_insights_sys_prompt
        prompt_unique_to_user = ' Generate these insights to be used for ' + user_purpose + ' by a/an ' + user_persona + '.'
        insights_sys_prompt += prompt_unique_to_user
        prompt = input
        print( "Insights extraction prompt\n" + insights_sys_prompt + "\n")
        output = self.send_prompt(prompt, insights_sys_prompt)
        self.log['insights'] = output
        return output

    """
    Method for sending prompt to the LLaMA 2 70B model to
    generate a title for the chat interface given the extracted insights
    In this method, prompt is made unique based on user persona and user's purpose for using the insights
    """
    def generate_title(self, insights, user_persona, user_purpose):
        find_title_sys_prompt = 'From the given insights, provide a title. Output should be in the following format: Title. Just give one title.'
        prompt_unique_to_user = ' Generate this title to be used for ' + user_purpose + ' by a/an ' + user_persona + '.'
        find_title_sys_prompt += prompt_unique_to_user
        prompt = "Extracted insights: " + insights + "Title: "
        print("Title generation prompt\n" + find_title_sys_prompt + "\n")
        output = self.send_prompt(prompt, find_title_sys_prompt)
        self.log['generate title'] = output
        return output

    """
    Method for sending prompt to the LLaMA 2 70B model to
    choose the most important images in an article given the image titles
    """
    def choose_images(self, insights, image_titles, user_persona, user_purpose):
        choose_images_sys_prompt = 'Based on the given information, choose the most important 3 images of the article. Specify the page that the image is located in the article like this: (Page: #number)'
        prompt_unique_to_user = ' Select these important images to be used for ' + user_purpose + ' by a/an ' + user_persona + '.'
        choose_images_sys_prompt += prompt_unique_to_user
        prompt = "Extracted insights: " + insights + "Image titles: " + image_titles + "Important sections: "
        print("Image selection prompt\n" + choose_images_sys_prompt + "\n")
        output = self.send_prompt(prompt, choose_images_sys_prompt)
        self.log['choose images'] = output
        return output
    
    """
    Method for generating a new prompt for the insights regeneration option
    Process_name signifies the name of the process for which the prompt is used (insights extraction or image selection)
    """
    def prompt_regeneration(self, process_name, original_prompt, user_problem):
        prompt_regeneration_sys_prompt = "Your role is a prompt generation tool. The process in question is named " + process_name + ". Modify the original prompt according to the problem identified as: " + user_problem + ". Do not give any example in the prompt. Keep it as short as possible."
        prompt = "Original prompt: " + original_prompt
        print("Prompt regeneration prompt\n" + prompt_regeneration_sys_prompt + "\n")
        output = self.send_prompt(prompt, prompt_regeneration_sys_prompt)
        return output
    

    def find_image_matches(self, important_images, image_title_pairs):
        find_images_sys_prompt = "Your task is to locate and return the exact image titles in the given important images that correspond to the key entries in the given image title pairs dictionary. Make sure to return the image name exactly as it appears in the key of the image title pairs dictionary."
        prompt = "Important images: " + important_images + ", Image title pairs: " + image_title_pairs
        output = self.send_prompt(prompt, find_images_sys_prompt)
        return output

    """
    Method for logging the model results to the logs.json file
    """
    def close(self):
        self.log['runtime (s)'] = self.time
        self.log['closing_timestamp'] = self.get_timestamp()
        json_file_name = "logs_w_time.json"
        # Read the existing JSON data from the file
        with open(json_file_name, 'r') as json_file:
            existing_data = json.load(json_file)

        # Append the new dictionary to the existing list
        existing_data.append(self.log)

        # Write the updated list back to the JSON file
        with open(json_file_name, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)
        
        