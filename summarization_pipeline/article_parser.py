import re
import subprocess

exec_path = './alpaca-exec-s'
#exec_path = './alpaca-exec-n'

def send_prompt(prompt):
    prompt = prompt.replace(' ', '_').replace('-', '_').replace('@', '_')
    args = [exec_path, '--prompt', prompt]
    try:
        # Run the C++ executable and capture the output
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        
        # Extract the output from the subprocess
        output = result.stdout.strip()
        return output    
    except subprocess.CalledProcessError as e:
        print(f"Error executing C++ code: {e}")
        print(f"Error message: {e.stderr}")
        return None
    
def is_section_model_response(text) :
        general_sections = ['Abstract','Introduction','Literature Review', 'Methodology', 'Keywords' 'Outcomes', 'Results', 'Acknowledgements','References']
        for section in general_sections:
            if section in text:
                return True
        prompt = 'Can "' + text + '" be a section for a scholarly article, yes or no?'
        output = send_prompt(prompt)
        if  output == 'Yes':
            return True
        else:
            return False
    
def is_section(section_key) :
    counter = 0
    for character in section_key :
        if character == '.' :
            counter += 1
        elif counter == 1 and character.isnumeric() :
            return False
        """
        elif counter == 1 and character.isalpha() :
            model_response = is_section_model_response(section_key)
            return model_response
        """     
    return True

# Processes a dictionary of sections and groups subsections under their respective main sections.
def group_subsections(sections_dict):
    new_dict = {}
    sub_dict = {}
    prev_section = ''
    for index in range(len(sections_dict)):
        key = list(sections_dict.keys())[index]
        if is_section(key):
            if sub_dict != {} and prev_section != '':
                new_dict[prev_section] = sub_dict # Insert the sub_dict as the value to the new_dict
                sub_dict = {}
            key = re.sub(r'[0-9.:]', '', key).strip()  # Remove integers and punctuation from key
            prev_section = key
            if prev_section not in list(new_dict.keys()):
                new_dict[prev_section] = list(sections_dict.values())[index]
        else:
            key = re.sub(r'[0-9.:]', '', key).strip()  # Remove integers and punctuation from key
            sub_dict[key] = list(sections_dict.values())[index]
    if sub_dict != {} and prev_section != '': # Insert the last sub_dict as the value of the last section name
        new_dict[prev_section] = sub_dict 
    return new_dict

# Define a function to handle the iterative grouping of summaries
def recursive_grouping(summaries, summarizer, max_length=70):
    # Base case: if there's only one summary, return it
    if len(summaries) == 1:
        return summaries[0]

    # If more than one summary, group them by two and generate new summaries
    new_summaries = []
    for i in range(0, len(summaries), 2):
        text = summaries[i]
        if i + 1 < len(summaries):  # Check to ensure we don't exceed the list index
            text += " " + summaries[i + 1]
        # Hugging face pipeline
        # new_summaries.append(summarizer(text, max_length=max_length, min_length=20, do_sample=False)[0]['summary_text'])

        # Alpaca model summarization
        summary = summarizer.summarize(text)
        new_summaries.append(summary)

    return recursive_grouping(new_summaries, summarizer, max_length + 10)  # Increase max_length for each new round

"""
def divide_article_into_sections(article,):
    sections = {}
    section_titles = re.findall(r'\d+\..+?\n', article)  # Find all lines that start with "number.title"
    
    # Remove the falsely selected section titles
    section_titles = [title for title in section_titles if '%' not in title] # EX: '2.5% ...' is not a section title

    # Check the correctness of the chosen section titles by checking the non-decreasing order of the section numbers
    correct_titles = []
    previous_number = 0  # Start with a sentinel value
    for title in section_titles:
        # Extract the number at the start of the title
        match = re.match(r'(\d+)(\.\d+)?', title)
        if match:
            number = float(match.group(1))
            # Check if the main number (before the dot) is non-decreasing
            if number == previous_number or number == (previous_number + 1):
                if is_section_model_response(title) == True :
                    correct_titles.append(title)
                    previous_number = number

    section_titles = correct_titles
    
    # Use zip to pair section titles with their corresponding text
    for title, next_title in zip(section_titles, section_titles[1:] + ['']):
        # Get the start and end positions of each section
        start_pos = article.find(title)
        end_pos = article.find(next_title)
        
        # Extract the section text and remove the section title
        section_text = article[start_pos + len(title):end_pos].strip()
        
        # Store the section in the dictionary with the title as the key
        sections[title.strip()] = section_text

    return sections
"""

def divide_article_into_sections(article):
    sections = {}
    section_titles = re.findall(r'\d+\..+?\n', article)  # Find all lines that start with "number.title"

    # Use zip to pair section titles with their corresponding text
    for title, next_title in zip(section_titles, section_titles[1:] + ['']):
        # Get the start and end positions of each section
        start_pos = article.find(title)
        if next_title:  # if there is a next title, find its position
            end_pos = article.find(next_title)
        else:  # if this is the last title, use the end of the string
            end_pos = len(article)
        
        # Extract the section text and remove the section title
        section_text = article[start_pos + len(title):end_pos].strip()
        
        # Store the section in the dictionary with the title as the key
        sections[title.strip()] = section_text

    return sections