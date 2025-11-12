"""
Test code with intentional Security, Performance, and Quality issues.
This file is designed to demonstrate issues for each reviewer agent.
"""
import os
import pickle

# SECURITY ISSUE: Hardcoded credentials
password = "admin123"

def get_user_data(user_id):
    # SECURITY ISSUE: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def load_config(filepath):
    # SECURITY ISSUE: Unsafe pickle deserialization
    with open(filepath, 'rb') as f:
        return pickle.load(f)

# PERFORMANCE ISSUE: O(n²) complexity - nested loops
def find_duplicates(users):
    result = []
    for user in users:
        for other in users:
            if user['id'] == other['id']:
                result.append(user)
    return result

# PERFORMANCE ISSUE: Linear search instead of O(1) lookup
def is_user_admin(user_id, admin_users):
    for admin in admin_users:
        if admin['id'] == user_id:
            return True
    return False

# QUALITY ISSUE: Overly complex function with too many parameters
def process_user_data(user_data, filters, options, config, validators, transformers):
    # Quality: Too many responsibilities
    output = []
    for item in user_data:
        if all(item.get(f) == filters[f] for f in filters if f in item):
            for transform in transformers:
                item = apply_transform(item, transform)
            output.append(item)
    return output

# QUALITY ISSUE: Poor naming conventions
def apply_transform(x, t):
    # Quality: Single letter parameters and variables
    a = x.get('val', 0)
    b = t.get('mult', 1)
    c = a * b
    d = c + t.get('offset', 0)
    return d

class UserService:
    """QUALITY ISSUE: Poor class design and naming"""
    def __init__(self):
        self.u = []  # Unclear name
        self.m = {}  # Single letter
    
    def add(self, x):  # Poor parameter naming
        self.u.append(x)
        if 'id' in x:
            self.m[x['id']] = x
