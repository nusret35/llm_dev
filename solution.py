from summarization_pipeline.pdf_section_extractor import extract_pdf_and_divide_sections
from summarization_pipeline.image_processing import extract_image_title_pairs, extract_titles_from_page, convert_response_to_dict, get_important_image_paths
from summarization_pipeline.greenness_slider import configure_models
from message_types import AllProcessess,Message, Process, ProcessCompleted, ErrorMessage
import fitz
import re
import asyncio


# Personalizing prompts by integrating user persona and purpose
'''
Describe Your Occupation:
-Academic Researcher
-Business Professional
-Student
-Entrepreneur
-Other (Please specify)
'''
'''
Where Will You Use These Insights?
-Academic Research
-Business Strategy Development
-Personal Knowledge Enhancement
-Educational Purposes
-Other (Please specify)
'''

# Regeneration of Extracted Insights Feature
'''
Title: Reason for Requesting Regeneration of Extracted Insights

Please let us know why you're requesting a regeneration of the insights extracted from the scholarly article. Your feedback is valuable in helping us improve. Select the option that best describes your reason:

1) Too short – The insights didn't provide enough detail.
2) Too long – The insights were more detailed than necessary, making it hard to extract useful information.
3) Too broad – The insights were not specific enough to the topic of interest.
4) Not actionable – The insights didn't provide clear next steps or actionable information.
5) Lacked depth or complexity – The insights did not delve deeply into the topic or missed critical nuances.
6) Other – Please specify.

If you choose "Other," kindly provide a brief description of your reason. This will help us better understand your needs and enhance our service.
'''

