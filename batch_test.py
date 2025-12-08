#!/usr/bin/env python3
"""
Batch Plagiarism Detection Testing
Processes multiple file pairs and saves results to CSV
Pairs files by number: file1.java <-> file1.cs, file2.java <-> file2.cs, etc.
"""

import os
import subprocess
import csv
import json
import re
from pathlib import Path
from datetime import datetime
import argparse

def run_detector(file1, file2, lang1, lang2):
    """
    Run the detector on a single file pair and parse output
    """
    cmd = [
        'python', 'detector_v9.py',
        '--file1', file1,
        '--file2', file2,
        '--lang1', lang1,
        '--lang2', lang2
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per pair
        )
        
        output = result.stdout
        
        # Parse key metrics using regex
        metrics = {
            'file1': os.path.basename(file1),
            'file2': os.path.basename(file2),
            'lang1': lang1,
            'lang2': lang2,
            'semantic': extract_metric(output, r'Semantic Similarity:\s+([\d.]+)'),
            'syntactic': extract_metric(output, r'Syntactic Similarity:\s+([\d.]+)'),
            'structural': extract_metric(output, r'Structural Similarity:\s+([\d.]+)'),
            'd_lang': extract_metric(output, r'Language Dissimilarity:\s+([\d.]+)'),
            'complexity': extract_metric(output, r'Complexity:\s+([\d.]+)'),
            'w_codebert': extract_metric(output, r'Gating Weights \(CodeBERT/AST/Token\):\s+([\d.]+)'),
            'w_ast': extract_metric(output, r'Gating Weights \(CodeBERT/AST/Token\):\s+[\d.]+\s+/\s+([\d.]+)'),
            'w_token': extract_metric(output, r'Gating Weights \(CodeBERT/AST/Token\):\s+[\d.]+\s+/\s+[\d.]+\s+/\s+([\d.]+)'),
            'final_score': extract_metric(output, r'Final Score:\s+([\d.]+)'),
            'threshold': extract_metric(output, r'Threshold:\s+([\d.]+)'),
            'prediction': extract_prediction(output),
            'confidence_margin': extract_metric(output, r'Confidence Margin:\s+([-\d.]+)')
        }
        
        return metrics
    
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ TIMEOUT: {file1} vs {file2}")
        return None
    except Exception as e:
        print(f"  ❌ ERROR: {file1} vs {file2} - {str(e)}")
        return None

def extract_metric(text, pattern):
    """Extract a numeric metric using regex"""
    match = re.search(pattern, text)
    return float(match.group(1)) if match else None

def extract_prediction(text):
    """Extract plagiarism prediction"""
    if 'PLAGIARISM (CLONE)' in text:
        return 'PLAGIARISM'
    elif 'NO PLAGIARISM' in text:
        return 'NO_PLAGIARISM'
    else:
        return 'UNKNOWN'

def extract_file_number(filename):
    """
    Extract numeric identifier from filename
    Examples:
        'file1.java' -> 1
        'file100.cs' -> 100
        'twosum_5.py' -> 5
        'assignment_003.c' -> 3
    """
    # Try to find any number in the filename
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None

def batch_test(test_cases, output_csv='results.csv'):
    """
    Run batch testing on multiple file pairs
    
    Args:
        test_cases: List of dicts with keys: file1, file2, lang1, lang2, ground_truth (optional)
        output_csv: Output CSV file path
    """
    results = []
    total = len(test_cases)
    
    print(f"\n{'='*80}")
    print(f"BATCH TESTING: {total} file pairs")
    print(f"{'='*80}\n")
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"[{idx}/{total}] Testing: {test_case['file1']} vs {test_case['file2']}")
        
        metrics = run_detector(
            test_case['file1'],
            test_case['file2'],
            test_case['lang1'],
            test_case['lang2']
        )
        
        if metrics:
            # Add ground truth if available
            if 'ground_truth' in test_case:
                metrics['ground_truth'] = test_case['ground_truth']
            
            results.append(metrics)
            print(f"  ✓ Score: {metrics['final_score']:.3f} | Prediction: {metrics['prediction']}")
        
        print()
    
    # Save to CSV
    save_results(results, output_csv)
    
    print(f"\n{'='*80}")
    print(f"✓ Batch testing complete! Results saved to: {output_csv}")
    print(f"{'='*80}\n")
    
    return results

