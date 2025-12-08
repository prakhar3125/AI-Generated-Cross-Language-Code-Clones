import os
import re
import pandas as pd
from tqdm import tqdm

def parse_code_file(filepath):
    """
    Parses a single file containing multiple language snippets.
    
    The format is expected to be:
    #input (Java code)
    #====================
    #gpt output=============
    Language_Label (Python/C/C# code)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # --- Extract Java Code ---
    java_match = re.search(r'#input\s*(.*?)\s*#=+', content, re.DOTALL)
    java_code = java_match.group(1).strip() if java_match else None
    
    # --- Extract Other Languages ---
    output_match = re.search(r'#gpt output=+\s*(.*)', content, re.DOTALL)
    if not output_match:
        return {'java': java_code, 'python': None, 'c': None, 'csharp': None}
        
    output_part = output_match.group(1).strip()
    
    # Enhanced pattern to match all separator variations:
    # - Python: / Python implementation: / Python Implementation: / //Python
    # - C: / C implementation: / C Implementation: / //C
    # - C#: / C# implementation: / C# Implementation: / //C#
    lang_pattern = re.compile(
        r'^\s*(?://\s*)?(Python|C#|C)\s*(?:[Ii]mplementation)?:?\s*$', 
        flags=re.MULTILINE
    )
    
    # Find all language headers and their positions
    matches = list(lang_pattern.finditer(output_part))
    
    clones = {}
    
    for i, match in enumerate(matches):
        lang_raw = match.group(1)
        # Normalize language names
        if lang_raw.lower() == 'python':
            lang_key = 'python'
        elif lang_raw == 'C#':
            lang_key = 'csharp'
        elif lang_raw == 'C':
            lang_key = 'c'
        else:
            continue
        
        # Extract code from end of this match to start of next match (or end of string)
        start_pos = match.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(output_part)
        
        code = output_part[start_pos:end_pos].strip()
        clones[lang_key] = code
    
    return {
        'java': java_code,
        'python': clones.get('python'),
        'c': clones.get('c'),
        'csharp': clones.get('csharp')
    }


def main():
    """Main script execution"""
    
    # The folder where you placed all your .java files
    DATA_FOLDER = 'java_files_folder'
    
    # The final output file
    OUTPUT_CSV = 'code_clones.csv'
    
    if not os.path.isdir(DATA_FOLDER):
        print(f"Error: Folder '{DATA_FOLDER}' not found.")
        print("Please create it and place your .java files inside.")
        return
    
    all_parsed_data = []
    
    java_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.java')]
    
    if not java_files:
        print(f"No .java files found in '{DATA_FOLDER}'")
        return
    
    print(f"Found {len(java_files)} .java files. Parsing...")
    
    failed_files = []
    
    for filename in tqdm(java_files, desc="Processing files"):
        filepath = os.path.join(DATA_FOLDER, filename)
        try:
            parsed_data = parse_code_file(filepath)
            parsed_data['filename'] = filename  # Add filename for reference
            all_parsed_data.append(parsed_data)
        except Exception as e:
            failed_files.append((filename, str(e)))
            print(f"\nWarning: Could not parse file '{filename}': {e}")
    
    if not all_parsed_data:
        print("No data was successfully parsed!")
        return
    
    df = pd.DataFrame(all_parsed_data)
    
    # Reorder columns: filename first, then languages
    df = df[['filename', 'java', 'python', 'c', 'csharp']]
    
    # Remove rows where any language code is missing (empty or None)
    initial_count = len(df)
    
    # First remove rows with None/NaN values
    df = df.dropna(subset=['java', 'python', 'c', 'csharp'])
    
    # Then remove rows where any cell is empty string or only whitespace
    # Replace empty strings with NaN first, then drop those rows
    df['java'] = df['java'].replace(r'^\s*$', None, regex=True)
    df['python'] = df['python'].replace(r'^\s*$', None, regex=True)
    df['c'] = df['c'].replace(r'^\s*$', None, regex=True)
df['csharp'] = df['csharp'].replace(r'^\s*$', None, regex=True)
    
    if len(df) == 0:
        print("\nWarning: No complete rows found! All rows had at least one missing language.")
        print("No CSV file was created.")
        return
    
    df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n{'='*60}")
    print(f"Successfully created '{OUTPUT_CSV}' with {len(df)} entries.")
    print(f"{'='*60}")
    
    # Statistics
    print("\nStatistics:")
    print(f"  Total files processed: {len(java_files)}")
    print(f"  Successfully parsed: {len(all_parsed_data)}")
    print(f"  Rows with all 4 languages: {len(df)}")
    print(f"  Rows removed (incomplete): {removed_count}")
    print(f"  Failed to parse: {len(failed_files)}")
    
    # Count non-null entries for each language
    print("\nCode snippets found:")
    for lang in ['java', 'python', 'c', 'csharp']:
        count = df[lang].notna().sum()
        print(f"  {lang.upper()}: {count}")
    
    if failed_files:
        print(f"\nFailed files ({len(failed_files)}):")
        for filename, error in failed_files[:5]:  # Show first 5
            print(f"  - {filename}: {error}")
        if len(failed_files) > 5:
            print(f"  ... and {len(failed_files) - 5} more")
    
    print(f"\n{'='*60}")
    print("CSV Preview (first 3 rows):")
    print(f"{'='*60}")
    # Show preview without truncation for better visibility
    pd.set_option('display.max_colwidth', 100)
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()
, None, regex=True)
    df['python'] = df['python'].replace(r'^\s*
    
    if len(df) == 0:
        print("\nWarning: No complete rows found! All rows had at least one missing language.")
        print("No CSV file was created.")
        return
    
    df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n{'='*60}")
    print(f"Successfully created '{OUTPUT_CSV}' with {len(df)} entries.")
    print(f"{'='*60}")
    
    # Statistics
    print("\nStatistics:")
    print(f"  Total files processed: {len(java_files)}")
    print(f"  Successfully parsed: {len(all_parsed_data)}")
    print(f"  Rows with all 4 languages: {len(df)}")
    print(f"  Rows removed (incomplete): {removed_count}")
    print(f"  Failed to parse: {len(failed_files)}")
    
    # Count non-null entries for each language
    print("\nCode snippets found:")
    for lang in ['java', 'python', 'c', 'csharp']:
        count = df[lang].notna().sum()
        print(f"  {lang.upper()}: {count}")
    
    if failed_files:
        print(f"\nFailed files ({len(failed_files)}):")
        for filename, error in failed_files[:5]:  # Show first 5
            print(f"  - {filename}: {error}")
        if len(failed_files) > 5:
            print(f"  ... and {len(failed_files) - 5} more")
    
    print(f"\n{'='*60}")
    print("CSV Preview (first 3 rows):")
    print(f"{'='*60}")
    # Show preview without truncation for better visibility
    pd.set_option('display.max_colwidth', 100)
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()
, None, regex=True)
    df['c'] = df['c'].replace(r'^\s*
    
    if len(df) == 0:
        print("\nWarning: No complete rows found! All rows had at least one missing language.")
        print("No CSV file was created.")
        return
    
    df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n{'='*60}")
    print(f"Successfully created '{OUTPUT_CSV}' with {len(df)} entries.")
    print(f"{'='*60}")
    
    # Statistics
    print("\nStatistics:")
    print(f"  Total files processed: {len(java_files)}")
    print(f"  Successfully parsed: {len(all_parsed_data)}")
    print(f"  Rows with all 4 languages: {len(df)}")
    print(f"  Rows removed (incomplete): {removed_count}")
    print(f"  Failed to parse: {len(failed_files)}")
    
    # Count non-null entries for each language
    print("\nCode snippets found:")
    for lang in ['java', 'python', 'c', 'csharp']:
        count = df[lang].notna().sum()
        print(f"  {lang.upper()}: {count}")
    
    if failed_files:
        print(f"\nFailed files ({len(failed_files)}):")
        for filename, error in failed_files[:5]:  # Show first 5
            print(f"  - {filename}: {error}")
        if len(failed_files) > 5:
            print(f"  ... and {len(failed_files) - 5} more")
    
    print(f"\n{'='*60}")
    print("CSV Preview (first 3 rows):")
    print(f"{'='*60}")
    # Show preview without truncation for better visibility
    pd.set_option('display.max_colwidth', 100)
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()
, None, regex=True)
    df['csharp'] = df['csharp'].replace(r'^\s*
    
    if len(df) == 0:
        print("\nWarning: No complete rows found! All rows had at least one missing language.")
        print("No CSV file was created.")
        return
    
    df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n{'='*60}")
    print(f"Successfully created '{OUTPUT_CSV}' with {len(df)} entries.")
    print(f"{'='*60}")
    
    # Statistics
    print("\nStatistics:")
    print(f"  Total files processed: {len(java_files)}")
    print(f"  Successfully parsed: {len(all_parsed_data)}")
    print(f"  Rows with all 4 languages: {len(df)}")
    print(f"  Rows removed (incomplete): {removed_count}")
    print(f"  Failed to parse: {len(failed_files)}")
    
    # Count non-null entries for each language
    print("\nCode snippets found:")
    for lang in ['java', 'python', 'c', 'csharp']:
        count = df[lang].notna().sum()
        print(f"  {lang.upper()}: {count}")
    
    if failed_files:
        print(f"\nFailed files ({len(failed_files)}):")
        for filename, error in failed_files[:5]:  # Show first 5
            print(f"  - {filename}: {error}")
        if len(failed_files) > 5:
            print(f"  ... and {len(failed_files) - 5} more")
    
    print(f"\n{'='*60}")
    print("CSV Preview (first 3 rows):")
    print(f"{'='*60}")
    # Show preview without truncation for better visibility
    pd.set_option('display.max_colwidth', 100)
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()
, None, regex=True)
    
    # Drop any rows with None/NaN in language columns
    df = df.dropna(subset=['java', 'python', 'c', 'csharp'])
    
    removed_count = initial_count - len(df)
    
    if len(df) == 0:
        print("\nWarning: No complete rows found! All rows had at least one missing language.")
        print("No CSV file was created.")
        return
    
    df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n{'='*60}")
    print(f"Successfully created '{OUTPUT_CSV}' with {len(df)} entries.")
    print(f"{'='*60}")
    
    # Statistics
    print("\nStatistics:")
    print(f"  Total files processed: {len(java_files)}")
    print(f"  Successfully parsed: {len(all_parsed_data)}")
    print(f"  Rows with all 4 languages: {len(df)}")
    print(f"  Rows removed (incomplete): {removed_count}")
    print(f"  Failed to parse: {len(failed_files)}")
    
    # Count non-null entries for each language
    print("\nCode snippets found:")
    for lang in ['java', 'python', 'c', 'csharp']:
        count = df[lang].notna().sum()
        print(f"  {lang.upper()}: {count}")
    
    if failed_files:
        print(f"\nFailed files ({len(failed_files)}):")
        for filename, error in failed_files[:5]:  # Show first 5
            print(f"  - {filename}: {error}")
        if len(failed_files) > 5:
            print(f"  ... and {len(failed_files) - 5} more")
    
    print(f"\n{'='*60}")
    print("CSV Preview (first 3 rows):")
    print(f"{'='*60}")
    # Show preview without truncation for better visibility
    pd.set_option('display.max_colwidth', 100)
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()