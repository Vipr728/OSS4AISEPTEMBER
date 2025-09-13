# Social Media Analysis Multi-Agent System

Minimal boilerplate for a multi-agent social media analysis system using [last-mile-ai MCP agent framework](https://github.com/lastmile-ai/mcp-agent).

## Overview

Four specialized AI agents for social media creator analysis:

1. **Orchestrator** - Main coordinator agent
2. **Summary Agent** - Content analysis and sentiment evaluation  
3. **Bias Detector** - Brand safety and bias detection
4. **Spam/Scam Detector** - Authenticity verification

## Files

- `main.py` - Main application entry point
- `orchestrator.py` - Main coordinator agent
- `summary_agent.py` - Content analysis specialist
- `bias_detector.py` - Bias and brand safety specialist  
- `spam_scam_detector.py` - Authenticity verification specialist

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Customization

Extend the agent classes in each file to implement your specific analysis logic. The boilerplate provides the basic structure for multi-agent coordination using the MCP framework's Swarm pattern.
