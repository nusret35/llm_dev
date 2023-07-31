import re

def is_section(section_key) :
    counter = 0
    for character in section_key :
        if character == '.' :
            counter += 1
        elif counter == 1 and character.isnumeric() :
            return False
        elif counter == 1 and character.isalpha() :
            return True     
    return True


def group_subsections(sections_dict):
    new_dict = {}
    sub_dict = {}
    prev_section = ''
    for index in range(len(sections_dict)):
        if is_section(list(sections_dict.keys())[index]):
            if sub_dict != {} and prev_section != '':
                new_dict[prev_section] = sub_dict
                sub_dict = {}
            prev_section = list(sections_dict.keys())[index]
            if prev_section not in list(new_dict.keys()):
                new_dict[prev_section] = list(sections_dict.values())[index]
        else:
           sub_dict[list(sections_dict.keys())[index]] = list(sections_dict.values())[index]
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


def divide_article_into_sections(article):
    sections = {}
    section_titles = re.findall(r'\d+\..+?\n', article)  # Find all lines that start with "number.title"
    
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