import os
import random
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

def generate_disease_dataset(base_path="data/disease", num_samples_per_class=50):
    """
    Generates synthetic leaf images for three classes:
    - Tomato___healthy: green background leaf.
    - Tomato___Early_blight: green leaf with small concentric yellow/brown circles.
    - Tomato___Late_blight: green leaf with large dark brown/black blotches.
    """
    classes = ["Tomato___healthy", "Tomato___Early_blight", "Tomato___Late_blight"]
    splits = {"train": 0.7, "val": 0.15, "test": 0.15}
    
    for split, ratio in splits.items():
        split_num = int(num_samples_per_class * ratio)
        for cls in classes:
            class_dir = os.path.join(base_path, split, cls)
            os.makedirs(class_dir, exist_ok=True)
            
            for i in range(split_num):
                # Create a blank image representing a leaf region
                img = Image.new("RGB", (224, 224), (240, 240, 240))  # light background
                draw = ImageDraw.Draw(img)
                
                # Draw leaf base (green ellipse)
                draw.ellipse([30, 40, 190, 180], fill=(34, 139, 34))  # Forest Green
                
                # Add class specific details
                if cls == "Tomato___Early_blight":
                    # Early blight has small yellow/brown spots
                    for _ in range(5):
                        cx = random.randint(60, 160)
                        cy = random.randint(60, 160)
                        r = random.randint(4, 10)
                        # Draw concentric rings
                        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(139, 90, 0)) # Brownish
                        draw.ellipse([cx-r+2, cy-r+2, cx+r-2, cy+r-2], fill=(218, 165, 32)) # Goldenrod
                elif cls == "Tomato___Late_blight":
                    # Late blight has large dark brown/black patches
                    for _ in range(2):
                        cx = random.randint(60, 160)
                        cy = random.randint(60, 160)
                        r = random.randint(15, 25)
                        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(47, 79, 79)) # Dark Slate Gray/Blackish
                        
                # Add some healthy leaf veins (always present)
                draw.line([110, 40, 110, 180], fill=(0, 100, 0), width=2)
                draw.line([110, 80, 70, 60], fill=(0, 100, 0), width=1)
                draw.line([110, 80, 150, 60], fill=(0, 100, 0), width=1)
                draw.line([110, 120, 60, 100], fill=(0, 100, 0), width=1)
                draw.line([110, 120, 160, 100], fill=(0, 100, 0), width=1)
                
                # Save image
                img_path = os.path.join(class_dir, f"{cls}_{split}_{i}.png")
                img.save(img_path)

def generate_crop_dataset(base_path="data/crop", num_samples=1000):
    """
    Generates synthetic tabular crop recommendation dataset mimicking Kaggle dataset.
    Features: N, P, K, temperature, humidity, ph, rainfall.
    Crops: Rice, Maize, Chickpea, Cotton, Mango, Banana, Grapes.
    """
    os.makedirs(base_path, exist_ok=True)
    
    crops = ["Rice", "Maize", "Chickpea", "Cotton", "Mango", "Banana", "Grapes"]
    data = []
    
    for i in range(num_samples):
        crop = random.choice(crops)
        if crop == "Rice":
            n = random.uniform(60, 100)
            p = random.uniform(35, 60)
            k = random.uniform(35, 45)
            temp = random.uniform(20, 30)
            hum = random.uniform(80, 95)
            ph = random.uniform(5.5, 7.0)
            rain = random.uniform(150, 300)
        elif crop == "Maize":
            n = random.uniform(60, 90)
            p = random.uniform(35, 55)
            k = random.uniform(15, 25)
            temp = random.uniform(18, 32)
            hum = random.uniform(55, 75)
            ph = random.uniform(5.5, 7.0)
            rain = random.uniform(60, 110)
        elif crop == "Chickpea":
            n = random.uniform(20, 50)
            p = random.uniform(55, 80)
            k = random.uniform(75, 85)
            temp = random.uniform(15, 25)
            hum = random.uniform(15, 30)
            ph = random.uniform(6.0, 8.5)
            rain = random.uniform(60, 90)
        elif crop == "Cotton":
            n = random.uniform(70, 100)
            p = random.uniform(35, 55)
            k = random.uniform(15, 25)
            temp = random.uniform(25, 35)
            hum = random.uniform(70, 85)
            ph = random.uniform(5.8, 7.5)
            rain = random.uniform(60, 95)
        elif crop == "Mango":
            n = random.uniform(20, 40)
            p = random.uniform(20, 40)
            k = random.uniform(20, 40)
            temp = random.uniform(27, 38)
            hum = random.uniform(45, 60)
            ph = random.uniform(4.5, 7.0)
            rain = random.uniform(90, 130)
        elif crop == "Banana":
            n = random.uniform(80, 120)
            p = random.uniform(70, 90)
            k = random.uniform(115, 145)
            temp = random.uniform(25, 30)
            hum = random.uniform(75, 85)
            ph = random.uniform(5.5, 6.5)
            rain = random.uniform(150, 250)
        elif crop == "Grapes":
            n = random.uniform(20, 40)
            p = random.uniform(120, 145)
            k = random.uniform(180, 205)
            temp = random.uniform(15, 28)
            hum = random.uniform(80, 85)
            ph = random.uniform(5.5, 6.5)
            rain = random.uniform(65, 80)
            
        data.append({
            "nitrogen": n,
            "phosphorus": p,
            "potassium": k,
            "temperature": temp,
            "humidity": hum,
            "ph": ph,
            "rainfall": rain,
            "crop": crop
        })
        
    df = pd.DataFrame(data)
    
    # Shuffle and split
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    n_train = int(len(df) * 0.7)
    n_val = int(len(df) * 0.15)
    
    train_df = df.iloc[:n_train]
    val_df = df.iloc[n_train:n_train+n_val]
    test_df = df.iloc[n_train+n_val:]
    
    train_df.to_csv(os.path.join(base_path, "train.csv"), index=False)
    val_df.to_csv(os.path.join(base_path, "val.csv"), index=False)
    test_df.to_csv(os.path.join(base_path, "test.csv"), index=False)

