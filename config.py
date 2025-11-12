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
        "url": "https://api.sim.ai/v1/agents/YOUR_PERFORMANCE_AGENT_ID/chat",
        "name": "Performance Reviewer"
    },
    "quality": {
        "url": "https://api.sim.ai/v1/agents/YOUR_QUALITY_AGENT_ID/chat",
        "name": "Quality Reviewer"
    }
}

# Load SIM.ai API key from environment variable
SIM_API_KEY = os.getenv('SIM_API_KEY', '')