from fastapi import FastAPI

app = FastAPI(title="Workout")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8800,log_level='info', reload=True)