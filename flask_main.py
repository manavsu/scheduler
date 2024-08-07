import flask
from flask import request, jsonify
from flask_cors import CORS
from schedule import PowerSchedule
from schedule_store import ScheduleStore
import logging

log = logging.getLogger("flask_main")
log.setLevel(logging.DEBUG)

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "boop"

@app.route('/schedule/')
def get_schedule():
    log.debug("Getting schedule")
    sch = [schedule.to_json() for schedule in ScheduleStore.load_all_schedule()]
    return jsonify(sch)

@app.route('/schedule/', methods=['POST'])
def post_schedule():
    log.debug("Saving schedule")
    try:
        data = request.get_json()
        schedules = [PowerSchedule.from_json(schedule) for schedule in data]
        ScheduleStore.save_schedule(schedules)
        return "Saved", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)