from flask import Flask, render_template
import urllib.request, json
app = Flask(__name__)

with urllib.request.urlopen("http://apis.is/petrol") as url:
	data = json.loads(url.read().decode())

company = []
for x in data["results"]:
	if x["company"] not in company:
		company.append(x["company"])

nafn95 = ""
nafnD = ""
laegsta95 = 100000
laegstaD = 100000
for y in data["results"]:
	if y["bensin95"] < laegsta95:
		laegsta95 = y["bensin95"]
		nafn95 = y["company"] + " - " + y["name"]
	if y["diesel"] < laegstaD:
		laegstaD = y["diesel"]
		nafnD = y["company"] + " - " + y["name"]
laegsta = [nafn95, laegsta95, nafnD, laegstaD]


@app.route('/')
def index():
	return render_template("index.html", company=company, laegsta=laegsta)

@app.route("/til/<ft>")
def fyrirtaeki(ft):
	return render_template("fyrirtaeki.html", data=data, ft=ft, laegsta=laegsta)

@app.route("/til/<ft>/<name>")
def stadur(ft,name):
	return render_template("stadur.html", data=data, ft=ft, name=name, laegsta=laegsta)

@app.errorhandler(404)
def error404(error):
	return "Síða ekki fundin", 404

if __name__ == "__main__":
	app.run(debug=True)