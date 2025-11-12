#!/usr/bin/env python3
import sys
from core.diff_parser import DiffParser
from core.orchestrator import ReviewOrchestrator
from config import AGENTS, SIM_API_KEY

def main():
    # Parse arguments
    repo_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    from_commit = sys.argv[2] if len(sys.argv) > 2 else 'HEAD~1'
    to_commit = sys.argv[3] if len(sys.argv) > 3 else 'HEAD'
    
    print(f"Analyzing changes in {repo_path} from {from_commit} to {to_commit}...")
    
    # Parse diff
    parser = DiffParser(repo_path)
    changed_files = parser.get_changed_files(from_commit, to_commit)
    
    if not changed_files:
        print("No changes detected.")
        return
    
    print(f"Found {len(changed_files)} changed files\n")
    
    # Add API key to agent configs
    agent_configs = {}
    for key, config in AGENTS.items():
        agent_configs[key] = {**config, 'api_key': SIM_API_KEY}
    
    # Run review
    orchestrator = ReviewOrchestrator(agent_configs)
    
    all_results = []
    for i, file_data in enumerate(changed_files, 1):
        print(f"[{i}/{len(changed_files)}] Reviewing {file_data['path']}...")
        result = orchestrator.review_file(file_data)
        all_results.append(result)
    
    # Generate report
    report = orchestrator.generate_report(all_results)
    
    # Save and display
    with open('review_report.md', 'w') as f:
        f.write(report)
    
    print("\n" + "="*60)
    print(report)
    print("="*60)
    print("\nReport saved to: review_report.md")

if __name__ == '__main__':
    main()