def generate_yield_dataset(base_path="data/yield", num_samples=1000):
    """
    Generates synthetic crop yield dataset.
    Features: crop (categorical), season (categorical), rainfall (numeric), temperature (numeric), area (numeric).
    Target: yield (numeric).
    """
    os.makedirs(base_path, exist_ok=True)
    
    crops = ["Rice", "Maize", "Chickpea", "Cotton", "Mango", "Banana", "Grapes"]
    seasons = ["Kharif", "Rabi", "Summer", "Whole Year"]
    
    data = []
    
    for _ in range(num_samples):
        crop = random.choice(crops)
        season = random.choice(seasons)
        
        # Ranges
        rain = random.uniform(400, 2500)
        temp = random.uniform(15, 38)
        area = random.uniform(0.5, 10.0)
        
        # Base yields by crop
        base_yields = {
            "Rice": 3.5,
            "Maize": 2.8,
            "Chickpea": 1.5,
            "Cotton": 2.0,
            "Mango": 4.5,
            "Banana": 8.0,
            "Grapes": 9.0
        }
        
        # Base factor based on environment
        rain_factor = 0.5 * np.sin((rain - 1000) / 1000)
        temp_factor = -0.05 * (temp - 25) ** 2 / 10.0
        
        # Yield formula (tonnes/hectare)
        y = base_yields[crop] + rain_factor + temp_factor + random.uniform(-0.5, 0.5)
        # Yield must be positive
        y = max(0.5, y)
        
        # Let's ensure the label is actual yield (tonnes/hectare). We will predict yield_per_area.
        data.append({
            "crop": crop,
            "season": season,
            "rainfall": rain,
            "temperature": temp,
            "area": area,
            "yield": y
        })
        
    df = pd.DataFrame(data)
    
    # Shuffle and split
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    n_train = int(len(df) * 0.7)
    n_val = int(len(df) * 0.15)
    
    train_df = df.iloc[:n_train]
    val_df = df.iloc[n_train:n_train+n_val]
    test_df = df.iloc[n_train+n_val:]
    
    train_df.to_csv(os.path.join(base_path, "train.csv"), index=False)
    val_df.to_csv(os.path.join(base_path, "val.csv"), index=False)
    test_df.to_csv(os.path.join(base_path, "test.csv"), index=False)

if __name__ == "__main__":
    print("Generating disease dataset...")
    generate_disease_dataset()
    print("Generating crop recommendation dataset...")
    generate_crop_dataset()
    print("Generating yield prediction dataset...")
    generate_yield_dataset()
    print("All datasets generated successfully!")
