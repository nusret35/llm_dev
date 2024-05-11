# Single slider for greenness
# 5 options
# greenness = {0, 0.25, 0.5, 0.75, 1.0}

from .langchain_extractor import Langchain_Extractor, LLAMA2_70B, LLAMA2_13B, LLAMA3_70B

def configure_models(greenness_input):

    extractor_dict = {}

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

    langchain_extractor_70B_model = Langchain_Extractor(model=LLAMA3_70B(), max_new_tokens=max_tokens)
    langchain_extractor_13B_model = Langchain_Extractor(model=LLAMA2_13B(), max_new_tokens=max_tokens)

    extractor_dict["llama_70B"] = langchain_extractor_70B_model
    extractor_dict["llama_13B"] = langchain_extractor_13B_model

    return extractor_dict, max_tokens