class Solution:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.greenness_input = 0.5
        self.extractor_70B_model, self.extractor_13B_model, self.max_tokens = configure_models(self.greenness_input)

    def preprocess_insights(self, insights):
        # Find the position of the last dot in the string
        last_dot_position = insights.rfind('.')

        # Check if the last two characters of the string are in the format "number."
        if (
            last_dot_position != -1
            and insights[last_dot_position - 2].isdigit()
            and insights[last_dot_position -1] == '.'
        ):
            insights = insights[:last_dot_position - 1]  # Include the dot before the number
        else:
            insights = insights[:last_dot_position + 1]

        # New preprocessing step to remove remaining "number." at the last line
        insights = re.sub(r'\s\d+\.\s*$', '', insights)

        # Check for a single '*' character at the last line and delete it if found
        if insights.rstrip().endswith('*'):
            insights = re.sub(r'\*\s*$', '', insights)

        insights = insights + "\n"

        return insights
    

    def preprocess_image_exp(self, explanations):
        # Find the position of the last dot in the string
        last_dot_position = explanations.rfind('.')

        # Check if the last two characters of the string are in the format "number."
        if (
            last_dot_position != -1
            and explanations[last_dot_position - 2].isdigit()
            and explanations[last_dot_position -1] == '.'
        ):
            return explanations[:last_dot_position - 1]  # Include the dot before the number
        else:
            return explanations[:last_dot_position + 1]


    def preprocess_title(self, title):
        start_pos = title.find('"')
        end_pos = title.rfind('"')
        return title[start_pos:end_pos]
    

    def generate_summary(self):
        # Getting and preprocessing PDF input
        sections_dict = extract_pdf_and_divide_sections(self.pdf_path)

       # Extracting section texts of important sections 
        abstract = sections_dict.get('abstract', "")
        print("Abstract: " + abstract + "\n")

        critical_sections = ["introduction", "conclusion", "discussion", "methodology"]

        critical_section_information = {}
        for section_name in critical_sections:
            critical_section_information[section_name] = sections_dict.get(section_name, "")

        """
        If at least two of the sections among "conclusion", "discussion", and "outcomes" are missing, 
        then take the last four sections (we keep each subsection seperately in the current formulation of sections_dict) 
        of the article (excluding keywords, acknowledgments, and references sections)
        """
        check_for_absence = ""
        critical_section_list = list(critical_section_information.items())
        for section_name, section_text in critical_section_list[-3:]:
            if section_text == "": check_for_absence += '0'

        if len(check_for_absence) >= 2:
            accepted = 0
            unwanted_sections = ["keywords", "acknowledgments", "references"]
            sections_list = list(sections_dict.items())
            for section_name, section_text in sections_list[::-1]: # Reverse iteration of the sections_list
                section_name = section_name.lower()
                section_text = sections_dict.get(section_name, "")
                if section_name not in unwanted_sections and section_text != "":
                    critical_section_information[section_name] = section_text
                    accepted += 1
                    if accepted >= 4:
                        break

        print("Important section titles:")
        for key, value in critical_section_information.items():
            print(key)

        # Summarizing important sections (using LLaMA 2 70B model)
        summarized_sections = {}
        for section_name, section_text in critical_section_information.items():
            if section_text != "":
                print("\nSummary is generated by LLaMA model...")
                summary = self.extractor_70B_model.summarize(section_name, section_text, self.max_tokens)
                summarized_sections[section_name] = summary
            else : summarized_sections[section_name] = None

        # Converting the section text information from dictionary to string
        # to feed it to the model as input
        def create_section_input(summarized_sections):
            # Initialize an empty string to store the formatted output
            section_input = ""

            # Iterate over each key-value pair in the dictionary
            for key, value in summarized_sections.items():
                if value != None:
                    # Append the key and value to the string with the specified format
                    section_input += f"{key}: {value} \n"

            return section_input

        section_input = create_section_input(summarized_sections)

        section_input_abstract = "abstract: " + abstract + section_input

        return section_input_abstract


    '''
    section_summary is provided as a string of summaries of the important sections of the article 
    '''
    def generate_insights(self, section_summary, user_persona, user_purpose, regeneration, reason_for_regeneration):
        # Extracting insights from the article using the summarized sections (using LLaMA 2 70B model)
        print("\nInsights are generated by LLaMA model...")
        insights = self.extractor_70B_model.extract_insights(section_summary, self.max_tokens, user_persona, user_purpose, regeneration, reason_for_regeneration)
        print("\nExtracted insights before processing:\n" + insights)

        insights = self.preprocess_insights(insights)
        print("\nExtracted insights after processing:\n\n\n" + insights)

        self.insights = insights

        return insights
    

    def generate_title(self, insights, user_persona, user_purpose):
        # Generating a meaningful title to be presented as the chat title in the interface (using LLaMA 2 13B model)
        title = self.extractor_70B_model.generate_title(insights, user_persona, user_purpose)
        print("\nTitle before preprocessing:\n" + title)

        #title = self.preprocess_title(title)
        #print("\nTitle after preprocessing:\n" + title)

        return title


    def generate_image_explanations(self, insights, user_persona, user_purpose):  
        # Choosing the most important figures/tables of the article (using LLaMA 2 13B model)
        # Open the file
        pdf_file = fitz.open(self.pdf_path)
        titles = []
        image_title_pairs = {}
        # Iterate over PDF pages
        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            page_image_title_pairs = extract_image_title_pairs(page,page_index)
            page_image_titles = extract_titles_from_page(page)
            image_title_pairs.update(page_image_title_pairs)
            for title in page_image_titles:
                title += " (Page:" + str(page_index+1) + ")"
                titles.append(title)

        pdf_file.close()

        image_titles = ""
        for title in titles:
            image_titles += title + "\n"
            
        important_images = self.extractor_13B_model.choose_images(insights, image_titles, user_persona, user_purpose)
        print("\nImportant images before processing:\n" + important_images)
        important_images = self.preprocess_image_exp(important_images)
        print("\nImportant images after processing:\n" + important_images)
        
        return important_images, image_title_pairs


    def display_images(self, important_images_explanation, image_title_pairs):
        # Displaying the fetched figures/tables that match the selected images
        important_images_explanation_list = convert_response_to_dict(important_images_explanation)
        
        # Check whether the important image is extracted
        found_images = get_important_image_paths(image_title_pairs, important_images_explanation_list)
    
        return found_images
    

    async def solution_pipeline_debug(self, send_message=None):
        if send_message:
            await send_message(AllProcessess('Generating section summaries,Generating insights,Generating title,Extracting images'))

        if send_message:
            await send_message(Process("Generating section summaries"))

        if send_message:
            await send_message(ProcessCompleted("Generating section summaries"))
            await send_message(Process("Generating insights"))

        if send_message:
            await send_message(ProcessCompleted("Generating insights"))
            await send_message(Process("Generating title"))
    
        if send_message:
            await send_message(ProcessCompleted("Generating title"))
            await send_message(Process("Extracting images"))

        if send_message:
            await send_message(ProcessCompleted("Extracting images"))

        title = "Navigating Digital Servitization: Choosing the Right Revenue Model for Your Business"

        insights = '''
                Key Insights:

                1. Manufacturing companies face challenges in choosing appropriate revenue models for their digital services, which can hinder their digital servitization transition.
                2. Customer digital readiness, digital service sophistication, and digital ecosystem partnerships are key factors that influence the choice of revenue models.
                3. Companies need to understand the nature and characteristics of different revenue models, such as subscription, usage-based, and performance-based models, and choose the ones that align with their business models.
                4. The choice of revenue model must consider the customer's digital awareness, value co-creation, and contractual arrangements for digital services.
                5. Digital service orientation and the type of data integration required also play a crucial role in selecting a suitable revenue model.
                6. Performance-based revenue models are commonly used for advanced digital services that incorporate expertise into data integration and analytics.
                7. Collaboration between ecosystem actors is essential to deliver seamless digital services, and data sharing and security are critical factors that enable focal companies to position components of digital services across various actors.
                8. Co-development of digital services with ecosystem partners is essential to leverage resources and skills and provide connected digital services.
        '''

        found_images = {'Fig. 2. Framework for the choice of revenue models for digital services': './images/page9/output_image0.png'}
        
        return title, insights, found_images


    async def solution_pipeline(self, send_message=None):
        if send_message:
            await send_message(AllProcessess('Generating section summaries,Generating insights,Generating title,Extracting images'))
    
        # Regeneration of Extracted Insights Option
        regeneration = 1 # if regeneration is requested by the user
        reason_for_regeneration = ""
        if regeneration:
            reason_for_regeneration = "Not actionable – The insights didn't provide clear next steps or actionable information."

        # Get user persona
        user_persona =  "Business Professional"

        # Get user's purpose for getting these insights
        user_purpose = "Business Strategy Development"

        if send_message:
            await send_message(Process("Generating section summaries"))

        section_summaries = self.generate_summary()

        if send_message:
            await send_message(ProcessCompleted("Generating section summaries"))
            await send_message(Process("Generating insights"))

        # Insights extraction and title generation steps are equipped with advanced prompt engineering
        # Prompts are made unique based on user persona and user's purpose for using the insights
        insights = self.generate_insights(section_summaries, user_persona, user_purpose, regeneration, reason_for_regeneration)

        if send_message:
            await send_message(ProcessCompleted("Generating insights"))
            await send_message(Process("Generating title"))
            
        title = self.generate_title(insights, user_persona, user_purpose)
        
        if send_message:
            await send_message(Process("Extracting images"))
            await send_message(ProcessCompleted("Generating title"))
        
        important_images_explanation, image_title_pairs = self.generate_image_explanations(insights, user_persona, user_purpose)
        found_images = self.display_images(important_images_explanation, image_title_pairs)

        if send_message:
            await send_message(ProcessCompleted("Extracting images"))

        self.extractor_13B_model.close()
        self.extractor_70B_model.close()

        return title, insights, found_images



