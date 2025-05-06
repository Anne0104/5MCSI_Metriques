from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from collections import Counter
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
                                                                                                                                       
app = Flask(__name__)  

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def newgraphique():
    return render_template("histogramme.html")

@app.route("/commits/")
def commits():
    url = "https://api.github.com/repos/Anne0104/5MCSI_Metriques/commits?per_page=20"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return f"Erreur API GitHub : {response.status_code}"
        data = response.json()
    except Exception as e:
        return f"Erreur lors de la récupération des commits : {str(e)}"

    minutes = []
    for commit in data:
        try:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(date_obj.minute)
        except:
            continue

    from collections import Counter
    minute_counts = Counter(minutes)
    sorted_minutes = sorted(minute_counts.items())

    labels = [f"{minute:02d}" for minute, _ in sorted_minutes]
    values = [count for _, count in sorted_minutes]

    return render_template("commits.html", labels=labels, values=values)


                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #aah
  
if __name__ == "__main__":
  app.run(debug=True)
