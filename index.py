from flask import Flask, request
import json
import time
from language_tool_python import LanguageTool

app = Flask(__name__)

class SpellCheckerModule:
    def __init__(self, language='en-US'):
        self.language_tool = LanguageTool(language)

    def correct_grammar(self, text):
        matches = self.language_tool.check(text)
        corrected_text = self.language_tool.correct(text)
        return corrected_text, matches

grammar_corrector = SpellCheckerModule()

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
        text = request.args.get('input', '')  # Retrieve input from query parameter
    elif request.method == 'POST':
        text = request.form.get('input', '')  # Retrieve input from form data

    corrected_text, mistakes = grammar_corrector.correct_grammar(text)

    # Construct the data_set dictionary
    data_set = {
        'input': text,
        'corrected_text': corrected_text,
        'mistakes': len(mistakes),
        'timestamp': time.time(),
        'mistake_details': [{ 'message': mistake.message}
                            for mistake in mistakes]
    }

    json_dump = json.dumps(data_set)

    return json_dump
if __name__ == "__main__":
    app.run(debug=True)

