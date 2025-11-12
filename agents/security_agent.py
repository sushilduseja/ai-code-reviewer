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
            # The response has 'output' which contains the actual findings
            if 'output' in result:
                output = result['output']
                # Check for vulnerabilities array (security agent specific)
                if 'vulnerabilities' in output and isinstance(output['vulnerabilities'], list):
                    # Convert to findings format
                    findings = []
                    for vuln in output['vulnerabilities']:
                        findings.append({
                            'severity': vuln.get('severity', 'medium'),
                            'line': vuln.get('line', 0),
                            'issue': vuln.get('issue', vuln.get('description', 'Unknown issue')),
                            'recommendation': vuln.get('recommendation', 'Review and fix')
                        })
                    return findings
                # Check for content field
                elif 'content' in output and isinstance(output['content'], str):
                    content = output['content']
                elif isinstance(output, dict) and 'findings' in output:
                    return output.get('findings', [])
                else:
                    content = output
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

