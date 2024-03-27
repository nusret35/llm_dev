from PIL import Image
from io import BytesIO
import time
from pipeline.new_solution import NewSolution

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    @classmethod
    def delete_instance(cls):
        del cls._instances[cls]


class Report(metaclass=Singleton):
    _section_summaries = ""
    _title = ""
    _insights = []
    _images_and_explanations = {}


    def __call__(cls,section_summaries="",title="",insights=[], images_and_explanations = {}):
        cls._section_summaries = section_summaries
        cls._title = title
        cls._insights = insights
        cls._images_and_explanations = images_and_explanations

    @classmethod
    def get_section_summaries(cls):
        return cls._section_summaries

    @classmethod
    def set_section_summaries(cls,event):
        cls._section_summaries = event

    
    @classmethod
    def update_title(cls,event):
        cls._title += event
    
    @classmethod
    def update_insights(cls,event):
        if event == "*":
            cls._insights.append("")
        else:
            if len(cls._insights) > 0:
                cls._insights[-1] += event

    


class UploadedArticle(metaclass=Singleton):
    _pdf_file_bytes = None
    _found_images = {}

    @classmethod
    def pdf_file(cls):
        return cls._pdf_file_bytes
    
    @classmethod 
    def set_pdf_file(cls,pdf_bytes):
        cls._pdf_file_bytes = pdf_bytes


    @classmethod
    def generate_report(cls):
        '''
        title = "Goodtimes Badtimes"
        insights = [
            "The article highlights the significance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns.",
            "The study identifies three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation.",
            "The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers.",
            "The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms, and provide strategies for effectively managing each quadrant.",
            "The study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions."
        ]
        '''

        solution = NewSolution(pdf_file_bytes=cls._pdf_file_bytes)
        report = Report()
        section_summaries = solution.generate_summary()
        report.set_section_summaries(section_summaries)

        return report



