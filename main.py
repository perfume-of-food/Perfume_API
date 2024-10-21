from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

# Define your FastAPI app
app = FastAPI()

# Define a model for the data you expect to receive
class DataModel(BaseModel):
    key: str
    value: Any

# Define a route to receive data via POST request
@app.post("/receive_data/")
async def receive_data(data: DataModel):
    # Process the data
    print(f"Received data: {data.key} = {data.value}")
    
    # Respond back to the frontend
    return {"message": "Data received successfully", "received_data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
