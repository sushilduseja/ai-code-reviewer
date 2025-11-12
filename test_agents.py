#!/usr/bin/env python3
"""
Quick test to verify agent responses
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import AGENTS, SIM_API_KEY
from agents.security_agent import SecurityAgent
from agents.performance_agent import PerformanceAgent
from agents.quality_agent import QualityAgent

# Add API key to config
for key in AGENTS:
    AGENTS[key]['api_key'] = SIM_API_KEY

# Test code with obvious issues
test_code = """
password = "hardcoded123"
api_key = "sk-test-123"

def find_items(items):
    for item in items:
        for other in items:
            if item == other:
                return True
    return False
"""

print("Testing Security Agent...")
security = SecurityAgent(AGENTS['security'])
sec_findings = security.review(test_code, "test.py")
print(f"Security findings: {sec_findings}\n")

print("Testing Performance Agent...")
perf = PerformanceAgent(AGENTS['performance'])
perf_findings = perf.review(test_code, "test.py")
print(f"Performance findings: {perf_findings}\n")

print("Testing Quality Agent...")
quality = QualityAgent(AGENTS['quality'])
qual_findings = quality.review(test_code, "test.py")
print(f"Quality findings: {qual_findings}\n")
