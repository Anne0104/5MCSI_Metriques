from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
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
    url = "https://api.github.com/repos/Anne0104/5MCSI_Metriques/commits"
    response = requests.get(url)
    data = response.json()

    from collections import Counter
    minutes = []

    for commit in data:
        try:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(date_obj.minute)
        except:
            continue

    # Compter les commits par minute
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
