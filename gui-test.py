import streamlit as st

# Set the page to wide mode which allows the content to use more horizontal space
st.set_page_config(layout="wide")

def create_images_in_container(images_and_explanations):
    items = images_and_explanations
    if items:
        num_columns = 3
        # We'll use all the available space in the page for the columns.
        columns = st.columns(num_columns)
        index = 0
        for key, value in items.items():
            if value['image']:  # Ensure there's an image to display
                col = columns[index % num_columns]  # Dynamic column assignment
                with col:
                    st.write(f"### {key}")
                    st.write(value['explanation'])
                    st.image(image=value['image'], use_column_width=True)
            else:
                col = columns[index % num_columns]  # Dynamic column assignment
                with col:
                    st.write(f"### {key}")
                    st.write(value['explanation'])
            index += 1
        st.markdown('---')  # Add spacing or separation

images_and_explanations = {
        'Fig. 1. Overview of the Research Method': {
            'explanation': 'Provides an outline of the methodology used in the study, including the research design, data collection methods, and analysis techniques.',
            'image': "https://static.streamlit.io/examples/cat.jpg"
        },
        'Table 3. Construct Correlations and AVEs': {
            'explanation': 'Presents the results of the construct correlations and average variance extracted (AVE) analysis, which assess the validity and reliability of the measurement model.',
            'image': None  # No image for this item
        },
        'Fig. 3. Relationship Marketing (RM) Strategies Matrix': {
            'explanation': 'Illustrates the RM strategies matrix, which identifies six quadrants representing different combinations of relationship mechanisms that companies can use to achieve their goals during times of economic crisis and recovery.',
            'image': "https://static.streamlit.io/examples/cat.jpg"
        }
    }

create_images_in_container(images_and_explanations)
