#!/usr/bin/env python3
"""
Main Classification Agent
Classifies comments as factual/neutral vs opinionated/polarized
Runs toxicity/PII guardrails using Gemini
"""

import json
import google.generativeai as genai
from typing import List, Dict, Any
from mcp_agent.agents.agent import Agent
from data_structures import Comment

class MainClassifierAgent:
    """
    Main classification agent using Gemini.
    Classifies comments and runs toxicity/PII guardrails.
    """
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create MCP agent for potential server integration
        self.mcp_agent = Agent(
            name="main_classifier",
            instruction="""You are a content classification agent. Analyze social media comments and classify them as:
            1. factual/neutral vs opinionated/polarized
            2. Check for toxicity, hate speech, PII
            3. Assign sentiment (positive/negative/neutral)
            4. Flag high-risk content for further review""",
            server_names=[],  # No external tools needed for basic classification
        )
    
    async def classify_comment(self, comment: Comment) -> Dict[str, Any]:
        """Classify a single comment using Gemini."""
        
        prompt = f"""You are a social media content analyst. Analyze this comment and respond with ONLY valid JSON:

Comment Text: "{comment.text}"
Author: @{comment.author_username}
Engagement: {comment.metrics}

Classify this comment and return exactly this JSON structure:
{{
  "comment_id": "{comment.id}",
  "classification": "factual",
  "sentiment": "positive",
  "toxicity_score": 0.1,
  "has_pii": false,
  "flagged": false,
  "risk_factors": []
}}

Classification options: "factual", "opinionated", "polarized"
Sentiment options: "positive", "negative", "neutral"
Toxicity score: number between 0.0 (clean) and 1.0 (very toxic)
Flag as true if toxicity > 0.7 or contains hate speech/PII
Risk factors: array of strings describing any concerns

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
            
            # Validate required fields
            required_fields = ["comment_id", "classification", "sentiment", "toxicity_score", "has_pii", "flagged"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required field: {field}")
            
            return result
            
        except (json.JSONDecodeError, ValueError, Exception) as e:
            print(f"⚠️ Gemini classification failed for {comment.id}: {str(e)}")
            
            # Enhanced fallback analysis
            text_lower = comment.text.lower()
            
            # Simple sentiment analysis
            positive_words = ["love", "great", "amazing", "good", "excellent", "helpful", "thanks"]
            negative_words = ["hate", "bad", "terrible", "awful", "worst", "stupid", "idiots", "trash"]
            
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                sentiment = "positive"
            elif neg_count > pos_count:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            # Simple toxicity detection
            toxic_words = ["idiot", "stupid", "hate", "trash", "scam", "awful", "terrible"]
            toxicity_score = min(1.0, sum(1 for word in toxic_words if word in text_lower) * 0.3)
            
            # Simple classification
            opinion_words = ["think", "feel", "believe", "opinion", "personally"]
            is_opinion = any(word in text_lower for word in opinion_words)
            
            return {
                "comment_id": comment.id,
                "classification": "opinionated" if is_opinion else "factual",
                "sentiment": sentiment,
                "toxicity_score": toxicity_score,
                "has_pii": False,
                "flagged": toxicity_score > 0.7,
                "risk_factors": [f"fallback_analysis: {str(e)}"]
            }
    
    async def classify_batch(self, comments: List[Comment]) -> List[Dict[str, Any]]:
        """Classify a batch of comments."""
        results = []
        for comment in comments:
            result = await self.classify_comment(comment)
            results.append(result)
        return results