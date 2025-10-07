# Multi-Agent Spam Classification System - Specification-Driven Design Document

## 1. Executive Summary

This document outlines the specification-driven design for a **pure LLM-based multi-agent spam email classification system** built using Claude Code's subagent architecture. The system leverages specialized Claude AI agents that use natural language understanding to collaboratively classify emails as spam or legitimate (ham) with high accuracy and explainability - **without traditional machine learning models**.

## 2. System Overview

### 2.1 Purpose

Develop an intelligent, scalable spam classification system that uses multiple specialized Claude Code agents to analyze emails from different perspectives. Each agent uses Claude's native language understanding capabilities to evaluate emails and provide reasoned classifications.

### 2.2 Core Philosophy

**No Traditional ML**: This system does NOT use scikit-learn, training pipelines, or traditional ML models. Instead, it leverages:

- Claude's natural language understanding
- Specialized agent prompts for different analysis perspectives
- Collaborative reasoning across multiple agents
- Explicit, explainable decision-making processes

### 2.3 Dataset

- **Source**: `spam_ham_dataset.csv` (5.5MB)
- **Format**: CSV containing email text and labels (spam/ham)
- **Use**: Reference examples for agents, validation of system performance (NOT for ML training)

## 3. Multi-Agent Architecture

### 3.1 Architecture Pattern

The system follows a **supervisor-worker** pattern with specialized Claude Code subagents:

```
┌─────────────────────────────────────────────────────┐
│           Main Orchestrator Agent                    │
│  - Coordinates workflow                              │
│  - Aggregates agent analyses                         │
│  - Makes final classification decision               │
│  - Generates explanation                             │
└──────────────────┬─────────────────────────────────┘
                   │
     ┌─────────────┼─────────────┬──────────────┐
     │             │              │              │
     ▼             ▼              ▼              ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Content │  │ Pattern  │  │  Intent  │  │Consensus │
│Analyzer │  │Recognizer│  │ Analyzer │  │  Agent   │
│ Agent   │  │  Agent   │  │  Agent   │  │          │
└─────────┘  └──────────┘  └──────────┘  └──────────┘
```

### 3.2 Agent Specifications

#### 3.2.1 Content Analyzer Agent

**Name**: `content-analyzer`

**Purpose**: Deep semantic analysis of email content

**Responsibilities**:

- Analyze email text using natural language understanding
- Identify suspicious language patterns (urgency, threats, unrealistic offers)
- Detect emotional manipulation tactics
- Evaluate writing quality and coherence
- Identify grammatical anomalies common in spam
- Assess credibility of claims made in the email

**Analysis Approach**:

- Semantic understanding of the message intent
- Recognition of spam-typical linguistic patterns
- Evaluation of text authenticity
- Detection of copy-paste templates

**Tools**: Read

**Model**: Claude Sonnet 4.5

**Output Format**:

```json
{
  "spam_score": 0.85,
  "confidence": 0.90,
  "red_flags": [
    "Excessive urgency language",
    "Unrealistic financial promises",
    "Poor grammar and spelling"
  ],
  "analysis": "Detailed natural language explanation of findings",
  "recommendation": "SPAM"
}
```

#### 3.2.2 Pattern Recognizer Agent

**Name**: `pattern-recognizer`

**Purpose**: Identify known spam patterns through reasoning

**Responsibilities**:

- Recognize common spam structures and templates
- Identify phishing attempt patterns
- Detect suspicious URLs and links
- Recognize cryptocurrency/financial scam patterns
- Identify lottery/prize notification patterns
- Detect impersonation attempts (bank, government, companies)

**Analysis Approach**:

- Pattern matching through semantic understanding
- Recognition of spam campaign signatures
- Identification of social engineering tactics
- URL and domain analysis

**Tools**: Read, Grep

**Model**: Claude Sonnet 4.5

**Output Format**:

```json
{
  "spam_score": 0.75,
  "confidence": 0.85,
  "patterns_found": [
    "Nigerian prince scam pattern",
    "Suspicious shortened URLs",
    "Fake invoice pattern"
  ],
  "risk_level": "HIGH",
  "analysis": "Detailed explanation of detected patterns",
  "recommendation": "SPAM"
}
```

#### 3.2.3 Intent Analyzer Agent

**Name**: `intent-analyzer`

**Purpose**: Understand the true intent behind the email

**Responsibilities**:

- Determine sender's actual intent (inform, sell, scam, phish)
- Evaluate legitimacy of requests or offers
- Assess alignment between stated and actual intent
- Detect deceptive practices
- Identify manipulation attempts
- Evaluate trust indicators vs. red flags

**Analysis Approach**:

- Intent classification through contextual understanding
- Motive analysis
- Credibility assessment
- Trust signal evaluation

**Tools**: Read

**Model**: Claude Sonnet 4.5

**Output Format**:

