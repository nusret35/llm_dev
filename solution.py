from summarization_pipeline.pdf_section_extractor import extract_pdf_and_divide_sections
from summarization_pipeline.image_processing import extract_image_title_pairs, extract_titles_from_page, convert_response_to_list, get_important_image_paths
from summarization_pipeline.greenness_slider import configure_models
import fitz

class Solution:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def preprocess_insights(self, insights):
        # Find the position of the last dot in the string
        last_dot_position = insights.rfind('.')

        # If a dot is found, return the part of the string until this dot
        if last_dot_position != -1:
            return insights[:last_dot_position + 1]
        
        # If no dot is found, return the original string
        return insights

    def preprocess_title(self, title):
        # Find the position of the colon in the string
        colon_pos = title.find(':')

        # Extract and return the portion of the title after the colon
        # Ensure that the colon is found and it is not the last character in the string
        if colon_pos != -1 and colon_pos != len(title) - 1:
            return title[colon_pos + 1:].strip()
        
        # If a suitable colon is not found, return the original string
        return title

    def solution_pipeline(self):  
        # Initializing the LLaMA 2 70B and 13B models after getting greenness_input from the user
        greenness_input = 0.5 #default greenness configuration
        extractor_70B_model, extractor_13B_model, max_tokens = configure_models(greenness_input)


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
                summary = extractor_70B_model.summarize(section_name, section_text, max_tokens)
                summarized_sections[section_name] = summary
                print("Summary of " + section_name + ": \n" + summary)
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


        # Extracting insights from the article using the summarized sections (using LLaMA 2 70B model)
        section_input_abstract = "abstract: " + abstract + section_input

        insights = extractor_70B_model.extract_insights(section_input_abstract, max_tokens)
        print("\nExtracted insights before processing:\n" + insights)

        insights = self.preprocess_insights(insights)
        print("\nExtracted insights after processing:\n" + insights)

        # Generating a meaningful title to be presented as the chat title in the interface (using LLaMA 2 13B model)
        title = extractor_13B_model.generate_title(insights)
        print("\nTitle before preprocessing:\n" + title)

        title = self.preprocess_title(title)
        print("\nTitle after preprocessing:\n" + title)


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
            
        important_images = extractor_13B_model.choose_images(insights, image_titles, max_tokens)
        print("\nImportant images:\n" + important_images)


        # Displaying the fetched figures/tables that match the selected images
        important_images_list = convert_response_to_list(important_images)

        # Check whether the important image is extracted
        found_images = get_important_image_paths(image_title_pairs, important_images_list)
        print("\nPaths of the extracted images that are among the important images:\n" + found_images)


        extractor_13B_model.close()
        extractor_70B_model.close()


if __name__ == "__main__":
    # Specify the path to the example PDF file
    example_pdf_path = "/Users/nusretkizilaslan/Downloads/buss_article-2.pdf"  # Replace with the actual path

    # Create an instance of the Solution class with the example PDF path
    solution_instance = Solution(example_pdf_path)

    # Run the solution_pipeline method
    solution_instance.solution_pipeline()