if __name__ == "__main__":
    # Specify the path to the example PDF file
    #example_pdf_path = "/Users/nusretkizilaslan/Desktop/AIProject/llm_dev/buss_article.pdf"
    example_pdf_path = "/Users/selinceydeli/Desktop/AIResearch/llm_dev/buss_article.pdf"

    # Create an instance of the Solution class with the example PDF path
    solution_instance = Solution(example_pdf_path)

    # Run the solution_pipeline method
    title, insights, found_images = asyncio.get_event_loop().run_until_complete( solution_instance.solution_pipeline() )

    # Below is for testing important images match functionality
    important_images = '''
    Based on the given information, the most important images for business strategy development by a business professional are:

    1. Fig. 1. Overview of the Research Method (Page:4): This image provides an overview of the research methodology used in the study, which can help business professionals understand the foundation of the findings and their applicability to real-world scenarios.
    2. Fig. 3. Relationship Marketing (RM) Strategies Matrix (Page:11): This image presents a clear and concise matrix that highlights the three key RM mechanisms and their configuration during economic crises and recoveries. This matrix can serve as a valuable tool for business professionals to develop effective relationship marketing strategies.
    3. Table 7. Mechanisms for Successful Relationship Management of a Business Cycle (BC) (Page:9): This table summarizes the mechanisms for successful relationship management during different stages of a business cycle. By understanding these mechanisms, business professionals can better navigate economic fluctuations and make informed decisions about their marketing strategies.

    These images provide actionable insights and practical tools for business professionals to improve their performance and mitigate the financial impact of economic downturns.
    '''

    image_title_pairs = {'Fig. 1. Overview of the Research Method': './images/page4/output_image0.png', 'Fig. 3. Relationship Marketing (RM) Strategies Matrix': './images/page11/output_image0.png'}

    #solution_instance.display_images(important_images,image_title_pairs)
