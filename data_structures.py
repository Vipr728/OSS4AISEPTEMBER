#!/usr/bin/env python3
"""
Data structures for social media analysis system
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any

@dataclass
class Comment:
    """Normalized comment structure from Ingestor."""
    id: str
    text: str
    author_id: str
    author_username: str
    author_bio: str
    timestamp: datetime
    metrics: Dict[str, int]  # likes, retweets, etc.
    author_followers: int = 0
    author_verified: bool = False
    
@dataclass
class PostAnalysis:
    """Running analysis state for a post."""
    post_id: str
    total_comments: int
    sentiment_distribution: Dict[str, int]
    toxicity_score: float
    bias_flags: List[Dict[str, Any]]
    summary_bullets: List[str]
    last_updated: datetime