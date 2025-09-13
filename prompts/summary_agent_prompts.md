# Summary Agent Prompt Engineering Guide

## 🎯 Purpose
The Summary Agent receives **processed data from multiple routing paths** (Triage → Summarizer AND Triage → Bias → Summarizer) and creates comprehensive insights that combine authentic engagement metrics with bias detection findings.

## 🔄 Dual Input Processing

### **Input Source 1: Direct from Triage** (Neutral/Clean Comments)
- Authentic user feedback
- Genuine questions and concerns
- Normal positive/negative sentiment
- Standard engagement patterns

### **Input Source 2: From Bias Agent** (Flagged Comments + Analysis)
- Comments with bias analysis results
- Commercial intent classifications
- Astroturfing detection results
- Account credibility assessments

## 🤖 Core Summary Generation Prompt

```
You are a social media analytics expert creating comprehensive post summaries. You receive data from two sources:

1. CLEAN COMMENTS (routed directly from triage):
   - Authentic user engagement
   - Genuine sentiment and feedback
   - Normal interaction patterns

2. FLAGGED COMMENTS (analyzed by bias detection):
   - Comments with potential bias/manipulation
   - Commercial intent analysis
   - Account credibility assessments
   - Astroturfing/coordination detection

Your job is to create a balanced summary that separates authentic engagement from potentially biased interactions.

CLEAN COMMENT DATA:
{clean_comments_summary}

BIAS ANALYSIS RESULTS:
{bias_analysis_results}

OVERALL METRICS:
- Total Comments: {total_comments}
- Clean Comments: {clean_count}
- Flagged Comments: {flagged_count}
- Bias Investigation Results: {bias_results_summary}

CREATE COMPREHENSIVE SUMMARY:

1. AUTHENTIC ENGAGEMENT ANALYSIS:
   - Sentiment distribution among clean comments only
   - Genuine user concerns and feedback themes
   - Organic conversation topics
   - Real user satisfaction indicators

2. BIAS IMPACT ASSESSMENT:
   - Commercial bias influence on overall sentiment
   - Astroturfing detection results
   - Coordinated behavior patterns
   - Authenticity vs manipulation ratio

3. CONTENT CREDIBILITY SCORING:
   - Overall authenticity percentage
   - Manipulation risk level
   - Organic engagement quality
   - Sponsor/brand awareness recommendations

RETURN JSON:
{
  "authentic_engagement": {
    "clean_comment_count": number,
    "organic_sentiment": {
      "positive": percentage,
      "negative": percentage,
      "neutral": percentage
    },
    "genuine_themes": ["list", "of", "organic", "topics"],
    "user_satisfaction_indicators": ["positive", "signals"],
    "real_concerns": ["legitimate", "issues", "raised"]
  },
  "bias_impact": {
    "flagged_comment_count": number,
    "commercial_bias_detected": number,
    "astroturfing_signals": number,
    "coordination_evidence": number,
    "manipulation_influence": {
      "sentiment_skew": "positive" | "negative" | "minimal",
      "engagement_inflation": percentage,
      "credibility_impact": "high" | "medium" | "low"
    }
  },
  "overall_assessment": {
    "authenticity_score": 0.0-1.0,
    "content_credibility": "high" | "medium" | "low",
    "manipulation_risk": "high" | "medium" | "low",
    "organic_vs_artificial_ratio": "percentage authentic",
    "sponsor_confidence_level": "high" | "medium" | "low"
  },
  "actionable_insights": [
    "bullet points with specific findings",
    "patterns detected in authentic engagement",
    "bias manipulation tactics identified",
    "recommendations for content creators/sponsors"
  ],
  "detailed_breakdown": {
    "authentic_feedback_summary": "Analysis of genuine user responses",
    "bias_pattern_analysis": "Specific manipulation techniques found",
    "credibility_factors": ["elements", "supporting", "authenticity"],
    "red_flags": ["concerning", "patterns", "detected"]
  }
}
```

## 🎨 Specialized Summary Types

### **High Authenticity Scenario** (90%+ clean comments)
```
Focus on genuine engagement quality:

AUTHENTIC ENGAGEMENT EMPHASIS:
- Highlight organic conversation themes
- Detailed analysis of genuine sentiment drivers
- User satisfaction and concern patterns
- Natural engagement flow analysis

BIAS MONITORING:
- Note small percentage of flagged content
- Mention bias detection as quality assurance
- Emphasize organic nature of overall engagement
- Provide confidence in authenticity

SPONSOR RECOMMENDATIONS:
- High confidence in engagement authenticity
- Safe for brand partnership decisions
- Genuine audience feedback valuable for product development
- Low risk of manipulation concerns
```

