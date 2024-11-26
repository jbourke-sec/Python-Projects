from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from together import Together

app = Flask(__name__,template_folder='template')

# Initialize Together API
client = Together(api_key="11cd65db83bca3bfd7fb13ea05de040b6992eb17e9d39c34915ac45d3e3d1085")

# Initialize Long Sequence Summarizer
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def long_sequence_summarizer(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], num_beams=4, max_length=200, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            summary = long_sequence_summarizer(text)
            ttps = extract_ttps(text)
            detections = build_detections(ttps)
            return render_template('result.html', summary=summary, ttps=ttps, detections=detections)
        except Exception as e:
            return render_template('error.html', error=str(e))
    return render_template('index.html')

def extract_ttps(text):
    ttps = []
    prompt = f"Extract the TTPs from the following text, start each TTP with \"TTP:\" and end with a new line: {text}"
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
              messages=[
                    {"role": "user", "content": prompt}   ],
        max_tokens=1000,
        temperature=0.5,
    )
    ttp_text = response.choices[0].message.content
    ttp_lines = ttp_text.splitlines()
    for line in ttp_lines:
        if line.startswith("TTP:"):
            tactic = line.split(":")[1].strip()
            technique = line.split(":")[2].strip() if len(line.split(":")) > 2 else ""
            ttps.append({'tactic': tactic, 'technique': technique})
    return ttps

def build_detections(ttps):
    detections = []
    for ttp in ttps:
        prompt = f"Build detection rules for {ttp['tactic']} using {ttp['technique']}"
        response = client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
              messages=[
                    {"role": "user", "content": prompt}   ],
            max_tokens=1000,
            temperature=0.5,
        )
        detection_text = response.choices[0].message.content
        detection_lines = detection_text.splitlines()
        detection = {'tactic': ttp['tactic'], 'technique': ttp['technique'], 'detection_rules': detection_lines}
        detections.append(detection)
    return detections

if __name__ == '__main__':
    app.run(debug=True)