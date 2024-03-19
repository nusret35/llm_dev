'''
Output parsers are classes that help structure language model responses.
'''

import os
from dotenv import load_dotenv
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from langchain_community.llms import Replicate

load_dotenv()

api_key = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = api_key

section_summaries = 'abstract:    \nBusiness cycles (BCs) can alter the conditions for long-term business-to-business (B2B) relationships. Based on \nrelationship marketing (RM) and interorganizational learning theories, the authors propose a model that explains \nrelationship configurations that reveal opportunities under economic uncertainty. In the Pilot Study, the authors \nidentify key mechanisms of RM process (communication openness, technical involvement, and customer value \nanticipation) and performance outcomes (price, cost-to-serve, and expectation of relationship continuity) from \nthe supplier’s view. In Study 1, the proposed model is tested with a sample of large size, market leader firms in \ntimes of economic crisis (T1). In Study 2, conducting a multi-group analysis, the same sample is used to test the \nmodel in times of recovery/expansion (T2). The findings offer directions for suppliers on how to leverage B2B \nrelationships through a BC. Particularly, the authors indicate that supplier’s performance is influenced differ-\nently by RM mechanisms during times of economic crisis versus times of recovery/expansion.   \nintroduction:  The article discusses the importance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns. The authors argue that RM can help firms navigate economic fluctuations and maintain long-term relationships with customers. They identify three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation. These mechanisms have direct and indirect effects on supplier performance, and their impact varies across different stages of the business cycle. The study contributes to both RM and business cycle literature by providing actionable strategies for managing B2B relationships during economic turbulence. The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers. \nmanagerial implications:  This section discusses the managerial implications of the proposed Relationship Mechanisms (RM) for achieving firm goals during times of economic crisis and recovery. The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms: Communication Openness (COM), Technical Involvement (INV), and Customer Value Anticipation (CVA). Each quadrant is named based on the empirical results and includes strategies for effectively managing each quadrant.\n\nThe first quadrant, "Value anticipation based on distant communication," focuses on increasing the selling price (PR) during an economic crisis. Suppliers should reduce their technical involvement with customers while still being able to enhance customer value anticipation through remote communication.\n\nThe second quadrant, "Cost-oriented joint collaboration," aims to reduce the cost-to-serve (CTS) during an economic crisis. Suppliers should establish strong technical involvement with customers, focusing on cost-reducing opportunities and generating savings for both actors.\n\nThe third quadrant, "Dyadic top management consensus," seeks to enhance the expectation of continuity (EC) during an economic crisis. Suppliers should exploit top management consensus with customers, nudging top managers to reach consensus on how to face the economic crisis together.\n\nThe fourth \ntheoretical implications:  This study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions. The authors argue that interorganizational relationships are crucial for coping with economic uncertainty and that buyer-seller relationships should be managed through effective communication openness, technical involvement, and customer value anticipation. They conducted a quantitative study in Chile, an emerging economy, and found that these mechanisms help transform tension created by economic fluctuations into learning opportunities for adapting the relationship during a business cycle (BC).\n\nThe findings have important theoretical implications for marketing literature, as they provide evidence for the key role of customer value anticipation and extend the dialectical view on buyer-seller relationships. The study also contributes to the dark side of B2B relationships\' theoretical underpinnings by showing that inherent tension created in a BC can be managed by RM mechanisms. Additionally, the investigation of buyer-seller relationships through a BC in an emerging economy answers calls for more marketing research in non-advanced settings.\n\nIn summary, the study highlights the importance of managing B2B relationships during economic downturns and provides insights into how suppliers can navigate economic fluctuations and maintain their performance. The findings contribute to the development of marketing theory and offer practical \ngeneral discussion:  This research aims to provide guidance for managing industrial businesses through business cycles (BCs) using relational marketing (RM) and inter-organizational learning theories. The study focuses on price, cost-to-serve, and expectation of continuity variations during a BC in an emerging economy. The process approach used follows a temporal structure and increases managerial relevance. The findings show that large size, market leader suppliers can successfully navigate a BC by utilizing various RM mechanisms. \n'

insights = """
1) The article highlights the significance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns.
2) The study identifies three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation.
3) The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers.
4) The authors propose a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms, providing strategies for effectively managing each quadrant during times of economic crisis and recovery.
5) The study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions.
6) The authors argue that interorganizational relationships are crucial for coping with economic uncertainty and that buyer-seller relationships should be managed through effective communication openness, technical involvement, and customer value anticipation.
7) The findings have important theoretical implications for marketing literature, as they provide evidence for the key role of customer value anticipation and extend the dialectical view on buyer-seller relationships.
8) The study also contributes to the dark side of B2B relationships' theoretical underpinnings by showing that inherent tension created in a BC can be managed by RM mechanisms.
9) The investigation of buyer-seller relationships through a BC in an emerging economy answers calls for more marketing research in non-advanced settings.
10) The study highlights the importance of managing B2B relationships during economic downturns and provides insights into how suppliers can navigate economic fluctuations and maintain their performance.
"""

llm = Replicate(
    model='meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    model_kwargs={"top_k": 50, "top_p": 0.95, "max_tokens": 500, "temperature": 0.5},
)

class Insights(BaseModel):
    summaries: str = Field(description="summaries for each section of the article")
    insights: List[str] = Field(description="list of key insights extracted from the article")

insights_query = "Provide insights about the article."

parser = PydanticOutputParser(pydantic_object=Insights)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

chain.invoke({"query": insights_query})

Insights(summaries=section_summaries,insights=insights)