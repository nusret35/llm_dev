import replicate
from dotenv import load_dotenv

class Stream_Output_Generator:
    def __init__(self, model, top_p=1, temperature=0.5, max_new_tokens=500, min_new_tokens=-1, repetition_penalty=1.15):
        model_dict = {
            '70B':'meta/llama-2-70b-chat',
            '13B':'meta/llama-2-13b-chat'
        }
        if model in model_dict:
            self.model = model_dict[model]
        else:
            self.model = model_dict['70B']
        self.top_p = top_p
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        self.min_new_tokens = min_new_tokens
        self.repetition_penalty = repetition_penalty

    def send_prompt(self, prompt, sys_prompt=None,callback=None):
        response = ""
        load_dotenv()
        for event in replicate.stream(
            self.model,
            input={
                "debug": False,
                "top_p": self.top_p,
                "temperature": self.temperature,
                "max_new_tokens": self.max_new_tokens,
                "min_new_tokens": self.min_new_tokens,
                "prompt": prompt,
                "system_prompt": sys_prompt if sys_prompt else "",
                "repetition_penalty": self.repetition_penalty
            }

        ):
            #print(str(event), end="")
            response += str(event)
            if callback:
                callback(str(event))

        return response

    def extract_insights(self, section_summaries, user_persona, user_purpose, regeneration, reason_for_regeneration,callback=None):

        prompt = f"""
            Provide insights about the article from the given summaries for each section of the article. This is the section summaries:
            {section_summaries}

            Give the insights in the following format:

            * insight 1
            * insight 2
            * insight 3
            * insight 4
            ...

            Do not include any introductory sentence.

            Do not include incomplete sentences.

            Generate these insights to be used for {user_purpose} by a/an {user_persona}.
        """
        # system_prompt = "You are a tool that generates insights."
        assert section_summaries != ""
        response = self.send_prompt(prompt,callback=callback)
        return response
    
    def generate_title(self, insights, user_persona, user_purpose, callback=None):
        prompt = f"""
            From the given insights,
            {insights}
            provide a title. Output should be in the following format: 
            {{
                "title": "title string"
            }}

            Generate this title to be used for {user_purpose} by a/an {user_persona}.
        """
        response = self.send_prompt(prompt,callback=callback)
        return response

    def choose_images(self, insights, image_titles, user_persona, user_purpose):
        prompt = f"""
            Choose the most important 3 images of the article using the image titles in the article and generated insights about the article. This is the image titles:
            {image_titles}
            
            This is the insights:
            {insights}

            Give the descriptions of the selected images in the following format:
            {{
                "Fig./Table 1. Title": "string explanation",
                "Fig./Table 2. Title": "string explanation",
                "Fig./Table 3. Title": "string explanation"
            }}
            Do not include any introductory sentence.

            Select these important images to be used for {user_purpose} by a/an {user_persona}.
        """
        system_prompt = "You are a tool that selects the most important images."
        response = self.send_prompt(prompt, system_prompt)
        return response


