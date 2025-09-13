# Bias Detection Agent Prompt Engineering Guide

## 🎯 Purpose
The Bias Detection Agent performs **deep profile analysis** on comments flagged by the Triage Agent to identify commercial bias, astroturfing, coordinated attacks, and inauthentic behavior.

## 🔍 Analysis Scope

### **Profile Bio Investigation**
- Brand partnerships and affiliations
- Undisclosed commercial relationships
- Professional vs personal account indicators
- Account purpose and authenticity signals

### **Bias Pattern Detection**
- **Commercial Bias**: Undisclosed sponsorships, affiliate marketing
- **Competitor Astroturfing**: Negative reviews promoting alternatives
- **Coordinated Attacks**: Organized harassment campaigns
- **Sock Puppet Accounts**: Fake personas for manipulation

## 🤖 Core Bias Analysis Prompt

```
You are a digital forensics expert specializing in social media bias detection. Analyze this flagged comment and author profile for signs of commercial bias, astroturfing, or coordinated inauthentic behavior.

COMMENT ANALYSIS:
- Text: {comment_text}
- Classification: {existing_classification}
- Sentiment: {sentiment}
- Toxicity: {toxicity_score}

AUTHOR PROFILE:
- Username: {author_username}
- Bio: {author_bio}
- Followers: {author_followers}
- Verified: {verified_status}
- Engagement: {likes} likes, {replies} replies, {retweets} shares

BIAS ANALYSIS FRAMEWORK:

1. COMMERCIAL BIAS INDICATORS:
   - Bio mentions brand partnerships/ambassador roles
   - Comment contains promotional language without #ad disclosure
   - Excessive enthusiasm for products ("life-changing", "amazing")
   - Discount codes or affiliate links
   - Bio lists multiple brand relationships

2. ASTROTURFING PATTERNS:
   - New account with strong product opinions
   - Generic username (firstname_lastname_year)
   - Bio mentions "exposing truth" or "honest reviews"
   - Promotes competitor products in negative reviews
   - Unusually high engagement for follower count

3. COORDINATED ATTACK SIGNALS:
   - Similar language patterns to other negative comments
   - Account created recently but posting aggressive content
   - Bio designed to establish "credibility" for attacks
   - Disproportionate negative emotion
   - Focus on character assassination vs product critique

4. AUTHENTICITY SIGNALS (POSITIVE):
   - Bio reflects genuine personal interests
   - Account age consistent with follower growth
   - Balanced comment history (mix of topics)
   - Normal engagement ratios
   - Specific, detailed feedback vs generic statements

RETURN DETAILED JSON:
{
  "bias_score": 0.0-1.0,
  "bias_type": "commercial" | "astroturfing" | "coordinated_attack" | "authentic",
  "confidence": 0.0-1.0,
  "risk_level": "low" | "medium" | "high",
  "bias_signals": {
    "commercial_indicators": {
      "score": 0.0-1.0,
      "evidence": ["list", "of", "specific", "findings"],
      "brand_affiliations": ["detected", "brands"]
    },
    "astroturfing_indicators": {
      "score": 0.0-1.0,
      "evidence": ["suspicious", "patterns", "found"],
      "account_age_suspicion": 0.0-1.0
    },
    "attack_coordination": {
      "score": 0.0-1.0,
      "evidence": ["coordination", "signals"],
      "language_patterns": ["detected", "patterns"]
    },
    "authenticity_signals": {
      "score": 0.0-1.0,
      "positive_indicators": ["genuine", "signals"],
      "credibility_factors": ["trust", "building", "elements"]
    }
  },
  "profile_analysis": {
    "bio_assessment": "Detailed analysis of bio content and red flags",
    "engagement_analysis": "Assessment of follower/engagement ratios",
    "account_credibility": 0.0-1.0,
    "professional_indicators": ["job", "title", "expertise", "areas"]
  },
  "recommendations": {
    "action": "monitor" | "flag" | "investigate" | "approve",
    "reasoning": "Specific explanation for recommendation",
    "follow_up": ["suggested", "additional", "checks"]
  },
  "detailed_explanation": "Comprehensive analysis explaining the bias determination with specific evidence and reasoning"
}
```

## 🎨 Specialized Prompts by Bias Type

### **Commercial Bias Detection**
```
Focus on undisclosed commercial relationships:

COMMERCIAL RED FLAGS:
- Bio lists multiple brand partnerships without disclosure in comment
- Promotional language intensity ("OBSESSED", "GAME-CHANGER") 
- Discount codes mentioned without #ad or #sponsored tags
- Bio mentions "PR friendly" or "partnerships welcome"
- Excessive product enthusiasm inconsistent with normal language patterns

SCORING CRITERIA:
- 0.8-1.0: Clear undisclosed sponsorship, multiple brand affiliations
- 0.6-0.7: Likely commercial intent, some disclosure missing
- 0.4-0.5: Possible affiliate relationship, unclear disclosure
- 0.2-0.3: Minimal commercial indicators
- 0.0-0.1: No commercial bias detected

Look for patterns like:
- "Brand ambassador for @Company1 @Company2 @Company3" in bio
- Comment: "This is AMAZING! Use code SAVE20!" without #ad
- Bio professional focus vs comment enthusiasm mismatch
```

