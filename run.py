
import streamlit as st
import pandas as pd
import requests
import logging

# Set up logging
logging.basicConfig(filename='streamlit_log.txt', level=logging.DEBUG)

# Streamlit app to upload Excel file and ask questions

st.title("Natural Language to SQL Streamlit App")

# File upload section
with st.form(key='file_upload_form'):
    file_uploaded = st.file_uploader("Upload Excel File to Store in DB", type=["xlsx"])
    upload_button = st.form_submit_button("Upload File")

# Question and demo section
with st.form(key='demo_form'):
    question = st.text_input("Ask a Question:", key='question_input')
    demo_button = st.form_submit_button("Click to Translate")

# Handle file upload
if file_uploaded and upload_button:
    st.subheader("Uploaded Excel File Preview")
    upload_url = "http://127.0.0.1:5001/upload_excel"
    files = {'file': file_uploaded}
    upload_response = requests.post(upload_url, files=files)
    st.write(upload_response.json())

    if upload_response.status_code == 200:
        st.success(upload_response.json().get('message', 'File uploaded successfully'))
        st.write("Type your Question Below")

# Handle question and demo
if question and demo_button:
    st.subheader("Stored Table Schemas")
    schemas_url = "http://127.0.0.1:5001/get_table_schemas"
    schemas_response = requests.get(schemas_url)

    if schemas_response.status_code == 200:
        table_schemas = schemas_response.json().get('table_schemas', [])
        for schema in table_schemas:
            st.write(f"Table Name: {schema['table_name']}")
            st.code(schema['schema_json'])
            st.write("-" * 50)

        ask_url = "http://127.0.0.1:5001/ask_question"
        params = {'question': question}
        response = requests.post(ask_url, data=params)

        if response.status_code == 200:
            result = response.json()['result']
            sql_query = response.json()['SQL']
            st.subheader("SQL Query:")
            st.code(sql_query)
            st.subheader("Result:")
            st.write(result)
        else:
            st.error("Error fetching result.")
=======
import streamlit as st
import pandas as pd
import requests
import logging

# Set up logging
logging.basicConfig(filename='streamlit_log.txt', level=logging.DEBUG)
import subprocess


# Streamlit app to upload Excel file and ask questions

st.title("Natural Language to SQL Streamlit App")

# File upload section
with st.form(key='file_upload_form'):
    file_uploaded = st.file_uploader("Upload Excel File to Store in DB", type=["xlsx"])
    upload_button = st.form_submit_button("Upload File")

# Question and demo section
with st.form(key='demo_form'):
    question = st.text_input("Ask a Question:", key='question_input')
    demo_button = st.form_submit_button("Click to Translate")

# Handle file upload
if file_uploaded and upload_button:
    st.subheader("Uploaded Excel File Preview")
    upload_url = "https://mocki.io/v1/fd148d60-1ec3-4d43-affb-1bdc36b6896e"
    files = {'file': file_uploaded}
    upload_response = requests.post(upload_url, files=files)
    st.write(upload_response.json())

    if upload_response.status_code == 200:
        st.success(upload_response.json().get('message', 'File uploaded successfully'))
        st.write("Type your Question Below")

# Handle question and demo
if question and demo_button:
    st.subheader("Stored Table Schemas")
    schemas_url = "https://mocki.io/v1/fd148d60-1ec3-4d43-affb-1bdc36b6896e"
    schemas_response = requests.get(schemas_url)

    if schemas_response.status_code == 200:
        table_schemas = schemas_response.json().get('table_schemas', [])
        for schema in table_schemas:
            st.write(f"Table Name: {schema['table_name']}")
            st.code(schema['schema_json'])
            st.write("-" * 50)

        ask_url = "https://mocki.io/v1/fd148d60-1ec3-4d43-affb-1bdc36b6896e"
        params = {'question': question}
        response = requests.post(ask_url, data=params)

        if response.status_code == 200:
            result = response.json()['result']
            sql_query = response.json()['SQL']
            st.subheader("SQL Query:")
            st.code(sql_query)
            st.subheader("Result:")
            st.write(result)
        else:
            st.error("Error fetching result.")
