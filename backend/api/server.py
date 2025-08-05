from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import pandas as pd

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/scrape", methods=["POST", "OPTIONS"])
def scrape():
    if request.method == "OPTIONS":
        # Respond to preflight request
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:3000"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json
    year = data["year"]
    event = data["event"]
    conference = data["conference"]
    level = data["level"]
    level_input = data["levelInput"]

    filepath_individual = f"../data/individual_results-{year}-{event}-{conference}-{level}-{level_input}.csv"
    filepath_team = f"../data/team_results-{year}-{event}-{conference}-{level}-{level_input}.csv"

    # Checks if files are already cached
    if not (os.path.exists(filepath_individual) and os.path.exists(filepath_team)):
        subprocess.run([
            "python3", "scrape_speechwire.py",
            str(year), str(event), str(conference), str(level), str(level_input)
        ], check=True)

    # Read CSVs into pandas DataFrames
    df_individual = pd.read_csv(filepath_individual)
    df_team = pd.read_csv(filepath_team)
    
    # Convert DataFrames to JSON
    individual_json = df_individual.to_dict(orient="records")
    team_json = df_team.to_dict(orient="records")

    response = jsonify({
        "individual_results": individual_json,
        "team_results": team_json
    })
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:3000"
    return response

if __name__ == "__main__":
    app.run(debug=True)
