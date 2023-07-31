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

    def select_sections(self, section_names):
        section_names_string = ''
        for section_name in section_names:
            section_names_string += section_name + ' '
        prompt = 'Sections: ' + section_names_string + '\n Give the important sections of this article to summarize the article with the given thesis statement'
        output = self._send_prompt(prompt)
        return output 

    def find_thesis_statament(self,text):
        prompt = 'What is the thesis statement of this text: ' + text
        output = self._send_prompt(prompt)
        return output
    
    def section_text(self,section_name,sections_dict):
        if section_name in list(sections_dict.keys()):
            if isinstance(sections_dict[section_name],str):
                return sections_dict[section_name]
            else:
                output = ''
                for item in list(sections_dict[section_name].values()):
                    output += item
                return output
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
    