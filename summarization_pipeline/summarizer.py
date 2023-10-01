import subprocess

class Summarizer :

    def __init__(self,model_path):
        self.model_path = model_path

    def _send_prompt(self,prompt):
        prompt = prompt.replace(' ', '_').replace('-', '_').replace('@', '_')
        args = [self.model_path, '--prompt', prompt]
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
        
    def prompt_generator(self,instruction,input):
        prompt = 'Instruction: ' + instruction + ".  Input: " + input 
        return prompt

    def summarize(self,text):
        length = len(text.split())
        summary_limit = max(30, int(length*0.5))
        prompt = "Summarize this text with maximum " + str(summary_limit) + " words: " + text
        output = self._send_prompt(prompt)
        return output

    def find_thesis_statament(self,text):
        prompt = 'What is the thesis statement of this text: ' + text
        output = self._send_prompt(prompt)
        return output
    
    # Returns the text of a section together with the text of its subsections
    def section_text(self,section_name,sections_dict):
        if section_name in sections_dict:
            # If the section exists and its value is a string, the function returns this string directly
            if isinstance(sections_dict[section_name], str):
                return sections_dict[section_name]
            # If the section exists and its value is a dictionary, 
            # the function concatenates all the string values from this dictionary
            else:  
                output = ''
                for item in sections_dict[section_name].values():
                    output += item + ' '  # Add a space for separation
                return output.strip()  # Remove trailing space
        return ''
    
    # What did the author set out to do? 
    # What was the outcome?
    def find_objective(self,title,sections_dict):
        abstract = self.section_text('Abstract',sections_dict)
        introduction = self.section_text('Introduction',sections_dict)
        conclusion = self.section_text('Conclusion',sections_dict)

        prompt = 'I have an article at hand, whose title is: ' + title + 'Whose abstract is: ' + abstract + 'Whose introduction is: ' + introduction + 'Whose conclusion is: ' + conclusion + '/n What did the author set out to do and what was the outcome?'
        output = self._send_prompt(prompt)
        return output
    
    """
    def select_sections(self,section_names,title):
        section_names_string = ''
        for section_name in section_names:
            section_names_string += section_name + ', '
        prompt= "Title of the article: " + title + "The above article is an important scholarly work on {field of study}. Considering its significance, the wide range of content it covers, and its impact on the field, identifying key sections for summarization is crucial. Please review the given sections and provide a list of the most important sections that would provide a comprehensive summary of the paper's main arguments, findings, and implications. Choose the sections from the given section names and return only these important section names!"
        output = self._send_prompt(prompt)
        output = output.split()
        return output
    """

    def select_sections(self, section_names,thesis_statement):
         section_names_string = ''
         for section_name in section_names:
             section_names_string += section_name + ' '
         prompt = 'Sections: ' + section_names_string + '\n Thesis statement: ' + thesis_statement + '\n Give the three most important section names among the given sections'
         output = self._send_prompt(prompt)
         return output

    # The section names are outputted as an array
    def select_sections_t(self,section_names,thesis):
        section_names_string = ''
        for section_name in section_names:
            section_names_string += section_name + ' '
        instruction = 'Find the 5 most significant section names of the scholarly article.'
        input = 'Section names: ' + section_names_string + '. \n Thesis statement: ' + thesis
        prompt = self.prompt_generator(instruction,input)
        #prompt = 'Given the section names of the article: ' + section_names_string + '. \n \n And the thesis statement: ' + thesis + '. \n \n For the purpose of summarization, give the most important 5 section names of this article: '
        output = self._send_prompt(prompt)
        output = output.split()
        return output

    # The section names are outputted as an array
    def select_sections_o(self,section_names,objective):
        section_names_string = ''
        for section_name in section_names:
            section_names_string += section_name + ' '
        prompt = 'Given the section names of the article: ' + section_names_string + 'And the objective: ' + objective + '\n Give the most important section names of this article to summarize the article: '
        output = self._send_prompt(prompt)
        output = output.split()
        return output
    
    # The most important 5 section names are outputted as an array
    def select_5_sections_t(self,section_names,thesis):
        section_names_string = ''
        for section_name in section_names:
            section_names_string += section_name + ' '
        prompt = 'Given the section names of the article: ' + section_names_string + 'And the thesis statement: ' + thesis + '\n Give the 5 most important section names of this article, on top of the introduction and the conclusion, to summarize the article: '
        output = self._send_prompt(prompt)
        output = output.split()
        return output
    


    