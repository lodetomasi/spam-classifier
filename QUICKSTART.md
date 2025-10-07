# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies

```bash
pip install pandas
```

### 2. Verify Dataset

```bash
python -c "import pandas as pd; df = pd.read_csv('data/spam_ham_dataset.csv'); print(f'Dataset loaded: {len(df)} emails')"
```

### 3. Test Dataset Sampler

```bash
python src/utils/dataset_sampler.py data/spam_ham_dataset.csv
```

## Phase 0: Build Knowledge Base (First Time Only)

### Step 1: Sample Dataset

```bash
python src/build_knowledge.py --dataset data/spam_ham_dataset.csv --samples 100
```

**Output**: Creates `data/temp_samples.json` with 100 sampled emails

### Step 2: Invoke Pattern Learner Agent

Ask Claude Code:

```
Use the pattern-learner agent to analyze the emails in data/temp_samples.json
and create a pattern catalog. Save the result to data/pattern_catalog.json
```

**What the agent does**:
- Reads the 100 sampled emails
- Identifies spam patterns (urgency, phishing, scams, etc.)
- Identifies ham patterns (transactional, informational, etc.)
- Extracts few-shot examples
- Saves everything to `data/pattern_catalog.json`

### Step 3: Verify Pattern Catalog

```bash
python src/build_knowledge.py --verify
```

You should see:
```
✓ Pattern catalog is valid
  - Spam content patterns: X
  - Ham patterns: Y
  - Spam examples: Z
  - Ham examples: W
```

## Phase 1: Classify Emails

### Step 1: Prepare Email for Classification

```bash
# Test with spam example
python src/classify_email.py --input examples/spam_example.txt

# Test with ham example
python src/classify_email.py --input examples/ham_example.txt

# Or use your own email text
python src/classify_email.py --text "URGENT! Click here to claim your prize!"
```

**Output**: Creates prompt files in `data/temp_prompts/` for each agent

### Step 2: Invoke Classification Agents

For each of the 3 agents, invoke them with their prompts:

#### Agent 1: Content Analyzer

Ask Claude Code:

```
Use the content-analyzer agent.
Read the prompt from data/temp_prompts/content-analyzer_prompt.txt
and analyze the email. Save your JSON response to
data/temp_results/content_analyzer_result.json
```

#### Agent 2: Pattern Recognizer

```
Use the pattern-recognizer agent.
Read the prompt from data/temp_prompts/pattern-recognizer_prompt.txt
and analyze the email. Save your JSON response to
data/temp_results/pattern_recognizer_result.json
```

#### Agent 3: Intent Analyzer

```
Use the intent-analyzer agent.
Read the prompt from data/temp_prompts/intent-analyzer_prompt.txt
and analyze the email. Save your JSON response to
data/temp_results/intent_analyzer_result.json
```

### Step 3: Invoke Consensus Agent

Ask Claude Code:

```
Use the consensus-agent.
Read these three files:
- data/temp_results/content_analyzer_result.json
- data/temp_results/pattern_recognizer_result.json
- data/temp_results/intent_analyzer_result.json

Synthesize them into a final classification and save to
data/temp_results/final_result.json
```

### Step 4: Display Results

```bash
python src/classify_email.py --load-results
```

**Output**: Beautiful formatted classification with:
- Final classification (SPAM/HAM/UNCERTAIN)
- Confidence score
- Agent agreement
- Key evidence
- Detailed reasoning

## Example Complete Workflow

```bash
# Phase 0 (one-time)
python src/build_knowledge.py --dataset data/spam_ham_dataset.csv
# [Invoke pattern-learner agent]
python src/build_knowledge.py --verify

# Phase 1 (for each email)
python src/classify_email.py --input examples/spam_example.txt
# [Invoke content-analyzer, pattern-recognizer, intent-analyzer agents]
# [Invoke consensus-agent]
python src/classify_email.py --load-results
```

## Tips

- **Save time**: After Phase 0, the pattern catalog is reusable for all emails
- **Batch processing**: You can classify multiple emails by running Phase 1 repeatedly
- **Update patterns**: Re-run Phase 0 monthly with new spam samples to keep patterns fresh
- **Review uncertain cases**: Emails flagged as UNCERTAIN should be manually reviewed

## Troubleshooting

### "Pattern catalog not found"

Run Phase 0 first:
```bash
python src/build_knowledge.py --dataset data/spam_ham_dataset.csv
```

### "Dataset not found"

Ensure your dataset is at:
```bash
ls -la data/spam_ham_dataset.csv
```

### "Agent not found"

Make sure agent files exist:
```bash
ls -la .claude/agents/
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Read [SPECIFICATION_DESIGN.md](SPECIFICATION_DESIGN.md) for architecture details
- Try classifying your own emails
- Experiment with different datasets

---

**Ready to start?** Run Phase 0 now:

```bash
python src/build_knowledge.py --dataset data/spam_ham_dataset.csv --samples 100
```
