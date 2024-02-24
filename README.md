# Business Insights Extraction from Scholarly Articles using Large Language Models (LLMs)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Overview

This project represents a groundbreaking approach to extracting actionable business insights from scholarly articles through the use of Meta's LLaMA 2 70B model, powered by NVIDIA's A100 80 GB Tensor Core GPU. By integrating advanced natural language processing (NLP) techniques and sophisticated prompt engineering, our methodology not only processes extensive scholarly texts but also optimizes the extraction of valuable insights by ensuring that the analysis is both rapid and precise. The aim is to utilize the unparalleled capabilities of LLMs to distill and leverage dense academic content for business intelligence.

## Solution Pipeline Explanation

Our solution pipeline consists of several stages designed to systematically process scholarly articles and extract insights effectively:

1. **Begin:** The pipeline commences with the input of scholarly articles in a PDF format.
2. **PDF Filtering:** We apply filters to the PDF to clean up the document from non-essential elements, creating a more accessible format for processing.
3. **Image Extraction from PDF:** Images are extracted for separate analysis to complement the textual data and provide a more comprehensive understanding.
4. **Conversion to Plain Text:** The filtered PDFs are converted into plain text, facilitating easier manipulation and processing.
5. **Division into Sections:** The text is divided into structured sections based on headings, enabling targeted analysis.
6. **Selection of Critical Sections:** We identify and select key sections that are likely to contain significant insights.
7. **Section Summarization:** These sections are then summarized, distilling the content to its essence.
8. **Identification of Important Images:** Concurrently, the importance of extracted images is assessed to enrich the analysis.
9. **Enhancement of Summaries:** The summaries are enhanced with insights from the important images, creating a richer narrative.
10. **Extraction of Insights:** Business insights are extracted from these enriched narratives.
11. **End:** The pipeline concludes with a set of actionable insights derived from the scholarly article.

This solution pipeline is powered by Meta's LLaMA 2 70B model, run using NVIDIA's A100 80 GB Tensor Core GPU, ensuring that the analysis is both rapid and precise.

## Project Structure

### A. Summarization Pipeline

The `summarization_pipeline` folder contains the following Python scripts:

1. **article_parser.py:** Parses articles into sections based on headings.
2. **image_processing.py:** Extracts images from articles and matches them to model-identified important images.
3. **orchestration.py:** Initializes the LLM (LLaMA 2 70B model) and defines the solution pipeline's execution methods.
4. **pdf_section_extractor.py:** Converts PDF files into clean, machine-readable text.

### B. Solution Script

- **solution.py:** The primary script that activates the solution pipeline, integrating all defined algorithms and model calls to tackle the insights extraction challenge.

## Getting Started

To utilize this project:

1. Ensure Python 3.6+ is installed.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Run `python solution.py` within the project directory to initiate the extraction process.

---

This README file now includes a complete explanation of the solution pipeline along with the technical details of the model and hardware used.
