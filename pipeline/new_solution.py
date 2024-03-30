from summarization_pipeline.pdf_section_extractor import extract_pdf_and_divide_sections
from summarization_pipeline.image_processing import extract_image_title_pairs, extract_titles_from_page, convert_response_to_dict, get_important_image_paths
from summarization_pipeline.greenness_slider import configure_models
from fitz import Document, fitz
import logging
import ast

class NewSolution:
    def __init__(self, pdf_path=None, pdf_file_bytes=None):
        self.pdf_path = pdf_path
        self.pdf_file_bytes = pdf_file_bytes
        self.greenness_input = 0 # Corresponds to 500 max_new_tokens
        self.stream_generator_70B_model, self.stream_generator_13B_model, self.langchain_extractor_70B_model, self.langchain_extractor_13B_model, self.max_tokens = configure_models(self.greenness_input)

        if pdf_path == None and pdf_file_bytes == None:
            raise RuntimeError('No pdf_path or pdf_file is given as parameter.')
        elif pdf_path:
            self.pdf_file = fitz.open(pdf_path)
        else:
            self.pdf_file = Document(stream=self.pdf_file_bytes,filetype="pdf")


    def generate_summary(self):
        # Getting and preprocessing PDF input
        sections_dict = extract_pdf_and_divide_sections(self.pdf_file)

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
        logging.debug(f"{critical_section_information.items()}")
        for section_name, section_text in critical_section_information.items():
            if section_text != "":
                print("\nSummary is generated by LLaMA model...")
                summary = self.langchain_extractor_70B_model.summarize(section_text)
                print(summary)
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
    def generate_insights(self, section_summary, user_persona, user_purpose, regeneration, reason_for_regeneration,callback=None):
        # Extracting insights from the article using the summarized sections (using LLaMA 2 70B model)
        print("\nInsights are generated by LLaMA model...")
        insights = self.stream_generator_70B_model.extract_insights(section_summary, user_persona, user_purpose, regeneration, reason_for_regeneration,callback=callback)
        self.insights = insights
        return insights
    

    def generate_title(self, insights, user_persona, user_purpose,callback=None):
        # Generating a meaningful title to be presented as the chat title in the interface (using LLaMA 2 13B model)
        print("Title is generated by LLaMA model...")
        response = self.stream_generator_70B_model.generate_title(insights, user_persona, user_purpose,callback=callback)
        title_json = ast.literal_eval(response)
        
        return title_json["title"]


    def generate_image_explanations(self, insights, user_persona, user_purpose):
        def join_dictionaries(images_and_explanations, title_image_pairs):
            joined_dict = {}
            for title, explanation in images_and_explanations.items():
                if title in title_image_pairs:
                    image = title_image_pairs[title]
                    joined_dict[title] = {'explanation': explanation, 'image': image}
                else:
                    joined_dict[title] = {'explanation': explanation, 'image': None}
            return joined_dict
        
        # Choosing the most important figures/tables of the article (using LLaMA 2 13B model)
        # Open the file
        pdf_file = fitz.open(self.pdf_path)
        titles = []
        image_title_pairs = {}
        # Iterate over PDF pages
        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            page_image_title_pairs = extract_image_title_pairs(page, page_index)
            page_image_titles = extract_titles_from_page(page)
            image_title_pairs.update(page_image_title_pairs)
            for title in page_image_titles:
                title += " (Page:" + str(page_index+1) + ")"
                titles.append(title)
    
        image_titles = ""
        for title in titles:
            image_titles += title + "\n"
        
        print("\n\nImages are chosen by LLaMA model...")
        response_text = self.stream_generator_70B_model.choose_images(insights, image_titles, user_persona, user_purpose)
        important_images = ast.literal_eval(response_text)
        joined_dict = join_dictionaries(important_images,image_title_pairs)

        return joined_dict


    def display_images(self, important_images_explanation, image_title_pairs):
        # Displaying the fetched figures/tables that match the selected images
        important_images_explanation_list = convert_response_to_dict(important_images_explanation)

        # Check whether the important image is extracted
        found_images = get_important_image_paths(image_title_pairs, important_images_explanation_list)
    
        return found_images
    

    def solution_pipeline(self):
        # Regeneration of Extracted Insights Option
        regeneration = 0 # if regeneration is requested by the user
        reason_for_regeneration = ""
        if regeneration:
            reason_for_regeneration = "Not actionable – The insights didn't provide clear next steps or actionable information."

        # Get user persona
        user_persona =  "Business Professional"
        # Get user's purpose for getting these insights
        user_purpose = "Business Strategy Development"

        section_summaries = self.generate_summary()

        # Insights extraction and title generation steps are equipped with advanced prompt engineering
        # Prompts are made unique based on user persona and user's purpose for using the insights
        insights = self.generate_insights(section_summaries, user_persona, user_purpose, regeneration, reason_for_regeneration)
        print(insights,"\n")

        insights = """
            1) The article provides insights into how businesses can navigate economic downturns and recoveries by fostering communication, involvement, and value anticipation between buyers and sellers.

            2) The study identifies key relationship process mechanisms, including communication openness, technical involvement, and customer value anticipation, which have direct and indirect effects on supplier performance.

            3) The authors propose a 2x3 matrix with six quadrants, each representing a different combination of RM mechanisms that companies can use to achieve their goals during times of economic crisis and recovery.

            4) The article highlights the importance of considering forward-looking measures such as customer lifetime value when investing in relationships.

            5) The study extends the dark side of B2B relationships' theoretical underpinnings by showing how the inherent tension created in a BC can be managed by RM mechanisms.

            6) The findings offer directions for suppliers on how to leverage B2B relationships through a BC, and indicate that supplier’s performance is influenced differently by RM mechanisms during times of economic crisis versus times of recovery/expansion.

            7) The article addresses a gap in current research and provides valuable insights for firms operating in emerging economies, contributing to both RM and BC literature.
        """

        title = self.generate_title(insights, user_persona, user_purpose)
        print(title)
        important_images = self.generate_image_explanations(insights, user_persona, user_purpose)
        print(important_images)


if __name__ == "__main__":
    #solution = NewSolution(pdf_path="/Users/nusretkizilaslan/Downloads/buss_article_2.pdf")
    solution = NewSolution(pdf_path="/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/buss_article.pdf")
    solution.solution_pipeline()