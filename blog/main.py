from fastapi import FastAPI

app = FastAPI()

@app.get('/blogapp')
def blogapp():
    return {'data': 'blogapp'}