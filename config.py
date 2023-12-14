import os

from dotenv import load_dotenv

load_dotenv()


model_path = 'gaussalgo/T5-LM-Large-text2sql-spider'

API_PORT = int(os.getenv("GPT_API_PORT"))