import logging

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import phospho
from app.core import config
from app.db.mongo import close_mongo_db, connect_and_init_db
from app.db.qdrant import close_qdrant, init_qdrant
from app.services.mongo.extractor import check_health

# Setup the Sentry SDK

if config.ENVIRONMENT == "production":
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=0.1,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=0.1,
    )
    sentry_sdk.set_level("warning")

# Used for to analyze the onboarding process
phospho.init(
    project_id="b20659d0932d4edbb2b9682d3e6a0ccb",
    api_key=config.PHOSPHO_API_KEY_ONBOARDING,
)

# Check that the

tags_metadata = [
    {
        "name": "projects",
        "description": "Operations with projects. A project represent an app or an agent. Each interaction betwwen this app and a user is a session.",
    },
    {
        "name": "sessions",
        "description": "Operations with sessions. A session is meant to represent a complete interaction with a user. For instance, you can see the new chat button on ChatGPT as a way to create a new session with the conversational agent. A session is composed of tasks.",
    },
    {
        "name": "tasks",
        "description": "Operations with tasks. A task represents a specific action that the user wants to perform. For instance, in ChatGPT, a task is the generation of a new message. A task is composed of steps.",
    },
]


app = FastAPI(
    title="phospho",
    summary="phospho http api",
    version="0.0.3",
    openapi_tags=tags_metadata,
    contact={
        "name": "phospho",
        "url": "https://phospho.app",
        "email": "contact@phospho.app",
    },
)

# Setup the CORS middleware
origins = [
    # "https://platform.phospho.ai",
    # "http://localhost",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database

app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("startup", init_qdrant)
app.add_event_handler("shutdown", close_mongo_db)
app.add_event_handler("shutdown", close_qdrant)


# Other services
app.add_event_handler("startup", check_health)


# Healthcheck
@app.get("/health")
def check_health():
    return {"status": "ok"}


### V0 API DELETED ###

logging.info(f"ENVIRONMENT : {config.ENVIRONMENT}")

### V2 API ###
# Following PropelAuth

from app.api.v2.endpoints import (
    evals,
    health,
    log,
    me,
    projects,
    sessions,
    tasks,
    tests,
)

api_v2 = FastAPI(
    title="phospho",
    summary="phospho http api v2",
    description="For more information, see the [documentation](https://docs.phospho.ai/).",
    version="0.2.1",
    contact={
        "name": "phospho",
        "url": "https://phospho.ai",
        "email": "contact@phospho.app",
    },
)

api_v2.include_router(me.router)
api_v2.include_router(evals.router)
api_v2.include_router(log.router)
api_v2.include_router(tasks.router)
api_v2.include_router(tests.router)
api_v2.include_router(projects.router)
api_v2.include_router(sessions.router)
api_v2.include_router(health.router)

# Mount the subapplication on the main app with the prefix /v2/
app.mount("/v2", api_v2)
# Also mount it on /v0/ for backward compatibility
app.mount("/v0", api_v2)


### PLATEFORM ENDPOINTS ###
from app.api.platform.endpoints import (
    debug,
    explore,
    metadata,
    organizations,
    projects,
    sessions,
    tasks,
)

api_platform = FastAPI()

api_platform.include_router(debug.router)
api_platform.include_router(organizations.router)
api_platform.include_router(projects.router)
api_platform.include_router(tasks.router)
api_platform.include_router(sessions.router)
api_platform.include_router(explore.router)
api_platform.include_router(metadata.router)

app.mount("/api", api_platform)
