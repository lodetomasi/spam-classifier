#!/usr/bin/env python3
"""
Real Agent Classifier - Uses ONLY real Claude agents via Task invocations
NO programmatic simulation, NO fake calls
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List
import sys


def load_pattern_catalog(path: str = "data/pattern_catalog.json") -> Dict:
    """Load the pattern catalog for agent context."""
    with open(path, 'r') as f:
        return json.load(f)


def load_samples(csv_path: str, n_samples: int = 10) -> List[Dict]:
    """Load balanced samples from dataset."""
    df = pd.read_csv(csv_path)

    # Get equal spam and ham
    spam_df = df[df['label_num'] == 1].head(n_samples // 2)
    ham_df = df[df['label_num'] == 0].head(n_samples // 2)

    samples = []
    for _, row in pd.concat([spam_df, ham_df]).iterrows():
        samples.append({
            'text': row['text'],
            'label': 'spam' if row['label_num'] == 1 else 'ham'
        })

    return samples


def format_pattern_context(catalog: Dict) -> str:
    """Format pattern catalog for agent context."""
    context = "KNOWN PATTERNS FROM CATALOG:\n"

    # Spam patterns
    if 'spam_patterns' in catalog:
        if 'intent_patterns' in catalog['spam_patterns']:
            context += "\nSpam Intent Patterns:\n"
            for pattern in catalog['spam_patterns']['intent_patterns']:
                freq = pattern.get('frequency', 'unknown')
                context += f"- {pattern['pattern_type']}: {pattern['description']} ({freq})\n"

    # Ham patterns
    if 'ham_patterns' in catalog:
        if 'legitimate_characteristics' in catalog['ham_patterns']:
            context += "\nLegitimate Email Patterns:\n"
            for pattern in catalog['ham_patterns']['legitimate_characteristics']:
                freq = pattern.get('frequency', 'unknown')
                context += f"- {pattern['pattern_type']}: {pattern['description']} ({freq})\n"

    return context


def create_agent_prompt(agent_type: str, email_text: str, pattern_context: str, other_results: Dict = None) -> str:
    """Create prompts for each agent type."""

    if agent_type == "content_analyzer":
        return f"""You are the Content Analyzer Agent for a spam classification system.

Your task: Analyze this email's content semantically and identify red flags.

EMAIL TEXT:
---
{email_text[:2000]}
---

{pattern_context}

Your response must include:
1. spam_score (0.0-1.0)
2. confidence (0.0-1.0)
3. red_flags (list of issues found)
4. patterns_detected (list of pattern types)
5. recommendation (SPAM, HAM, or UNCERTAIN)

Return ONLY a JSON object with these fields."""

    elif agent_type == "pattern_recognizer":
        return f"""You are the Pattern Recognizer Agent for a spam classification system.

Your task: Identify known spam patterns in this email.

EMAIL TEXT:
---
{email_text[:2000]}
---

{pattern_context}

Your response must include:
1. spam_score (0.0-1.0)
2. confidence (0.0-1.0)
3. patterns_found (list of specific patterns identified)
4. risk_level (CRITICAL, HIGH, MEDIUM, LOW)
5. urls_analyzed (list of URL analysis)
6. recommendation (SPAM, HAM, or UNCERTAIN)

Return ONLY a JSON object with these fields."""

    elif agent_type == "intent_analyzer":
        context_info = ""
        if other_results:
            context_info = f"\n\nCONTEXT FROM OTHER AGENTS:\n"
            if 'content' in other_results:
                context_info += f"- Content Analyzer: spam_score={other_results['content'].get('spam_score', 0):.2f}\n"
            if 'pattern' in other_results:
                context_info += f"- Pattern Recognizer: risk_level={other_results['pattern'].get('risk_level', 'UNKNOWN')}\n"

        return f"""You are the Intent Analyzer Agent for a spam classification system.

Your task: Determine the true intent behind this email.

EMAIL TEXT:
---
{email_text[:2000]}
---

{pattern_context}{context_info}

Your response must include:
1. spam_score (0.0-1.0)
2. confidence (0.0-1.0)
3. primary_intent (e.g., PHARMACEUTICAL_SALES, PIRATED_SOFTWARE_SALES, FINANCIAL_FRAUD, PHISHING, BUSINESS_COMMUNICATION, TRANSACTIONAL)
4. legitimacy_score (0.0-1.0)
5. deception_indicators (list of deceptive tactics)
6. trust_signals (list of legitimate indicators, if any)
7. risk_if_complied (description of user risk)
8. recommendation (SPAM, HAM, or UNCERTAIN)

Return ONLY a JSON object with these fields."""

    elif agent_type == "consensus":
        content = other_results.get('content', {})
        pattern = other_results.get('pattern', {})
        intent = other_results.get('intent', {})

        return f"""You are the Consensus Agent for a spam classification system.

Your task: Synthesize all agent analyses into a final classification.

AGENT RESULTS:
---
Content Analyzer:
- spam_score: {content.get('spam_score', 0)}
- confidence: {content.get('confidence', 0)}
- recommendation: {content.get('recommendation', 'UNKNOWN')}

Pattern Recognizer:
- spam_score: {pattern.get('spam_score', 0)}
- confidence: {pattern.get('confidence', 0)}
- recommendation: {pattern.get('recommendation', 'UNKNOWN')}
- risk_level: {pattern.get('risk_level', 'UNKNOWN')}

