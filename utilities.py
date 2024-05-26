import streamlit as st
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
        .normal-font {
            font-size:10px !important;
        }
                
    </style>
    """, unsafe_allow_html=True)

def list_insights(insights):
    all_insights = ""
    for insight in insights:
        all_insights += f'<li class="insight">{insight}</li>'
    
    return all_insights

def create_report(title, insights, images_and_explanations, output_filename):

    def addSignature(doc):
        doc.append(Spacer(1,10))
        doc.append(Paragraph("Created by Insight Extractor", ParagraphStyle(name="report title",
                                                            fontFamily='Helvetica',
                                                            fontSize=9,
                                                            textColor='grey')))
        doc.append(Spacer(1,30))
        return doc

    def addTitle(doc):
        doc.append(Paragraph(title, ParagraphStyle(name="report title",
                                                        fontFamily='Helvetica',
                                                        fontSize=25,
                                                        leading=30,
                                                        alignment=TA_LEFT)))
        doc.append(Spacer(1,30))
        return doc
    
    def addParagpraphs(doc):
        for insight in insights:
            doc.append(Paragraph(f"• {insight}", ParagraphStyle(name="report insight",
                                                          fontFamily='Helvetica',
                                                          fontSize=14,
                                                          leading=16)))
            doc.append(Spacer(1,10))
        return doc
    
    def addImages(doc):
        # To be implemented...
        pass
    
    document = []
    document = addSignature(document)
    document = addTitle(document)
    
    # Build PDF document
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=12, leftMargin=12,
                            topMargin=12, bottomMargin=12)
    pdf.build(addParagpraphs(document))
    
    # Get binary data
    buffer.seek(0)
    binary_data = buffer.getvalue()
    buffer.close()
    
    return binary_data



if __name__ == "__main__":
    # Example usage:
    title = "Monthly Report Monthly Report Monthly Report Monthly Report Monthly Report Monthly Report"
    insights = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam hendrerit nisi sed sollicitudin pellentesque. ",
        "Nunc posuere purus rhoncus pulvinar aliquam. Ut aliquet tristique nisl vitae volutpat. Nulla aliquet porttitor venenatis.",
        "Donec a dui et dui fringilla consectetur id nec massa.  Nam hendrerit nisi sed sollicitudin pellentesque.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam hendrerit nisi sed sollicitudin pellentesque. ",
        "Nunc posuere purus rhoncus pulvinar aliquam. Ut aliquet tristique nisl vitae volutpat. Nulla aliquet porttitor venenatis.",
        "Donec a dui et dui fringilla consectetur id nec massa.  Nam hendrerit nisi sed sollicitudin pellentesque.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam hendrerit nisi sed sollicitudin pellentesque. ",
        "Nunc posuere purus rhoncus pulvinar aliquam. Ut aliquet tristique nisl vitae volutpat. Nulla aliquet porttitor venenatis.",
        "Donec a dui et dui fringilla consectetur id nec massa.  Nam hendrerit nisi sed sollicitudin pellentesque.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam hendrerit nisi sed sollicitudin pellentesque. ",
        "Nunc posuere purus rhoncus pulvinar aliquam. Ut aliquet tristique nisl vitae volutpat. Nulla aliquet porttitor venenatis.",
        "Donec a dui et dui fringilla consectetur id nec massa.  Nam hendrerit nisi sed sollicitudin pellentesque.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam hendrerit nisi sed sollicitudin pellentesque. ",
        "Nunc posuere purus rhoncus pulvinar aliquam. Ut aliquet tristique nisl vitae volutpat. Nulla aliquet porttitor venenatis.",
        "Donec a dui et dui fringilla consectetur id nec massa.  Nam hendrerit nisi sed sollicitudin pellentesque.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam hendrerit nisi sed sollicitudin pellentesque. ",
        "Nunc posuere purus rhoncus pulvinar aliquam. Ut aliquet tristique nisl vitae volutpat. Nulla aliquet porttitor venenatis.",
        "Donec a dui et dui fringilla consectetur id nec massa.  Nam hendrerit nisi sed sollicitudin pellentesque.",
    ]
    images_and_explanations = {
        "Sales Chart": {
            "image": Image("RGB", (400, 200), "gray"),  # Dummy image
            "explanation": "The sales chart shows a steady growth trend throughout the month."
        },
        "Customer Feedback": {
            "image": None,  # No image provided
            "explanation": "Positive feedback received from customers regarding product quality and service."
        }
    }
    output_filename = "monthly_report.pdf"

    create_report(title, insights, images_and_explanations, output_filename)
