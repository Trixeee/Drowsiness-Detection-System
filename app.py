from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

def load_dashboard_data():
    with open('dashboard_data.json', 'r') as f:
        return json.load(f)

def save_dashboard_data(data):
    with open('dashboard_data.json', 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/grid')
def get_grid():
    data = load_dashboard_data()
    return jsonify({'grid': data['grid'], 'path': data['path']})

@app.route('/api/alert_tree')
def get_alert_tree():
    data = load_dashboard_data()
    return jsonify({'order': data['alert_order']})

@app.route('/api/event_log')
def get_event_log():
    data = load_dashboard_data()
    return jsonify({'event_log': data.get('event_log', [])})

@app.route('/api/history')
def get_history():
    data = load_dashboard_data()
    return jsonify({'history': data.get('history', [])})

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    data = load_dashboard_data()
    data['history'] = []
    save_dashboard_data(data)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True) 