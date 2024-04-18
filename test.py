def remove_unfinished_sentence(text):
    last_dot = text.rfind('.')
    clean_text = text[:last_dot+1]
    return clean_text

text = """
 * Insight 1: The article highlights the importance of digital servitization in manufacturing companies and how it can lead to a competitive business strategy. Digital servitization involves making the transition from products to services or a combination of both, where companies need to capture profits from investing in R&D or implementing new technologies. However, only a limited number of studies have explored revenue models holistically, and most empirics have been built on revenue models for data-driven services. Therefore, there is a need for further research to advance understanding of the factors that influence the choice of revenue models for digital services in manufacturing companies.
* Insight 2: The study reveals that subscription models are the simplest and less risky option to capture value for digital services, where customers can be charged over a recurring period based on transactional contracts. Usage-based revenue models represent a moderate risk because companies can perceive a potential gap in the flow of revenues in an arrangement where payments are settled through pre-negotiated fees in a unit of measure logic (mostly hourly-based metrics). Performance-based revenue models are the most complex and riskiest option as they depend on the actual usage and performance of the digital service.
* Insight 3: The framework provided in the article offers a four-step approach to choosing revenue models for digital services. The first step assesses the customer's digital readiness, including their awareness, digital value co-creation, and contractual arrangements for digital services. The second step evaluates the sophistication of the digital service, such as basic vs. advanced services. The third step assesses digital ecosystem partnerships, which involve data exchange and collaboration between actors. Finally, the fourth step involves selecting the suitable revenue model based on the previous assessments. This framework can guide managers in making informed decisions about revenue models that align with their digital servitization goals.
* Insight 4: Digital ecosystem partnerships play a 
"""

clean = remove_unfinished_sentence(text)
print(clean)