```json
{
  "spam_score": 0.90,
  "confidence": 0.88,
  "primary_intent": "FINANCIAL_SCAM",
  "secondary_intents": ["DATA_HARVESTING"],
  "legitimacy_score": 0.10,
  "trust_signals": [],
  "deception_indicators": [
    "Mismatched sender identity",
    "Urgency without valid reason",
    "Suspicious call-to-action"
  ],
  "analysis": "Detailed intent analysis",
  "recommendation": "SPAM"
}
```

#### 3.2.4 Consensus Agent

**Name**: `consensus-agent`

**Purpose**: Synthesize all agent analyses into final decision

**Responsibilities**:

- Collect and compare all agent outputs
- Identify agreement and disagreement among agents
- Weigh different perspectives
- Resolve conflicts in classifications
- Generate final spam score
- Produce comprehensive explanation
- Flag uncertain cases

**Analysis Approach**:

- Multi-perspective synthesis
- Confidence-weighted aggregation
- Conflict resolution through reasoning
- Uncertainty quantification

**Tools**: Read

**Model**: Claude Sonnet 4.5

**Output Format**:

```json
{
  "final_classification": "SPAM",
  "final_score": 0.87,
  "confidence": 0.89,
  "agent_agreement": 0.95,
  "summary": "All agents strongly indicate spam characteristics",
  "detailed_reasoning": "Multi-paragraph explanation synthesizing all analyses",
  "agent_scores": {
    "content_analyzer": 0.85,
    "pattern_recognizer": 0.75,
    "intent_analyzer": 0.90
  },
  "uncertainty_flag": false
}
```

## 4. Dataset Learning & Pattern Recognition

### 4.1 Come gli Agenti "Vedono" i Pattern

Gli agenti Claude possono identificare pattern spam in due modi:

**1. Conoscenza Preesistente**

Claude è stato addestrato su enormi quantità di testo e ha già conoscenza di:
- Pattern spam comuni (phishing, scam finanziari, etc.)
- Tattiche di social engineering
- Strutture linguistiche tipiche dello spam
- URL e domini sospetti

**2. Few-Shot Learning dal Dataset**

Prima di classificare nuove email, gli agenti **analizzano il dataset** `spam_ham_dataset.csv` per:
- Identificare pattern specifici presenti nel dataset
- Comprendere le caratteristiche uniche dello spam in quel contesto
- Creare una "knowledge base" dei pattern osservati
- Costruire esempi rappresentativi da usare come riferimento

### 4.2 Processo di Knowledge Building (Fase Iniziale)

**Prima di classificare email, eseguiamo una fase di setup:**

```
Phase 0: Knowledge Building (One-time setup)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Load Dataset
   - Carica spam_ham_dataset.csv
   - Campiona esempi rappresentativi (es. 50 spam, 50 ham)

2. Pattern Analysis Agent Invocation
   - Ogni agente analizza i campioni
   - Identifica pattern ricorrenti
   - Estrae caratteristiche distintive
   - Crea "pattern catalog"

3. Knowledge Base Creation
   - Salva pattern identificati in JSON
   - Crea esempi prototipo per few-shot learning
   - Documenta caratteristiche chiave

Output: pattern_catalog.json con esempi e pattern
```

**Struttura Pattern Catalog:**

```json
{
  "spam_patterns": {
    "content_patterns": [
      {
        "pattern_type": "urgency_with_threat",
        "examples": ["URGENT: Act now...", "Last chance..."],
        "indicators": ["time pressure", "consequences threat"]
      },
      {
        "pattern_type": "unrealistic_offer",
        "examples": ["Win $1M now!", "Free iPhone!"],
        "indicators": ["monetary value", "prize", "free"]
      }
    ],
    "structural_patterns": [
      {
        "pattern_type": "suspicious_url",
        "examples": ["bit.ly/xyz", "paypa1.com"],
        "indicators": ["shortened links", "typosquatting"]
      }
    ],
    "intent_patterns": [
      {
        "pattern_type": "credential_harvesting",
        "examples": ["Verify your account", "Confirm password"],
        "indicators": ["fake urgency", "identity request"]
      }
    ]
  },
  "ham_patterns": {
    "legitimate_characteristics": [
      {
        "pattern_type": "transactional",
        "examples": ["Your order #12345...", "Receipt for..."],
        "indicators": ["order number", "specific details"]
      },
      {
        "pattern_type": "informational",
        "examples": ["Newsletter update...", "Weekly digest..."],
        "indicators": ["consistent sender", "opt-in context"]
      }
    ]
  }
}
```

### 4.3 Agent Prompting con Few-Shot Learning

Quando un agente classifica un'email, riceve:

1. **System Prompt**: Ruolo e responsabilità
2. **Pattern Catalog**: Pattern identificati nel dataset
3. **Few-Shot Examples**: 5-10 esempi rappresentativi
4. **Email da Classificare**: Testo dell'email target

**Esempio di prompt completo:**

