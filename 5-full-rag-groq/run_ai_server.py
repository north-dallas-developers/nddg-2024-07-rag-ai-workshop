from flask import Flask, request, jsonify
from ai_query_logic import make_query

app = Flask(__name__, static_url_path='', static_folder='web/static')

@app.route("/")
def hello_world():
    return app.send_static_file('index.html')



@app.route('/send-query', methods=['POST'])
def process_query():
    query = request.form.get('query')

    result = make_query(query)

    response = {
        'original_query': query,
        'message': result.choices[0].message.content
    }
    
    return jsonify(response)
