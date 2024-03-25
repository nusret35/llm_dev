from pydantic import BaseModel
from PIL import Image
from io import BytesIO

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
    def __init__(self,title,insights=None, images_and_explanations = None):
        self.title = title
        self.insights = insights
        self.images_and_explanations = images_and_explanations


class UploadedArticle(metaclass=Singleton):
    def __init__(self,pdf_file,found_images=None):
        self.pdf_file = pdf_file
        self.found_images = found_images or {}
    
    
    @classmethod
    def generate_report(cls):
        
        title = "Goodtimes Badtimes"
        insights = [
            "The article highlights the significance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns.",
            "The study identifies three key mechanisms that explain how RM affects supplier performance during economic contraction and recovery: communication openness, technical involvement, and customer value anticipation.",
            "The findings suggest that firms should focus on building trust, sharing knowledge, and fostering collaboration to adapt to changing market conditions and maintain strong relationships with their customers.",
            "The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of the three RM mechanisms, and provide strategies for effectively managing each quadrant.",
            "The study investigates how business-to-business (B2B) suppliers can navigate economic downturns and maintain their performance during recessions."
        ]

        pil_image = Image.open('/Users/nusretkizilaslan/Downloads/gs.png')
        image_bytes_io = BytesIO()
        pil_image.save(image_bytes_io, format='PNG')
        image_bytes_io.seek(0)

        images_and_explanations = {
            'Fig. 1 Some Picture': {
                'image':image_bytes_io,
                'explanation': 'image explanation'
            }
        }

        return Report(title=title,
                      insights=insights,
                      images_and_explanations=images_and_explanations)

