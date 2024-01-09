from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import sqlite3
from upload_excel import TableSchema
import config
ask_question = Blueprint('ask_question', __name__)

engine = create_engine('sqlite:///database/Batsman17.sqlite3', echo=True)
model_path =config.model_path
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

@ask_question.route('/ask_question', methods=['POST'])
def ask_question_route():
    question = request.form.get('question')

    # Retrieve all uploaded table names and schemas from the database
    all_schemas = get_all_schemas_from_db()

    if not all_schemas:
        return jsonify({'error': 'No tables found. Upload Excel file first.'})

    # Generate SQL query from the question
    print(all_schemas)
    input_text = f"Question: {question} Schema: {all_schemas}"
    model_inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(input_ids=model_inputs['input_ids'], attention_mask=model_inputs['attention_mask'], max_length=512)
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Execute the SQL query
    conn = sqlite3.connect('database/Batsman17.sqlite3')
    cursor = conn.cursor()
    cursor.execute(output_text)
    print(output_text)
    result = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the result as JSON
    if result:
        return jsonify({'result': result,'SQL':output_text})
    else:
        return jsonify({'result': 'No data found.'})

def get_all_schemas_from_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    all_schemas = session.query(TableSchema).all()
    session.close()

    schemas_str = ""
    for schema in all_schemas:
        schemas_str += f'"{schema.table_name}" {schema.schema_json}\n\n'

    return schemas_str
