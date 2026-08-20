import os
import json
import time
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

def calculate_ece(probs, labels, n_bins=10):
    """
    Calculates the Expected Calibration Error (ECE).
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == labels)
    
    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        
        # Find samples in this bin
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)
        
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += prop_in_bin * np.abs(avg_confidence_in_bin - accuracy_in_bin)
            
    return float(ece)

def train_model(data_dir="data/disease", artifact_dir="artifacts/disease", epochs=5, batch_size=16):
    os.makedirs(artifact_dir, exist_ok=True)
    
    # Image transforms
    data_transforms = {
        "train": transforms.Compose([
            transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        "val": transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        "test": transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }
    
    # Datasets and Loaders
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
                      for x in ["train", "val", "test"]}
    
    dataloaders = {x: DataLoader(image_datasets[x], batch_size=batch_size, shuffle=(x == "train"), num_workers=0)
                   for x in ["train", "val", "test"]}
    
    class_names = image_datasets["train"].classes
    class_mapping = {i: name for i, name in enumerate(class_names)}
    
    # Save class mapping
    with open(os.path.join(artifact_dir, "class_mapping.json"), "w") as f:
        json.dump(class_mapping, f, indent=4)
        
    # Preprocessing params
    preprocessing_config = {
        "image_size": 224,
        "mean": [0.485, 0.456, 0.406],
        "std": [0.229, 0.224, 0.225]
    }
    with open(os.path.join(artifact_dir, "preprocessing.json"), "w") as f:
        json.dump(preprocessing_config, f, indent=4)
        
    # Model definition
    # Using lightweight MobileNetV3 small
    model = models.mobilenet_v3_small(weights=None)
    # Modify classifier layer for 3 classes
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(in_features, len(class_names))
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training Loop
    print(f"Training started on device: {device}...")
    start_time = time.time()
    
    for epoch in range(epochs):
        print(f"Epoch {epoch+1}/{epochs}")
        print("-" * 10)
        
        for phase in ["train", "val"]:
            if phase == "train":
                model.train()
            else:
                model.eval()
                
            running_loss = 0.0
            running_corrects = 0
            
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                optimizer.zero_grad()
                
                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)
                    
                    if phase == "train":
                        loss.backward()
                        optimizer.step()
                        
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
                
            epoch_loss = running_loss / len(image_datasets[phase])
            epoch_acc = running_corrects.double() / len(image_datasets[phase])
            
            print(f"{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
            
    training_duration = time.time() - start_time
    print(f"Training complete in {training_duration:.2f}s")
    
    # Save Model Weights
    torch.save(model.state_dict(), os.path.join(artifact_dir, "model.pt"))
    print("Model saved to artifacts/disease/model.pt")
    
    # Evaluation on test set
    model.eval()
    all_preds = []
    all_labels = []
    all_probs = []
    
    with torch.no_grad():
        for inputs, labels in dataloaders["test"]:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    all_probs = np.array(all_probs)
    
    # Calculate evaluation metrics
    test_acc = np.mean(all_preds == all_labels)
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average="macro", zero_division=0)
    conf_mat = confusion_matrix(all_labels, all_preds).tolist()
    ece = calculate_ece(all_probs, all_labels)
    
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test Macro F1: {f1:.4f}")
    print(f"Test ECE (Calibration Error): {ece:.4f}")
    
    # Save metadata.json
    metadata = {
        "model_name": "mobilenet_v3_small",
        "model_version": "disease_v1",
        "dataset": "CropAI Synthetic Plant Pathology Image Dataset",
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "training_duration_seconds": round(training_duration, 2),
        "random_seed": 42,
        "metrics": {
            "test_accuracy": float(test_acc),
            "macro_precision": float(precision),
            "macro_recall": float(recall),
            "macro_f1": float(f1),
            "ece": ece
        },
        "confusion_matrix": conf_mat,
        "classes": class_names
    }
    
    with open(os.path.join(artifact_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Metadata saved to artifacts/disease/metadata.json")

if __name__ == "__main__":
    train_model()
