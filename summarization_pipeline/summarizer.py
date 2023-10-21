import subprocess
from transformers import pipeline
import torch


class Summarizer : 

    def __init__(self,exec_path=None):
        self.exec_path = exec_path

    def get_llama_response(self, prompt: str) -> None:
        pipe = pipeline("text-generation", model="meta-llama/Llama-2-70b-chat-hf",torch_dtype=torch.float16)
        output = pipe(prompt)
        print(output)

    def _make_prompt(self,instruction):
        prompt = "Below is an instruction that describes a task. Write a response that appropriately completes the request\n### Instruction:" + instruction + "\n### Response:"
        return prompt
    
    def _make_prompt_2(self,instruction, input):
        prompt = "### Instruction:" + instruction  + "\n### Input: "+ input + "\n### Response:"
        return prompt
    
    def _send_prompt(self,prompt):
        #./main -m ./models/7B/./ggml-model-q4_0.bin -n 1024 --repeat_penalty 1.0 --color -ins -f ./prompts/summarization2.txt
        #model_path = '/Users/nusretkizilaslan/Desktop/AIProject/llama2/llama.cpp/models/./7B/ggml-vocab-q4_0.bin'
        #model_path = '/Users/selinceydeli/Desktop/llama/llama.cpp/models/7B/ggml-model-q4_0.bin'
        #alpaca_path = "/Users/selinceydeli/Desktop/llama/llama.cpp/models/alpaca.13b.ggmlv3.q8_0.bin"
        alpaca_path = '/Users/nusretkizilaslan/Desktop/AIProject/llama2/llama.cpp/models/alpaca.13b.ggmlv3.q8_0.bin'
        args = [self.exec_path, '-m', alpaca_path, '--color','-p',prompt,'--ctx_size','4096','-n','-1', '-b','256','--top_k','10000','--temp', '0.2','--repeat_penalty','1.1','-t','7']
        
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
    
    def return_response(self, output):
        position = output.rfind("### Response:")
        if position != -1:  # Check whether "### Response:" is found
            position += len("### Response:")  # Move position after "### Response:"
            response = output[position:]  # Slice the string from the new position to the end
            return response.strip()  # Strip is used to remove any leading/trailing whitespace or newlines
        else:
            return "### Response: not found in the text"

    def summarize(self,text):
        instruction = "Summarize this text: " + text
        #prompt = self._make_prompt(instruction)
        output = self._send_prompt(instruction)
        response = self.return_response(output)
        return response

    def find_thesis_statament(self,text):
        instruction = 'What is the thesis statement of this text: ' + text
        prompt = self._make_prompt(instruction)
        output = self._send_prompt(prompt)
        response = self.return_response(output)
        return response
    
    def enrich_abstract_1(self,abstract,sections):
        prompt = '### Instruction:Expand the abstract based on the important information from the given Introduction, Conclusion, Methodology, and Outcomes. Return the enlarged abstract.'
        prompt = prompt + '\n' + '### Input:'
        prompt = prompt + '\n' + '- Abstract: ' + abstract
        for section, text in sections.items():
            if text != None:
                prompt = prompt + '\n- ' + section + ': ' + text
                print('\n')
                print('\n')
        prompt += '### Response: '
        print(prompt)
        output = self._send_prompt(prompt)
        response = self.return_response(output)
        return response
    
    def enrich_abstract_2(self,abstract,sections):
        base_instruction = "Expand the abstract based on the important information from the given section texts. Return the enlarged abstract."
        #base_instruction = "Concatenate the absract with the important information from the given section texts. Return the concatenated abstract."
        instruction = 'Abstract: '+ abstract
        for section, text in sections.items():
            if text != None:
                instruction += '\\' + section + ':' + text 
        instruction += base_instruction
        prompt = self._make_prompt(instruction)
        #prompt = instruction
        output = self._send_prompt(prompt)
        response = self.return_response(output)
        return response
    

    # Returns the text of a section together with the text of its subsections
    def section_text(self, section_name, sections_dict):
        # Convert section_name to lowercase for case-insensitive comparison
        section_name_lower = section_name.lower()
        
        for key, value in sections_dict.items():
            # Convert each key to lowercase for case-insensitive comparison
            if section_name_lower == key.lower():
                # If the section exists and its value is a string, the function returns this string directly
                if isinstance(value, str):
                    return value
                # If the section exists and its value is a dictionary,
                # the function concatenates all the string values from this dictionary
                else:  
                    output = ''
                    for item in value.values():
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
    