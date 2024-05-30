import re

def shorten_text(long_string):
    # Split the long string into sentences based on periods
    sentences = long_string.split('.')

    # Exclude the last sentence if there are more than one sentence
    if len(sentences) > 1:
        shortened = '.'.join(sentences[:-2])
    else:
        shortened = long_string

    return shortened


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


def is_correct_title(title):
    for c in title:
        if ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z'):
            return True
    return False
        

def divide_article_into_sections(article):
    sections = {}
    section_titles = re.findall(r'\d+\.\s*.+?\n|\d+.+?\n', article)
    
    # Remove the falsely selected section titles
    section_titles = [title for title in section_titles if '%' not in title] # EX: '2.5% ...' is not a section title
    # Check the correctness of the chosen section titles by checking the non-decreasing order of the section numbers
    correct_titles = []
    previous_number = 0  # Start with a sentinel value
    for title in section_titles:
        pos = article.find(title)
        prev_pos = pos-1
        # Extract the number at the start of the title
        print(title)
        match = re.match(r'(\d+)(\.\d+)?', title)
        if match:
            number = float(match.group(1))
            # Check if the main number (before the dot) is non-decreasing
            if number == previous_number or number == (previous_number + 1):
                # Check if there is a new line char before the title number
                if article[prev_pos] == '\n':
                    if is_correct_title(title):
                        correct_titles.append(title)
                        previous_number = number
                    
    section_titles = correct_titles

    assert len(section_titles) != 0
    print(len(section_titles))

    # Use zip to pair section titles with their corresponding text
    for title, next_title in zip(section_titles, section_titles[1:] + ['']):
        # Get the start and end positions of each section
        start_pos = article.find(title)
        end_pos = article.find(next_title)
        
        # Extract the section text and remove the section title
        section_text = article[start_pos + len(title):end_pos].strip()
        
        # Store the section in the dictionary with the title as the key
        sections[title.strip()] = section_text
    
    abstract_types = ["abstract", "Abstract", "a b s t r a c t", "A B S T R A C T"]
    for type in abstract_types:
        if type in article:
            start_pos = article.find(type)
            end_pos = article.find(list(sections.keys())[0])
            section_text = article[start_pos + len(type):end_pos]
            new_sections_dic = {'abstract':section_text}
            new_sections_dic.update(sections)
            sections = new_sections_dic
            break

    # Cleaned sections dictionary
    cleaned_sections_dict = {}

    # Regular expression to match integers and punctuation
    regex = re.compile('[0-9\.\,\!\?\:\;\-\—\(\)]')

    for key, value in sections.items():
        # Remove integers and punctuation from the key
        cleaned_key = regex.sub('', key)
        # Convert key to lowercase
        cleaned_key = cleaned_key.lower()
        # Remove any extra whitespace
        cleaned_key = cleaned_key.strip()
        # Add to the cleaned dictionary
        cleaned_sections_dict[cleaned_key] = value

    return cleaned_sections_dict