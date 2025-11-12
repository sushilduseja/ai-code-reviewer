import requests
import json
from typing import Dict, List

class QualityAgent:
    def __init__(self, config: Dict):
        self.url = config['url']
        self.name = config['name']
        self.api_key = config.get('api_key')
    
    def review(self, code_diff: str, file_path: str) -> List[Dict]:
        """Send code to SIM.ai agent for quality review"""
        headers = {'Content-Type': 'application/json'}
        
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        
        # SIM.ai workflow format
        payload = {
            "code": code_diff,
            "file_path": file_path
        }
        
        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # Extract from workflow response structure
            if 'output' in result:
                output = result['output']
                
                # Check for quality-specific issues structure
                if 'issues' in output and isinstance(output['issues'], list):
                    # Convert issues to findings format
                    findings = []
                    for issue in output['issues']:
                        findings.append({
                            'severity': issue.get('severity', 'MEDIUM'),
                            'line': issue.get('line', 0),
                            'issue': issue.get('description', issue.get('type', 'Unknown issue')),
                            'recommendation': issue.get('suggestion', 'Review and fix')
                        })
                    return findings
                
                # Fallback: look for content field
                content = output.get('content', output)
            elif 'data' in result:
                content = result['data']
            else:
                content = result
            
            # Handle string content (JSON in string)
            if isinstance(content, str):
                # Try to extract JSON from markdown
                if '```json' in content:
                    json_str = content.split('```json')[1].split('```')[0].strip()
                    findings = json.loads(json_str)
                else:
                    # Try direct parse
                    findings = json.loads(content)
                return findings.get('findings', [])
            
            # Handle dict content
            return content.get('findings', [])
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] {self.name} JSON decode failed: {e}")
            content_preview = content[:200] if isinstance(content, str) else str(content)[:200]
            print(f"[ERROR] Content was: {content_preview}")
            return []
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] {self.name} HTTP Error: {e.response.status_code}")
            print(f"[ERROR] Response body: {e.response.text[:500]}")
            return []
        except Exception as e:
            print(f"[ERROR] {self.name} failed: {e}")
            return []


