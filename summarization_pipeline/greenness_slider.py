# Single slider for greenness
# 5 options
# greenness = {0, 0.25, 0.5, 0.75, 1.0}

from summarization_pipeline.orchestration import Extractor

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

    extractor_70B_model = Extractor(model='70B', max_new_tokens=max_tokens)
    extractor_13B_model = Extractor(model='13B', max_new_tokens=max_tokens)

    return extractor_70B_model, extractor_13B_model, max_tokens