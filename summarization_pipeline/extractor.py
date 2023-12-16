import replicate
import os

class Extractor:

    def send_prompt(self, prompt, sys_prompt):
        rp_client = replicate.Client(api_token='r8_6sb3qvFAQAmMLpoRSoIXUvUKkQ3Wjbq3UsxLe')
        output = rp_client.run(
            "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": prompt,
            "temperature": 0.75,
            "system_prompt": sys_prompt,
            "max_new_tokens": 1000,
            "min_new_tokens": -1
        })
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
        return output
    
    
    """
    Method for sending prompt to the LLaMA 2 70B model to
    enrich the abstract given the section texts and abstract
    """
    def enrich_abstract(self, sections, abstract):
        enrich_sys_prompt = 'Using the section texts you are given, enlarge the abstract to get a longer and more comprehensive summary of the article. While enlarging the abstract, integrate key information, findings, and implications from the given sections. Avoid any repetition of information.'
        prompt = "Section texts: " + sections + "Abstract: " + abstract + "Enriched abstract: "
        output = self.send_prompt(prompt, enrich_sys_prompt)
        return output

    """
    Method for sending prompt to the LLaMA 2 70B model to
    extract insights from an article given the important article sections
    """
    def extract_insights(self, input):
        insights_sys_prompt = 'You are a tool that extracts key insights from an article. You will be provided with article sections. As an output, you should provide concise insights about the given article in bulletpoints.'
        prompt = input
        output = self.send_prompt(prompt, insights_sys_prompt)
        return output

    """
    Method for sending prompt to the LLaMA 2 70B model to
    generate a title for the chat interface given the extracted insights
    """
    def generate_title(self, insights):
        find_title_sys_prompt = "From the given insights, provide a title."
        prompt = "Extracted insights: " + insights + "Title: "
        output = self.send_prompt(prompt, find_title_sys_prompt)
        return output

    """
    Method for sending prompt to the LLaMA 2 70B model to
    choose the most important images in an article given the image titles
    """
    def choose_images(self, insights, image_titles):
        choose_images_sys_prompt = "Given the image titles, choose the most important 3 images of the article based on the insights extracted from the article. Output should be in the following format: Image title (Page: Page number) - Explanation"
        prompt = "Extracted insights: " + insights + "Image titles: " + image_titles + "Important sections: "
        output = self.send_prompt(prompt, choose_images_sys_prompt)
        return output