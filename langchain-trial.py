import os
import json
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.llms import Replicate

load_dotenv()

api_key = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = api_key

insight_schema=json.dumps({
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "Insight1": {
      "type": "string",
      "format": "sentence as a bullet point",
      "description": "The first insight extracted from the text."
    },
    "Insight2": {
      "type": "string",
      "format": "sentence as a bullet point",
      "description": "The second insight extracted from the text."
    },
    "Insight3": {
      "type": "string",
      "format": "sentence as a bullet point",
      "description": "The third insight extracted from the text."
    },
    "Insight4": {
      "type": "string",
      "format": "sentence as a bullet point",
      "description": "The fourth insight extracted from the text."
    },
    "Insight5": {
      "type": "string",
      "format": "sentence as a bullet point",
      "description": "The fifth insight extracted from the text."
    },
    "Insight6": {
      "type": "string",
      "format": "sentence as a bullet point",
      "description": "The sixth insight extracted from the text."
    },
    "Insight7": {
      "type": "string",
      "format": "sentence as a bullet point",
      "description": "The seventh insight extracted from the text."
    }
  },
  "required": ["Insight1", "Insight2", "Insight3", "Insight4", "Insight5"],
  "additionalProperties": False
})

section_summaries = 'abstract:    \nBusiness cycles (BCs) can alter the conditions for long-term business-to-business (B2B) relationships. Based on \nrelationship marketing (RM) and interorganizational learning theories, the authors propose a model that explains \nrelationship configurations that reveal opportunities under economic uncertainty. In the Pilot Study, the authors \nidentify key mechanisms of RM process (communication openness, technical involvement, and customer value \nanticipation) and performance outcomes (price, cost-to-serve, and expectation of relationship continuity) from \nthe supplier’s view. In Study 1, the proposed model is tested with a sample of large size, market leader firms in \ntimes of economic crisis (T1). In Study 2, conducting a multi-group analysis, the same sample is used to test the \nmodel in times of recovery/expansion (T2). The findings offer directions for suppliers on how to leverage B2B \nrelationships through a BC. Particularly, the authors indicate that supplier’s performance is influenced differ-\nently by RM mechanisms during times of economic crisis versus times of recovery/expansion.   \nintroduction:  The article discusses the importance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns. The authors argue that RM can help firms navigate economic fluctuations and maintain long-term relationships with customers. They identify three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation. These mechanisms have direct and indirect effects on supplier performance, and their impact varies across different stages of the business cycle. The study contributes to both RM and business cycle literature by providing actionable strategies for managing B2B relationships during economic turbulence. The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers. \nmanagerial implications:  This section discusses the managerial implications of the proposed Relationship Mechanisms (RM) for achieving firm goals during times of economic crisis and recovery. The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms: Communication Openness (COM), Technical Involvement (INV), and Customer Value Anticipation (CVA). Each quadrant is named based on the empirical results and includes strategies for effectively managing each quadrant.\n\nThe first quadrant, "Value anticipation based on distant communication," focuses on increasing the selling price (PR) during an economic crisis. Suppliers should reduce their technical involvement with customers while still being able to enhance customer value anticipation through remote communication.\n\nThe second quadrant, "Cost-oriented joint collaboration," aims to reduce the cost-to-serve (CTS) during an economic crisis. Suppliers should establish strong technical involvement with customers, focusing on cost-reducing opportunities and generating savings for both actors.\n\nThe third quadrant, "Dyadic top management consensus," seeks to enhance the expectation of continuity (EC) during an economic crisis. Suppliers should exploit top management consensus with customers, nudging top managers to reach consensus on how to face the economic crisis together.\n\nThe fourth \ntheoretical implications:  This study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions. The authors argue that interorganizational relationships are crucial for coping with economic uncertainty and that buyer-seller relationships should be managed through effective communication openness, technical involvement, and customer value anticipation. They conducted a quantitative study in Chile, an emerging economy, and found that these mechanisms help transform tension created by economic fluctuations into learning opportunities for adapting the relationship during a business cycle (BC).\n\nThe findings have important theoretical implications for marketing literature, as they provide evidence for the key role of customer value anticipation and extend the dialectical view on buyer-seller relationships. The study also contributes to the dark side of B2B relationships\' theoretical underpinnings by showing that inherent tension created in a BC can be managed by RM mechanisms. Additionally, the investigation of buyer-seller relationships through a BC in an emerging economy answers calls for more marketing research in non-advanced settings.\n\nIn summary, the study highlights the importance of managing B2B relationships during economic downturns and provides insights into how suppliers can navigate economic fluctuations and maintain their performance. The findings contribute to the development of marketing theory and offer practical \ngeneral discussion:  This research aims to provide guidance for managing industrial businesses through business cycles (BCs) using relational marketing (RM) and inter-organizational learning theories. The study focuses on price, cost-to-serve, and expectation of continuity variations during a BC in an emerging economy. The process approach used follows a temporal structure and increases managerial relevance. The findings show that large size, market leader suppliers can successfully navigate a BC by utilizing various RM mechanisms. \n'

llm = Replicate(
    model="andreasjansson/llama-2-70b-chat-gguf:51b87745820e6a8de6ad7bceb340bb6ba85f7ba6dab8e02bb7e2de0853425f4c",
    model_kwargs={"top_k": 50, "top_p": 0.95, "max_tokens": 500, "temperature": 0.8, "jsonschema": insight_schema},
)

prompt = 'You are a helpful assistant that extracts key insights from an article that is summarized as\n' + section_summaries + '\nAs an output, you should provide concise insights. Respond with json that adheres to the following jsonschema:\n {jsonschema}'  
print(prompt)
response = llm(prompt)
print(response)