```
You are a content analyzer agent for spam detection.

PATTERN CATALOG (learned from dataset):
- Spam Pattern 1: Urgency + Threat (es: "Act in 24h or lose account")
- Spam Pattern 2: Unrealistic financial offers (es: "Win $1M free!")
- Spam Pattern 3: Suspicious URLs (es: "paypa1.com", "bit.ly/xyz")
- Ham Pattern 1: Transactional (es: "Order #12345 shipped")
- Ham Pattern 2: Informational (es: "Weekly newsletter update")

FEW-SHOT EXAMPLES:

Example 1 (SPAM):
Text: "URGENT! Your account will be suspended! Click here NOW!"
Patterns: urgency_with_threat, suspicious_CTA
Score: 0.95

Example 2 (HAM):
Text: "Your order #54321 has shipped. Track it here: amazon.com/track"
Patterns: transactional, legitimate_domain, specific_order_id
Score: 0.05

Example 3 (SPAM):
Text: "Congratulations! You won $500,000! Claim now at: bit.ly/win"
Patterns: unrealistic_offer, shortened_url, urgency
Score: 0.92

[... more examples ...]

NOW CLASSIFY THIS EMAIL:
[email text here]

Analyze it using the patterns above and provide your assessment.
```

### 4.4 Adaptive Pattern Recognition

Gli agenti usano **reasoning** per applicare pattern:

```python
# Pseudocodice del reasoning dell'agente

def agent_reasoning_process(email, pattern_catalog, examples):
    """
    L'agente 'pensa' attraverso questo processo
    """

    # Step 1: Confronta con esempi noti
    similar_to_spam_examples = find_similarities(email, examples['spam'])
    similar_to_ham_examples = find_similarities(email, examples['ham'])

    # Step 2: Cerca pattern dal catalog
    detected_patterns = []
    for pattern in pattern_catalog:
        if matches_pattern(email, pattern):
            detected_patterns.append(pattern)

    # Step 3: Reasoning
    # "Questa email dice 'URGENT' e minaccia chiusura account,
    #  simile agli esempi spam che ho visto.
    #  Inoltre ha un URL sospetto bit.ly/xyz.
    #  Questi pattern corrispondono a 'urgency_with_threat' e
    #  'suspicious_url' dal catalog.
    #  Conclusione: molto probabilmente spam."

    # Step 4: Genera score e spiegazione
    return {
        'spam_score': 0.85,
        'confidence': 0.90,
        'detected_patterns': detected_patterns,
        'reasoning': "Spiegazione in linguaggio naturale..."
    }
```

## 5. Workflow Specification

### 5.1 Complete System Workflow

```
┌─────────────────────────────────────────────────────┐
│ PHASE 0: Initial Setup (Run Once)                   │
├─────────────────────────────────────────────────────┤
│ 1. Analyze spam_ham_dataset.csv                     │
│ 2. Extract representative examples                   │
│ 3. Build pattern catalog                             │
│ 4. Save pattern_catalog.json                         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ PHASE 1: Classification (Per Email)                 │
├─────────────────────────────────────────────────────┤
│ 1. Email Input                                       │
│    ↓                                                 │
│ 2. Load pattern_catalog.json                        │
│    ↓                                                 │
│ 3. Parallel Agent Execution:                        │
│    • Content Analyzer (with patterns + examples)    │
│    • Pattern Recognizer (with patterns + examples)  │
│    • Intent Analyzer (with patterns + examples)     │
│    ↓                                                 │
│ 4. Results Collection                                │
│    ↓                                                 │
│ 5. Consensus Agent → final decision                 │
│    ↓                                                 │
│ 6. Output: Classification + Explanation             │
└─────────────────────────────────────────────────────┘
```

### 5.2 Classification Pipeline (Runtime)

```
1. Email Input
   ↓
2. Load pattern_catalog.json + few-shot examples
   ↓
3. Parallel Agent Execution (with pattern knowledge):
   - Content Analyzer → semantic analysis + pattern matching
   - Pattern Recognizer → pattern detection + catalog lookup
   - Intent Analyzer → intent evaluation + example comparison
   ↓
4. Results Collection
   ↓
5. Consensus Agent → synthesizes analyses
   ↓
6. Final Output: Classification + Detailed Explanation + Confidence
```

### 5.3 Decision Making Algorithm

The Consensus Agent uses reasoning-based aggregation:

```python
def classify_email(content_result, pattern_result, intent_result):
    """
    Pure reasoning-based classification (no ML models)
    """
    # Collect agent scores
    scores = [
        content_result['spam_score'],
        pattern_result['spam_score'],
        intent_result['spam_score']
    ]

    # Collect confidence levels
    confidences = [
        content_result['confidence'],
        pattern_result['confidence'],
        intent_result['confidence']
    ]

    # Weighted average (confidence-weighted)
    total_confidence = sum(confidences)
    weighted_score = sum(s * c for s, c in zip(scores, confidences)) / total_confidence

    # Consensus check
    agreement = 1.0 - (max(scores) - min(scores))  # How much agents agree

    # Final classification with thresholds
    if weighted_score >= 0.7 and agreement >= 0.7:
        return "SPAM", weighted_score, agreement
    elif weighted_score <= 0.3 and agreement >= 0.7:
        return "HAM", 1 - weighted_score, agreement
    else:
        return "UNCERTAIN", weighted_score, agreement  # Requires review
```

