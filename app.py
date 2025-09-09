from flask import Flask, request, render_template
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Store last 5 translations
history = []

@app.route('/', methods=['GET', 'POST'])
def home():
    translated = None
    sentence = ''
    target_lang = ''
    
    if request.method == 'POST':
        sentence = request.form['sentence'].strip()
        target_lang = request.form['language'].strip()  # keep case-sensitive
        
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(sentence)
            
            # Save in history (max 5 items)
            history.append({'sentence': sentence, 'language': target_lang, 'translated': translated})
            if len(history) > 5:
                history.pop(0)
        except Exception as e:
            translated = f"Error: {e}"

    return render_template('index.html', translated=translated, sentence=sentence,
                           target_lang=target_lang, history=history)

if __name__ == "__main__":
    app.run(debug=True)
