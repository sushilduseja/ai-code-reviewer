# AI Multi-Agent Code Review System

Automated code review using specialized AI agents for security, performance, and quality analysis via SIM.ai workflows.

## Features
- **Multi-Agent Analysis**: Parallel security, performance, and quality reviews
- **Git Integration**: Analyzes diffs between commits automatically
- **Structured Reports**: Generates markdown reports with findings organized by severity
- **SIM.ai Powered**: Uses production-grade AI workflows for code analysis
- **Fast & Efficient**: ThreadPoolExecutor for parallel agent execution
- **Zero-Config Setup**: Just add your API key to `.env`

## Architecture

```
┌─────────────────┐
│   Git Diff      │
│   Parser        │
└────────┬────────┘
         │
         ├─────────────────────────────┐
         ▼                             ▼
    ┌─────────────────┐    ┌──────────────────┐
    │ Changed Files   │    │ Code Changes     │
    └────────┬────────┘    └──────────┬───────┘
             │                        │
             └────────────┬───────────┘
                          │
                  ┌───────▼──────────┐
                  │  Orchestrator    │
                  │  (ThreadPool)    │
                  └────┬────┬────┬───┘
                       │    │    │
        ┌──────────────┐│    │    │┌──────────────┐
        │              │└────┼────┘│              │
        ▼              ▼     ▼     ▼              ▼
    ┌─────────┐  ┌─────────┐  ┌──────────┐
    │Security │  │Performance│ │ Quality  │
    │ Agent   │  │ Agent     │ │ Agent    │
    └────┬────┘  └─────┬─────┘ └────┬─────┘
         │             │            │
         └─────────────┴────────────┘
                      │
              ┌───────▼──────┐
              │Report Writer │
              └───────┬──────┘
                      │
              ┌───────▼──────────┐
              │review_report.md  │
              └──────────────────┘
```

## Installation

### Prerequisites
- Python 3.8+
- Git
- SIM.ai API Key

### Setup
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API key:
```env
SIM_API_KEY=your_api_key_here
```

## Usage

### Analyze Code Changes
```bash
python main.py /path/to/repo [from_commit] [to_commit]
```

**Examples:**
```bash
# Analyze changes between two commits
python main.py . HEAD~1 HEAD

# Analyze changes in current repo (default: HEAD~1 to HEAD)
python main.py .

# Analyze changes in specific directory
python main.py /path/to/project HEAD~5 HEAD
```

### Test Individual Agents
```bash
python test_agents.py
```

This runs each agent on sample test code and displays findings.

## Output

The system generates a `review_report.md` file with organized findings:

```markdown
# AI Code Review Report

## File: `example.py`

### Security Issues
**[CRITICAL]** Line 1
- Issue: Hardcoded password 'admin123' exposed in source code
- Recommendation: Use environment variables or secure credential management

### Performance Issues
**[HIGH]** Line 42
- Issue: O(n²) nested loop complexity
- Recommendation: Use set-based approach for O(n) complexity

### Quality Issues
**[MEDIUM]** Line 15
- Issue: Function name is vague and doesn't describe purpose
- Recommendation: Rename to be more descriptive
```

## Agents

### Security Agent
**Workflow**: `845faaf5-b6aa-4c6d-9019-7eddb97da6a5`

Detects:
- Hardcoded credentials (passwords, API keys, tokens)
- SQL injection vulnerabilities
- Unsafe deserialization
- Missing input validation
- Security best practice violations

### Performance Agent
**Workflow**: `ba0f060e-ccb4-42ef-8d86-3a0ff1d932b4`

Detects:
- Algorithm complexity issues (O(n²), O(n³), etc.)
- Memory inefficiencies
- Inefficient data structure usage
- Lack of early termination optimization
- Scalability problems

### Quality Agent
**Workflow**: `c2a5be01-67af-474b-a6e7-dfd93c5a693c`

Detects:
- Poor naming conventions
- Deep nesting and cyclomatic complexity
- Missing error handling
- Magic strings/numbers
- Code maintainability issues

## Configuration

### Environment Variables
- `SIM_API_KEY`: Your SIM.ai API key (required)

### Agent Configuration
Agent endpoints are configured in `config.py`:
```python
AGENTS = {
    "security": {
        "url": "https://www.sim.ai/api/workflows/845faaf5-b6aa-4c6d-9019-7eddb97da6a5/execute",
        "name": "Security Reviewer"
    },
    # ... other agents
}
```

## Project Structure
```
ai-code-reviewer/
├── main.py                 # CLI entry point
├── config.py               # Agent configuration
├── requirements.txt        # Python dependencies
├── .env                    # API key (git-ignored)
├── .gitignore              # Git ignore rules
├── test_code.py            # Sample code with intentional issues
├── test_agents.py          # Agent test runner
├── review_report.md        # Generated review report
├── core/
│   ├── diff_parser.py      # Git diff parsing
│   └── orchestrator.py     # Multi-agent orchestration
└── agents/
    ├── security_agent.py   # Security analysis
    ├── performance_agent.py# Performance analysis
    └── quality_agent.py    # Code quality analysis
```

## How It Works

1. **Diff Parsing**: Analyzes git diff to extract changed files and modifications
2. **Parallel Processing**: Sends code changes to all three agents simultaneously
3. **Finding Extraction**: Parses workflow responses and extracts findings
4. **Report Generation**: Combines all findings into a structured markdown report

## Example Workflow

```bash
$ python main.py . HEAD~1 HEAD
Analyzing changes in . from HEAD~1 to HEAD...
Found 2 changed files

[1/2] Reviewing test_code.py...
[2/2] Reviewing utils.py...

Review complete. Report saved to: review_report.md
```

## Troubleshooting

### "401 Unauthorized" Error
- Verify `SIM_API_KEY` is set in `.env`
- Check that the API key is valid and not expired

### "NO_CODE_PROVIDED" Error
- Ensure the git diff is being parsed correctly
- Verify changed files contain valid Python code

### Agents Return Empty Findings
- Run `python test_agents.py` to verify agents are working
- Check that code has actual issues (test code includes examples)

## Development

### Running Tests
```bash
python test_agents.py
```

### Adding Custom Agents
1. Create new agent file in `agents/` directory
2. Implement the same interface as existing agents
3. Update `orchestrator.py` to include the new agent
4. Add configuration to `config.py`

## Performance

- **Parallelization**: All three agents run simultaneously using ThreadPoolExecutor
- **Timeout**: 60-second timeout per agent API call
- **Rate Limiting**: Built-in retry logic with exponential backoff

## License
MIT

## Support
For issues or questions, please refer to the SIM.ai documentation at https://www.sim.ai