##TEST##
if __name__ == "__main__":
    section_summaries = 'abstract:    \nBusiness cycles (BCs) can alter the conditions for long-term business-to-business (B2B) relationships. Based on \nrelationship marketing (RM) and interorganizational learning theories, the authors propose a model that explains \nrelationship configurations that reveal opportunities under economic uncertainty. In the Pilot Study, the authors \nidentify key mechanisms of RM process (communication openness, technical involvement, and customer value \nanticipation) and performance outcomes (price, cost-to-serve, and expectation of relationship continuity) from \nthe supplier’s view. In Study 1, the proposed model is tested with a sample of large size, market leader firms in \ntimes of economic crisis (T1). In Study 2, conducting a multi-group analysis, the same sample is used to test the \nmodel in times of recovery/expansion (T2). The findings offer directions for suppliers on how to leverage B2B \nrelationships through a BC. Particularly, the authors indicate that supplier’s performance is influenced differ-\nently by RM mechanisms during times of economic crisis versus times of recovery/expansion.   \nintroduction:  The article discusses the importance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns. The authors argue that RM can help firms navigate economic fluctuations and maintain long-term relationships with customers. They identify three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation. These mechanisms have direct and indirect effects on supplier performance, and their impact varies across different stages of the business cycle. The study contributes to both RM and business cycle literature by providing actionable strategies for managing B2B relationships during economic turbulence. The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers. \nmanagerial implications:  This section discusses the managerial implications of the proposed Relationship Mechanisms (RM) for achieving firm goals during times of economic crisis and recovery. The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms: Communication Openness (COM), Technical Involvement (INV), and Customer Value Anticipation (CVA). Each quadrant is named based on the empirical results and includes strategies for effectively managing each quadrant.\n\nThe first quadrant, "Value anticipation based on distant communication," focuses on increasing the selling price (PR) during an economic crisis. Suppliers should reduce their technical involvement with customers while still being able to enhance customer value anticipation through remote communication.\n\nThe second quadrant, "Cost-oriented joint collaboration," aims to reduce the cost-to-serve (CTS) during an economic crisis. Suppliers should establish strong technical involvement with customers, focusing on cost-reducing opportunities and generating savings for both actors.\n\nThe third quadrant, "Dyadic top management consensus," seeks to enhance the expectation of continuity (EC) during an economic crisis. Suppliers should exploit top management consensus with customers, nudging top managers to reach consensus on how to face the economic crisis together.\n\nThe fourth \ntheoretical implications:  This study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions. The authors argue that interorganizational relationships are crucial for coping with economic uncertainty and that buyer-seller relationships should be managed through effective communication openness, technical involvement, and customer value anticipation. They conducted a quantitative study in Chile, an emerging economy, and found that these mechanisms help transform tension created by economic fluctuations into learning opportunities for adapting the relationship during a business cycle (BC).\n\nThe findings have important theoretical implications for marketing literature, as they provide evidence for the key role of customer value anticipation and extend the dialectical view on buyer-seller relationships. The study also contributes to the dark side of B2B relationships\' theoretical underpinnings by showing that inherent tension created in a BC can be managed by RM mechanisms. Additionally, the investigation of buyer-seller relationships through a BC in an emerging economy answers calls for more marketing research in non-advanced settings.\n\nIn summary, the study highlights the importance of managing B2B relationships during economic downturns and provides insights into how suppliers can navigate economic fluctuations and maintain their performance. The findings contribute to the development of marketing theory and offer practical \ngeneral discussion:  This research aims to provide guidance for managing industrial businesses through business cycles (BCs) using relational marketing (RM) and inter-organizational learning theories. The study focuses on price, cost-to-serve, and expectation of continuity variations during a BC in an emerging economy. The process approach used follows a temporal structure and increases managerial relevance. The findings show that large size, market leader suppliers can successfully navigate a BC by utilizing various RM mechanisms. \n'
    insights = """
        Sure, here are the insights from the article summary:

        1. Effective communication openness, technical involvement, and customer value anticipation can help transform tension created by economic fluctuations into learning opportunities for adapting the relationship during a business cycle (BC).
        2. The findings provide evidence for the key role of customer value anticipation and extend the dialectical view on buyer-seller relationships.
        3. The study also contributes to the dark side of B2B relationships' theoretical underpinnings by showing that inherent tension created in a BC can be managed by RM mechanisms.
        4. The investigation of buyer-seller relationships through a BC in an emerging economy answers calls for more marketing research in non-advanced settings.
        5. The study highlights the importance of managing B2B relationships during economic downturns and provides insights into how suppliers can navigate economic fluctuations and maintain their performance.
        6. The findings contribute to the development of marketing theory and offer practical guidance for managing industrial businesses through BCs using RM and inter-organizational learning theories.
        7. Large size, market leader suppliers can successfully navigate a BC by utilizing various RM mechanisms.
    """
    # Get user persona
    user_persona =  "Business Professional"
    # Get user's purpose for getting these insights
    user_purpose = "Business Strategy Development"
    image_titles = "'Fig. 1. Overview of the Research Method (Page:4)\nFig. 2. Conceptual Model (Page:5)\nTable 1. Sample Characteristics (Page:6)\nTable 2. CFA Results (Page:7)\nTable 3. Construct Correlations and AVEs (Page:7)\nTable 4. MIIV-2SLS Results (Page:7)\nTable 5. Measurement Invariance (Page:9)\nTable 6. Results – Multi-group Analysis (from MLR estimation) (Page:9)\nTable 7. Mechanisms for Successful Relationship Management of a Business Cycle (BC) (Page:9)\nFig. 3. Relationship Marketing (RM) Strategies Matrix (Page:11)\n'"
    stream_output_generator = Stream_Output_Generator("13B")
    insights = stream_output_generator.extract_insights(section_summaries, user_persona, user_purpose, "", "")
    print()
    important_images = stream_output_generator.choose_images(insights,image_titles, user_persona, user_purpose)
    print()
    print(insights+"\n")
    print(important_images+"\n")