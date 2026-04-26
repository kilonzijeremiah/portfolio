import joblib
import numpy as np

# load once
model = joblib.load("model/model.pkl")

def execute_task(task_type, payload):

    if task_type == "predict":
        features = payload.get("features", [])

        if not features:
            return {"error": "No features provided"}

        arr = np.array(features).reshape(1, -1)
        prediction = model.predict(arr).tolist()

        return {"prediction": prediction}

    if task_type == "health":
        return {"status": "HEART-LAYER running"}

    return {"error": "Unknown task"}
