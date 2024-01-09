from flask import Flask
from upload_excel import upload_excel
from ask_question import ask_question
 
app = Flask(__name__)
 
app.register_blueprint(upload_excel)
app.register_blueprint(ask_question)
 
if __name__ == '__main__':
    app.run(debug=True, port=config.API_PORT)