### **Astroturfing Detection**
```
Focus on fake grassroots behavior:

ASTROTURFING RED FLAGS:
- Account created recently (2024) but posting with authority
- Generic biographical information or corporate-style language
- Username patterns: firstname_lastname_numbers
- Bio mentions "truth-telling" or "exposing fake reviews"
- Negative review paired with competitor recommendations
- Engagement anomalies (high likes, low followers)

ANALYSIS QUESTIONS:
1. Does account age match the confidence level of opinions?
2. Is the bio designed to establish false credibility?
3. Are engagement metrics suspicious for account age?
4. Does comment promote alternatives while attacking current product?
5. Is language too polished for claimed user type?

DETECTION PATTERNS:
- "Product reviewer since 2024" + strong negative opinions
- "Helping people make smart purchases" + competitor promotion
- Bio establishing expertise + account created last month
```

### **Coordinated Attack Detection**
```
Focus on organized harassment patterns:

COORDINATION INDICATORS:
- Similar aggressive language patterns across multiple accounts
- Accounts created in clusters (same time period)
- Bios designed to appear authoritative for specific attacks
- Disproportionate emotional response to product/creator
- Language escalation beyond normal consumer complaints

PATTERN ANALYSIS:
- Compare language patterns to known coordinated campaigns
- Check for identical phrases or unusual word choices
- Assess if criticism focuses on character vs product
- Evaluate if response intensity matches claimed experience
- Look for synchronized timing of negative comments

RED FLAG COMBINATIONS:
- New account + extreme language + character attacks
- Multiple accounts with similar bio patterns
- Coordinated use of specific accusatory terms
- Focus on creator credibility rather than product issues
```

## 📊 Scoring Methodology

### **Overall Bias Score Calculation**
```
bias_score = weighted_average([
    commercial_indicators * 0.3,
    astroturfing_indicators * 0.3,
    attack_coordination * 0.2,
    (1 - authenticity_signals) * 0.2
])

risk_level = {
    0.0-0.3: "low",
    0.3-0.7: "medium", 
    0.7-1.0: "high"
}
```

### **Account Credibility Factors**
```
credibility_score = calculate_credibility([
    follower_count_appropriateness,
    bio_authenticity,
    engagement_ratio_normalcy,
    account_age_consistency,
    verification_status,
    content_history_depth
])
```

## 🔧 Fallback Analysis

If Gemini API fails, use rule-based detection:

```python
def fallback_bias_detection(comment, author_bio):
    commercial_keywords = ["ambassador", "partner", "affiliate", "PR", "brand", "code", "discount"]
    astroturf_keywords = ["truth", "exposing", "honest", "real", "fake"]
    attack_keywords = ["fraud", "scam", "liar", "terrible", "worst"]
    
    bio_commercial = count_keywords(author_bio, commercial_keywords)
    text_promotional = count_keywords(comment.text, ["amazing", "life-changing", "must-have"])
    
    # Simple scoring
    commercial_score = (bio_commercial + text_promotional) / 10
    
    engagement_ratio = comment.metrics["likes"] / max(comment.author_followers, 1)
    anomaly_score = min(1.0, engagement_ratio * 5)
    
    overall_bias = max(commercial_score, anomaly_score)
    
    return {
        "bias_score": min(1.0, overall_bias),
        "bias_type": "commercial" if commercial_score > anomaly_score else "astroturfing",
        "confidence": 0.6,  # Lower confidence for fallback
        "detailed_explanation": f"Fallback analysis detected {overall_bias:.2f} bias score"
    }
```

## 🎯 Quality Assurance

### **Validation Checks**
- Ensure bias score aligns with evidence provided
- Verify recommendations match risk level
- Check that explanations reference specific bio/comment content
- Confirm authenticity signals are properly weighted

### **Common False Positives to Avoid**
- Verified accounts with legitimate brand partnerships
- Authentic negative experiences that happen to be strongly worded
- Normal users who happen to follow brands they like
- Professional reviewers with transparent disclosure practices

### **Calibration Guidelines**
- Reserve 0.8+ scores for clear undisclosed commercial relationships
- Use 0.6-0.7 range for suspicious but uncertain cases
- Weight authenticity signals heavily for established accounts
- Consider context: beauty influencer having beauty brand partnerships is normal

## 📈 Performance Monitoring

### **Accuracy Metrics**
- Manual validation of high-risk flagged accounts
- False positive rate tracking
- Community feedback on flagged vs approved comments
- Brand partnership disclosure compliance improvements

### **Continuous Learning**
- Update keyword lists based on emerging astroturfing tactics
- Refine scoring thresholds based on validation results
- Add new bias categories as manipulation techniques evolve
- Improve prompt specificity based on edge cases discovered