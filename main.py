from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading

from heartlayer.engine import execute_task

app = FastAPI()

# allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = {}

class TaskRequest(BaseModel):
    project_id: str
    task_type: str
    payload: dict


def run_task(project_id, task_type, payload):
    try:
        result = execute_task(task_type, payload)

        tasks[project_id] = {
            "status": "completed",
            "result": result
        }

    except Exception as e:
        tasks[project_id] = {
            "status": "error",
            "error": str(e)
        }


@app.post("/internal/execute")
async def execute(task: TaskRequest):
    tasks[task.project_id] = {"status": "running"}

    threading.Thread(
        target=run_task,
        args=(task.project_id, task.task_type, task.payload)
    ).start()

    return {"status": "accepted"}


@app.get("/runtime/{project_id}")
async def runtime(project_id: str):
    return tasks.get(project_id, {"status": "running"})
