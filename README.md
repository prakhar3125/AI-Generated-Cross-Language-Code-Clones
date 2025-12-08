# Enhancing Plagiarism Detection in AI-Generated Code: Dynamic Multi-Modal Semantic-Structural Analysis
### **System File Registry & Descriptions**
---

| **File Name** | **Pipeline Stage** | **Description** |
| :--- | :--- | :--- |
| **`build_dataset.py`** | **Stage 1: Data Preparation** | Parses raw `.java` files containing multilingual code snippets (from `cross_language.zip`) and converts them into a standardized dataset (`code_clones.csv`). |
| **`extract_features.py`** | **Stage 2: Feature Extraction** | Computes Semantic (CodeBERT), Structural (AST), and Syntactic (Token) similarity scores and outputs numerical features (`gptclonebench_features.csv`). |
| **`train_model.py`** | **Stage 3: Model Training** | Trains the neural **Gating Network**, learns optimal weights for similarity experts, and saves the best model to `best_gating_model.pth`. |
| **`detect_plagiarism.py`** | **Stage 4: Inference** | Main detection engine. Loads `best_gating_model.pth`, evaluates two input source files, and predicts the plagiarism score. |
| **`batch_test.py`** | **Automation Utility** | Bulk-testing script that matches files by ID across directories and generates a consolidated evaluation report. |
| **`cross_language.zip`** | **Input Corpus** | Raw dataset containing Type-IV cross-language code clones across Java, Python, C, and C#. |
| **`code_clones.csv`** | **Intermediate Dataset** | Structured CSV file mapping equivalent algorithm implementations across languages. |
| **`gptclonebench_features.csv`** | **Training Features** | Contains normalized similarity features + metadata used to train the neural gating model. |
| **`best_gating_model.pth`** | **Model Artifact** | Saved neural network weights used for inference. |

---



This system detects plagiarism in AI-generated code across multiple programming languages using a multi-expert neural network approach.



## Pipeline Architecture

