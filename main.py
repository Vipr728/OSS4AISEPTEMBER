#!/usr/bin/env python3
"""
Social Media Analysis Multi-Agent System
Minimal boilerplate for multi-agent social media analysis using last-mile-ai MCP framework.
"""

import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.workflows.swarm.swarm_orchestrator import SwarmOrchestrator
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

from orchestrator import OrchestratorAgent
from summary_agent import SummaryAgent
from bias_detector import BiasDetectorAgent
from spam_scam_detector import SpamScamDetectorAgent


class SocialMediaAnalyzer:
    """Main application class for social media analysis."""
    
    def __init__(self):
        self.app = MCPApp(name="social-media-analyzer")
        self.agents = {}
        self.swarm = None
        
    async def initialize(self):
        """Initialize all agents."""
        self.agents = {
            "orchestrator": OrchestratorAgent(),
            "summary": SummaryAgent(),
            "bias_detector": BiasDetectorAgent(),
            "spam_scam_detector": SpamScamDetectorAgent()
        }
        
        # Setup Swarm orchestrator
        self.swarm = SwarmOrchestrator(
            agents=list(self.agents.values()),
            llm_factory=OpenAIAugmentedLLM,
            initial_agent="orchestrator"
        )
    
    async def analyze_creator(self, creator_data: dict) -> dict:
        """Analyze a creator using the multi-agent system."""
        analysis_request = f"""
        Analyze this social media creator for sponsor evaluation:
        {creator_data}
        
        Provide comprehensive analysis including sentiment, bias detection, and authenticity verification.
        """
        
        result = await self.swarm.generate_str(analysis_request)
        return {"creator": creator_data.get("name", "Unknown"), "analysis": result}
    
    async def run(self):
        """Main application entry point."""
        async with self.app.run():
            await self.initialize()
            
            async with self.agents["orchestrator"], \
                      self.agents["summary"], \
                      self.agents["bias_detector"], \
                      self.agents["spam_scam_detector"]:
                
                # Example usage
                sample_data = {
                    "name": "example_creator",
                    "content": ["Sample post 1", "Sample post 2"],
                    "engagement": {"likes": 1000, "comments": 50}
                }
                
                result = await self.analyze_creator(sample_data)
                print(f"Analysis result: {result}")


async def main():
    analyzer = SocialMediaAnalyzer()
    await analyzer.run()


if __name__ == "__main__":
    asyncio.run(main())
