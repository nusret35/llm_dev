# Single slider for greenness
# 5 options
# greenness = {0, 0.25, 0.5, 0.75, 1.0}

from summarization_pipeline.stream_output_generator import Stream_Output_Generator
from summarization_pipeline.langchain_extractor import Langchain_Extractor

def configure_models(greenness_input):

    if greenness_input == 0:
        max_tokens = 500
    elif greenness_input == 0.25:
        max_tokens = 400
    elif greenness_input == 0.5:
        max_tokens = 300
    elif greenness_input == 0.75:
        max_tokens = 200
    elif greenness_input == 1.0:
        max_tokens = 100
    else: #default case
        max_tokens = 500

    stream_generator_70B_model = Stream_Output_Generator(model='70B', max_new_tokens=max_tokens)
    stream_generator_13B_model = Stream_Output_Generator(model='13B', max_new_tokens=max_tokens)

    langchain_extractor_70B_model = Langchain_Extractor(model='70B', max_new_tokens=max_tokens)
    langchain_extractor_13B_model = Langchain_Extractor(model='13B', max_new_tokens=max_tokens)

    return stream_generator_70B_model, stream_generator_13B_model, langchain_extractor_70B_model, langchain_extractor_13B_model, max_tokens