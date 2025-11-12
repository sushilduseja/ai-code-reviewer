# test_code.py
password = "hardcoded123"  # Security issue

def process_users(users):  # Performance issue: O(n²)
    result = []
    for user in users:
        for other in users:
            if user['id'] == other['id']:
                result.append(user)
    return result

def long_function():  # Quality issue: too long
    x = 1
    # ... 60+ lines of code
    return x
