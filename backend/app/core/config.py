"""
App configuration file
"""

import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv()  # take environment variables from .env.
logger.info("Loading environment variables from .env file")

### ENVIRONMENT ###
# To check if we are in production or `test` environment.
# ENV can be test, staging or production. Default: staging
ENVIRONMENT = os.getenv("ENVIRONMENT", "staging")
logger.info(f"ENVIRONMENT: {ENVIRONMENT}")

### MONGODB ###
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_NAME = os.getenv("MONGODB_NAME")
MONGODB_MAXPOOLSIZE = 10
MONGODB_MINPOOLSIZE = 1

if ENVIRONMENT == "production" and MONGODB_NAME != "production":
    raise Exception("MONGODB_NAME is not set to 'production' in production environment")
if MONGODB_NAME == "production" and ENVIRONMENT != "production":
    raise Exception("MONGODB_NAME is set to 'production' in non-production environment")


### DATABASE ###
KEY_COLLECTION = "keys"
KEY_PREFIX = "sk-"

### GCP ###

PROJECT_ID_GCLOUD = "portal-385519"  # Project ID

# Google Storage Buckets
APP_TEMPLATE_BUCKET = "phospho-app-template"
APP_TEMPLATE_VERSION = "v0_0_3"
AGENTS_BUCKET = "phospho-agents"  # AGENTS_BUCKET/PROJECT_NAME/agent
BUILD_LOGS_BUCKET = "phospho-build-logs"  # BUILD_LOGS_BUCKET/PROJECT_NAME/timestamp/ -> timestamp of build
CLONED_REPO_BUCKET = "cloned_repo"

# Google Cloud Run
REGION = "europe-west9"
MAX_INSTANCES = 5

### USAGE LIMITS ###
# Maximum number of projects per user
MAX_PROJECTS_PER_USER = 100

DEFAULT_MAX_QUERY_LIMIT = 1000
MAX_NUMBER_OF_SCREENED_TASKS_PER_PROJECT = 10000
PLAN_HOBBY_MAX_NB_TASKS = 5 * 1000

PLAN_HOBBY_MAX_USERS = 1
PLAN_PRO_MAX_USERS = 15


### SECURITY ###

EXCLUDED_LOG_KEYWORDS = ["gserviceaccount", "googleapis.com"]

### DOCUMENTATION ##

# Hide the github endpoints in the OpenAPI documentation
if ENVIRONMENT == "test":
    SHOW_GITHUB_ENDPOINTS = True
    SHOW_LOGS_ENDPOINTS = True
    SHOW_DEPLOYMENTS_ENDPOINTS = True
    SHOW_SECRETS_ENDPOINTS = True
    SHOW_NOTIFICATIONS_ENDPOINTS = True
else:
    SHOW_GITHUB_ENDPOINTS = False
    SHOW_LOGS_ENDPOINTS = False
    SHOW_DEPLOYMENTS_ENDPOINTS = False
    SHOW_SECRETS_ENDPOINTS = False
    SHOW_NOTIFICATIONS_ENDPOINTS = False

ADMIN_EMAIL = "notifications@phospho.app"  # Used when new users sign up

### OPENAI ###
OPENAI_ORGANIZATION = "org-kH8tMbx6wJGWWUb3qQiLk73Z"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

### Vector Search ###
QDRANT_URL = os.getenv("QDRANT_URL")
if QDRANT_URL is None:
    raise Exception("QDRANT_URL is missing from the environment variables")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
if QDRANT_API_KEY is None:
    raise Exception("QDRANT_API_KEY is missing from the environment variables")

### WATCHERS ###
OPENAI_MODEL_ID = "gpt-4"  # "gpt-4"
OPENAI_MODEL_ID_FOR_EVAL = "gpt-4"
OPENAI_MODEL_ID_FOR_EVENTS = "gpt-3.5-turbo-16k"
EVALUATION_SOURCE = "phospho-4"  # If phospho
FEW_SHOT_MIN_NUMBER_OF_EXAMPLES = 10  # Make it even
FEW_SHOT_MAX_NUMBER_OF_EXAMPLES = 50  # Imposed by Cohere API

### TESTING ###
# Testing variables are only used in the test environment
# This default value is PLB's User ID
if ENVIRONMENT == "test":
    TESTING_UID = os.getenv("TESTING_UID", "e4M5ZDH2pwXz8ddEbVIR")

### SLACK ###
SLACK_URL = os.getenv("SLACK_URL")

### SENTRY ###
SENTRY_DSN = os.getenv("SENTRY_DSN")

### PROPELAUTH ###
PROPELAUTH_URL = os.getenv("PROPELAUTH_URL")
PROPELAUTH_API_KEY = os.getenv("PROPELAUTH_API_KEY")

### CICD ###
CICD_PROJECTS = ["VQcNOtKLbszDeMBVaJSr"]

### RESEND EMAILS ###
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_AUDIENCE_ID = "156e4585-8241-48ba-9ac6-9f4ffc77b955"

### COHERE ###
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Used to log event suggestions
PHOSPHO_API_KEY_ONBOARDING = os.getenv("PHOSPHO_API_KEY_ONBOARDING")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
assert (
    STRIPE_SECRET_KEY is not None
), "STRIPE_SECRET_KEY is missing from the environment variables"
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
assert (
    STRIPE_WEBHOOK_SECRET is not None
), "STRIPE_WEBHOOK_SECRET is missing from the environment variables"

if ENVIRONMENT == "production":
    PHOSPHO_FRONTEND_URL = "https://platform.phospho.ai"
elif ENVIRONMENT == "staging":
    PHOSPHO_FRONTEND_URL = "https://phospho-portal.vercel.app"
else:
    PHOSPHO_FRONTEND_URL = "http://localhost:3000"

if ENVIRONMENT == "production":
    PRO_PLAN_STRIPE_PRICE_ID = "price_1OaocDKMbS7I1rNcY7OPEIIG"
else:
    PRO_PLAN_STRIPE_PRICE_ID = "price_1OaqA5KMbS7I1rNc2GckVfKD"

if ENVIRONMENT == "production":
    PRO_PLAN_STRIPE_PRODUCT_ID = "prod_PPduEtJMWyC8cX"
else:
    PRO_PLAN_STRIPE_PRODUCT_ID = "prod_PPfVCWrqXiXKUy"

### EXTRACTOR ###
EXTRACTOR_SECRET_KEY = os.getenv("EXTRACTOR_SECRET_KEY")
EXTRACTOR_URL = os.getenv("EXTRACTOR_URL")
# TODO: move this to a startup check
assert (
    EXTRACTOR_URL is not None
), "EXTRACTOR_URL is missing from the environment variables"
