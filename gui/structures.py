from PIL import Image
from io import BytesIO
import time
from pipeline.new_solution import NewSolution
from fitz import fitz
import threading
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utilities import create_report

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    @classmethod
    def delete_instance(cls):
        if cls in cls._instances.keys():
            del cls._instances[cls]


class Report(metaclass=Singleton):
    _title = ""
    _insights = []
    _images_and_explanations = {}
    _is_insight_generation_called = False 
    _insights_ready_event = threading.Event()

    def __call__(cls,section_summaries="",title="",insights=[], images_and_explanations = {}):
        cls._section_summaries = section_summaries
        cls._title = title
        cls._insights = insights
        cls._images_and_explanations = images_and_explanations
    
    def __delattr__(cls, __name: str) -> None:
        cls._is_insight_generation_called = False

    @classmethod
    def get_title(cls):
        cls._insights_ready_event.wait() 
        yielded_text = "## "
        for char in cls._title:
            if char != "\n" and char != '"':
                yielded_text += char
                yield yielded_text
                time.sleep(0.01)
                yielded_text = ""
    
    @classmethod
    def get_insights(cls):
        for insight in  cls._insights:
            yielded_text = "• "
            for char in insight:
                yielded_text += char
                yield yielded_text
                time.sleep(0.01)
                yielded_text = ""
            yield "\n"
        cls._insights_ready_event.set() 
    
    @classmethod
    def get_images(cls):
        return cls._images_and_explanations

    @classmethod
    def _update_title(cls,event):
        if event != '"':
            cls._title += event
    
    @classmethod
    def _update_insights(cls,event):
        for char in event:
            if  char == "*":
                cls._insights.append("")
            else:
                if len(cls._insights) > 0:
                    cls._insights[-1] += char

    @classmethod
    def generate_report(cls):
        uploaded_article = UploadedArticle()

        solution = NewSolution(pdf_file_bytes=uploaded_article.get_pdf_file())

        # Generate insights
        insights = solution.generate_insights(uploaded_article.get_section_summaries(),
                                        user_persona=uploaded_article.get_occupation(),
                                        user_purpose=uploaded_article.get_usage(),
                                        regeneration=False,
                                        reason_for_regeneration="",
                                        callback=cls._update_insights)
        
        print(insights)

        cls._images_and_explanations = solution.generate_image_explanations(insights,
                                                                user_persona=uploaded_article.get_occupation(),
                                                                user_purpose=uploaded_article.get_usage(),
                                                            )
        print(cls._images_and_explanations)
        
        cls._title = solution.generate_title(insights=insights,
                                        user_persona=uploaded_article.get_occupation(),
                                        user_purpose=uploaded_article.get_usage(),
                                        )
        
        print(cls._title)

    @classmethod
    def generate_pdf(cls):
        pdf_data = create_report(title=cls._title,
                                    images_and_explanations=cls._images_and_explanations,
                                    insights=cls._insights,
                                    output_filename="report.pdf")

        return pdf_data

class UploadedArticle(metaclass=Singleton):
    _section_summaries = ""
    _pdf_file_bytes = None
    _found_images = {}
    _occupation = ""
    _usage = ""

    @classmethod
    def get_pdf_file(cls):
        return cls._pdf_file_bytes
    
    @classmethod 
    def set_pdf_file(cls,pdf_bytes):
        cls._pdf_file_bytes = pdf_bytes

    @classmethod
    def set_occupation(cls,occupation):
        cls._occupation = occupation

    @classmethod
    def get_occupation(cls):
        return cls._occupation
    
    @classmethod
    def get_usage(cls):
        return cls._usage
    
    @classmethod
    def set_usage(cls,usage):
        cls._usage = usage

    @classmethod
    def set_section_summaries(cls,section_summaries):
        cls._section_summaries = section_summaries

    @classmethod
    def get_section_summaries(cls):
       return cls._section_summaries

    @classmethod
    def generate_section_summaries(cls):
        solution = NewSolution(pdf_file_bytes=cls._pdf_file_bytes)
        cls._section_summaries = solution.generate_summary()
        return cls._section_summaries
        