### **Mixed Authenticity Scenario** (60-80% clean comments)
```
Balance authentic insights with bias awareness:

BALANCED ANALYSIS:
- Separate authentic feedback from biased content
- Compare organic sentiment vs artificially influenced
- Identify which bias types are affecting perception
- Assess overall credibility impact

CREDIBILITY IMPACT:
- Moderate confidence in overall sentiment
- Specific bias patterns affecting perception
- Recommendations for deeper investigation
- Authentic user signals still valuable

ACTIONABLE INSIGHTS:
- Focus on clean comments for genuine feedback
- Flag specific bias manipulation tactics
- Recommend monitoring for coordination
- Suggest bias mitigation strategies
```

### **High Manipulation Scenario** (40%+ flagged content)
```
Emphasize manipulation detection and authentic signal extraction:

MANIPULATION FOCUS:
- Detailed bias pattern analysis
- Coordinated behavior evidence
- Commercial influence assessment
- Authentic signal extraction from noise

RISK ASSESSMENT:
- High manipulation risk identified
- Specific tactics used for bias
- Credibility significantly impacted
- Organic feedback difficult to assess

IMMEDIATE ACTIONS:
- Recommend bias investigation expansion
- Suggest authentic engagement verification
- Flag for manual review by sponsors
- Provide bias mitigation recommendations
```

## 📊 Aggregation Logic

### **Authentic Sentiment Calculation**
```python
# Only use clean comments for authentic sentiment
authentic_sentiment = calculate_sentiment(clean_comments_only)

# Compare to overall sentiment including flagged comments
total_sentiment = calculate_sentiment(all_comments)

sentiment_manipulation_impact = total_sentiment - authentic_sentiment
```

### **Credibility Scoring**
```python
authenticity_score = (
    clean_comment_count / total_comments * 0.6 +
    (1 - average_bias_score) * 0.3 +
    account_credibility_average * 0.1
)

content_credibility = {
    0.8-1.0: "high",
    0.6-0.8: "medium",
    0.0-0.6: "low"
}
```

### **Bias Impact Assessment**
```python
manipulation_influence = {
    "sentiment_skew": calculate_skew(authentic_vs_total_sentiment),
    "engagement_inflation": flagged_engagement / total_engagement,
    "credibility_impact": assess_impact(bias_types_detected)
}
```

## 🔧 Fallback Summary Generation

If Gemini API fails, use structured aggregation:

```python
def fallback_summary(clean_comments, bias_results):
    # Basic sentiment aggregation
    authentic_sentiment = aggregate_sentiment(clean_comments)
    
    # Simple bias impact calculation
    bias_count = len(bias_results)
    total_count = len(clean_comments) + bias_count
    authenticity_percentage = len(clean_comments) / total_count
    
    # Generate basic insights
    insights = [
        f"Analyzed {total_count} total comments",
        f"{authenticity_percentage:.1%} appear authentic",
        f"{bias_count} comments flagged for potential bias",
        f"Organic sentiment: {authentic_sentiment}"
    ]
    
    return {
        "authentic_engagement": {"organic_sentiment": authentic_sentiment},
        "bias_impact": {"flagged_comment_count": bias_count},
        "overall_assessment": {"authenticity_score": authenticity_percentage},
        "actionable_insights": insights
    }
```

## 🎯 Summary Quality Guidelines

### **Actionable Insights Should Include:**
1. **For Sponsors**: Confidence level in engagement authenticity
2. **For Creators**: Specific bias patterns affecting their content
3. **For Platforms**: Manipulation tactics requiring attention
4. **For Users**: Transparency about content authenticity

### **Avoid These Common Issues:**
- Mixing authentic and biased sentiment without distinction
- Ignoring bias impact on overall perception
- Over-weighting small amounts of biased content
- Under-communicating manipulation risks

### **Quality Metrics:**
- Clear separation of authentic vs biased insights
- Specific evidence for credibility assessments
- Actionable recommendations based on findings
- Appropriate confidence levels for different scenarios

## 📈 Continuous Improvement

### **Summary Accuracy Validation**
- Compare predicted authenticity with manual verification
- Track sponsor decision confidence based on summaries
- Monitor false positive/negative rates in bias detection
- Validate authenticity score correlations with real outcomes

### **Prompt Optimization**
- Refine insight generation based on user feedback
- Improve bias impact communication clarity
- Enhance authenticity scoring accuracy
- Develop better risk communication frameworks

### **Integration Enhancement**
- Improve data flow from bias detection results
- Optimize clean comment processing efficiency
- Enhance credibility factor weighting
- Develop real-time summary updating capabilities