Intent Analyzer:
- spam_score: {intent.get('spam_score', 0)}
- confidence: {intent.get('confidence', 0)}
- recommendation: {intent.get('recommendation', 'UNKNOWN')}
- primary_intent: {intent.get('primary_intent', 'UNKNOWN')}
- legitimacy_score: {intent.get('legitimacy_score', 0)}
---

Your response must include:
1. final_classification (SPAM, HAM, or UNCERTAIN)
2. final_score (0.0-1.0) - weighted average using confidence weights: content 30%, pattern 35%, intent 35%
3. confidence (0.0-1.0) - average of agent confidences
4. agent_agreement (0.0-1.0) - 1.0 minus the range between min and max scores
5. summary (brief explanation)
6. key_evidence (list of top 3-5 evidence points)

Return ONLY a JSON object with these fields."""


def parse_agent_response(response: str) -> Dict:
    """Parse agent response and extract JSON."""
    # Find JSON in response
    start = response.find('{')
    end = response.rfind('}') + 1

    if start == -1 or end == 0:
        raise ValueError(f"No JSON found in response: {response[:200]}")

    json_str = response[start:end]
    return json.loads(json_str)


def calculate_metrics(results: List[Dict]) -> Dict:
    """Calculate classification performance metrics."""
    tp = sum(1 for r in results if r['actual'] == 'spam' and r['predicted'] == 'SPAM')
    tn = sum(1 for r in results if r['actual'] == 'ham' and r['predicted'] == 'HAM')
    fp = sum(1 for r in results if r['actual'] == 'ham' and r['predicted'] == 'SPAM')
    fn = sum(1 for r in results if r['actual'] == 'spam' and r['predicted'] == 'HAM')

    total = len(results)
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'false_positive_rate': fpr,
        'false_negative_rate': fnr,
        'confusion_matrix': {
            'true_positives': tp,
            'true_negatives': tn,
            'false_positives': fp,
            'false_negatives': fn
        },
        'total_samples': total
    }


def print_metrics_report(metrics: Dict):
    """Print formatted metrics report."""
    print("\n" + "="*70)
    print("PERFORMANCE METRICS (REAL AGENTS)")
    print("="*70)
    print(f"\n📊 Overall Performance:")
    print(f"  Accuracy:  {metrics['accuracy']:.2%} {'✓' if metrics['accuracy'] >= 0.95 else '✗'}")
    print(f"  Precision: {metrics['precision']:.2%} {'✓' if metrics['precision'] >= 0.94 else '✗'}")
    print(f"  Recall:    {metrics['recall']:.2%} {'✓' if metrics['recall'] >= 0.93 else '✗'}")
    print(f"  F1-Score:  {metrics['f1_score']:.2%} {'✓' if metrics['f1_score'] >= 0.94 else '✗'}")

    cm = metrics['confusion_matrix']
    print(f"\n📋 Confusion Matrix:")
    print(f"  True Positives:  {cm['true_positives']}")
    print(f"  True Negatives:  {cm['true_negatives']}")
    print(f"  False Positives: {cm['false_positives']}")
    print(f"  False Negatives: {cm['false_negatives']}")
    print("="*70)


def main():
    """Main function - this is a TEMPLATE that shows the structure.

    IMPORTANT: This script generates prompts that you must use with the Task tool.
    It does NOT invoke agents programmatically (that's impossible from Python).

    The actual invocation must be done by Claude Code using the Task tool.
    """

    print("\n" + "="*70)
    print("REAL AGENT CLASSIFIER")
    print("="*70)
    print("\nThis script prepares prompts for real agent invocation.")
    print("Agents must be invoked via Claude Code's Task tool.\n")

    # Load data
    catalog = load_pattern_catalog()
    samples = load_samples('data/spam_ham_dataset.csv', n_samples=int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    pattern_context = format_pattern_context(catalog)

    print(f"Loaded {len(samples)} samples\n")

    # Generate prompts for first sample
    sample = samples[0]
    print(f"Sample 0: {sample['label']}")
    print(f"Text preview: {sample['text'][:100]}...\n")

    print("="*70)
    print("PROMPTS FOR AGENT INVOCATION")
    print("="*70)

    print("\n[1] CONTENT ANALYZER PROMPT:")
    print("-"*70)
    print(create_agent_prompt("content_analyzer", sample['text'], pattern_context))

    print("\n[2] PATTERN RECOGNIZER PROMPT:")
    print("-"*70)
    print(create_agent_prompt("pattern_recognizer", sample['text'], pattern_context))

    print("\n[3] INTENT ANALYZER PROMPT:")
    print("-"*70)
    print(create_agent_prompt("intent_analyzer", sample['text'], pattern_context, {'content': {'spam_score': 0.95}, 'pattern': {'risk_level': 'HIGH'}}))

    print("\n[4] CONSENSUS AGENT PROMPT:")
    print("-"*70)
    print(create_agent_prompt("consensus", sample['text'], pattern_context, {
        'content': {'spam_score': 0.95, 'confidence': 0.98, 'recommendation': 'SPAM'},
        'pattern': {'spam_score': 0.93, 'confidence': 0.97, 'recommendation': 'SPAM', 'risk_level': 'HIGH'},
        'intent': {'spam_score': 0.96, 'confidence': 0.99, 'recommendation': 'SPAM', 'primary_intent': 'FRAUD', 'legitimacy_score': 0.04}
    }))

    print("\n" + "="*70)
    print("Next step: Use these prompts with Claude Code's Task tool")
    print("="*70)


if __name__ == '__main__':
    main()
