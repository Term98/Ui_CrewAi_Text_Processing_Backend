from flask import Flask, jsonify , request , abort
from uuid import uuid4
from threading import Thread
from datetime import datetime
from flask_cors import CORS
import os

import json
from crew import TextProcessingCrew
from job_manager import append_event, jobs , jobs_lock , Event

app = Flask(__name__)
CORS(app,resources={r"/api/*":{"origins":"*"}})

def kickoff_crew(job_id:str, input:str):
    print(f"""Running crew for {job_id} with the input given {input}""")

    # Setup The Crew Here
    results = None
    try:
        textprocessingCrew = TextProcessingCrew(job_id)
        textprocessingCrew.setup_crew(input)
        results = textprocessingCrew.kickoff()
    except Exception as  e:
        print(f"""CREW FAILED : {str(e)}""")
        append_event(job_id, f"""CREW FAILED:{str(e)}""")
        with jobs_lock:
            jobs[job_id].status = "ERROR"
            jobs[job_id].result = str(e)
 
    # Run THe Crew Here
    with jobs_lock:
        jobs[job_id].status = "COMPLETED"
        jobs[job_id].result = results
        jobs[job_id].events.append(Event(
            data="CREW COMPLETED",timestamp=datetime.now()
        ))


    # Let App Know We Are Done
# create a post
@app.route("/api/hello",methods=['GET'])
def run_hello():
    return jsonify({'Message':"Succesfull"}) , 200

@app.route("/api/crew",methods=['POST'])
def run_crew():
    data = request.json
    if not data or 'input' not in data:
        abort(400, description = "Invalid request with missing data")
    job_id = str(uuid4())
    input= data['input']

    #Run the crew
    thread = Thread(target=kickoff_crew , args=(job_id,input))
    thread.start()

    return jsonify({'job_id':job_id}) , 200

@app.route('/api/crew/<job_id>',methods=['GET'])
def get_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            abort(404, description="Job not found")

     # Parse the job.result string into a JSON object
    try:
        result_json = json.loads(job.result)
    except json.JSONDecodeError:
        result_json = job.result

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    }) , 200

if __name__ == '__main__':
    app.run(debug=True,port=os.getenv('PORT'))