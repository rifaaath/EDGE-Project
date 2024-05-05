import streamlit as st
import requests
import json

url = "http://localhost:8000"

# Title and header
st.set_page_config(layout="wide")
st.title("SKYNET")
st.header("Analyze and Translate Your Code")

# Upload code file
uploaded_file = st.file_uploader("Choose a code file:", type=["txt", "delphi", "cob", "vb", "py"])

# Language selection
selected_language = st.selectbox("Select language:", ["delphi", "cobol", "vb", "cpp"])

# Analyze and translate buttons (disabled initially)
analyze_button = st.button("Analyze Code", disabled=uploaded_file is None)
translate_button = st.button("Translate Code", disabled=uploaded_file is None)

if uploaded_file is not None:
    # # Process code on button click
    if analyze_button:
        code_content = uploaded_file.read().decode("utf-8")
        # print(code_content)
        source_lang = uploaded_file.name.split(".")[-1]  # Extract file extension as source language
        data = {"fileContent": code_content, "source": source_lang, "dest": selected_language}
        # Send POST request with JSON body to Flask API endpoint
        response = requests.post(url+"/api/analyze", json=json.dumps(data))

        if response.status_code == 200:
            # Display results upon successful response
            analysis_results = response.json()["result"]
            print(analysis_results)
            st.write("## Analysis Results")
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Original Code")
                st.code(code_content, language="python")
            with col2:
                st.write("### Translated Code")
                st.code(analysis_results, language="python")  # Display formatted code
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    # if translate_button:
    #     code = uploaded_file.read().decode("utf-8")
    #     translated_code = translate_code(code, selected_language, "target_language")  # Replace with target language
    #     st.write("## Translated Code")
    #     st.code(translated_code, language="python")  # Display formatted code
