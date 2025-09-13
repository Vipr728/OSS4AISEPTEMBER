#!/usr/bin/env python3
"""
Multi-Agent Social Media Analysis System
Using last-mile-ai mcp-agent framework with Gemini AI
Modular design with separate agent files
"""

import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv

from data_structures import Comment
from orchestrator import SocialMediaOrchestrator

# Load environment variables
load_dotenv()

async def main():
    """Example usage of the multi-agent social media analyzer."""
    
    # Check if API key is set
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("❌ Please set GEMINI_API_KEY environment variable")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return
    
    # Initialize orchestrator with all agents
    orchestrator = SocialMediaOrchestrator(gemini_api_key)
    
    # Sample comment data showcasing different triage scenarios
    sample_comments = [
        # BIAS CASE: Suspicious promotional comment with brand-heavy bio
        Comment(
            id="comment_1",
            text="OMG this is literally THE BEST product ever!! 😍 Use code AMAZING15 for discount! Life changing!!! #ad #sponsored #blessed",
            author_id="promo_user_123",
            author_username="luxurylifestyle_babe",
            author_bio="Brand ambassador for @TechCorp @BeautyBrand @FashionHouse | PR friendly | Partnerships welcome! 💎✨",
            timestamp=datetime.now(),
            metrics={"likes": 87, "replies": 3, "retweets": 24},
            author_followers=15420,
            author_verified=False
        ),
        
        # NEUTRAL CASE: Balanced, genuine-looking feedback
        Comment(
            id="comment_2", 
            text="Thanks for the honest review. I've been considering this product for a while. The price point seems reasonable for the features mentioned.",
            author_id="regular_user_456",
            author_username="tech_curious_mom",
            author_bio="Mom of 2 | Love trying new tech gadgets | Honest reviews only",
            timestamp=datetime.now(),
            metrics={"likes": 12, "replies": 4, "retweets": 1},
            author_followers=342,
            author_verified=False
        ),
        
        # BIAS CASE: Coordinated negative attack with suspicious profile
        Comment(
            id="comment_3",
            text="This creator is a FRAUD! Don't trust anything they say. Their previous reviews were all LIES. Save your money people!!",
            author_id="throwaway_789", 
            author_username="truth_teller_2024",
            author_bio="Exposing fake influencers and scam products since 2024 | Follow for REAL truth",
            timestamp=datetime.now(),
            metrics={"likes": 156, "replies": 47, "retweets": 89},
            author_followers=1,
            author_verified=False
        ),
        
        # NEUTRAL CASE: Simple positive feedback, normal profile
        Comment(
            id="comment_4",
            text="Good breakdown of the features. Appreciate you mentioning both pros and cons instead of just hyping it up.",
            author_id="longtime_viewer_101",
            author_username="sarah_thompson",
            author_bio="Software engineer | Dog mom | Coffee enthusiast ☕",
            timestamp=datetime.now(),
            metrics={"likes": 23, "replies": 2, "retweets": 0},
            author_followers=1247,
            author_verified=False
        ),
        
        # BIAS CASE: Fake negative review from competitor
        Comment(
            id="comment_5",
            text="Terrible quality! I returned mine immediately. Try @CompetitorBrand instead - much better value and customer service!",
            author_id="definitely_real_user",
            author_username="product_expert_pro",
            author_bio="Product reviewer | Helping people make smart purchases | @CompetitorBrand affiliate partner",
            timestamp=datetime.now(),
            metrics={"likes": 73, "replies": 15, "retweets": 32},
            author_followers=8934,
            author_verified=False
        ),
        
        # NEUTRAL CASE: Genuine question from real user
        Comment(
            id="comment_6",
            text="Has anyone tried this with sensitive skin? I'm interested but worried about allergic reactions based on the ingredient list.",
            author_id="skincare_seeker",
            author_username="jenny_wellness",
            author_bio="Skincare journey | Sensitive skin struggles | Sharing what works",
            timestamp=datetime.now(),
            metrics={"likes": 8, "replies": 12, "retweets": 2},
            author_followers=567,
            author_verified=False
        )
    ]
    
    try:
        print("🚀 Starting Multi-Agent Social Media Analysis")
        print("=" * 60)
        
        # Run the full analysis pipeline
        result = await orchestrator.analyze_post_comments("beauty_product_review_2024", sample_comments)
        
        print("\n" + "="*60)
        print("MULTI-AGENT SOCIAL MEDIA ANALYSIS REPORT")
        print("="*60)
        
        # Pretty print the results
        print(f"\n📊 POST SUMMARY:")
        summary = result["summary"]
        print(f"   Total Comments: {summary['total_comments']}")
        print(f"   Sentiment Distribution: {summary['sentiment_distribution']}")
        print(f"   Average Toxicity: {summary['average_toxicity']:.3f}/1.0")
        
        print(f"\n💡 KEY INSIGHTS:")
        for bullet in summary["summary_bullets"]:
            print(f"   • {bullet}")
        
        print(f"\n⚠️ RISK ASSESSMENT:")
        risk = result["risk_assessment"]
        print(f"   Overall Risk: {risk['overall_risk'].upper()}")
        print(f"   Flagged Comments: {risk['flagged_comments']}")
        print(f"   High Bias Users: {risk['high_bias_users']}")
        
        print(f"\n📋 RECOMMENDATIONS:")
        for rec in risk["recommendations"]:
            print(f"   • {rec}")
        
        print(f"\n🔍 DETAILED ANALYSIS:")
        print(f"   Classifications: {len(result['classifications'])} comments analyzed")
        print(f"   Bias Analyses: {len(result['bias_analyses'])} flagged users analyzed")
        
        # Save full results to file for detailed review
        with open("analysis_results.json", "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n💾 Full results saved to: analysis_results.json")
        
        print("\n✅ Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())