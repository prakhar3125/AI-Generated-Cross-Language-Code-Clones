# gating_model.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import os
import warnings
warnings.filterwarnings("ignore")

# -------------------------------
# 1. GATING NETWORK (MLP)
# -------------------------------
class GatingNetwork(nn.Module):
    def __init__(self, input_size=6, hidden_size=16, dropout=0.3):
        super(GatingNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, 3),  # 3 experts: CodeBERT, AST, Token
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.network(x)


# -------------------------------
# 2. DATASET
# -------------------------------
class CodePairDataset(Dataset):
    def __init__(self, X_data, S_data, labels):
        self.X_data = torch.tensor(X_data, dtype=torch.float32)
        self.S_data = torch.tensor(S_data, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.X_data[idx], self.S_data[idx], self.labels[idx]


# -------------------------------
# 3. F1 SCORE HELPER
# -------------------------------
def compute_f1(preds, labels, threshold=0.5):
    preds = (preds >= threshold).float().cpu().numpy()
    labels = labels.cpu().numpy()
    return f1_score(labels, preds, average='binary', zero_division=0)


# -------------------------------
# 4. TRAINING FUNCTION
# -------------------------------
def train_model(model, train_loader, val_loader, optimizer, loss_fn, epochs=100, device='cpu', patience=10):
    model.to(device)
    best_val_f1 = 0.0
    best_model_path = 'best_gating_model.pth'
    epochs_without_improvement = 0

    print(f"Training on {device} | Epochs: {epochs} | Patience: {patience}")

    for epoch in range(epochs):
        # --- Training ---
        model.train()
        train_loss = 0.0
        for x_batch, s_batch, label_batch in train_loader:
            x_batch = x_batch.to(device)
            s_batch = s_batch.to(device)
            label_batch = label_batch.to(device)

            weights = model(x_batch)  # [B, 3]
            final_score = torch.sum(weights * s_batch, dim=1, keepdim=True)  # [B, 1]
            loss = loss_fn(final_score, label_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        avg_train_loss = train_loss / len(train_loader)

        # --- Validation ---
        model.eval()
        val_loss = 0.0
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for x_batch, s_batch, label_batch in val_loader:
                x_batch = x_batch.to(device)
                s_batch = s_batch.to(device)
                label_batch = label_batch.to(device)

                weights = model(x_batch)
                final_score = torch.sum(weights * s_batch, dim=1, keepdim=True)
                loss = loss_fn(final_score, label_batch)

                val_loss += loss.item()
                all_preds.append(final_score)
                all_labels.append(label_batch)

        avg_val_loss = val_loss / len(val_loader)
        all_preds = torch.cat(all_preds)
        all_labels = torch.cat(all_labels)
        val_f1 = compute_f1(all_preds, all_labels)

        print(f"Epoch {epoch+1:3d} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f} | Val F1: {val_f1:.4f}")

        # --- Save Best Model ---
        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            torch.save({
                'model_state_dict': model.state_dict(),
                'val_f1': best_val_f1,
                'epoch': epoch
            }, best_model_path)
            print(f"  → New best model saved! F1: {best_val_f1:.4f}")
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        # --- Early Stopping ---
        if epochs_without_improvement >= patience:
            print(f"Early stopping at epoch {epoch+1}")
            break

    print(f"\nTraining complete. Best Val F1: {best_val_f1:.4f}")
    return best_model_path


# -------------------------------
# 5. EVALUATION FUNCTION
# -------------------------------
def evaluate_model(model, test_loader, loss_fn, device='cpu'):
    model.eval()
    test_loss = 0.0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for x_batch, s_batch, label_batch in test_loader:
            x_batch = x_batch.to(device)
            s_batch = s_batch.to(device)
            label_batch = label_batch.to(device)

            weights = model(x_batch)
            final_score = torch.sum(weights * s_batch, dim=1, keepdim=True)
            loss = loss_fn(final_score, label_batch)

            test_loss += loss.item()
            all_preds.append(final_score)
            all_labels.append(label_batch)

    avg_test_loss = test_loss / len(test_loader)
    all_preds = torch.cat(all_preds)
    all_labels = torch.cat(all_labels)
    test_f1 = compute_f1(all_preds, all_labels)

    print(f"\nTest Results:")
    print(f"  Test Loss: {avg_test_loss:.4f}")
    print(f"  Test F1:   {test_f1:.4f}")

    return test_f1


# -------------------------------
# 6. MAIN EXECUTION
# -------------------------------
if __name__ == "__main__":
    # --- CONFIG ---
    CSV_PATH = 'gptclonebench_features.csv'  # ← Your generated file
    BATCH_SIZE = 64
    EPOCHS = 100
    PATIENCE = 10
    LR = 0.001
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    # --- Load Data ---
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    print(f"Loading data from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    required_cols = ['S_CodeBERT', 'S_AST', 'S_Token', 'D_lang', 'label']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing required columns. Found: {list(df.columns)}")

    # --- Feature Engineering ---
    df['S_CodeBERT_minus_S_AST'] = np.abs(df['S_CodeBERT'] - df['S_AST'])
    df['one_minus_S_AST'] = 1.0 - df['S_AST']

    # --- Define X and S ---
    X_columns = ['S_CodeBERT', 'S_AST', 'S_Token', 'D_lang',
                 'S_CodeBERT_minus_S_AST', 'one_minus_S_AST']
    S_columns = ['S_CodeBERT', 'S_AST', 'S_Token']  # Expert scores

    X_data = df[X_columns].values
    S_data = df[S_columns].values
    labels = df['label'].values

    print(f"Total samples: {len(df)}")
    print(f"Positive (label=1): {labels.sum()} | Negative (label=0): {len(labels) - labels.sum()}")

    # --- Train/Val/Test Split (70/15/15) ---
    X_train, X_temp, S_train, S_temp, y_train, y_temp = train_test_split(
        X_data, S_data, labels, test_size=0.3, random_state=42, stratify=labels
    )
    X_val, X_test, S_val, S_test, y_val, y_test = train_test_split(
        X_temp, S_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )

    print(f"Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

    # --- Datasets & Loaders ---
    train_dataset = CodePairDataset(X_train, S_train, y_train)
    val_dataset = CodePairDataset(X_val, S_val, y_val)
    test_dataset = CodePairDataset(X_test, S_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    # --- Model, Optimizer, Loss ---
    model = GatingNetwork(input_size=len(X_columns))
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-5)
    loss_fn = nn.BCELoss()

    # --- Train ---
    best_model_path = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=EPOCHS,
        device=DEVICE,
        patience=PATIENCE
    )

    # --- Load Best Model & Evaluate ---
    print(f"\nLoading best model from {best_model_path}...")
    checkpoint = torch.load(best_model_path, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])

    test_f1 = evaluate_model(model, test_loader, loss_fn, device=DEVICE)

    print(f"\nFinal Test F1 Score: {test_f1:.4f}")