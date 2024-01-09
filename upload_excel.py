from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy import inspect

upload_excel = Blueprint('upload_excel', __name__)

engine = create_engine('sqlite:///database/Batsman17.sqlite3', echo=True)
Base = declarative_base()

# Define a TableSchema model for the database
class TableSchema(Base):
    __tablename__ = 'table_schemas'
    id = Column(Integer, primary_key=True)
    table_name = Column(String, unique=True)
    schema_json = Column(String)

Base.metadata.create_all(engine)

@upload_excel.route('/get_table_schemas', methods=['GET'])
def get_table_schemas():
    session = sessionmaker(bind=engine)()
    schemas = session.query(TableSchema).all()
    session.close()

    schema_list = [{'table_name': schema.table_name, 'schema_json': schema.schema_json} for schema in schemas]

    return jsonify({'table_schemas': schema_list})

# Dynamically create a new table class outside the route function
DynamicTable = None

@upload_excel.route('/upload_excel', methods=['POST'])
def upload_excel_route():
    global DynamicTable
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Create a unique table name based on the file name
    table_name = file.filename.replace('.', '_').lower()

    # Read Excel file into a DataFrame
    df = pd.read_excel(file)  # Specify sheet name if applicable

    # Initialize columns outside the conditional block
    columns = None

    # Check if the table already exists
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        # Dynamically create a new table class if it doesn't exist
        DynamicTable = type('DynamicTable', (Base,), {
            '__tablename__': table_name,
            'id': Column(Integer, primary_key=True),
            **{col: Column(Integer) if pd.api.types.is_integer_dtype(df[col]) else
                    Column(Float) if pd.api.types.is_float_dtype(df[col]) else
                    Column(String) for col in df.columns}
        })

        # Create the table
        DynamicTable.__table__.create(engine)

        # Extract column names and types for the response
        columns = {col: str(getattr(DynamicTable, col).type) for col in df.columns}

        # Save schema information to the database
        save_schema_to_db(table_name, columns)
    else:
        # If the table already exists, append the new schema to the existing one
        existing_schema = load_schema_from_db(table_name)
        existing_schema.update({col: str(getattr(DynamicTable, col).type) for col in df.columns})
        save_schema_to_db(table_name, existing_schema)

    # Insert data into the dynamic table
    df.to_sql(table_name, engine, index=False, if_exists='replace')

    return jsonify({'message': f'Table {table_name} created/updated and data inserted successfully', 'schema': columns})

def save_schema_to_db(table_name, schema):
    session = sessionmaker(bind=engine)()
    existing_schema = session.query(TableSchema).filter_by(table_name=table_name).first()

    if existing_schema:
        # Update schema if table already exists
        existing_schema.schema_json = str(schema)
    else:
        # Save a new schema if table doesn't exist
        new_schema = TableSchema(table_name=table_name, schema_json=str(schema))
        session.add(new_schema)

    session.commit()
    session.close()

def load_schema_from_db(table_name):
    session = sessionmaker(bind=engine)()
    existing_schema = session.query(TableSchema).filter_by(table_name=table_name).first()
    session.close()

    return {} if not existing_schema else eval(existing_schema.schema_json)
