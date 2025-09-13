# Main Classifier Agent Prompt Engineering Guide

## 🎯 Purpose
The Main Classifier Agent provides **foundational content analysis** for all comments, performing initial classification, sentiment analysis, and toxicity detection. This analysis feeds into both the Triage Agent (for routing decisions) and the final Summary Agent.

## 🔍 Analysis Dimensions

### **Content Classification**
- **Factual**: Objective statements, data, verifiable claims
- **Opinionated**: Subjective views, personal experiences, emotional responses
- **Promotional**: Marketing content, calls-to-action, commercial intent
- **Informational**: Questions, requests for clarification, neutral inquiries

### **Sentiment Analysis**
- **Positive**: Favorable opinions, satisfaction, recommendations
- **Negative**: Complaints, dissatisfaction, criticism
- **Neutral**: Balanced views, informational content, questions

### **Toxicity Detection**
- **High (0.7-1.0)**: Abusive language, harassment, hate speech
- **Medium (0.4-0.6)**: Insults, aggressive tone, personal attacks
- **Low (0.1-0.3)**: Mild negativity, frustration, criticism
- **None (0.0)**: Civil discourse, constructive feedback

## 🤖 Core Classification Prompt

```
You are a content moderation and analysis expert. Analyze this social media comment across multiple dimensions to provide foundational insights for further processing.

COMMENT TO ANALYZE:
Text: {comment_text}
Author: {author_username}
Context: {post_context}

ANALYSIS FRAMEWORK:

1. CONTENT CLASSIFICATION:
   Determine the primary nature of this comment:
   - "factual": Contains verifiable information, data, or objective statements
   - "opinionated": Expresses personal views, subjective experiences, emotions
   - "promotional": Contains marketing language, calls-to-action, commercial intent
   - "informational": Asks questions, seeks clarification, neutral inquiry

2. SENTIMENT ANALYSIS:
   Assess the overall emotional tone:
   - "positive": Favorable, satisfied, recommending, enthusiastic
   - "negative": Critical, disappointed, warning others, frustrated
   - "neutral": Balanced, informational, no clear emotional direction

3. TOXICITY ASSESSMENT:
   Evaluate harmful content level (0.0-1.0):
   - 0.8-1.0: Severe abuse, harassment, hate speech, threats
   - 0.6-0.7: Strong insults, personal attacks, aggressive language
   - 0.4-0.5: Mild insults, dismissive language, confrontational tone
   - 0.2-0.3: Frustration, mild criticism, negative but civil
   - 0.0-0.1: Constructive criticism, civil disagreement, neutral/positive

4. RISK FACTOR IDENTIFICATION:
   Identify specific concerning elements:
   - "abusive_language": Insults, profanity, derogatory terms
   - "personal_attacks": Targeting individual character vs content
   - "false_claims": Unsubstantiated accusations, misinformation
   - "spam_indicators": Repetitive content, excessive promotion
   - "privacy_violations": Sharing personal information inappropriately

5. PII DETECTION:
   Check for personally identifiable information:
   - Email addresses, phone numbers, home addresses
   - Full names (when not public figures)
   - Financial information, social security numbers
   - Private social media handles or personal accounts

RETURN STRUCTURED JSON:
{
  "classification": "factual" | "opinionated" | "promotional" | "informational",
  "confidence": 0.0-1.0,
  "sentiment": "positive" | "negative" | "neutral",
  "sentiment_intensity": 0.0-1.0,
  "toxicity_score": 0.0-1.0,
  "has_pii": boolean,
  "risk_factors": ["list", "of", "identified", "risks"],
  "flagged": boolean,
  "analysis_details": {
    "classification_reasoning": "Explanation for content type determination",
    "sentiment_indicators": ["words", "phrases", "that", "indicate", "sentiment"],
    "toxicity_evidence": ["specific", "toxic", "language", "found"],
    "constructive_elements": ["positive", "aspects", "if", "any"],
    "context_considerations": "How context affects interpretation"
  },
  "moderation_recommendation": {
    "action": "approve" | "review" | "flag" | "remove",
    "priority": "low" | "medium" | "high" | "urgent",
    "reasoning": "Specific justification for recommendation"
  }
}
```

## 🎨 Specialized Classification Prompts

### **Factual vs Opinionated Distinction**
```
FACTUAL INDICATORS:
- "According to the specifications..."
- "The product measures 5 inches..."
- "It contains these ingredients:"
- "The warranty covers..."
- "Available in these colors:"
- Statistical information or verifiable data

OPINIONATED INDICATORS:
- "I think/feel/believe..."
- "In my experience..."
- "This seems/appears..."
- Emotional language ("amazing", "terrible", "disappointing")
- Personal comparisons ("better than", "worse than")
- Subjective quality assessments

CLASSIFICATION LOGIC:
If comment contains >70% verifiable information → "factual"
If comment contains >70% personal views/emotions → "opinionated"
If comment contains clear promotional intent → "promotional"
If comment primarily asks questions → "informational"
```

### **Sentiment Analysis with Context**
```
POSITIVE SENTIMENT PATTERNS:
- Satisfaction expressions: "love it", "works perfectly", "exceeded expectations"
- Recommendations: "would buy again", "highly recommend", "must-have"
- Gratitude: "thanks for the honest review", "helpful information"
- Enthusiasm: excitement, positive emoji usage, exclamation points

NEGATIVE SENTIMENT PATTERNS:
- Dissatisfaction: "disappointed", "waste of money", "poor quality"
- Warnings: "don't buy", "avoid this", "save your money"
- Frustration: "can't believe", "such a hassle", complaint language
- Regret: "wish I hadn't", "should have known better"

NEUTRAL SENTIMENT PATTERNS:
- Information seeking: questions without emotional charge
- Balanced reviews: "pros and cons", "mixed experience"
- Factual statements without opinion markers
- Process descriptions without value judgments

CONTEXT CONSIDERATIONS:
- Sarcasm detection: positive words in negative context
- Cultural differences in expression
- Product category norms (luxury vs budget expectations)
- Comparison context (relative to alternatives)
```

