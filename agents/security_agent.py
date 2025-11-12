import requests
import json
from typing import Dict, List

class SecurityAgent:
    def __init__(self, config: Dict):
        self.url = config['url']
        self.name = config['name']
        self.api_key = config.get('api_key')
    
    def review(self, code_diff: str, file_path: str) -> List[Dict]:
        """Send code to SIM.ai agent for security review"""
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        prompt = f"""Review this code diff for security vulnerabilities:

File: {file_path}

```diff
{code_diff}
```

Provide findings in JSON format only, no other text."""
        
        payload = {
            "message": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            # Extract JSON from response (may be in 'message' or 'response' field)
            content = result.get('message', result.get('response', ''))
            
            # Try to parse JSON from response
            try:
                findings = json.loads(content)
                return findings.get('findings', [])
            except json.JSONDecodeError:
                # Extract JSON from markdown code blocks if present
                if '```json' in content:
                    json_str = content.split('```json')[1].split('```')[0].strip()
                    findings = json.loads(json_str)
                    return findings.get('findings', [])
                return []
        except Exception as e:
            print(f"Error calling {self.name}: {e}")
            return []
