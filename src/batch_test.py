#!/usr/bin/env python3
"""
Batch Testing with Real Agents
Tests classification on multiple emails and calculates metrics
"""

import json
import pandas as pd
from datetime import datetime


def load_test_samples(csv_path: str, n_samples: int = 20) -> list:
    """Load balanced test samples."""
    df = pd.read_csv(csv_path)

    # Get equal spam and ham
    spam_samples = df[df['label_num'] == 1].head(n_samples // 2)
    ham_samples = df[df['label_num'] == 0].head(n_samples // 2)

    samples = []
    for idx, row in spam_samples.iterrows():
        samples.append({
            'id': len(samples),
            'label': 'spam',
            'text': row['text'][:500]  # First 500 chars for display
        })

    for idx, row in ham_samples.iterrows():
        samples.append({
            'id': len(samples),
            'label': 'ham',
            'text': row['text'][:500]
        })

    return samples


def save_test_set(samples: list, output_path: str):
    """Save test set to file."""
    with open(output_path, 'w') as f:
        json.dump(samples, f, indent=2)
    print(f"✓ Test set saved to {output_path}")


def calculate_metrics(results: list) -> dict:
    """Calculate performance metrics from results."""
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


def main():
    print("\n" + "="*70)
    print("BATCH TEST WITH REAL AGENTS")
    print("="*70)
    print()

    # Load test samples
    n_samples = 20  # 10 spam + 10 ham
    samples = load_test_samples('data/spam_ham_dataset.csv', n_samples)

    print(f"✓ Loaded {len(samples)} test samples ({n_samples//2} spam, {n_samples//2} ham)\n")

    # Save test set
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_file = f'data/test_set_{timestamp}.json'
    save_test_set(samples, test_file)

    # Display samples
    print("\n" + "="*70)
    print("TEST SAMPLES")
    print("="*70)
    for sample in samples:
        preview = sample['text'][:80].replace('\n', ' ').replace('\r', ' ')
        print(f"\n[{sample['id']}] {sample['label'].upper()}")
        print(f"    {preview}...")

    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\nTo test with real agents:")
    print("1. For each email, invoke all 4 agents via Task tool")
    print("2. Record results in format:")
    print("   {'id': 0, 'actual': 'spam', 'predicted': 'SPAM', 'score': 0.98}")
    print(f"\n3. Save results to: results/test_results_{timestamp}.json")
    print("4. Run: python src/batch_test.py --calculate results/test_results_*.json")
    print()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--calculate':
        # Calculate metrics from results file
        results_file = sys.argv[2]
        with open(results_file, 'r') as f:
            results = json.load(f)

        metrics = calculate_metrics(results)

        print("\n" + "="*70)
        print("TEST RESULTS")
        print("="*70)
        print(f"\n📊 Overall Performance:")
        print(f"  Accuracy:  {metrics['accuracy']:.2%}")
        print(f"  Precision: {metrics['precision']:.2%}")
        print(f"  Recall:    {metrics['recall']:.2%}")
        print(f"  F1-Score:  {metrics['f1_score']:.2%}")

        cm = metrics['confusion_matrix']
        print(f"\n📋 Confusion Matrix:")
        print(f"  TP: {cm['true_positives']}, TN: {cm['true_negatives']}")
        print(f"  FP: {cm['false_positives']}, FN: {cm['false_negatives']}")
        print("="*70 + "\n")
    else:
        main()
