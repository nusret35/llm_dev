import subprocess

class Summarizer :
    def __init__(self,model_path):
        self.model_path = model_path
        pass



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