from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from transformers import pipeline
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Load IPC sections and encode them once
df = pd.read_csv('ipc_sections.csv')
ipc= [words for words in df['Description']]
ipca=[]
for words in df['Description']:
    words = words.replace('.', ' ') 
    words = words.replace('\n\n\n', ' ')
    words = words.replace('\n\n', ' ')
    words = words.replace('\n', ' ')
    ipca.append(words)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
ansembedding = model.encode(ipca)
print('hi')
@app.route('/get_ipc')
def get_ipc():
    return jsonify({'result': ipc,})

@app.route('/process_query', methods=['POST'])
def process_query():
    print("inside")
    data = request.get_json()
    question = data['question']
    print(question)
    # Encode the query
    
    quesembedding = model.encode(question)

    # Find relevant sections
    relevant_sections = util.semantic_search(quesembedding, ansembedding)

    result = []
    for i in range(len(relevant_sections[0])):
        result.append(ipc[relevant_sections[0][i]['corpus_id']])

    # Create context for question-answering model
    context = ipc[relevant_sections[0][0]['corpus_id']] + ipc[relevant_sections[0][1]['corpus_id']]

    # Question-answering pipeline
    qa_model = pipeline("question-answering")
    answer = qa_model(question=question, context=context)['answer']
    print (result)
    return jsonify({'result': result, 'answer': answer})

if __name__ == '__main__':

    app.run(debug=True)
