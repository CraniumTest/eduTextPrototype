from flask import Flask, request, jsonify
from transformers import pipeline
from googletrans import Translator

app = Flask(__name__)

# Initialize LLM pipeline
question_answering = pipeline("question-answering")
translator = Translator()

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    context = data.get('context', '')
    question = data.get('question', '')
    preferred_language = data.get('language', 'en')
    
    # Translate question and context if necessary
    if preferred_language != 'en':
        question = translator.translate(question, src=preferred_language, dest='en').text
        context = translator.translate(context, src=preferred_language, dest='en').text

    # Get answer using LLM
    result = question_answering(question=question, context=context)
    answer = result['answer']
    
    # Translate answer back to preferred language
    if preferred_language != 'en':
        answer = translator.translate(answer, src='en', dest=preferred_language).text
    
    return jsonify({'answer': answer})


@app.route('/recommend', methods=['POST'])
def recommend_learning_materials():
    data = request.json
    progress = data.get('progress', {})
    # Simulate recommendation logic based on progress
    recommendations = ["Resource 1", "Exercise 2", "Quiz 3"]
    return jsonify({'recommendations': recommendations})


if __name__ == '__main__':
    app.run(debug=True)
