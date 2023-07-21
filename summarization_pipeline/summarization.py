from transformers import pipeline
import torch
import re
import subprocess

"""
summarizer = pipeline(
    "summarization",
    "pszemraj/long-t5-tglobal-base-16384-book-summary",
    device=0 if torch.cuda.is_available() else -1,
)
"""


def alpaca_model_summarization(input):
    
    prompt = 'Summarize this text: ' + input
    # Path to the compiled C++ executable 'chat_app'
    cpp_executable = './alpaca-model'

    # Prepare the command-line arguments for the C++ executable
    # Replace any spaces or special characters in 'prompt' with underscores (_) 
    prompt = prompt.replace(' ', '_').replace('-', '_').replace('@', '_')
    args = [cpp_executable, '--prompt', prompt]

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

 # Define a function to handle the iterative grouping of summaries

def recursive_grouping(summaries, max_length=70):
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
        summary = alpaca_model_summarization(text)
        new_summaries.append(summary)


    return recursive_grouping(new_summaries, max_length + 10)  # Increase max_length for each new round


if __name__ == "__main__":
    # Load the summarization pipeline
    # summarizer = pipeline("summarization")

    # Read txt document
    with open('summarization_pipeline/data2.txt', 'r') as file:
        text = file.read()

    sections = re.split('\d+\..+\n', text)  # Split on lines that start with "number.title"
    sections = [section.strip() for section in sections if section.strip()]

    print(len(sections))

    summaries = []

    for section in sections:
        section = section.strip()  # Remove any leading/trailing whitespace
        # Hugging Face pipeline summarization
        #summaries.append(summarizer(section, max_length=50, min_length=20, do_sample=False)[0]['summary_text'])

        # Alpaca model summarization
        summary = alpaca_model_summarization(section)
        print(summary)
        summaries.append(summary)

    # I realized that we do not need to consider the subsections seperately. 
    # The redex for the sections already handle the seperation of the subsections. 
    # So I commented out the below for-loop. 

    """
    for section in sections:
        section = section.strip()  # remove any leading/trailing whitespace

        # Split the sections further into subsections
        subsections = re.split('\d+\.\d+\..+\n', section)  # Split on lines that start with "number.number.title"
        subsections = [subsection.strip() for subsection in subsections if subsection.strip()]

        for subsection in subsections:
            subsection = subsection.strip() 

            # Split the subsections further into sub-subsections
            subsubsections = re.split('\d+\.\d+\.\d+\..+\n', subsection)  # Split on lines that start with "number.number.number.title"
            subsubsections = [subsubsection.strip() for subsubsection in subsubsections if subsubsection.strip()]

            for subsubsection in subsubsections:
                subsubsection = subsubsection.strip() 
                summaries.append(summarizer(subsubsection, max_length=50, min_length=25, do_sample=False)[0]['summary_text'])
    """


    final_summary = recursive_grouping(summaries)

    print()
    print(final_summary)