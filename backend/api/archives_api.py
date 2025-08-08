from flask import Blueprint, request, jsonify
from backend.query.archives import format_archives_results

bp = Blueprint("archives_api", __name__)

@bp.route("/get_archives", methods=["GET"])
def get_archives():
    try:
        year = int(request.args.get("year"))
        conference = int(request.args.get("conference"))
        event = request.args.get("event")
        level = request.args.get("level")
        level_input = int(request.args.get("level_input"))

        formatted_individual, individual_columns = format_archives_results(year, conference, event, level, level_input, is_team=False)
        try:
            formatted_team, team_columns = format_archives_results(year, conference, event, level, level_input, is_team=True)
        except RuntimeError:
            formatted_team, team_columns = None, []

        return jsonify({
            "individual_results": formatted_individual.to_dict(orient="records") if not formatted_individual.empty else [],
            "individual_columns": individual_columns,
            "team_results": formatted_team.to_dict(orient="records") if formatted_team is not None and not formatted_team.empty else [],
            "team_columns": team_columns,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
