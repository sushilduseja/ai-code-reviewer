import git
from typing import List, Dict

class DiffParser:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
    
    def get_diff(self, from_commit: str = "HEAD~1", to_commit: str = "HEAD") -> str:
        """Get unified diff between commits"""
        return self.repo.git.diff(from_commit, to_commit)
    
    def get_changed_files(self, from_commit: str = "HEAD~1", to_commit: str = "HEAD") -> List[Dict]:
        """Parse diff into structured format"""
        diff = self.get_diff(from_commit, to_commit)
        files = []
        current_file = None
        
        for line in diff.split('\n'):
            if line.startswith('diff --git'):
                if current_file:
                    files.append(current_file)
                parts = line.split()
                filepath = parts[2].replace('a/', '')
                current_file = {
                    'path': filepath,
                    'changes': []
                }
            elif current_file and (line.startswith('+') or line.startswith('-')):
                if not line.startswith('+++') and not line.startswith('---'):
                    current_file['changes'].append(line)
        
        if current_file:
            files.append(current_file)
        
        return files