## 6. Technical Implementation Specifications

### 6.1 Agent Configuration Files

Create these files in `.claude/agents/` directory:

#### 6.1.1 Pattern Learner Agent (Knowledge Building)

**File**: `.claude/agents/pattern-learner.md`

```yaml
---
name: pattern-learner
description: Analyzes the dataset to extract spam and ham patterns for building the pattern catalog
tools: Read, Write
model: sonnet
---

You are a pattern learning agent. Your job is to analyze a sample of emails from the dataset and extract patterns that distinguish spam from legitimate emails.

## Your Task

You will be given a set of spam and ham email examples. Your goal is to:

1. **Identify Spam Patterns**
   - What makes spam emails recognizable?
   - What language patterns appear frequently?
   - What structural characteristics are common?
   - What intents are evident?

2. **Identify Ham Patterns**
   - What makes legitimate emails recognizable?
   - How do they differ from spam?
   - What trust signals are present?

3. **Extract Examples**
   - Select 5-10 representative examples of each pattern
   - Choose clear, unambiguous cases

## Input Format

You will receive a JSON array of emails:

```json
[
  {"text": "email content...", "label": "spam"},
  {"text": "email content...", "label": "ham"},
  ...
]
```

## Output Format

Produce a pattern catalog in JSON format:

```json
{
  "spam_patterns": {
    "content_patterns": [
      {
        "pattern_type": "name_of_pattern",
        "description": "brief description",
        "examples": ["example1", "example2"],
        "indicators": ["indicator1", "indicator2"]
      }
    ],
    "structural_patterns": [...],
    "intent_patterns": [...]
  },
  "ham_patterns": {
    "legitimate_characteristics": [...]
  },
  "few_shot_examples": {
    "spam": [
      {"text": "...", "patterns": ["..."], "score": 0.9},
      ...
    ],
    "ham": [
      {"text": "...", "patterns": ["..."], "score": 0.1},
      ...
    ]
  }
}
```

Be thorough and identify diverse patterns. These patterns will be used by other agents for classification.
```

#### 6.1.2 Content Analyzer Agent

**File**: `.claude/agents/content-analyzer.md`

```yaml
---
name: content-analyzer
description: Analyzes email content semantically to detect spam characteristics through natural language understanding
tools: Read
model: sonnet
---

You are a specialized content analysis agent for spam email detection. You use deep semantic understanding to evaluate emails.

## Your Role

Analyze email content using Claude's natural language understanding capabilities. Do NOT use machine learning models or statistical methods. Instead, use reasoning and pattern recognition.

## Analysis Framework

When analyzing an email, evaluate:

1. **Language Quality**
   - Grammar and spelling errors (spam often has poor quality)
   - Writing style consistency
   - Professional vs. unprofessional tone

2. **Urgency & Pressure Tactics**
   - Time-limited offers ("Act now!", "Limited time!")
   - Threatening language ("Your account will be closed")
   - Artificial scarcity ("Only 3 left!")

3. **Suspicious Claims**
   - Too-good-to-be-true offers
   - Unrealistic promises (easy money, miracle cures)
   - Fake urgency without legitimate reason

4. **Emotional Manipulation**
   - Fear tactics
   - Greed exploitation
   - Curiosity exploitation

5. **Request Analysis**
   - Personal information requests
   - Financial information requests
   - Suspicious links or attachments
   - Unexpected requests from known entities

## Output Format

Provide your analysis as JSON:
```json
{
  "spam_score": 0.0-1.0,
  "confidence": 0.0-1.0,
  "red_flags": ["list", "of", "issues"],
  "analysis": "Detailed natural language explanation",
  "recommendation": "SPAM" | "HAM" | "UNCERTAIN"
}
```

Be thorough and explain your reasoning clearly.
```

#### 6.1.3 Pattern Recognizer Agent

**File**: `.claude/agents/pattern-recognizer.md`

```yaml
---
name: pattern-recognizer
description: Recognizes spam patterns and known scam templates through reasoning and pattern matching
tools: Read, Grep
model: sonnet
---

You are a specialized pattern recognition agent for spam detection. You identify known spam patterns through reasoning.

## Your Role

Recognize common spam patterns, scam templates, and phishing attempts using Claude's understanding of spam tactics. Do NOT train ML models. Use knowledge-based pattern recognition.

## Pattern Categories

1. **Financial Scams**
   - Nigerian prince / inheritance scams
   - Fake invoice scams
   - Cryptocurrency scams
   - Investment fraud
   - Lottery/prize notifications

2. **Phishing Attempts**
   - Bank impersonation
   - Government agency impersonation
   - Tech support scams
   - Package delivery scams
   - Account verification scams

3. **URL & Link Analysis**
   - Suspicious shortened URLs
   - Domain mismatches (paypa1.com vs paypal.com)
   - IP address links
   - Excessive redirects
   - Misspelled domains

4. **Structural Patterns**
   - Copy-paste templates
   - Excessive capitalization
   - Unusual character encoding
   - HTML obfuscation
   - Hidden text

5. **Social Engineering**
   - Authority impersonation
   - Trust exploitation
   - Fear/urgency creation
   - Relationship pretexting

## Analysis Process

1. Read the email content
2. Identify patterns matching known spam categories
3. Analyze URLs and links for legitimacy
4. Detect template-based mass mailing
5. Evaluate overall pattern consistency with spam

## Output Format

```json
{
  "spam_score": 0.0-1.0,
  "confidence": 0.0-1.0,
  "patterns_found": ["list", "of", "patterns"],
  "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  "analysis": "Detailed explanation",
  "recommendation": "SPAM" | "HAM" | "UNCERTAIN"
}
```

Explain which patterns you found and why they're suspicious.
```