def save_results(results, output_csv):
    """Save results to CSV file"""
    if not results:
        print("⚠️ No results to save")
        return
    
    fieldnames = results[0].keys()
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def load_test_cases_from_directory(dir1, dir2, lang1, lang2, ground_truth_file=None):
    """
    Auto-generate test cases from two directories by matching file numbers
    
    Args:
        dir1: Directory containing original files (e.g., file1.java, file2.java, ...)
        dir2: Directory containing comparison files (e.g., file1.cs, file2.cs, ...)
        lang1: Language of files in dir1
        lang2: Language of files in dir2
        ground_truth_file: Optional CSV with columns: file1, file2, is_plagiarism
    
    Example:
        dir1/file1.java  <->  dir2/file1.cs
        dir1/file2.java  <->  dir2/file2.cs
        dir1/file100.java <-> dir2/file100.cs
    """
    # Load ground truth if available
    ground_truth = {}
    if ground_truth_file and os.path.exists(ground_truth_file):
        with open(ground_truth_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['file1'], row['file2'])
                ground_truth[key] = row['is_plagiarism']
    
    # Get all files from both directories
    ext1 = get_extension(lang1)
    ext2 = get_extension(lang2)
    
    files1 = list(Path(dir1).glob(f'*.{ext1}'))
    files2 = list(Path(dir2).glob(f'*.{ext2}'))
    
    # Build dictionaries mapping file numbers to file paths
    files1_dict = {}
    for f in files1:
        num = extract_file_number(f.name)
        if num is not None:
            files1_dict[num] = f
        else:
            print(f"⚠️ Warning: Could not extract number from {f.name}, skipping...")
    
    files2_dict = {}
    for f in files2:
        num = extract_file_number(f.name)
        if num is not None:
            files2_dict[num] = f
        else:
            print(f"⚠️ Warning: Could not extract number from {f.name}, skipping...")
    
    # Find common file numbers
    common_numbers = sorted(set(files1_dict.keys()) & set(files2_dict.keys()))
    
    if not common_numbers:
        print(f"❌ ERROR: No matching file pairs found!")
        print(f"   Files in {dir1}: {sorted(files1_dict.keys())}")
        print(f"   Files in {dir2}: {sorted(files2_dict.keys())}")
        return []
    
    print(f"\n✓ Found {len(common_numbers)} matching file pairs")
    print(f"  File numbers: {common_numbers[:10]}{'...' if len(common_numbers) > 10 else ''}")
    
    # Find missing pairs
    only_in_dir1 = set(files1_dict.keys()) - set(files2_dict.keys())
    only_in_dir2 = set(files2_dict.keys()) - set(files1_dict.keys())
    
    if only_in_dir1:
        print(f"  ⚠️ Files in {dir1} without matches: {sorted(only_in_dir1)}")
    if only_in_dir2:
        print(f"  ⚠️ Files in {dir2} without matches: {sorted(only_in_dir2)}")
    
    # Create test cases for matching pairs
    test_cases = []
    for num in common_numbers:
        f1 = files1_dict[num]
        f2 = files2_dict[num]
        
        test_case = {
            'file1': str(f1),
            'file2': str(f2),
            'lang1': lang1,
            'lang2': lang2
        }
        
        # Add ground truth if available
        key = (f1.name, f2.name)
        if key in ground_truth:
            test_case['ground_truth'] = ground_truth[key]
        
        test_cases.append(test_case)
    
    return test_cases

def get_extension(lang):
    """Get file extension for language"""
    extensions = {
        'java': 'java',
        'python': 'py',
        'c': 'c',
        'csharp': 'cs'
    }
    return extensions.get(lang, lang)

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch Plagiarism Detection Testing - Pairs files by number",
        epilog="""
Examples:
  # Compare file1.java <-> file1.cs, file2.java <-> file2.cs, etc.
  python batch_test.py --dir1 java_files --dir2 csharp_files --lang1 java --lang2 csharp
  
  # Same language comparison
  python batch_test.py --dir1 originals --dir2 submissions --lang1 java --lang2 java --output results.csv
  
  # With ground truth
  python batch_test.py --dir1 originals --dir2 submissions --lang1 java --lang2 java --ground-truth truth.csv
  
  # Using JSON config
  python batch_test.py --config test_config.json
        """
    )
    parser.add_argument('--dir1', type=str, help="Directory with original files (e.g., file1.java, file2.java)")
    parser.add_argument('--dir2', type=str, help="Directory with comparison files (e.g., file1.cs, file2.cs)")
    parser.add_argument('--lang1', type=str, default='java', choices=['java', 'python', 'c', 'csharp'])
    parser.add_argument('--lang2', type=str, default='java', choices=['java', 'python', 'c', 'csharp'])
    parser.add_argument('--output', type=str, default='results.csv', help="Output CSV file")
    parser.add_argument('--ground-truth', type=str, help="Ground truth CSV file")
    parser.add_argument('--config', type=str, help="JSON config file with test cases")
    args = parser.parse_args()
    
    # Load test cases
    if args.config:
        # Load from JSON config
        print(f"\n✓ Loading test cases from config: {args.config}")
        with open(args.config, 'r') as f:
            config = json.load(f)
            test_cases = config['test_cases']
    elif args.dir1 and args.dir2:
        # Auto-generate from directories with numbered file matching
        print(f"\n✓ Scanning directories for numbered file pairs...")
        print(f"  Directory 1: {args.dir1} (*.{get_extension(args.lang1)})")
        print(f"  Directory 2: {args.dir2} (*.{get_extension(args.lang2)})")
        
        test_cases = load_test_cases_from_directory(
            args.dir1, args.dir2, args.lang1, args.lang2, args.ground_truth
        )
        
        if not test_cases:
            print("\n❌ No valid test cases found. Exiting.")
            exit(1)
    else:
        print("❌ Error: Provide either --config or both --dir1 and --dir2")
        exit(1)
    
    # Run batch testing
    results = batch_test(test_cases, args.output)