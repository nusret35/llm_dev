import os
from dotenv import load_dotenv
from langchain.llms import Replicate
from .article_parser import shorten_text

class Langchain_Extractor:
    def __init__(self, model, top_p=0.95, temperature=0.5, max_new_tokens=500, min_new_tokens=-1, repetition_penalty=1.15):
        model_dict = {
            '70B':'meta/llama-2-70b-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48',
            '13B':'meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d'
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

        
    def send_prompt(self, prompt, callback=None):
        load_dotenv()
        llm = Replicate(
            model=self.model,
            model_kwargs={"top_p": self.top_p, "max_tokens": self.max_new_tokens, "temperature": self.temperature, "min_new_tokens": self.min_new_tokens, "repetition_penalty": self.repetition_penalty}
        )
        response = llm(prompt)

        if callback:
            callback(response)

        return response
    
    
    def summarize(self, section_text):
        prompt = f"""
            Provide a summary of the text which is a section of an article. This is the section text:
            {section_text}
        """
        try :
            response = self.send_prompt(prompt)
        except:
            # Summary is too long. Exclude the last sentence
            shortened = shorten_text(section_text)

            # Recursively call the function until it fits the token size
            response = self.summarize(shortened)

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
        assert image_titles != ""
        prompt = f"""
            Choose the most important 3 images of the article using the image titles in the article and generated insights about the article. This is the image titles:
            {image_titles}
            
            This is the insights:
            {insights}

            Give the descriptions of the selected images in the given JSON format. Always include the commas:
            {{
                "Fig./Table 1. Title": "string explanation",
                "Fig./Table 2. Title": "string explanation",
                "Fig./Table 3. Title": "string explanation"
            }}
            Do not include any introductory sentence.

            Select these important images to be used for {user_purpose} by a/an {user_persona}.
        """
        response = self.send_prompt(prompt)
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
    
    
def main():
    section_summaries = 'abstract:    \nBusiness cycles (BCs) can alter the conditions for long-term business-to-business (B2B) relationships. Based on \nrelationship marketing (RM) and interorganizational learning theories, the authors propose a model that explains \nrelationship configurations that reveal opportunities under economic uncertainty. In the Pilot Study, the authors \nidentify key mechanisms of RM process (communication openness, technical involvement, and customer value \nanticipation) and performance outcomes (price, cost-to-serve, and expectation of relationship continuity) from \nthe supplier’s view. In Study 1, the proposed model is tested with a sample of large size, market leader firms in \ntimes of economic crisis (T1). In Study 2, conducting a multi-group analysis, the same sample is used to test the \nmodel in times of recovery/expansion (T2). The findings offer directions for suppliers on how to leverage B2B \nrelationships through a BC. Particularly, the authors indicate that supplier’s performance is influenced differ-\nently by RM mechanisms during times of economic crisis versus times of recovery/expansion.   \nintroduction:  The article discusses the importance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns. The authors argue that RM can help firms navigate economic fluctuations and maintain long-term relationships with customers. They identify three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation. These mechanisms have direct and indirect effects on supplier performance, and their impact varies across different stages of the business cycle. The study contributes to both RM and business cycle literature by providing actionable strategies for managing B2B relationships during economic turbulence. The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers. \nmanagerial implications:  This section discusses the managerial implications of the proposed Relationship Mechanisms (RM) for achieving firm goals during times of economic crisis and recovery. The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms: Communication Openness (COM), Technical Involvement (INV), and Customer Value Anticipation (CVA). Each quadrant is named based on the empirical results and includes strategies for effectively managing each quadrant.\n\nThe first quadrant, "Value anticipation based on distant communication," focuses on increasing the selling price (PR) during an economic crisis. Suppliers should reduce their technical involvement with customers while still being able to enhance customer value anticipation through remote communication.\n\nThe second quadrant, "Cost-oriented joint collaboration," aims to reduce the cost-to-serve (CTS) during an economic crisis. Suppliers should establish strong technical involvement with customers, focusing on cost-reducing opportunities and generating savings for both actors.\n\nThe third quadrant, "Dyadic top management consensus," seeks to enhance the expectation of continuity (EC) during an economic crisis. Suppliers should exploit top management consensus with customers, nudging top managers to reach consensus on how to face the economic crisis together.\n\nThe fourth \ntheoretical implications:  This study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions. The authors argue that interorganizational relationships are crucial for coping with economic uncertainty and that buyer-seller relationships should be managed through effective communication openness, technical involvement, and customer value anticipation. They conducted a quantitative study in Chile, an emerging economy, and found that these mechanisms help transform tension created by economic fluctuations into learning opportunities for adapting the relationship during a business cycle (BC).\n\nThe findings have important theoretical implications for marketing literature, as they provide evidence for the key role of customer value anticipation and extend the dialectical view on buyer-seller relationships. The study also contributes to the dark side of B2B relationships\' theoretical underpinnings by showing that inherent tension created in a BC can be managed by RM mechanisms. Additionally, the investigation of buyer-seller relationships through a BC in an emerging economy answers calls for more marketing research in non-advanced settings.\n\nIn summary, the study highlights the importance of managing B2B relationships during economic downturns and provides insights into how suppliers can navigate economic fluctuations and maintain their performance. The findings contribute to the development of marketing theory and offer practical \ngeneral discussion:  This research aims to provide guidance for managing industrial businesses through business cycles (BCs) using relational marketing (RM) and inter-organizational learning theories. The study focuses on price, cost-to-serve, and expectation of continuity variations during a BC in an emerging economy. The process approach used follows a temporal structure and increases managerial relevance. The findings show that large size, market leader suppliers can successfully navigate a BC by utilizing various RM mechanisms. \n'
    langchain_extractor_70B = Langchain_Extractor("70B")
    section_text="'The positive effects and dynamics of relationship marketing (RM) \nhave been well established in the literature (e.g., Palmatier, Dant, \nGrewal, & Evans, 2006; Zhang, Watson IV, Palmatier, & Dant, 2016), \nespecially for business-to-business (B2B) settings (Mora Cortez & \nJohnston, 2017). However, the influence of increasing competition, \ncustomer complexity, and market turbulence is creating a latent hazard \nfor the sustainability of established buyer–seller relationships. Nordin \nand Ravald (2016) assert that a long-term relationship can suffer from a \nchange in customer needs or when the supplier’s portfolio and strategy \nare modified. These changes are commonly triggered by fluctuations in \nthe business environment (Dekimpe & Deleersnyder, 2018). One key \ncontextual factor is a change in the economic trajectory. The contraction \nfacet of a business cycle (BC) is characterized by a downturn in gross \ndomestic product (GDP) and local currency depreciation. For example, \nThailand experienced a drop in GDP growth from 5.5% to −10% during \nthe Asian crisis with a fall of the Thai baht from approximately 25 baht \nper 1 USD to>50 baht (Grewal & Tansuhaj, 2001). In this scenario, high \nlevels of uncertainty and related threats endanger the viability of an \norganization (Ellram & Krause, 2014). Therefore, companies strive to \nmanage and survive economic fluctuations. Crises emerge from a bank \nrun and/or correction in the exchange rate of a country. The latter can \nbe identified more objectively (Dutt & Padmanabhan, 2011) and, thus, is \nthe focus of this research. \nExtant literature on RM suggests that interorganizational learning is \nan important way for firms to access markets, develop marketing re-\nsponses, and leverage process capabilities of partners (e.g., Im & Rai, \n2008; Mora Cortez & Hidalgo, 2022; Yang, Fang, Fang, & Chou, 2014). \nIn this sense, Williamson (1991) recognizes that bilateral relationships \ncan be established to minimize potential governance problems during \nthe exchange. The advantage of organizations over markets (i.e., nomi-\nnal price dependency) and hierarchy (i.e., authoritative control) lies in \nleveraging the human ability to take initiative, cooperate, and learn \n(Ghoshal & Moran, 1996; Im & Rai, 2008). Therefore, if organizations \nfail to create the relationship context necessary to build new knowledge, \neconomic failure is anticipated (Holmqvist, 2003; Ghoshal & Moran, \n1996). Particularly, macro-economic uncertainty introduces relevant \ncontingencies to the exchange, creating an adaptation problem (Heide, \n1994). \nPrior research on transformational relationship events has generally \nfocused on ad hoc strategies (e.g., Salo, T¨ahtinen, & Ulkuniemi, 2009) \nand the attitudes and behaviors of practitioners (e.g., Nordin & Ravald, \n2016), neglecting the potential impact of environmental turbulence. The \nrepercussions of economic swings have been widely investigated from \ndifferent perspectives, including those of market orientation (Brenˇciˇc, \n* Corresponding author. \nE-mail addresses: rfmc@sam.sdu.dk (R. Mora Cortez), wesleyj@gsu.edu (W.J. Johnston), michael.ehret@uni-graz.at (M. Ehret).  \n<image: ICCBased(RGB,sRGB v4 ICC preference perceptual intent beta), width: 248, height: 271, bpc: 8>Contents lists available at ScienceDirect \nJournal of Business Research \njournal homepage: www.elsevier.com/locate/jbusres \n<image: ICCBased(RGB,sRGB v4 ICC preference perceptual intent beta), width: 236, height: 298, bpc: 8>https://doi.org/10.1016/j.jbusres.2023.114063 \nReceived 16 November 2022; Received in revised form 18 May 2023; Accepted 21 May 2023   \nJournal of Business Research 165 (2023) 114063\nPfajfar, & Raskovik, 2012), psychology (Halpern, 1989), social policy \n(Weick, 1988), sales force activities (Lee & Cadogan, 2009), strategic \ncapabilities (Grewal & Tansuhaj, 2001), technological structure (Pau-\nchant & Douville, 1994), and trust and privacy on the Internet (Luo, \n2002). In an effort to keep developing the understanding of buyer–seller \nrelationships, Nordin and Ravald (2016, p. 2496) called for research \nregarding the need to explore relationship dynamics in business contexts \ncharacterized by high turbulence following quantitative testing. A BC \naccounts for high turbulence during economic contraction (Ellram & \nKrause, 2014; Jüttner & Maklan, 2011), providing an appropriate \nsetting for this research. \nIndustrial suppliers, such as Grainger, successfully navigated \ncustomer relationships during the subprime mortgage crisis and read-\napted when the economy expanded again, making clear that firms adjust \ntheir behavior during a BC (Dixon & Adamson, 2012). What have they \ndone? Buyers and sellers, via social networks, foster communication, \ninvolvement, and value anticipation to adjust the direction of a rela-\ntionship. Previous research on RM has focused on general strategies for \nmanaging relationship performance, such as identifying learning pro-\ncesses to improve absorptive capacity of firms (Lichtenthaler, 2009), \nknowledge \nsharing \nambidexterity \n(Im \n& \nRai, \n2008), \nconflict-coordination learning based on positive attitudes and avoidance \nbehaviors (Chang & Gotcher, 2010), accounting for strength-of-ties by \nrelational embeddedness and knowledge redundancy (Rindfleisch & \nMoorman, 2001), or interactive learning involving experience sharing \nand shared interpretation among individuals of different organizations \n(Yang et al., 2014). However, none of these valuable studies has \nexplained how a firm should adapt relationship mechanisms during a \nBC. \nA review of the BC marketing literature indicates the need for \nresearch in a B2B setting, extending the study of economic fluctuations \nbeyond the often-used U.S. context (see Dekimpe & Deleersnyder, \n2018). Emerging economies are notorious for a substantial share and a \ncritical role of interorganizational relationships in business organization \n(Khana & Palepu, 2010). For a substantial share of emerging economies, \ncommodities dominate gross domestic products (GDP) that are noto-\nrious for cyclical behavior (Drechsel & Tenreyo, 2018). \nTo the best of our knowledge, there is no previous work that in-\ntegrates a BC, an industrial setting, and an emerging economy. We add \nto this body of research by studying the impact of RM process on \ndetermining the specific contribution of long-life customers in emerging \neconomies during periods of contraction and expansion. We investigate \nthese phenomena in the context of the recent fall of commodities. In \nbrief, this paper will address this research gap and contribute a frame-\nwork that answers: (1) How is RM process linked to firm performance \nduring a BC (from the supplier’s perspective)? and (2) What are the different \nmechanisms related to increased firm performance during both times of crisis \n(contraction) and recovery (expansion)? \nWe adopt RM and interorganizational learning theories to identify \nrelationship tenets that help suppliers find the way to sustain or increase \nperformance from their B2B long-life customers during economic \nswings. We contribute to the RM literature and BC literature. First, we \nidentify the key relationship process mechanisms explaining the diver-\ngence between managing B2B markets in times of economic crisis and \nrecovery: (A) communication openness, (B) technical involvement, and \n(C) customer value anticipation, which have direct and indirect effects \non the supplier’s performance. Second, we test the difference in the \nmodeled relationship mechanisms, allowing the identification of clear \nstrategies to manage a BC. This is consistent with calls to make the \nrecommendations in BC studies more actionable and concrete (e.g., \nDekimpe & Deleersnyder, 2018). Finally, unlike most extant work in the \nRM and BC domains that has examined performance as an aggregative \nmeasure (e.g., Grewal & Tansuhaj, 2001) or through price fluctuations \n(e.g., Gordon, Goldfarb, & Li, 2013) at the firm or category level (see \nDekimpe & Deleersnyder, 2018, p. 33), we consider three outcome \nvariables: (1) selling price, (2) cost-to-serve, and (3) expectation of \nrelationship continuity, at the customer level. The recent coronavirus \nsituation and Ukraine conflict are calling for more research in crisis \nsettings (e.g., Mora Cortez & Johnston, 2020), positioning this study as \ntimely and needed.'"
    response = langchain_extractor_70B.summarize(section_text)
    print(response)
    insights = """
    Sure, here are the insights from the article summary:

    1.⁠ ⁠Relationship marketing (RM) can help businesses navigate economic downturns and maintain their performance during recessions.
    2.⁠ ⁠The study found that RM mechanisms have direct and indirect effects on supplier performance during economic contraction and recovery, and their impact varies across different stages of the business cycle.
    3.⁠ ⁠Building trust, sharing knowledge, and fostering collaboration with customers is crucial for managing B2B relationships during economic turbulence.
    4.⁠ ⁠Suppliers should focus on increasing selling price (PR) during an economic crisis by reducing technical involvement with customers while still enhancing customer value anticipation through remote communication.
    5.⁠ ⁠Cost-oriented joint collaboration can reduce cost-to-serve (CTS) during an economic crisis, and suppliers should establish strong technical involvement with customers to generate savings for both actors.
    6.⁠ ⁠Top management consensus with customers is essential in enhancing expectation of continuity (EC) during an economic crisis.
    7.⁠ ⁠Effective communication openness, technical involvement, and customer value anticipation can transform tension created by economic fluctuations into learning opportunities for adapting the relationship during a BC.
    """
    response = langchain_extractor_70B.generate_title(insights,"","")
    print(response)

def main2():
    section_summaries = 'abstract:    \nBusiness cycles (BCs) can alter the conditions for long-term business-to-business (B2B) relationships. Based on \nrelationship marketing (RM) and interorganizational learning theories, the authors propose a model that explains \nrelationship configurations that reveal opportunities under economic uncertainty. In the Pilot Study, the authors \nidentify key mechanisms of RM process (communication openness, technical involvement, and customer value \nanticipation) and performance outcomes (price, cost-to-serve, and expectation of relationship continuity) from \nthe supplier’s view. In Study 1, the proposed model is tested with a sample of large size, market leader firms in \ntimes of economic crisis (T1). In Study 2, conducting a multi-group analysis, the same sample is used to test the \nmodel in times of recovery/expansion (T2). The findings offer directions for suppliers on how to leverage B2B \nrelationships through a BC. Particularly, the authors indicate that supplier’s performance is influenced differ-\nently by RM mechanisms during times of economic crisis versus times of recovery/expansion.   \nintroduction:  The article discusses the importance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns. The authors argue that RM can help firms navigate economic fluctuations and maintain long-term relationships with customers. They identify three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation. These mechanisms have direct and indirect effects on supplier performance, and their impact varies across different stages of the business cycle. The study contributes to both RM and business cycle literature by providing actionable strategies for managing B2B relationships during economic turbulence. The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers. \nmanagerial implications:  This section discusses the managerial implications of the proposed Relationship Mechanisms (RM) for achieving firm goals during times of economic crisis and recovery. The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms: Communication Openness (COM), Technical Involvement (INV), and Customer Value Anticipation (CVA). Each quadrant is named based on the empirical results and includes strategies for effectively managing each quadrant.\n\nThe first quadrant, "Value anticipation based on distant communication," focuses on increasing the selling price (PR) during an economic crisis. Suppliers should reduce their technical involvement with customers while still being able to enhance customer value anticipation through remote communication.\n\nThe second quadrant, "Cost-oriented joint collaboration," aims to reduce the cost-to-serve (CTS) during an economic crisis. Suppliers should establish strong technical involvement with customers, focusing on cost-reducing opportunities and generating savings for both actors.\n\nThe third quadrant, "Dyadic top management consensus," seeks to enhance the expectation of continuity (EC) during an economic crisis. Suppliers should exploit top management consensus with customers, nudging top managers to reach consensus on how to face the economic crisis together.\n\nThe fourth \ntheoretical implications:  This study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions. The authors argue that interorganizational relationships are crucial for coping with economic uncertainty and that buyer-seller relationships should be managed through effective communication openness, technical involvement, and customer value anticipation. They conducted a quantitative study in Chile, an emerging economy, and found that these mechanisms help transform tension created by economic fluctuations into learning opportunities for adapting the relationship during a business cycle (BC).\n\nThe findings have important theoretical implications for marketing literature, as they provide evidence for the key role of customer value anticipation and extend the dialectical view on buyer-seller relationships. The study also contributes to the dark side of B2B relationships\' theoretical underpinnings by showing that inherent tension created in a BC can be managed by RM mechanisms. Additionally, the investigation of buyer-seller relationships through a BC in an emerging economy answers calls for more marketing research in non-advanced settings.\n\nIn summary, the study highlights the importance of managing B2B relationships during economic downturns and provides insights into how suppliers can navigate economic fluctuations and maintain their performance. The findings contribute to the development of marketing theory and offer practical \ngeneral discussion:  This research aims to provide guidance for managing industrial businesses through business cycles (BCs) using relational marketing (RM) and inter-organizational learning theories. The study focuses on price, cost-to-serve, and expectation of continuity variations during a BC in an emerging economy. The process approach used follows a temporal structure and increases managerial relevance. The findings show that large size, market leader suppliers can successfully navigate a BC by utilizing various RM mechanisms. \n'
    langchain_extractor_70B = Langchain_Extractor("70B")
    response = langchain_extractor_70B.extract_insights(section_summaries,"","","","")
    print(response)
    
##TEST##
if __name__ == "__main__":
    main()
