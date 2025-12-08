# 📘 AI-Generated Code Plagiarism Detection System  
### **System File Registry & Descriptions**

Below is the detailed registry of all major files used throughout the pipeline.

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

If you want, I can also generate:
✅ Pipeline flow diagram  
✅ Folder structure diagram  
✅ Badges + logo for your README  
