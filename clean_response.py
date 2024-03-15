import re
import base64

def remove_double_quotes(input_string):
    return input_string.replace('"', '')

def convert_to_string_array(input_string):
    # Remove the first line
    input_string = input_string.split('\n', 1)[-1]
    
    # Remove numerics at the beginning of each line
    input_string = re.sub(r'^\d+\.\s*', '', input_string, flags=re.MULTILINE)
    
    # Split the remaining text into sentences based on full stops ('.') or newlines ('\n')
    sentences = input_string.split('.\n')
    
    # Remove any leading or trailing whitespace from each sentence
    sentences = [sentence.strip() for sentence in sentences]
    
    return sentences

def convert_images_to_base64(image_dict):
    base64_dict = {}
    for key, image_path in image_dict.items():
        with open(image_path, 'rb') as file:
            image_bytes = file.read()
            base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
        base64_dict[key] = base64_encoded
    return base64_dict

# Example usage:
image_dict = {
    'Fig. 2. Framework for the choice of revenue models for digital services': './images/page9/output_image0.png'
}

base64_dict = convert_images_to_base64(image_dict)
print(base64_dict)

image_dict = {
    'Fig. 2. Framework for the choice of revenue models for digital services': './images/page9/output_image0.png'
}

bytes_dict = convert_images_to_base64(image_dict)
print(bytes_dict)