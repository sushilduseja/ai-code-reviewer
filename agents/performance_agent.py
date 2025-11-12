import requests
import json
from typing import Dict, List

class PerformanceAgent:
    def __init__(self, config: Dict):
        self.url = config['url']
        self.name = config['name']
        self.api_key = config.get('api_key')
    
    def review(self, code_diff: str, file_path: str) -> List[Dict]:
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        
        prompt = f"""Review this code diff for performance issues:

File: {file_path}

```diff
{code_diff}
```

Provide findings in JSON format only, no other text."""
        
        payload = {"message": prompt, "stream": False}
        
        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=30)
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
