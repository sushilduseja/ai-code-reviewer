import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# SIM.ai Agent Configuration
AGENTS = {
    "security": {
        "url": "https://www.sim.ai/api/workflows/845faaf5-b6aa-4c6d-9019-7eddb97da6a5/execute",
        "name": "Security Reviewer"
    },
    "performance": {
        "url": "https://www.sim.ai/api/workflows/ba0f060e-ccb4-42ef-8d86-3a0ff1d932b4/execute",
        "name": "Performance Reviewer"
    },
    "quality": {
        "url": "https://www.sim.ai/api/workflows/c2a5be01-67af-474b-a6e7-dfd93c5a693c/execute",
        "name": "Quality Reviewer"
    }
}

# Load SIM.ai API key from environment variable
SIM_API_KEY = os.getenv('SIM_API_KEY', '')