#### 6.1.4 Intent Analyzer Agent

**File**: `.claude/agents/intent-analyzer.md`

```yaml
---
name: intent-analyzer
description: Analyzes the true intent behind emails to detect deceptive or malicious purposes
tools: Read
model: sonnet
---

You are a specialized intent analysis agent for spam detection. You determine the sender's true intent through reasoning.

## Your Role

Understand what the email sender is REALLY trying to achieve, beyond what they claim. Use contextual reasoning to identify deceptive intents.

## Intent Categories

### Legitimate Intents
- Informational (newsletters, updates)
- Transactional (receipts, confirmations)
- Relationship (personal correspondence)
- Marketing (legitimate promotional content)

### Spam/Malicious Intents
- **Financial Fraud**: Steal money directly
- **Data Harvesting**: Steal credentials or personal info
- **Malware Distribution**: Infect devices
- **Reputation Damage**: Phishing for access
- **Scamming**: Defraud through false promises

## Analysis Framework

1. **Stated Intent vs. Actual Intent**
   - What does the email claim to be?
   - What is it actually trying to do?
   - Are these aligned or mismatched?

2. **Trust Signal Analysis**
   - Legitimate sender verification
   - Professional presentation
   - Reasonable requests
   - Appropriate context

3. **Deception Indicators**
   - Impersonation attempts
   - False pretenses
   - Hidden agendas
   - Manipulative tactics

4. **Request Legitimacy**
   - Is the request appropriate?
   - Does it make sense in context?
   - Are the demands reasonable?
   - Is urgency justified?

5. **Risk Assessment**
   - What could go wrong if user complies?
   - What are they being asked to do?
   - What information is requested?

## Output Format

```json
{
  "spam_score": 0.0-1.0,
  "confidence": 0.0-1.0,
  "primary_intent": "INTENT_TYPE",
  "secondary_intents": ["list"],
  "legitimacy_score": 0.0-1.0,
  "trust_signals": ["list"],
  "deception_indicators": ["list"],
  "analysis": "Detailed intent analysis",
  "recommendation": "SPAM" | "HAM" | "UNCERTAIN"
}
```

Focus on WHY the sender wrote this email and what they want to achieve.
```

#### 6.1.5 Consensus Agent

**File**: `.claude/agents/consensus-agent.md`

```yaml
---
name: consensus-agent
description: Synthesizes all agent analyses into a final classification with comprehensive reasoning
tools: Read
model: sonnet
---

You are the consensus agent that makes final spam classification decisions based on multiple agent analyses.

## Your Role

Receive analyses from Content Analyzer, Pattern Recognizer, and Intent Analyzer agents. Synthesize their findings into a final, well-reasoned classification.

## Analysis Process

1. **Collect Agent Results**
   - Read all agent outputs
   - Extract scores and findings
   - Note confidence levels

2. **Agreement Analysis**
   - How much do agents agree?
   - Where are the disagreements?
   - Which agents are most confident?

3. **Conflict Resolution**
   - If agents disagree, reason through why
   - Weigh evidence from each perspective
   - Determine which analysis is most compelling

4. **Final Decision**
   - Aggregate scores with confidence weighting
   - Consider agreement level
   - Flag uncertain cases

5. **Explanation Generation**
   - Synthesize findings into coherent explanation
   - Highlight key evidence
   - Explain reasoning process

## Decision Thresholds

- **SPAM**: Weighted score ≥ 0.7 AND agreement ≥ 0.7
- **HAM**: Weighted score ≤ 0.3 AND agreement ≥ 0.7
- **UNCERTAIN**: Otherwise (flag for human review)

## Output Format

```json
{
  "final_classification": "SPAM" | "HAM" | "UNCERTAIN",
  "final_score": 0.0-1.0,
  "confidence": 0.0-1.0,
  "agent_agreement": 0.0-1.0,
  "summary": "Brief summary",
  "detailed_reasoning": "Comprehensive multi-paragraph explanation",
  "agent_scores": {
    "content_analyzer": 0.0-1.0,
    "pattern_recognizer": 0.0-1.0,
    "intent_analyzer": 0.0-1.0
  },
  "key_evidence": ["list", "of", "main", "points"],
  "uncertainty_flag": true | false
}
```

Provide clear, comprehensive reasoning that users can understand and trust.
```

