from fastapi import FastAPI
from workout_api.routes import api_router
from fastapi_pagination import add_pagination

app = FastAPI(title="Workout")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8800,log_level='info', reload=True)
app.include_router(api_router)

add_pagination(app) 