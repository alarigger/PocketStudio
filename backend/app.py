from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
import time
import uuid

app = FastAPI()

executor = ThreadPoolExecutor(max_workers=4)

jobs = {}

# ----------------------------
# HEAVY TASK
# ----------------------------

def scan_assets(job_id):

    jobs[job_id]["status"] = "running"

    # simulate heavy scan
    time.sleep(5)

    fake_assets = [
        "dragon_model.ma",
        "castle_texture.png",
        "hero_rig.blend"
    ]

    jobs[job_id]["status"] = "finished"
    jobs[job_id]["result"] = fake_assets


# ----------------------------
# START SCAN
# ----------------------------

@app.post("/scan")

def start_scan():

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "result": None
    }

    executor.submit(scan_assets, job_id)

    return {
        "job_id": job_id
    }


# ----------------------------
# JOB STATUS
# ----------------------------

@app.get("/job/{job_id}")

def get_job(job_id):

    return jobs.get(job_id, {
        "status": "unknown"
    })