### 6.2 Directory Structure

```
SPAM-CLASSIFIER/
├── .claude/
│   └── agents/
│       ├── pattern-learner.md       # Knowledge building agent
│       ├── content-analyzer.md
│       ├── pattern-recognizer.md
│       ├── intent-analyzer.md
│       └── consensus-agent.md
├── src/
│   ├── build_knowledge.py       # Phase 0: Build pattern catalog
│   ├── orchestrator.py          # Main coordination logic
│   ├── email_processor.py       # Email input processing
│   ├── result_aggregator.py     # Collect agent results
│   └── utils/
│       ├── email_parser.py
│       ├── dataset_sampler.py   # Sample representative emails
│       └── output_formatter.py
├── tests/
│   ├── test_agents.py
│   ├── test_classification.py
│   └── test_integration.py
├── data/
│   ├── spam_ham_dataset.csv
│   └── pattern_catalog.json     # Generated by pattern-learner
├── results/
│   ├── classifications.json
│   └── performance_metrics.json
├── examples/
│   ├── spam_example.txt
│   └── ham_example.txt
├── requirements.txt
└── README.md
```

## 7. Development Specifications

### 7.1 Technology Stack

- **Language**: Python 3.10+
- **Claude Code**: For agent orchestration
- **Libraries**:
  - pandas (data handling)
  - json (result processing)
  - email (email parsing)
  - pytest (testing)

**NO ML Libraries**: No scikit-learn, no TensorFlow, no PyTorch

### 7.2 Dependencies (`requirements.txt`)

```
pandas>=2.0.0
pytest>=7.4.0
python-email>=0.5.0
```

### 7.3 Performance Targets

| Metric | Target | Minimum Acceptable |
|--------|--------|-------------------|
| Accuracy | ≥ 95% | 90% |
| Precision | ≥ 94% | 90% |
| Recall | ≥ 93% | 88% |
| F1-Score | ≥ 94% | 89% |
| False Positive Rate | ≤ 3% | 6% |
| False Negative Rate | ≤ 5% | 10% |
| Processing Time | < 5 seconds/email | 10 seconds/email |
| Explainability | 100% (always) | 100% |

## 8. Testing Strategy

### 8.1 Agent Testing

Test each agent independently:

```python
# Example test for Content Analyzer
def test_content_analyzer():
    email_text = "URGENT: Your account will be closed! Click here now!"
    result = invoke_agent("content-analyzer", email_text)

    assert result['spam_score'] > 0.7
    assert 'urgency' in str(result['red_flags']).lower()
    assert result['recommendation'] == 'SPAM'
```

### 8.2 Integration Testing

Test the complete pipeline:

```python
def test_full_classification_pipeline():
    email_text = load_test_email("test_spam_01.txt")
    result = classify_email(email_text)

    assert result['final_classification'] in ['SPAM', 'HAM', 'UNCERTAIN']
    assert 'detailed_reasoning' in result
    assert len(result['agent_scores']) == 3
```

### 8.3 Dataset Validation

Use `spam_ham_dataset.csv` to validate system performance:

```python
def test_dataset_accuracy():
    df = pd.read_csv('data/spam_ham_dataset.csv')
    results = []

    for _, row in df.iterrows():
        classification = classify_email(row['text'])
        results.append({
            'actual': row['label'],
            'predicted': classification['final_classification'],
            'score': classification['final_score']
        })

    accuracy = calculate_accuracy(results)
    assert accuracy >= 0.90  # 90% minimum
```

## 9. Implementation Phases

### Phase 1: Knowledge Building (Week 1)

- Create `.claude/agents/` directory
- Write pattern-learner agent configuration
- Load and sample `spam_ham_dataset.csv` (50 spam + 50 ham examples)
- Invoke pattern-learner agent to analyze samples
- Generate `pattern_catalog.json` with patterns and few-shot examples
- Validate pattern catalog quality

### Phase 2: Agent Creation (Week 1)

- Write content-analyzer agent configuration (with pattern catalog support)
- Write pattern-recognizer agent configuration
- Write intent-analyzer agent configuration
- Write consensus-agent agent configuration
- Test each agent individually with pattern catalog
- Validate agent responses

### Phase 3: Orchestrator Development (Week 1-2)

- Implement `build_knowledge.py` (Phase 0 setup script)
- Implement main orchestration logic
- Create parallel agent invocation system (with pattern catalog loading)
- Implement result collection
- Test agent coordination

### Phase 4: Data Processing (Week 2)

- Build email parsing utilities
- Create data loaders for CSV dataset
- Implement dataset sampler for knowledge building
- Implement result formatting
- Build output exporters

### Phase 5: Testing & Validation (Week 2-3)

- Test knowledge building process
- Run agents on test emails (with pattern knowledge)
- Validate against dataset
- Calculate performance metrics
- Tune agent prompts and pattern catalog if needed

### Phase 6: Integration & Refinement (Week 3)

- End-to-end integration testing (Phase 0 + Phase 1)
- Performance optimization
- Error handling
- Edge case handling

