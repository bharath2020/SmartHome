#!/usr/bin/env python3
from flask import Flask, request, render_template
import os
import json
import time
import datetime
from smarthomemongo import SmartHomeDB

app = Flask(__name__)
smartDB = SmartHomeDB()


@app.route('/')
def index():
	records = smartDB.getCurrentStats('raspberry')
	if( 'timestamp' in records.keys() ):
		ts = datetime.datetime.fromtimestamp(records['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
		records['timestamp_string'] = ts
	print(records)

	return render_template('index.html',records=records)


@app.route('/add', methods=['POST'])
def add():
	recordJson = request.get_json()
	smartDB.insertTemperaturePoint(recordJson)
	return 'Success', 200

@app.route('/update_stats', methods=['POST'])
def update_stats():
	recordJson = request.get_json()
	smartDB.updateCurrentStats(recordJson)
	return 'Success', 200

@app.route('/get_current_stats',methods=['GET'])
def get_current_stats():
	record = smartDB.getCurrentStats()
	return json.dumps(record)

@app.route('/line_graph')
def get_line_graph():
	return render_template('graph.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)




