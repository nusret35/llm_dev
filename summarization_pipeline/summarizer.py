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

    def summarize(self,text):
        prompt = "Summarize this text: " + text
        output = self._send_prompt(text)
        return output

    def find_thesis_statament(self,text):
        prompt = 'What is the thesis statement of this text: ' + text
        output = self._send_prompt(prompt)
        return output
    
    def section_text(self,section_name,sections_dict):
        if section_name in sections_dict:
            if isinstance(sections_dict[section_name], str):
                return sections_dict[section_name]
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
    
    # The section names are outputted as an array
    def select_sections_t(self,section_names,thesis):
        section_names_string = ''
        for section_name in section_names:
            section_names_string += section_name + ' '
        prompt = 'Given the section names of the article: ' + section_names_string + 'And the thesis statement: ' + thesis + '\n Give the most important section names of this article to summarize the article: '
        output = self._send_prompt(prompt)
        important_sections = []
        prev_word = ''
        for char in output:
            while char != ' ':
                prev_word += char
            important_sections.append(prev_word)
            prev_word = ''
        return important_sections 

    # The section names are outputted as an array
    def select_sections_o(self,section_names,objective):
        section_names_string = ''
        for section_name in section_names:
            section_names_string += section_name + ' '
        prompt = 'Given the section names of the article: ' + section_names_string + 'And the objective: ' + objective + '\n Give the most important section names of this article to summarize the article: '
        output = self._send_prompt(prompt)
        important_sections = []
        prev_word = ''
        for char in output:
            while char != ' ':
                prev_word += char
            important_sections.append(prev_word)
            prev_word = ''
        return important_sections 
    
    # The most important 5 section names are outputted as an array
    def select_5_sections_t(self,section_names,objective):
        section_names_string = ''
        for section_name in section_names:
            section_names_string += section_name + ' '
        prompt = 'Given the section names of the article: ' + section_names_string + 'And the thesis statement: ' + objective + '\n Give the 5 most important section names of this article, on top of the introduction and the conclusion, to summarize the article: '
        output = self._send_prompt(prompt)
        important_sections = []
        prev_word = ''
        for char in output:
            while char != ' ':
                prev_word += char
            important_sections.append(prev_word)
            prev_word = ''
        return important_sections 