#!/usr/bin/env python3
"""
Bias Detection Agent
On flagged comments, analyzes commenter profiles for bias likelihood
Computes lightweight bias scores using Gemini

📚 PROMPT ENGINEERING GUIDE: See prompts/bias_detection_prompts.md
   - Profile bio analysis techniques
   - Commercial bias detection patterns
   - Astroturfing identification methods
   - Coordinated attack recognition
   - Account credibility assessment
"""

import json
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from mcp_agent.agents.agent import Agent
from data_structures import Comment

class BiasDetectionAgent:
    """
    Bias detection agent for flagged comments using Gemini.
    Analyzes commenter profiles for bias likelihood.
    """
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.profile_cache: Dict[str, Dict] = {}
        
        # Create MCP agent for potential server integration
        self.mcp_agent = Agent(
            name="bias_detector",
            instruction="""You are a bias detection agent. For flagged comments, analyze:
            1. Commenter's bio for brand affiliations
            2. Posting patterns for promotional content
            3. Account credibility signals (age, followers)
            4. Compute bias likelihood scores""",
            server_names=[],
        )
    
    async def analyze_commenter_bias(self, comment: Comment, classification: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze bias likelihood for flagged commenters."""
        
        if not classification.get("flagged", False):
            return None
        
        prompt = f"""You are a bias detection specialist. Analyze this flagged commenter.

Comment: "{comment.text}"
Author: @{comment.author_username}
Bio: "{comment.author_bio}"
Metrics: {comment.metrics}

Analyze for bias indicators and respond with ONLY this JSON format:
{{
  "comment_id": "{comment.id}",
  "author_id": "{comment.author_id}", 
  "bias_score": 0.3,
  "bias_signals": {{
    "brand_affinity": 0.2,
    "promotional_content": 0.1,
    "account_credibility": 0.8
  }},
  "risk_level": "low",
  "explanation": "Brief explanation"
}}

Scoring (0.0-1.0):
- brand_affinity: Brand mentions, ambassador status, partnerships
- promotional_content: Promo codes, ads, repetitive marketing language  
- account_credibility: Account authenticity indicators
- bias_score: Overall bias likelihood
Risk levels: "low", "medium", "high"

Respond with ONLY the JSON, no other text."""
        
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
            
            result = json.loads(response_text)
            return result
            
        except (json.JSONDecodeError, ValueError, Exception) as e:
            print(f"⚠️ Gemini bias analysis failed for {comment.id}: {str(e)}")
            
            # Enhanced fallback analysis
            brand_affinity = self._detect_brand_signals(comment.author_bio, comment.text)
            promo_content = self._detect_promo_signals(comment.text)
            credibility = self._estimate_credibility(comment.author_bio, comment.metrics)
            
            bias_score = (brand_affinity * 0.4 + promo_content * 0.4 + (1 - credibility) * 0.2)
            
            if bias_score > 0.7:
                risk_level = "high"
            elif bias_score > 0.4:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                "comment_id": comment.id,
                "author_id": comment.author_id,
                "bias_score": bias_score,
                "bias_signals": {
                    "brand_affinity": brand_affinity,
                    "promotional_content": promo_content,
                    "account_credibility": credibility
                },
                "risk_level": risk_level,
                "explanation": f"Fallback analysis: {str(e)}"
            }
    
    def _detect_brand_signals(self, bio: str, text: str) -> float:
        """Simple brand affinity detection."""
        brand_keywords = ["sponsored", "ambassador", "partner", "affiliate", "brand", "promo", "code"]
        combined_text = (bio + " " + text).lower()
        
        matches = sum(1 for keyword in brand_keywords if keyword in combined_text)
        return min(1.0, matches / len(brand_keywords))
    
    def _detect_promo_signals(self, text: str) -> float:
        """Simple promotional content detection."""
        promo_keywords = ["buy", "discount", "sale", "code", "link", "check out", "amazing", "must have"]
        text_lower = text.lower()
        
        matches = sum(1 for keyword in promo_keywords if keyword in text_lower)
        return min(1.0, matches / len(promo_keywords))
    
    def _estimate_credibility(self, comment: Comment) -> float:
        """Simple credibility estimation based on follower count and verification."""
        base_credibility = 0.5
        
        # Boost for verified accounts
        if comment.author_verified:
            base_credibility += 0.3
        
        # Boost for higher follower counts (logarithmic scale)
        if comment.author_followers > 0:
            follower_boost = min(0.3, (comment.author_followers / 100000) * 0.3)
            base_credibility += follower_boost
        
        return min(1.0, base_credibility)
    
    async def analyze_batch_bias(self, comments: List[Comment], classifications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze bias for all flagged comments in a batch."""
        bias_results = []
        
        for comment, classification in zip(comments, classifications):
            if classification.get("flagged", False):
                bias_result = await self.analyze_commenter_bias(comment, classification)
                if bias_result:
                    bias_results.append(bias_result)
        
        return bias_results
    
    def get_bias_summary(self, bias_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of bias analysis results."""
        if not bias_analyses:
            return {"total_analyzed": 0, "risk_distribution": {}, "average_bias_score": 0.0}
        
        risk_counts = {"low": 0, "medium": 0, "high": 0}
        total_bias_score = 0.0
        
        for analysis in bias_analyses:
            risk_level = analysis.get("risk_level", "medium")
            risk_counts[risk_level] += 1
            total_bias_score += analysis.get("bias_score", 0.0)
        
        return {
            "total_analyzed": len(bias_analyses),
            "risk_distribution": risk_counts,
            "average_bias_score": total_bias_score / len(bias_analyses),
            "high_risk_count": risk_counts["high"]
        }