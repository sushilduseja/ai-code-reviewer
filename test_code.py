# test_code.py
import os
import subprocess
import pickle

# SECURITY ISSUES
password = "hardcoded123"  # Security: Hardcoded credentials
api_key = "sk-sim-y4Dn3ibuPSHU8JYvrhygLCgmrVGdYR-f"  # Security: Exposed API key

def get_user_data(user_id):
    # Security: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def load_user_config(filepath):
    # Security: Unsafe pickle deserialization
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def execute_command(user_input):
    # Security: Command injection vulnerability
    os.system(f"echo {user_input}")

# PERFORMANCE ISSUES
def process_users(users):
    # Performance: O(n²) nested loop - inefficient duplicate detection
    result = []
    for user in users:
        for other in users:
            if user['id'] == other['id']:
                result.append(user)
    return result

def find_items(items, target):
    # Performance: O(n) linear search when set lookup would be O(1)
    for item in items:
        if item == target:
            return True
    return False

def calculate_fibonacci(n):
    # Performance: O(2^n) recursive without memoization
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# QUALITY ISSUES
def long_function():
    # Quality: Function too long (should be broken into smaller functions)
    x = 1
    y = 2
    z = x + y
    a = z * 2
    b = a - 1
    c = b * 3
    d = c / 2
    e = d + 10
    f = e * y
    g = f - z
    h = g + a
    i = h * b
    j = i - c
    k = j + d
    l = k * e
    m = l - f
    n = m + g
    o = n * h
    p = o - i
    q = p + j
    r = q * k
    s = r - l
    t = s + m
    u = t * n
    v = u - o
    w = v + p
    x_final = w * q
    return x_final

def process_data(data, filters, options, config, cache, timeout):
    # Quality: Too many parameters (function signature too complex)
    processed = []
    for item in data:
        if all(item.get(k) == v for k, v in filters.items()):
            if options.get('transform'):
                item = apply_transform(item, options)
            processed.append(item)
    return processed

def apply_transform(item, options):
    # Quality: Poor variable naming
    a = item.get('x', 0)
    b = item.get('y', 0)
    c = a + b
    d = c * 2
    e = d - 5
    f = e / 2
    return f

class UserManager:
    def __init__(self):
        self.uu = []  # Quality: Unclear variable name
        self.d = {}   # Quality: Single letter variable name
    
    def add(self, u):  # Quality: Poor parameter naming
        self.uu.append(u)
        self.d[u.get('id')] = u
    
    def get(self, uid):  # Quality: Inconsistent naming (uid vs u)
        return self.d.get(uid)
