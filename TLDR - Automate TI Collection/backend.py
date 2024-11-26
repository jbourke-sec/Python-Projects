from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from together import Together
import re
import json
import validators

app = Flask(__name__,template_folder='template')

# Initialize Together API
client = Together(api_key="API_KEY")

# Initialize VirusTotal API
virustotal_api_key = "API_KEY"

# Initialize Long Sequence Summarizer
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def extract_iocs(text):
    iocs = []
    ipv4s = re.findall(r'\b\d{1,3}\[?\.\]?\d{1,3}\[?\.\]?\d{1,3}\[?\.\]?\d{1,3}\b', text)
    ipv6s = re.findall(r'\b(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\b', text)
    urls = re.findall(r'(http|ftp|https)://[\w-]+(\[?\.\]?[\w-]+)+([\w.,@?^=%&amp;:/~+#-]*[\w@?^=%&amp;/~+#-])?', text)
    domains = re.findall(r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\[?\.\]?)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\b', text)
    md5s = re.findall(r'\b[0-9a-fA-F]{32}\b', text)
    sha1s = re.findall(r'\b[0-9a-fA-F]{40}\b', text)
    sha256s = re.findall(r'\b[0-9a-fA-F]{64}\b', text)
    sha512s = re.findall(r'\b[0-9a-fA-F]{128}\b', text)
    for ipv4 in ipv4s:
        iocs.append({'type': 'ipv4', 'value': re.sub(r'\[\.\]', '.', ipv4)})
    for ipv6 in ipv6s:
        iocs.append({'type': 'ipv6', 'value': ipv6})
    for url in urls:
        iocs.append({'type': 'url', 'value': re.sub(r'\[\.\]', '.', url)})
    for domain in domains:
        if validators.domain(re.sub(r'\[\.\]', '.', ipv4)):
            iocs.append({'type': 'domain', 'value': re.sub(r'\[\.\]', '.', domain)})
    for md5 in md5s:
        iocs.append({'type': 'md5', 'value': md5})
    for sha1 in sha1s:
        iocs.append({'type': 'sha1', 'value': sha1})
    for sha256 in sha256s:
        iocs.append({'type': 'sha256', 'value': sha256})
    for sha512 in sha512s:
        iocs.append({'type': 'sha512', 'value': sha512})
    return iocs

def enrich_iocs(iocs):
    enriched_iocs = []
    for ioc in iocs:
        if ioc['type'] == 'ipv4':
            response = requests.get(f"https://www.virustotal.com/api/v3/ip_addresses/{ioc['value']}", headers={"x-apikey": virustotal_api_key})
            if response.status_code == 200:
                data = json.loads(response.text)
                ioc['enrichment'] = data['data']['attributes']['last_analysis_stats']
            else:
              ioc['enrichment'] = "No Enrichment Available"  
        elif ioc['type'] == 'ipv6':
            response = requests.get(f"https://www.virustotal.com/api/v3/ip_addresses/{ioc['value']}", headers={"x-apikey": virustotal_api_key})
            if response.status_code == 200:
                data = json.loads(response.text)
                ioc['enrichment'] = data['data']['attributes']['last_analysis_stats']
            else:
              ioc['enrichment'] = "No Enrichment Available"  
        elif ioc['type'] == 'url':
            response = requests.get(f"https://www.virustotal.com/api/v3/urls/{ioc['value']}", headers={"x-apikey": virustotal_api_key})
            if response.status_code == 200:
                data = json.loads(response.text)
                ioc['enrichment'] = data['data']['attributes']['last_analysis_stats']
            else:
              ioc['enrichment'] = "No Enrichment Available"  
        elif ioc['type'] == 'domain':
            response = requests.get(f"https://www.virustotal.com/api/v3/domains/{ioc['value']}", headers={"x-apikey": virustotal_api_key})
            if response.status_code == 200:
                data = json.loads(response.text)
                ioc['enrichment'] = data['data']['attributes']['last_analysis_stats']
            else:
              ioc['enrichment'] = "No Enrichment Available"  
        elif ioc['type'] == 'md5':
            response = requests.get(f"https://www.virustotal.com/api/v3/files/{ioc['value']}", headers={"x-apikey": virustotal_api_key})
            if response.status_code == 200:
                data = json.loads(response.text)
                ioc['enrichment'] = data['data']['attributes']['last_analysis_stats']
            else:
              ioc['enrichment'] = "No Enrichment Available"  
        elif ioc['type'] == 'sha1':
            response = requests.get(f"https://www.virustotal.com/api/v3/files/{ioc['value']}", headers={"x-apikey": virustotal_api_key})
            if response.status_code == 200:
                data = json.loads(response.text)
                ioc['enrichment'] = data['data']['attributes']['last_analysis_stats']
            else:
              ioc['enrichment'] = "No Enrichment Available"  
        elif ioc['type'] == 'sha256':
            response = requests.get(f"https://www.virustotal.com/api/v3/files/{ioc['value']}", headers={"x-apikey": virustotal_api_key})
            if response.status_code == 200:
                data = json.loads(response.text)
                ioc['enrichment'] = data['data']['attributes']['last_analysis_stats']
            else:
              ioc['enrichment'] = "No Enrichment Available"  
        elif ioc['type'] == 'sha512':
            response = requests.get(f"https://www.virustotal.com/api/v3/files/{ioc['value']}", headers={"x-apikey": virustotal_api_key})
            if response.status_code == 200:
                data = json.loads(response.text)
                ioc['enrichment'] = data['data']['attributes']['last_analysis_stats']
            else:
              ioc['enrichment'] = "No Enrichment Available"  
        enriched_iocs.append(ioc)
    return enriched_iocs

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
            iocs = extract_iocs(text)
            enriched_iocs = enrich_iocs(iocs)
            return render_template('result.html', summary=summary, ttps=ttps, detections=detections, iocs=enriched_iocs)
        except Exception as e:
            return render_template('error.html', error=str(e))
    return render_template('index.html')

def extract_ttps(text):
    ttps = []
    prompt = f"Extract the TTPs from the following text, start each TTP with \"TTP:\" and end with a new line, each should contain the reference text from the page in brackets: {text}"
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