if __name__ == '__main__':
    section_summaries = 'abstract:    \nBusiness cycles (BCs) can alter the conditions for long-term business-to-business (B2B) relationships. Based on \nrelationship marketing (RM) and interorganizational learning theories, the authors propose a model that explains \nrelationship configurations that reveal opportunities under economic uncertainty. In the Pilot Study, the authors \nidentify key mechanisms of RM process (communication openness, technical involvement, and customer value \nanticipation) and performance outcomes (price, cost-to-serve, and expectation of relationship continuity) from \nthe supplier’s view. In Study 1, the proposed model is tested with a sample of large size, market leader firms in \ntimes of economic crisis (T1). In Study 2, conducting a multi-group analysis, the same sample is used to test the \nmodel in times of recovery/expansion (T2). The findings offer directions for suppliers on how to leverage B2B \nrelationships through a BC. Particularly, the authors indicate that supplier’s performance is influenced differ-\nently by RM mechanisms during times of economic crisis versus times of recovery/expansion.   \nintroduction:  The article discusses the importance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns. The authors argue that RM can help firms navigate economic fluctuations and maintain long-term relationships with customers. They identify three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation. These mechanisms have direct and indirect effects on supplier performance, and their impact varies across different stages of the business cycle. The study contributes to both RM and business cycle literature by providing actionable strategies for managing B2B relationships during economic turbulence. The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers. \nmanagerial implications:  This section discusses the managerial implications of the proposed Relationship Mechanisms (RM) for achieving firm goals during times of economic crisis and recovery. The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms: Communication Openness (COM), Technical Involvement (INV), and Customer Value Anticipation (CVA). Each quadrant is named based on the empirical results and includes strategies for effectively managing each quadrant.\n\nThe first quadrant, "Value anticipation based on distant communication," focuses on increasing the selling price (PR) during an economic crisis. Suppliers should reduce their technical involvement with customers while still being able to enhance customer value anticipation through remote communication.\n\nThe second quadrant, "Cost-oriented joint collaboration," aims to reduce the cost-to-serve (CTS) during an economic crisis. Suppliers should establish strong technical involvement with customers, focusing on cost-reducing opportunities and generating savings for both actors.\n\nThe third quadrant, "Dyadic top management consensus," seeks to enhance the expectation of continuity (EC) during an economic crisis. Suppliers should exploit top management consensus with customers, nudging top managers to reach consensus on how to face the economic crisis together.\n\nThe fourth \ntheoretical implications:  This study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions. The authors argue that interorganizational relationships are crucial for coping with economic uncertainty and that buyer-seller relationships should be managed through effective communication openness, technical involvement, and customer value anticipation. They conducted a quantitative study in Chile, an emerging economy, and found that these mechanisms help transform tension created by economic fluctuations into learning opportunities for adapting the relationship during a business cycle (BC).\n\nThe findings have important theoretical implications for marketing literature, as they provide evidence for the key role of customer value anticipation and extend the dialectical view on buyer-seller relationships. The study also contributes to the dark side of B2B relationships\' theoretical underpinnings by showing that inherent tension created in a BC can be managed by RM mechanisms. Additionally, the investigation of buyer-seller relationships through a BC in an emerging economy answers calls for more marketing research in non-advanced settings.\n\nIn summary, the study highlights the importance of managing B2B relationships during economic downturns and provides insights into how suppliers can navigate economic fluctuations and maintain their performance. The findings contribute to the development of marketing theory and offer practical \ngeneral discussion:  This research aims to provide guidance for managing industrial businesses through business cycles (BCs) using relational marketing (RM) and inter-organizational learning theories. The study focuses on price, cost-to-serve, and expectation of continuity variations during a BC in an emerging economy. The process approach used follows a temporal structure and increases managerial relevance. The findings show that large size, market leader suppliers can successfully navigate a BC by utilizing various RM mechanisms. \n'

    uploaded_article = UploadedArticle()

    uploaded_article.set_pdf_file(fitz.open('/Users/nusretkizilaslan/Downloads/buss_article_2.pdf').tobytes())
    
    uploaded_article.set_section_summaries(section_summaries)

    uploaded_article.set_occupation('academician')

    uploaded_article.set_usage('academic purposes')

    report = Report()

    report.generate_report()

    print(report.get_insights())