| File Name              | Pipeline Stage           | Description                                                                                                                                                              |
|------------------------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `build_dataset.py`     | Stage 1: Data Preparation | Parses raw source files (from zip archives), extracts code snippets across languages (Java, Python, C, C#), and compiles them into a structured CSV dataset.           |
| `extract_features.py`  | Stage 2: Feature Engineering | Reads the structured dataset and computes similarity scores using three experts: Semantic (CodeBERT), Structural (AST), and Syntactic (Token). Generates training features. |
| `train_model.py`       | Stage 3: Model Training   | Defines and trains the "Gating Network" (Neural Network) to learn optimal weights for combining the three expert scores. Saves model to `best_gating_model.pth`.        |
| `detect_plagiarism.py` | Stage 4: Inference        | Main entry point for detection. Loads trained model and compares two specific files to determine plagiarism with detailed confidence scores.                            |
| `batch_test.py`        | Automation               | Utility script that automates detection across entire directories. Matches files by number and runs detector on all pairs, saving results to report CSV.                |

---

## Data Files

| File Name                      | Description                                                                                           |
|--------------------------------|-------------------------------------------------------------------------------------------------------|
| `cross_language.zip`           | Raw source data containing the original code clone examples.                                          |
| `code_clones.csv`              | Cleaned, intermediate dataset containing code pairs sorted by problem ID.                             |
| `gptclonebench_features.csv`   | Numerical feature vectors used for training the neural network (contains scores, not raw code).       |
| `best_gating_model.pth`        | Saved binary file containing the trained weights of the Gating Network.                               |

---

## Detailed File Documentation

### STAGE 1: Data Preparation

#### `build_dataset.py`

**Purpose:** Converts raw multi-language code files into structured dataset

**Input Files:**
- `cross_language.zip` - Contains Java files with embedded Python, C, and C# implementations

**Output Files:**
- `code_clones.csv` - Structured dataset where each row contains the same algorithm implemented in 4 languages

**What it does:**
- Extracts code snippets from specially formatted Java files
- Organizes them into rows where each row = one algorithm in 4 languages (Java, Python, C, C#)

**Sample Output (`code_clones.csv`):**
```
filename       | java          | python          | c             | csharp
Example1.java  | <java_code>   | <python_code>   | <c_code>      | <csharp_code>
```

---

### STAGE 2: Feature Extraction

#### `extract_features.py`

**Purpose:** Calculates similarity scores between code pairs

**Input Files:**
- `code_clones.csv` - The structured dataset from Stage 1

**Output Files:**
- `gptclonebench_features.csv` - Contains similarity scores and labels for training

**What it does:**
- Creates code pairs (both matching and non-matching algorithms)
- Calculates three different similarity scores for each pair:
  - Semantic similarity (meaning-based)
  - Structural similarity (code structure)
  - Syntactic similarity (text-based)
- Adds contextual information (language differences, score disagreements)
- Labels each pair as plagiarism (1) or not plagiarism (0)

**Sample Output (`gptclonebench_features.csv`):**
```
S_CodeBERT | S_AST | S_Token | D_lang | S_CodeBERT_minus_S_AST | one_minus_S_AST | label
0.980      | 0.580 | 0.014   | 1.0    | 0.400                  | 0.420           | 1
0.979      | 0.582 | 0.000   | 0.0    | 0.397                  | 0.418           | 0
```

**Interpretation:**
- **Row 1:** High semantic (0.98), low token (0.01), different languages → Cross-language clone (Label 1)
- **Row 2:** High semantic (0.98), low token (0.00), same language → Refactored code (Label 0)

---

### STAGE 3: Model Training

#### `train_model.py`

**Purpose:** Trains the neural network to intelligently combine similarity scores

**Input Files:**
- `gptclonebench_features.csv` - Feature vectors with labels from Stage 2

**Output Files:**
- `best_gating_model.pth` - Trained neural network model

**What it does:**
- Splits data into training, validation, and test sets (70% / 15% / 15%)
- Trains a neural network to predict optimal weights for the three similarity scores
- Learns when to trust which similarity method based on the scenario
- Saves the best performing model

**Sample Training Output:**
```
Training Statistics:
  Total pairs: 10,608
  Train: 7,426 pairs
  Validation: 1,591 pairs
  Test: 1,591 pairs

Best Model Performance:
  Best Validation F1: 0.8157 (epoch 3)
  Test F1: 0.8107 (after calibration)
  Optimal Threshold: 0.5000
```

---

### STAGE 4: Plagiarism Detection

#### `detect_plagiarism.py`

**Purpose:** Analyzes two code files and determines if plagiarism exists

**Input Files:**
- `best_gating_model.pth` - The trained model from Stage 3
- Two code files provided by user (e.g., `student_A.java`, `student_B.py`)

**Output:**
- Console output showing similarity scores, weights, and final decision

**What it does:**
- Loads the trained neural network model
- Calculates three similarity scores for the input code pair
- Uses the trained model to determine optimal weights for each score
- Computes final weighted similarity score
- Applies adaptive threshold based on code complexity
- Reports whether plagiarism is detected with confidence level

**Sample Detection Output:**
```
Loading trained model...
Loaded model with Val F1: 0.8157

Computing semantic similarity...
S_CodeBERT = 0.947

Computing structural similarity...
S_AST = 0.185

Computing syntactic similarity...
S_Token = 0.042

Gating Weights:
  w_CodeBERT = 0.995
  w_AST      = 0.003
  w_Token    = 0.002

Code Complexity: 0.650
Adaptive Threshold: 0.520

================================================================================
FINAL RESULTS
================================================================================
Semantic Similarity:    0.947
Structural Similarity:  0.185
Syntactic Similarity:   0.042
Language Dissimilarity: 1.000
Gating Weights:         0.995 / 0.003 / 0.002
Final Score:            0.942
Threshold:              0.520
Confidence Margin:      +0.422
Prediction:             PLAGIARISM
================================================================================
```

**Interpretation:**
- High semantic score (0.947) but low structural/syntactic scores
- Different languages detected (1.000)
- Network assigns 99.5% weight to semantic similarity
- Final score (0.942) exceeds threshold (0.520)
- **Result:** Plagiarism detected with high confidence (+0.422)

---

### AUTOMATION

#### `batch_test.py`

**Purpose:** Automates plagiarism detection across multiple file pairs

**Input Files:**
- `best_gating_model.pth` - The trained model
- Multiple code file pairs for testing

**Output:**
- Batch results for all tested pairs

**What it does:**
- Runs plagiarism detection on multiple code pairs automatically
- Used for evaluation and benchmarking the system

**Sample Batch Output:**
```
Batch Testing Results:
======================
Pair 1: student_A.java vs student_B.py → PLAGIARISM (Score: 0.942)
Pair 2: student_C.cpp vs student_D.cs → NOT PLAGIARISM (Score: 0.385)
Pair 3: student_E.java vs student_F.java → PLAGIARISM (Score: 0.873)

Summary:
  Total pairs tested: 3
  Plagiarism detected: 2
  No plagiarism: 1
```

---

## GPTCloneBench (Original Dataset Source)

GPTCloneBench Repository:  
https://github.com/srlabUsask/GPTCloneBench

This is the official benchmark used for generating **semantic** and **cross-language** code clones.  
Our project uses the **cross-language clone dataset** provided in the repository.

### 🔹 For Cross-language clones, use these two files from the original repo:
- `cross_language.zip`  
- `cross_language_part_2.zip`  

These contain the raw multilingual Type-IV code clones used by GPTCloneBench.  
They are provided as **stand-alone clones (not system-injected)**.

GPTCloneBench is based on:
- SemanticCloneBench  
- GPT-based clone generation  
- Research published at *ICSME 2023* & *IWSC 2023*



