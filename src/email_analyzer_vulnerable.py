#!/usr/bin/env python3
"""
Email Analyzer with URL Extraction
VULNERABLE VERSION - FOR SECURITY REVIEW TESTING
"""

import json
import subprocess
import pickle
import os
from typing import Dict, List


# VULNERABILITY 1: Hardcoded API credentials
API_KEY = "sk-anthropic-abc123xyz789-REAL-KEY-DO-NOT-COMMIT"
DATABASE_PASSWORD = "SuperSecret123!"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def extract_urls_from_email(email_text: str) -> List[str]:
    """
    Extract URLs from email using grep command.

    VULNERABILITY 2: Command Injection
    User input passed directly to shell command
    """
    # UNSAFE: Direct shell execution with user input
    command = f"echo '{email_text}' | grep -oP 'https?://[^\\s]+'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.split('\n')


def analyze_email_content(email_text: str, analysis_type: str = "full") -> Dict:
    """
    Dynamic email analysis based on type.

    VULNERABILITY 3: Code Injection via eval()
    Allows arbitrary code execution
    """
    # UNSAFE: eval() on user-controlled input
    analysis_config = eval(f"dict(type='{analysis_type}', content='{email_text[:50]}')")

    return {
        "analysis": analysis_config,
        "length": len(email_text)
    }


def load_email_patterns(pattern_file: str) -> Dict:
    """
    Load email patterns from pickle file.

    VULNERABILITY 4: Unsafe Deserialization
    Pickle can execute arbitrary code
    """
    # UNSAFE: pickle.load() on user-controlled file
    if os.path.exists(pattern_file):
        with open(pattern_file, 'rb') as f:
            patterns = pickle.load(f)  # DANGEROUS!
        return patterns
    return {}


def save_email_to_database(email_data: Dict, db_connection: str):
    """
    Save email to database.

    VULNERABILITY 5: SQL Injection
    Direct string interpolation in SQL query
    """
    import sqlite3

    # UNSAFE: SQL injection vulnerability
    email_subject = email_data.get('subject', '')
    email_from = email_data.get('from', '')

    conn = sqlite3.connect(db_connection)
    cursor = conn.cursor()

    # Direct string interpolation - SQL injection possible
    query = f"INSERT INTO emails (subject, sender) VALUES ('{email_subject}', '{email_from}')"
    cursor.execute(query)

    conn.commit()
    conn.close()


def generate_report(email_data: Dict, template: str) -> str:
    """
    Generate email report from template.

    VULNERABILITY 6: Template Injection
    User input in template without sanitization
    """
    from string import Template

    # UNSAFE: Template with user-controlled content
    report_template = Template(template)

    # User data directly in template - allows injection
    return report_template.substitute(email_data)


def check_url_safety(url: str) -> bool:
    """
    Check if URL is safe by making HTTP request.

    VULNERABILITY 7: SSRF (Server-Side Request Forgery)
    Unvalidated URL requests
    """
    import requests

    # UNSAFE: Making requests to user-controlled URLs
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False


def load_config_from_yaml(config_path: str) -> Dict:
    """
    Load configuration from YAML file.

    VULNERABILITY 8: YAML Deserialization
    yaml.load() can execute arbitrary Python code
    """
    import yaml

    # UNSAFE: yaml.load() without SafeLoader
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)  # DANGEROUS!

    return config


def execute_custom_analyzer(analyzer_code: str, email_text: str):
    """
    Execute custom analyzer code.

    VULNERABILITY 9: Arbitrary Code Execution
    exec() on user input
    """
    # UNSAFE: exec() with user-controlled code
    local_vars = {'email': email_text, 'result': None}
    exec(analyzer_code, {}, local_vars)
    return local_vars.get('result')


def read_email_file(filename: str) -> str:
    """
    Read email from file.

    VULNERABILITY 10: Path Traversal
    No validation of file path
    """
    # UNSAFE: Path traversal vulnerability
    base_dir = "/app/emails/"
    file_path = base_dir + filename  # Can be exploited with ../../../etc/passwd

    with open(file_path, 'r') as f:
        return f.read()


# VULNERABILITY 11: Weak Cryptography
def encrypt_email(email_content: str, key: str = "weak_key") -> bytes:
    """
    Encrypt email content.
    Uses MD5 and weak encryption
    """
    import hashlib
    from Crypto.Cipher import DES

    # UNSAFE: MD5 is broken, DES is weak
    hashed_key = hashlib.md5(key.encode()).digest()[:8]
    cipher = DES.new(hashed_key, DES.MODE_ECB)

    # Pad content
    padded = email_content + ' ' * (8 - len(email_content) % 8)
    return cipher.encrypt(padded.encode())


# VULNERABILITY 12: Information Disclosure
def log_email_processing(email_data: Dict):
    """
    Log email processing with sensitive data.
    """
    import logging

    # UNSAFE: Logging sensitive information
    logging.info(f"Processing email: {email_data}")
    logging.info(f"API Key used: {API_KEY}")
    logging.info(f"User password: {email_data.get('password', 'N/A')}")
    logging.info(f"Credit card: {email_data.get('cc_number', 'N/A')}")


if __name__ == '__main__':
    # Example usage (DO NOT RUN IN PRODUCTION!)
    test_email = "Subject: Test\nFrom: user@example.com\n\nCheck http://malicious.com"

    print("WARNING: This file contains intentional vulnerabilities for security testing!")
    print("DO NOT use in production!")