### Phase 7: Documentation & Deployment (Week 4)

- Complete documentation
- Create usage examples
- Write user guide (including knowledge building step)
- Deploy system

## 10. Usage Specifications

### 10.1 Command Line Interface

```bash
# PHASE 0: Build knowledge base (run once)
python build_knowledge.py --dataset data/spam_ham_dataset.csv --samples 100

# PHASE 1: Classify emails

# Classify a single email
python classify_email.py --input email.txt

# Classify email from text
python classify_email.py --text "Email content here..."

# Batch classification
python classify_email.py --batch emails_folder/

# Validate against dataset
python validate.py --dataset spam_ham_dataset.csv

# Run specific agent (for testing)
python run_agent.py --agent content-analyzer --input email.txt
```

### 10.2 Python API

```python
from spam_classifier import SpamClassifier

# Initialize classifier
classifier = SpamClassifier()

# Classify email
email_text = "CONGRATULATIONS! You've won $1,000,000! Click here to claim!"

result = classifier.classify(email_text)

print(f"Classification: {result['final_classification']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Reasoning: {result['detailed_reasoning']}")

# Example output:
# {
#   'final_classification': 'SPAM',
#   'final_score': 0.94,
#   'confidence': 0.92,
#   'agent_agreement': 0.97,
#   'summary': 'All agents strongly indicate spam: unrealistic prize claim, urgency tactics, suspicious CTA',
#   'detailed_reasoning': '...',
#   'agent_scores': {
#     'content_analyzer': 0.92,
#     'pattern_recognizer': 0.98,
#     'intent_analyzer': 0.93
#   },
#   'key_evidence': [
#     'Unrealistic financial promise',
#     'Urgency language without context',
#     'Generic prize notification pattern',
#     'Intent clearly fraudulent'
#   ]
# }
```

### 10.3 Orchestrator Implementation Example

```python
import json
from typing import Dict

def load_pattern_catalog() -> Dict:
    """Load the pattern catalog generated in Phase 0."""
    with open('data/pattern_catalog.json', 'r') as f:
        return json.load(f)


def classify_email(email_text: str) -> Dict:
    """
    Classify an email using multi-agent system with pattern knowledge.

    This uses Claude Code agents (no ML models).
    """

    # Step 1: Load pattern catalog (few-shot examples + patterns)
    pattern_catalog = load_pattern_catalog()

    # Step 2: Prepare agent context (patterns + examples + email)
    agent_context = {
        "pattern_catalog": pattern_catalog,
        "email_text": email_text
    }

    # Step 3: Invoke agents in parallel (with pattern knowledge)
    print("Invoking specialized agents with pattern knowledge...")

    content_result = invoke_claude_agent(
        "content-analyzer",
        agent_context
    )
    pattern_result = invoke_claude_agent(
        "pattern-recognizer",
        agent_context
    )
    intent_result = invoke_claude_agent(
        "intent-analyzer",
        agent_context
    )

    # Step 4: Aggregate results
    agent_results = {
        "content_analyzer": content_result,
        "pattern_recognizer": pattern_result,
        "intent_analyzer": intent_result
    }

    # Step 5: Invoke consensus agent
    consensus_input = json.dumps(agent_results, indent=2)
    final_result = invoke_claude_agent("consensus-agent", consensus_input)

    return final_result


def invoke_claude_agent(agent_name: str, context: Dict) -> Dict:
    """
    Invoke a Claude Code agent using the Task tool.

    The agent receives:
    - Pattern catalog with learned patterns
    - Few-shot examples
    - Email to classify

    In practice, this would use Claude Code's agent invocation system.
    """
    # Format the prompt with pattern catalog + email
    prompt = format_agent_prompt(agent_name, context)

    # This is pseudocode - actual implementation uses Claude Code Task tool
    # Example: Task(subagent_type=agent_name, prompt=prompt)
    pass


def format_agent_prompt(agent_name: str, context: Dict) -> str:
    """
    Format the prompt for an agent including pattern catalog and examples.
    """
    catalog = context['pattern_catalog']
    email = context['email_text']

    # Include pattern catalog and few-shot examples in the prompt
    prompt = f"""
PATTERN CATALOG (learned from dataset):
{json.dumps(catalog['spam_patterns'], indent=2)}
{json.dumps(catalog['ham_patterns'], indent=2)}

FEW-SHOT EXAMPLES:
{format_examples(catalog['few_shot_examples'])}

NOW CLASSIFY THIS EMAIL:
{email}

Analyze using the patterns above and provide your assessment.
"""
    return prompt
```

## 11. Advantages of LLM-Only Approach

### 11.1 Benefits

1. **No Training Required**
   - No need to split dataset
   - No hyperparameter tuning
   - No model maintenance
   - Immediate deployment

2. **Full Explainability**
   - Every decision has natural language reasoning
   - Users understand WHY email was classified
   - Transparent decision process
   - Auditable classifications

3. **Adaptability**
   - Handles new spam patterns immediately
   - No retraining needed for new tactics
   - Understanding-based (not pattern-memorization)
   - Generalizes to novel spam types