### **Toxicity Scoring Guidelines**
```
HIGH TOXICITY (0.7-1.0):
- Direct insults: "you're an idiot", "stupid people"
- Profanity directed at individuals
- Hate speech, discrimination, harassment
- Threats or intimidation
- Extreme aggression: "I hope you fail"

MEDIUM TOXICITY (0.4-0.6):
- Dismissive language: "obviously you don't understand"
- Mocking or condescending tone
- Mild personal attacks: "typical influencer"
- Aggressive disagreement: "you're completely wrong"
- Inflammatory generalizations

LOW TOXICITY (0.1-0.3):
- Frustrated tone without personal attacks
- Strong criticism of product/content (not person)
- Disappointed language without aggression
- Blunt feedback without insults

NO TOXICITY (0.0):
- Constructive criticism
- Respectful disagreement
- Neutral or positive language
- Professional feedback tone
```

## 🔧 Fallback Classification Logic

If Gemini API fails, use rule-based classification:

```python
def fallback_classifier(comment_text):
    # Simple keyword-based classification
    factual_keywords = ["measures", "contains", "specifications", "according to", "data shows"]
    opinion_keywords = ["think", "feel", "believe", "in my opinion", "seems like"]
    promo_keywords = ["buy", "discount", "code", "link", "check out", "sponsored"]
    
    factual_score = count_keywords(comment_text, factual_keywords)
    opinion_score = count_keywords(comment_text, opinion_keywords)
    promo_score = count_keywords(comment_text, promo_keywords)
    
    # Classification logic
    if promo_score > 0:
        classification = "promotional"
    elif factual_score > opinion_score:
        classification = "factual"
    elif opinion_score > 0:
        classification = "opinionated"
    else:
        classification = "informational"
    
    # Simple sentiment analysis
    positive_words = ["good", "great", "love", "amazing", "recommend"]
    negative_words = ["bad", "terrible", "hate", "awful", "avoid"]
    
    pos_count = count_keywords(comment_text, positive_words)
    neg_count = count_keywords(comment_text, negative_words)
    
    if pos_count > neg_count:
        sentiment = "positive"
    elif neg_count > pos_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Basic toxicity detection
    toxic_words = ["idiot", "stupid", "trash", "scam", "fraud"]
    toxicity_score = min(1.0, count_keywords(comment_text, toxic_words) * 0.3)
    
    return {
        "classification": classification,
        "confidence": 0.7,  # Lower confidence for fallback
        "sentiment": sentiment,
        "toxicity_score": toxicity_score,
        "has_pii": False,  # Conservative default
        "risk_factors": ["parse_error: Gemini API unavailable"],
        "flagged": toxicity_score > 0.5
    }
```

## 📊 Quality Assurance

### **Classification Accuracy Checks**
- Verify classification aligns with content analysis
- Ensure sentiment matches emotional tone
- Confirm toxicity score reflects harmful content level
- Check flagging threshold appropriateness

### **Edge Case Handling**
```
SARCASM DETECTION:
"Oh great, another 'life-changing' product" → Negative sentiment despite "great"

CONTEXTUAL TOXICITY:
"This is trash" (about product) vs "You are trash" (personal attack)

CULTURAL SENSITIVITY:
Different communication styles across cultures
Varying directness levels in feedback

DOMAIN-SPECIFIC LANGUAGE:
Technical terms that might seem harsh but are standard
Industry jargon that could be misinterpreted
```

### **Calibration Standards**
- Reserve 0.8+ toxicity for clear abusive content
- Use 0.6-0.7 for aggressive but not abusive language
- Maintain consistency in factual vs opinionated boundaries
- Ensure promotional detection captures clear commercial intent

## 📈 Performance Optimization

### **Batch Processing**
```
Analyze these {n} comments for classification:

For each comment, provide the same detailed analysis format.
Maintain consistency across similar comment types.
Return array of {n} classification results.
```

### **Speed vs Accuracy Balance**
- Pre-filter obvious cases (clear promotional language)
- Focus detailed analysis on ambiguous content
- Use confidence scores to indicate analysis certainty
- Implement fast-track for clearly benign content

## 🎯 Integration Points

### **Triage Agent Input**
Main Classifier provides foundational analysis that Triage Agent uses for routing decisions:
- Commercial intent indicators feed into bias detection triggers
- Toxicity scores help identify content needing deeper analysis
- Sentiment intensity affects routing confidence

### **Summary Agent Input**
Classification results contribute to final summary generation:
- Content type distribution across all comments
- Sentiment patterns and toxicity trends
- Risk factor aggregation and flagging statistics
- Quality indicators for overall engagement assessment

## 🔄 Continuous Improvement

### **Accuracy Monitoring**
- Track classification consistency across similar content
- Monitor false positive/negative rates for toxicity detection
- Validate sentiment analysis against human judgment
- Assess PII detection completeness and accuracy

### **Prompt Refinement**
- Update classification criteria based on new content types
- Refine toxicity thresholds based on moderation outcomes
- Improve sentiment analysis for domain-specific language
- Enhance factual vs opinionated distinction clarity