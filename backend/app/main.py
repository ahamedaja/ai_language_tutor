# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routes import auth, lessons, exercises, progress
# from app.db import init_db

# app = FastAPI(title="AI Language Tutor API")
# @app.on_event("startup")
# async def startup_event():
#     # Initialize DB indexes and seed sample lessons/users when empty
#     init_db()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
# app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
# app.include_router(progress.router, prefix="/api/progress", tags=["progress"])


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, lessons, exercises, progress, quiz  # Added quiz
from app.db import init_db

app = FastAPI(title="AI Language Tutor API")

@app.on_event("startup")
async def startup_event():
    # Initialize DB indexes and seed sample lessons/users when empty
    try:
        init_db()
    except Exception as e:
        print(f"Warning: init_db failed: {e}")
        # Continue running even if init_db fails

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])  # Added quiz route
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