4. **Ease of Development**
   - No ML expertise required
   - Faster iteration (just update prompts)
   - Easier debugging (read agent reasoning)
   - Simpler codebase

5. **Multi-Perspective Analysis**
   - Different angles on same problem
   - Reduces blind spots
   - Consensus-based decisions
   - Higher confidence

### 11.2 Considerations

1. **API Costs**
   - Each classification requires 4 LLM calls
   - Consider caching for repeated emails
   - Batch processing for efficiency

2. **Latency**
   - ~3-5 seconds per email (parallel agents)
   - Acceptable for non-real-time use
   - Can be optimized with batching

3. **Consistency**
   - LLM outputs can vary slightly
   - Use temperature=0 for deterministic results
   - Consensus mechanism adds stability

## 12. Monitoring & Maintenance

### 12.1 Performance Monitoring

Track these metrics:

- Classification accuracy (against known labels)
- Agent agreement rates
- Uncertainty flag frequency
- Processing time per email
- False positive/negative rates

### 12.2 Maintenance Tasks

- Review uncertain classifications weekly
- Update agent prompts based on new spam tactics
- Regenerate pattern catalog with new spam samples (monthly)
- Add new pattern categories to pattern-learner agent
- Validate against fresh spam samples monthly

### 12.3 Logging

Log format:

```json
{
  "timestamp": "2025-10-07T10:30:00Z",
  "email_id": "abc123",
  "classification": "SPAM",
  "confidence": 0.94,
  "agent_scores": {...},
  "processing_time_ms": 4250
}
```

## 13. Success Criteria

System is successful when:

1. **Accuracy**: Achieves ≥95% on validation dataset
2. **Explainability**: 100% of classifications have clear reasoning
3. **Speed**: Processes emails in <5 seconds on average
4. **Agreement**: Agents reach consensus (≥0.7) in >90% of cases
5. **Reliability**: Maintains performance over time without retraining
6. **Usability**: Simple API and clear explanations

## 14. Future Enhancements

- **Learning from Corrections**: When humans override, store feedback for prompt refinement and pattern catalog updates
- **Specialized Agents**: Add domain-specific agents (finance, healthcare, etc.)
- **Confidence Calibration**: Fine-tune thresholds based on user feedback
- **Multi-Language**: Add agents for non-English emails with language-specific patterns
- **Image Analysis**: Agent for analyzing email images/attachments
- **Real-time Adaptation**: Continuous pattern catalog updates with latest spam tactics
- **Active Learning**: Identify emails where agents are uncertain and use them to improve pattern catalog

## 15. Example Classification

### Input Email

```
Subject: URGENT: Your PayPal Account Has Been Limited!

Dear Valued Customer,

Your PayPal account has been limited due to suspicious activity.
You must verify your identity within 24 hours or your account will
be permanently closed and funds forfeited.

Click here to verify now: http://paypa1-secure.com/verify

Failure to act immediately will result in account termination.

PayPal Security Team
```

### Expected Output

```json
{
  "final_classification": "SPAM",
  "final_score": 0.96,
  "confidence": 0.94,
  "agent_agreement": 0.95,

  "summary": "This is a phishing email impersonating PayPal. All agents agree this is spam with very high confidence.",

  "detailed_reasoning": "This email exhibits multiple strong spam indicators across all analysis dimensions. The Content Analyzer identified severe urgency tactics ('URGENT', '24 hours', 'immediately') combined with threats of account closure and fund forfeiture, which are classic phishing pressure techniques. The Pattern Recognizer detected a clear PayPal impersonation pattern with a suspicious URL (paypa1-secure.com instead of paypal.com), which is a common phishing tactic. The Intent Analyzer determined the primary intent is credential harvesting through a fake verification page, with secondary intent of creating panic to bypass rational thinking. All three agents scored this above 0.9 for spam likelihood with strong confidence, resulting in unanimous agreement that this is a malicious phishing attempt.",

  "agent_scores": {
    "content_analyzer": 0.95,
    "pattern_recognizer": 0.98,
    "intent_analyzer": 0.96
  },

  "key_evidence": [
    "Extreme urgency and threat language",
    "PayPal impersonation with typosquatted domain",
    "Suspicious URL structure",
    "Credential harvesting intent clear",
    "Fear-based manipulation tactics",
    "Unrealistic 24-hour ultimatum"
  ],

  "uncertainty_flag": false
}
```

## 16. References

1. Anthropic Claude Code Documentation - Subagents
2. Anthropic Engineering - Multi-Agent Research System
3. "Machine Learning for Email Spam Filtering: Review and Approaches" (2025)
4. Claude Code Best Practices (Anthropic)

---

**Document Version**: 3.0 - LLM-Only Architecture with Pattern Learning
**Date**: October 7, 2025
**Approach**: Pure Claude Code Multi-Agent System with Few-Shot Learning (No Traditional ML)
**Key Innovation**: Pattern catalog extraction from dataset for context-aware classification
**Status**: Specification Complete - Ready for Implementation
