import requests
import json
import time
from typing import Dict, List

class QualityAgent:
    def __init__(self, config: Dict):
        self.url = config['url']
        self.name = config['name']
        self.api_key = config.get('api_key')
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def review(self, code_diff: str, file_path: str) -> List[Dict]:
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        
        prompt = f"""Review this code diff for quality and maintainability issues:

File: {file_path}

```diff
{code_diff}
```

Provide findings in JSON format only, no other text."""
        
        payload = {"message": prompt, "stream": False}
        
        # Retry logic for rate limiting
        for attempt in range(self.max_retries):
            try:
                response = requests.post(self.url, json=payload, headers=headers, timeout=30)
                
                # Handle rate limiting with backoff
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                        print(f"{self.name}: Rate limited. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"Error calling {self.name}: 429 Too Many Requests (max retries exceeded)")
                        return []
                
                response.raise_for_status()
                result = response.json()
                content = result.get('message', result.get('response', ''))
                
                try:
                    findings = json.loads(content)
                    return findings.get('findings', [])
                except json.JSONDecodeError:
                    if '```json' in content:
                        json_str = content.split('```json')[1].split('```')[0].strip()
                        findings = json.loads(json_str)
                        return findings.get('findings', [])
                    return []
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    key_status = "API key is missing" if not self.api_key else "API key is invalid or workflow ID is inaccessible"
                    print(f"Error calling {self.name}: 401 Unauthorized - {key_status}")
                else:
                    print(f"Error calling {self.name}: {e}")
                return []
            except Exception as e:
                print(f"Error calling {self.name}: {e}")
                return []
        
        return []

