# Business Insights Extraction from Scholarly Articles using Large Language Models (LLMs)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Overview

This project employs a hybrid approach, combining Meta's LLaMA 2 13B and LLaMA 2 70B models, to extract actionable business insights from scholarly articles. The dual-model pipeline leverages the strengths of each model according to the complexity of the task, utilizing NVIDIA's A100 80 GB Tensor Core GPU to process extensive scholarly texts for high-value business intelligence.

By integrating advanced natural language processing (NLP) techniques and sophisticated prompt engineering, our methodology not only processes extensive scholarly texts but also optimizes the extraction of valuable insights by ensuring that the analysis is both rapid and precise. The aim is to utilize the unparalleled capabilities of LLMs to distill and leverage dense academic content for business intelligence.

You may try it on web: https://insight-extractor.streamlit.app

## Hybrid Solution Pipeline Explanation

Our hybrid solution pipeline employs a strategic approach to task distribution between two models, optimizing each model's strengths for various tasks:

1. **Start:** The process initiates with the user inputting an article in PDF format.
2. **PDF Extraction:** The article is preprocessed to extract text and images.
3. **Choosing Critical Sections:** The user guides the system to identify critical sections for detailed analysis.
4. **Section Summarization:** Summarizes the chosen sections to distill the core content.
5. **Enriching the Abstract:** The abstract is enriched by integrating insights from the summaries of the critical sections, forming a comprehensive overview.
6. **Insights Extraction:** Extracts insights from the enriched abstract, utilizing the more capable model for complex inference.
7. **Finding a Title:** Generates a suitable title for the insights extracted to be displayed in a chat interface.
8. **Image Extraction:** Images are extracted, and their relevance is evaluated.
9. **End:** The pipeline culminates in actionable business insights presented to the user.

This hybrid pipeline allows for efficient use of LLMs, applying the appropriate model to tasks based on complexity, ensuring a fast and accurate analysis.

The diagram illustrating our hybrid solution pipeline is presented below, delineating the specific processes and the corresponding tasks assigned to the LLaMA 2 13B and LLaMA 2 70B models.

![Flowchart](https://github.com/nusret35/llm_dev/assets/120125253/33fb65af-84a0-447f-9325-7fadf035452e)

## Project Structure

### A. Summarization Pipeline

The `summarization_pipeline` folder contains essential Python scripts:

1. **article_parser.py:** Parses articles into sections.
2. **image_processing.py:** Extracts images and matches them with significant ones identified by the model.
3. **orchestration.py:** Initializes the LLMs and orchestrates the pipeline based on task complexity.
4. **pdf_section_extractor.py:** Converts PDF files into clean, machine-readable text.

### B. Solution Script

- **solution.py:** Activates the solution pipeline, integrating all defined algorithms and model calls.

## Getting Started

- Ensure Python 3.6+ is installed.

- Optionally, you can create and activate the virtual environment.
```bash
    python -m venv .venv
    source ./.venv/bin/activate
```

- Install the requirements.
```bash
    pip install -r requirements.txt
```

## License

The project is licensed under the MIT License.

---

This README now accurately reflects your hybrid solution pipeline and details which tasks are allocated to the LLaMA 2 13B and LLaMA 2 70B models, in line with the latest pipeline diagram you've provided.
