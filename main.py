import flask
from flask import request, jsonify
from flask_cors import CORS
from schedule import PowerSchedule
from schedule_store import Store

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "boop"

@app.route('/schedule/')
def get_schedule():
    return jsonify([schedule.to_json() for schedule in Store.get_all_schedules()])

@app.route('/schedule/', methods=['POST'])
def post_schedule():
    try:
        data = request.get_json()
        print(data)
        schedules = [PowerSchedule.from_json(schedule) for schedule in data]
        Store.save_schedules(schedules)
        return "Saved", 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)