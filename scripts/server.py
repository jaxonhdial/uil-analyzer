from flask import Flask, request, send_file
import subprocess
import zipfile
import os

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    year = data["year"]
    event = data["event"]
    conference = data["conference"]
    district = data["district"]
    region = data["region"]
    state = data["state"]

    # Call your Python script (modify as needed)
    subprocess.run([
        "python3", "scrape_speechwire.py",
        event, str(conference), str(district), str(region), str(state), str(year)
    ])

    # Zip up CSVs
    with zipfile.ZipFile("results.zip", "w") as zf:
        zf.write("individual_results.csv")
        zf.write("team_results.csv")

    return send_file("results.zip", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
