from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
from agents.security_agent import SecurityAgent
from agents.performance_agent import PerformanceAgent
from agents.quality_agent import QualityAgent

class ReviewOrchestrator:
    def __init__(self, config: Dict):
        self.agents = {
            'security': SecurityAgent(config['security']),
            'performance': PerformanceAgent(config['performance']),
            'quality': QualityAgent(config['quality'])
        }
    
    def review_file(self, file_data: Dict) -> Dict:
        """Run all agents in parallel on a single file"""
        file_path = file_data['path']
        code_diff = '\n'.join(file_data['changes'])
        
        results = {
            'file': file_path,
            'security': [],
            'performance': [],
            'quality': []
        }
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.agents['security'].review, code_diff, file_path): 'security',
                executor.submit(self.agents['performance'].review, code_diff, file_path): 'performance',
                executor.submit(self.agents['quality'].review, code_diff, file_path): 'quality'
            }
            
            for future in as_completed(futures):
                agent_type = futures[future]
                try:
                    findings = future.result()
                    results[agent_type] = findings
                except Exception as e:
                    print(f"Error in {agent_type} agent: {e}")
        
        return results
    
    def generate_report(self, all_results: List[Dict]) -> str:
        """Generate markdown report"""
        report = ["# AI Code Review Report\n"]
        
        for result in all_results:
            report.append(f"## File: `{result['file']}`\n")
            
            for category in ['security', 'performance', 'quality']:
                findings = result[category]
                if findings:
                    report.append(f"### {category.title()} Issues\n")
                    for finding in findings:
                        severity = finding.get('severity', 'medium').upper()
                        line = finding.get('line', 'N/A')
                        issue = finding.get('issue', 'No description')
                        recommendation = finding.get('recommendation', 'No recommendation')
                        
                        report.append(f"**[{severity}]** Line {line}")
                        report.append(f"- Issue: {issue}")
                        report.append(f"- Recommendation: {recommendation}\n")
            
            report.append("---\n")
        
        return '\n'.join(report)
