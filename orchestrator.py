#!/usr/bin/env python3
"""
Multi-Agent Orchestrator
Coordinates all agents and manages the analysis pipeline
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from mcp_agent.app import MCPApp

from data_structures import Comment, PostAnalysis
from main_classifier_agent import MainClassifierAgent
from summary_agent import SummaryAgent
from bias_detection_agent import BiasDetectionAgent

class SocialMediaOrchestrator:
    """Orchestrates the multi-agent analysis pipeline."""
    
    def __init__(self, gemini_api_key: str):
        # Initialize all agents with Gemini
        self.main_agent = MainClassifierAgent(gemini_api_key)
        self.summary_agent = SummaryAgent(gemini_api_key) 
        self.bias_agent = BiasDetectionAgent(gemini_api_key)
        
        # Initialize MCP app for potential server integration
        self.app = MCPApp(name="social_media_analysis")
        
    async def analyze_post_comments(self, post_id: str, comments: List[Comment]) -> Dict[str, Any]:
        """Run full multi-agent analysis pipeline on post comments."""
        
        print(f"🔄 Starting analysis of {len(comments)} comments for post {post_id}")
        
        try:
            # Step 1: Main agent classifies all comments
            print("📊 Running classification and toxicity detection...")
            classifications = await self.main_agent.classify_batch(comments)
            flagged_count = len([c for c in classifications if c.get("flagged", False)])
            print(f"   ✓ Classified {len(classifications)} comments, {flagged_count} flagged")
            
            # Step 2: Summary agent updates running stats
            print("📈 Updating summary statistics...")
            post_analysis = await self.summary_agent.update_post_analysis(post_id, classifications)
            print(f"   ✓ Updated summary: {post_analysis.total_comments} total comments")
            
            # Step 3: Bias agent analyzes flagged comments
            print("🔍 Analyzing bias for flagged comments...")
            bias_analyses = await self.bias_agent.analyze_batch_bias(comments, classifications)
            print(f"   ✓ Analyzed bias for {len(bias_analyses)} flagged comments")
            
            # Generate final risk assessment
            risk_assessment = self._generate_risk_assessment(
                post_analysis, classifications, bias_analyses
            )
            
            result = {
                "post_id": post_id,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_comments": post_analysis.total_comments,
                    "sentiment_distribution": post_analysis.sentiment_distribution,
                    "average_toxicity": post_analysis.toxicity_score,
                    "summary_bullets": post_analysis.summary_bullets
                },
                "classifications": classifications,
                "bias_analyses": bias_analyses,
                "risk_assessment": risk_assessment
            }
            
            print("✅ Analysis completed successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            raise e
    
    def _generate_risk_assessment(self, 
                                 post_analysis: PostAnalysis, 
                                 classifications: List[Dict[str, Any]], 
                                 bias_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate overall risk assessment."""
        
        flagged_comments = len([c for c in classifications if c.get("flagged", False)])
        high_bias_users = len([b for b in bias_analyses if b.get("bias_score", 0) > 0.7])
        
        # Determine overall risk level
        if post_analysis.toxicity_score > 0.6 or high_bias_users > 2:
            overall_risk = "high"
        elif post_analysis.toxicity_score > 0.3 or flagged_comments > 0:
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        return {
            "overall_risk": overall_risk,
            "flagged_comments": flagged_comments,
            "high_bias_users": high_bias_users,
            "average_toxicity": post_analysis.toxicity_score,
            "recommendations": self._generate_recommendations(overall_risk, post_analysis)
        }
    
    def _generate_recommendations(self, risk_level: str, analysis: PostAnalysis) -> List[str]:
        """Generate actionable recommendations based on risk level."""
        recommendations = []
        
        if risk_level == "high":
            recommendations.extend([
                "⚠️ High risk detected - consider content moderation",
                "Review flagged comments for potential removal",
                "Monitor for coordinated inauthentic behavior"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "Monitor comment trends closely",
                "Consider additional bias detection on flagged users"
            ])
        else:
            recommendations.append("✅ Low risk - continue normal monitoring")
        
        if analysis.toxicity_score > 0.5:
            recommendations.append("Implement stronger toxicity filtering")
        
        return recommendations
    
    async def get_post_summary(self, post_id: str) -> Dict[str, Any]:
        """Get current summary for a specific post."""
        return self.summary_agent.get_post_summary(post_id)
    
    async def run_with_app(self):
        """Run with MCP app context for server integration."""
        async with self.app.run() as mcp_agent_app:
            return mcp_agent_app