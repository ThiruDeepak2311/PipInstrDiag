import streamlit as st
import base64
import pandas as pd
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from PIL import Image
from collections import defaultdict
import os
import openpyxl
import numpy as np
import time

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
from sahi.utils.yolov8 import download_yolov8s_model

yolov8_model_path = r"C:\Users\Deepak Thirukkumaran\Desktop\best.pt"
download_yolov8s_model(yolov8_model_path)

component_names = {
    4: "Gate valve",
    5: "Diaphragm",
    7: "Plug",
    15: "Rotary valve",
    21: "Flange"
}

def process_file(file):
    st.image(file, caption="Uploaded Image")

def pred(file, confidence_threshold):
    detection_model = AutoDetectionModel.from_pretrained(
        model_type='yolov8',
        model_path=yolov8_model_path,
        confidence_threshold=confidence_threshold,
        device="cpu",  # or 'cuda:0'
    )

    image = Image.open(file)

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    start_time = time.time()  # Start measuring the inference time

    result = get_sliced_prediction(
        image,
        detection_model,
        slice_height=200,
        slice_width=200,
        overlap_height_ratio=0.5,
        overlap_width_ratio=0.5,
    )

    end_time = time.time()  # Stop measuring the inference time
    inference_time = end_time - start_time

    result.export_visuals(export_dir="./exports", hide_labels=False)
    st.image("exports/prediction_visual.png", channels="RGB", caption="Inference Image")
    st.write(f"Inference Time: {inference_time:.2f} seconds")

    class_counts = defaultdict(int)
    for object_prediction in result.object_prediction_list:
        class_label = object_prediction.category.name
        class_counts[class_label] += 1

    data = pd.DataFrame({
        "Component Name": [component_names.get(int(class_label), "") for class_label in class_counts.keys()],
        "Count": list(class_counts.values()),
    })

    # Display the table
    st.table(data.style.set_table_styles([{"selector": "table", "props": [("width", "100%")]}]))

    # Add a Download button using streamlit's download_button function
    df = data.to_csv(index=False)
    st.download_button(
        "Download",
        df,
        "file.csv",
        "text/csv",
        key='download-csv'
    )

    # Save DataFrame as an Excel file using openpyxl
    excel_writer = pd.ExcelWriter('predictions.xlsx', engine='openpyxl')
    data.to_excel(excel_writer, index=False, sheet_name='Sheet1')
    workbook = excel_writer.book
    worksheet = workbook['Sheet1']

    # Set column widths
    worksheet.column_dimensions['A'].width = 15.86
    worksheet.column_dimensions['B'].width = 8.05

    # Save the Excel file
    #excel_writer.save()


html_template = """
<div style="border: 2px dashed #ccc; padding: 20px; text-align: center">
    <h4>Drag and Drop Files Here</h4>
    <p style="color: #999">Limit 200MB per file • JPEG, PNG</p>
</div>
"""

st.title("P&ID Component Detection")

st.markdown(html_template, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Pick a file", type=["jpeg", "jpg", "png"], accept_multiple_files=False)

if uploaded_file is not None:
    max_size = 200 * 1024 * 1024  # 200MB
    file_size = len(uploaded_file.getvalue())
    if file_size > max_size:
        st.error("File size exceeds the maximum limit (200MB).")
    else:
        process_file(uploaded_file)
        confidence_threshold = st.slider("Set Confidence Threshold", 0.0, 1.0, 0.4, step=0.05)
        if st.button("Predict"):
            pred(uploaded_file, confidence_threshold)


