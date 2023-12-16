import replicate
import re
from pdf_section_extractor import extract_pdf_and_divide_sections, extract_pdf, capture_image_titles
from article_parser import divide_article_into_sections
from image_processing import extract_titles_from_page, extract_image_title_pairs, get_important_image_paths,convert_response_to_list
import fitz

    
#business_pdf1_path = "/Users/nusretkizilaslan/Downloads/selo-article.pdf"
#pdf_path = "/Users/selinceydeli/Desktop/sabancı/OPIM407/Individual Assignment-3/Predicting_Freshman_Student_Attrition_Article.pdf"
#business_pdf1_path = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/buss_article.pdf"
business_pdf1_path = "/Users/nusretkizilaslan/Downloads/buss_article.pdf"
sections_dict = extract_pdf_and_divide_sections(business_pdf1_path)
extracted_pdf = extract_pdf(business_pdf1_path)

insights = '''
* Relationship marketing (RM) is crucial for business-to-business (B2B) companies to navigate economic downturns and recoveries.
* During economic uncertainty, firms need to adapt their RM strategies to address changing customer needs and maintain relationships.
* A framework linking RM process mechanisms to firm performance during economic contractions and expansions has been proposed, which includes three key relationship tenets: communication openness, technical involvement, and customer value anticipation.
* These tenets have direct and indirect effects on supplier performance and can help firms manage business-to-business relationships (BCs).
* The study provides actionable strategies for managing BCs during economic contractions and expansions, including establishing high levels of communication without increasing technical collaboration, exploiting top management consensus, and leveraging technical involvement with customers.
* The findings have important implications for theory, extending existing research streams and providing insights into how B2B relationships can be managed during times of economic uncertainty.
* The study contributes to the dark side of B2B relationships’ theoretical underpinnings by demonstrating how the inherent tension created in a BC can be managed by RM mechanisms.
* The study extends BC marketing literature outside of the often-used US environment by investigating buyer-seller relationships through a BC in an emerging economy, Chile.
'''

# Open the file
pdf_file = fitz.open(business_pdf1_path)
titles = []
image_title_pairs = {}
# Iterate over PDF pages
for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    page_image_title_pairs = extract_image_title_pairs(page,page_index)
    page_image_titles = extract_titles_from_page(page)
    image_title_pairs.update(page_image_title_pairs)
    for title in page_image_titles:
        title += " (Page:" + str(page_index+1) + ")"
        print(title)
        titles.append(title)

pdf_file.close()


image_titles = ""
for title in titles:
    image_titles += title + "\n"


#response = choose_images(insights, image_titles)

# API token ran out. Here is the hard coded response of the LLM
response = "1. Fig. 2. Conceptual Model (Page:5) - This image presents the conceptual model of the study, which highlights the relationship between the RM process mechanisms and firm performance during economic contractions and expansions. It also illustrates the three key relationship tenets proposed by the authors, which are communication openness, technical involvement, and customer value anticipation. Understanding this model is crucial to grasping the main findings and implications of the study.\n2. Table 3. Construct Correlations and AVEs (Page:7) -  This table presents the results of the confirmatory factor analysis (CFA) and shows the correlations between the constructs and the average variance extracted (AVE). The table provides evidence for the validity and reliability of the measures used in the study, which is essential for establishing the credibility of the research findings.\n3. Fig. 3. Relationship Marketing (RM) Strategies Matrix (Page:11) - This image presents a matrix that summarizes the RM strategies suggested by the authors for managing business-to-business relationships during economic contractions and expansions. The matrix includes strategies such as establishing high levels of communication without increasing technical collaboration, exploiting top management consensus, and leveraging technical involvement with customers."

important_images_list = convert_response_to_list(response)


# Check whether the important image is extracted
found_images = get_important_image_paths(image_title_pairs,important_images_list)

print(found_images)



