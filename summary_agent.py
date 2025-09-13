#!/usr/bin/env python3
"""
Summary Agent
Incrementally updates per-post "controlled sentiment" state
Maintains running stats and bullet summaries using Gemini

📚 PROMPT ENGINEERING GUIDE: See prompts/summary_agent_prompts.md
   - Dual input processing (clean + bias-analyzed comments)
   - Authentic engagement vs manipulation analysis
   - Credibility scoring methodology
   - Actionable insight generation
   - Quality assurance guidelines
"""

import json
import google.generativeai as genai
from datetime import datetime
from typing import Dict, List, Any
from mcp_agent.agents.agent import Agent
from data_structures import PostAnalysis

class SummaryAgent:
    """
    Incremental sentiment summarization agent using Gemini.
    Maintains running stats and bullet summaries per post.
    """
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.post_states: Dict[str, PostAnalysis] = {}
        
        # Create MCP agent for potential server integration
        self.mcp_agent = Agent(
            name="summary_agent", 
            instruction="""You are a summarization agent. Your job is to:
            1. Maintain running sentiment statistics for posts
            2. Generate bullet-point summaries of comment trends
            3. Track toxicity patterns over time
            4. Provide controlled sentiment analysis updates""",
            server_names=[],
        )
    
    async def update_post_analysis(self, post_id: str, classifications: List[Dict[str, Any]]) -> PostAnalysis:
        """Update running analysis for a post."""
        
        # Initialize or get existing analysis
        if post_id not in self.post_states:
            self.post_states[post_id] = PostAnalysis(
                post_id=post_id,
                total_comments=0,
                sentiment_distribution={"positive": 0, "negative": 0, "neutral": 0},
                toxicity_score=0.0,
                bias_flags=[],
                summary_bullets=[],
                last_updated=datetime.now()
            )
        
        analysis = self.post_states[post_id]
        
        # Update basic stats
        new_comments = len(classifications)
        old_total = analysis.total_comments
        analysis.total_comments += new_comments
        
        # Update sentiment distribution and toxicity
        total_toxicity = analysis.toxicity_score * old_total
        
        for classification in classifications:
            sentiment = classification.get("sentiment", "neutral")
            analysis.sentiment_distribution[sentiment] += 1
            
            # Add to running toxicity total
            toxicity = classification.get("toxicity_score", 0.0)
            total_toxicity += toxicity
        
        # Recalculate average toxicity
        analysis.toxicity_score = total_toxicity / analysis.total_comments if analysis.total_comments > 0 else 0.0
        
        # Generate new summary bullets using Gemini
        analysis.summary_bullets = await self._generate_summary_bullets(analysis, classifications)
        analysis.last_updated = datetime.now()
        
        return analysis
    
    async def _generate_summary_bullets(self, analysis: PostAnalysis, new_classifications: List[Dict[str, Any]]) -> List[str]:
        """Generate bullet point summary using Gemini."""
        
        prompt = f"""You are a social media analyst. Create a bullet-point summary.

Current Stats:
- Total comments: {analysis.total_comments}
- Sentiment: {analysis.sentiment_distribution}
- Average toxicity: {analysis.toxicity_score:.3f}

Recent classifications: {len(new_classifications)} new comments analyzed

Create 3-4 bullet points and respond with ONLY a JSON array:
["Bullet point 1", "Bullet point 2", "Bullet point 3"]

Focus on sentiment trends, toxicity levels, and key insights."""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Check if response is empty
            if not response or not response.text or not response.text.strip():
                raise ValueError("Empty response from Gemini")
            
            response_text = response.text.strip()
            
            # Try to extract JSON if it's wrapped in markdown
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            
            bullets = json.loads(response_text)
            return bullets if isinstance(bullets, list) else []
            
        except (json.JSONDecodeError, ValueError, Exception) as e:
            print(f"⚠️ Gemini summary failed: {str(e)}")
            
            # Enhanced fallback bullets
            total = analysis.total_comments
            pos_pct = (analysis.sentiment_distribution["positive"] / total) * 100 if total > 0 else 0
            neg_pct = (analysis.sentiment_distribution["negative"] / total) * 100 if total > 0 else 0
            neu_pct = (analysis.sentiment_distribution["neutral"] / total) * 100 if total > 0 else 0
            
            bullets = [
                f"📊 Analyzed {total} total comments",
                f"💭 Sentiment: {pos_pct:.1f}% positive, {neg_pct:.1f}% negative, {neu_pct:.1f}% neutral",
                f"⚠️ Toxicity level: {analysis.toxicity_score:.2f}/1.0"
            ]
            
            if analysis.toxicity_score > 0.5:
                bullets.append("🚨 High toxicity detected - review recommended")
            elif analysis.toxicity_score > 0.3:
                bullets.append("⚠️ Moderate toxicity - monitor closely")
            else:
                bullets.append("✅ Low toxicity - healthy discussion")
                
            return bullets
    
    def get_post_summary(self, post_id: str) -> Dict[str, Any]:
        """Get current summary for a post."""
        if post_id not in self.post_states:
            return {"error": "Post not found"}
        
        analysis = self.post_states[post_id]
        return {
            "post_id": post_id,
            "total_comments": analysis.total_comments,
            "sentiment_distribution": analysis.sentiment_distribution,
            "average_toxicity": analysis.toxicity_score,
            "summary_bullets": analysis.summary_bullets,
            "last_updated": analysis.last_updated.isoformat()
        }