# Multi-Agent Social Media Analysis - Prompt Engineering Documentation

## 🎯 System Overview

This documentation provides comprehensive prompt engineering guidelines for the **triage-based multi-agent social media analysis system**. Each agent has specialized prompts designed for optimal performance and clear reasoning.

## 📁 Documentation Structure

### 🔀 [Triage Agent Prompts](./triage_agent_prompts.md)
**Purpose**: Intelligent comment routing based on bias signals
- **Route to Bias Agent**: Suspicious promotional content, attacks, anomalies
- **Route to Summarizer**: Neutral, authentic engagement
- **Key Features**: Fast pre-filtering, batch processing, confidence scoring
- **Use Cases**: Commercial intent detection, astroturfing identification, engagement anomaly detection

### 🔍 [Bias Detection Agent Prompts](./bias_detection_prompts.md)
**Purpose**: Deep profile analysis for flagged comments
- **Commercial Bias**: Undisclosed sponsorships, affiliate marketing
- **Astroturfing**: Fake grassroots behavior, sock puppet accounts
- **Coordinated Attacks**: Organized harassment campaigns
- **Key Features**: Bio analysis, engagement pattern detection, credibility scoring

### 📊 [Summary Agent Prompts](./summary_agent_prompts.md)
**Purpose**: Comprehensive insights from dual input sources
- **Clean Comments**: Direct from triage (authentic engagement)
- **Flagged Comments**: With bias analysis results
- **Key Features**: Authenticity scoring, manipulation impact assessment, sponsor recommendations

### 🏷️ [Main Classifier Agent Prompts](./main_classifier_prompts.md)
**Purpose**: Foundational content analysis for all comments
- **Classification**: Factual, opinionated, promotional, informational
- **Sentiment**: Positive, negative, neutral with intensity
- **Toxicity**: 0.0-1.0 scoring with risk factors
- **Key Features**: PII detection, moderation recommendations, quality assurance

## 🔄 Agent Interaction Flow

```
Comments → Main Classifier → Triage Agent → {
    ├── Clean Comments → Summary Agent
    ├── Flagged Comments → Bias Detection → Summary Agent
}
```

### **Data Flow Details:**
1. **Main Classifier** analyzes all comments for basic classification, sentiment, toxicity
2. **Triage Agent** uses classification results to route comments intelligently
3. **Bias Detection** performs deep analysis on flagged comments only
4. **Summary Agent** combines authentic engagement data with bias analysis results

## 🎨 Prompt Engineering Best Practices

### **Consistency Across Agents**
- **JSON Output Format**: All agents return structured JSON for reliable parsing
- **Confidence Scores**: 0.0-1.0 scale for uncertainty quantification
- **Evidence-Based Reasoning**: Specific examples and explanations required
- **Fallback Logic**: Rule-based alternatives when AI fails

### **Quality Assurance**
- **Calibration Standards**: Consistent scoring thresholds across agents
- **Edge Case Handling**: Sarcasm, cultural differences, domain-specific language
- **Validation Checks**: Ensure outputs align with input evidence
- **Performance Monitoring**: Track accuracy and false positive/negative rates

### **Optimization Strategies**
- **Batch Processing**: Analyze multiple comments simultaneously for efficiency
- **Pre-filtering**: Fast keyword-based routing before expensive AI analysis
- **Confidence Thresholds**: Skip uncertain cases or flag for manual review
- **Contextual Adaptation**: Adjust prompts based on content domain and audience

## 🚀 Implementation Guidelines

### **Getting Started**
1. Review agent-specific documentation for detailed prompt examples
2. Understand the triage-based routing logic and decision criteria
3. Configure confidence thresholds based on your accuracy requirements
4. Set up fallback logic for API failures or uncertain classifications

### **Customization Options**
- **Domain Adaptation**: Modify keyword lists for specific industries (beauty, tech, finance)
- **Severity Tuning**: Adjust toxicity and bias scoring thresholds
- **Cultural Localization**: Adapt language patterns for different regions
- **Platform Specificity**: Customize for different social media platforms

### **Performance Tuning**
- **Latency Optimization**: Balance analysis depth with response speed
- **Accuracy Calibration**: Fine-tune scoring based on validation data
- **Resource Management**: Optimize API usage through intelligent batching
- **Scalability Planning**: Design for handling increasing comment volumes

## 📈 Monitoring and Improvement

### **Key Metrics**
- **Routing Accuracy**: Percentage of correctly triaged comments
- **Bias Detection Precision**: True positive rate for manipulation detection
- **Summary Quality**: Relevance and actionability of generated insights
- **Processing Efficiency**: Comments analyzed per minute/hour

### **Continuous Learning**
- **Prompt Iteration**: Regular updates based on performance data
- **Keyword Evolution**: Update detection patterns for new manipulation tactics
- **Threshold Adjustment**: Refine scoring based on real-world outcomes
- **Domain Expansion**: Add support for new content types and platforms

## 🔗 Quick Links

- **Agent Files**: [main_classifier_agent.py](../main_classifier_agent.py), [bias_detection_agent.py](../bias_detection_agent.py), [summary_agent.py](../summary_agent.py)
- **Data Structures**: [data_structures.py](../data_structures.py)
- **Orchestration**: [orchestrator.py](../orchestrator.py)
- **Example Usage**: [main.py](../main.py)

## 📞 Support

For questions about prompt engineering or agent behavior:
1. Check the relevant agent-specific documentation
2. Review example outputs in the codebase
3. Test with provided dummy data scenarios
4. Monitor agent logs for debugging information

---

*This documentation is designed to support hackathon development and production deployment of the multi-agent social media analysis system.*