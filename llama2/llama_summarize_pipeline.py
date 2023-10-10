from summarization_pipeline.summarizer import Summarizer
import transformers 
from langchain import PromptTemplate

sum = Summarizer()

template = """
Write a concise summary of the following text delimited by triple backquotes. 
Return your response in bullet points which covers the key point of the text.
'''{text}'''
BULLET POINT SUMMARY
"""

prompt = PromptTemplate(template=template, )
output = sum.get_llama_response('Summarize the given text The COVID-19 pandemic had a major impact on healthcare systems across the world. In the United Kingdom, one of the strategies used by hospitals to cope with the surge in patients infected with SARS-Cov-2 was to cancel a vast number of elective treatments planned and limit its resources for non-critical patients. This resulted in a 30% drop in the number of people joining the waiting list in 2020–2021 versus 2019–2020.Once the pandemic subsides and resources are freed for elective treatment, the expectation is that the patients failing to receive treatment throughout the pandemic would trigger a significant backlog on the waiting list post-pandemic with major repercussions to patient health and quality of life. As the nation emerges from the worst phase of the pandemic, hospitals are focusing on strategies to prioritise patients for elective treatments. A key challenge in this context is the ability to quantify the expected backlog and predict the delays experienced by patients as an outcome of the prioritisation policies. This study presents an approach based on discrete-event simulation to predict the elective waiting list backlog along with the delay in treatment based on a predetermined prioritisation policy. The model is demonstrated using data on the endoscopy waiting list at Cambridge University Hospitals. The model shows that 21% of the patients on the waiting list will experience a delay less than 18-weeks, the acceptable threshold set by the National Health Service (NHS). A longer-term scenario analysis based on the model reveals investment in NHS resources will have a significant positive outcome for addressing the waiting lists. The model presented in this paper has the potential to be an invaluable tool for post-pandemic planning for hospitals around the world that are facing a crisis of treatment backlog.')

