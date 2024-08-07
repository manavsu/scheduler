import flask
from flask import request, jsonify, send_from_directory
from flask_cors import CORS
from schedule import PowerSchedule
from schedule_store import ScheduleStore
import logging

log = logging.getLogger("flask_main")
log.setLevel(logging.DEBUG)

app = flask.Flask(__name__, static_folder='build_ui')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    print(send_from_directory(app.static_folder, 'index.html'))
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def server_ui(path):
    return send_from_directory(app.static_folder, path)

@app.route('/schedule/')
def get_schedule():
    log.debug("Getting schedules.")
    sch = [schedule.to_json() for schedule in ScheduleStore.load_all_schedules()]
    return jsonify(sch)

@app.route('/schedule/', methods=['POST'])
def post_schedule():
    log.debug("Saving schedules.")
    try:
        data = request.get_json()
        schedules = [PowerSchedule.from_json(schedule) for schedule in data]
        ScheduleStore.save_schedules(schedules)
        return "Saved", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)