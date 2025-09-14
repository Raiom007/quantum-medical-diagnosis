"""
Quantum Medical Image Classification - Data Preparation
FREE Dataset: Breast Cancer Wisconsin from sklearn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

class MedicalDataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.quantum_scaler = MinMaxScaler(feature_range=(0, 2*np.pi))
        self.pca = None
        
    def load_breast_cancer_data(self):
        """
        Load FREE Breast Cancer Wisconsin Dataset
        - 569 samples
        - 30 features (tumor characteristics)
        - Binary classification: malignant(1) vs benign(0)
        """
        data = load_breast_cancer()
        X = data.data
        y = data.target
        feature_names = data.feature_names
        
        print(f"Dataset Shape: {X.shape}")
        print(f"Classes: {np.unique(y)} (0=malignant, 1=benign)")
        print(f"Class Distribution: {np.bincount(y)}")
        
        return X, y, feature_names
    
    def exploratory_data_analysis(self, X, y, feature_names):
        """Comprehensive EDA for medical data"""
        
        # Create DataFrame for easier analysis
        df = pd.DataFrame(X, columns=feature_names)
        df['diagnosis'] = y
        
        # Basic statistics
        print("\n=== DATASET STATISTICS ===")
        print(df.describe())
        
        # Visualizations
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Class distribution
        axes[0,0].bar(['Malignant', 'Benign'], np.bincount(y))
        axes[0,0].set_title('Cancer Diagnosis Distribution')
        axes[0,0].set_ylabel('Count')
        
        # Feature correlation heatmap
        correlation_matrix = df.corr()
        sns.heatmap(correlation_matrix.iloc[:10, :10], 
                   annot=True, cmap='coolwarm', ax=axes[0,1])
        axes[0,1].set_title('Feature Correlation Matrix (Top 10)')
        
        # Feature importance visualization
        important_features = ['mean radius', 'mean texture', 'mean perimeter', 
                            'mean area', 'mean smoothness']
        df[important_features].boxplot(ax=axes[1,0])
        axes[1,0].set_title('Key Feature Distributions')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # PCA visualization
        pca_temp = PCA(n_components=2)
        X_pca = pca_temp.fit_transform(self.scaler.fit_transform(X))
        
        scatter = axes[1,1].scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
        axes[1,1].set_title('PCA Visualization (2 Components)')
        axes[1,1].set_xlabel('First Principal Component')
        axes[1,1].set_ylabel('Second Principal Component')
        plt.colorbar(scatter, ax=axes[1,1])
        
        plt.tight_layout()
        plt.savefig('medical_data_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return df
    
    def prepare_quantum_data(self, X, y, n_features=8, test_size=0.2):
        """
        Prepare data for quantum processing
        - Reduce dimensionality for quantum efficiency
        - Scale features for quantum encoding
        - Split into train/test sets
        """
        
        # Step 1: Feature selection using PCA
        print(f"\n=== QUANTUM DATA PREPARATION ===")
        print(f"Original features: {X.shape[1]}")
        
        # Standardize first
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply PCA for dimensionality reduction
        self.pca = PCA(n_components=n_features)
        X_reduced = self.pca.fit_transform(X_scaled)
        
        explained_variance = self.pca.explained_variance_ratio_.sum()
        print(f"Reduced to {n_features} features")
        print(f"Retained variance: {explained_variance:.3f}")
        
        # Step 2: Quantum-specific scaling (0 to 2π)
        X_quantum = self.quantum_scaler.fit_transform(X_reduced)
        
        # Step 3: Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_quantum, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"Training samples: {X_train.shape[0]}")
        print(f"Testing samples: {X_test.shape[0]}")
        
        return X_train, X_test, y_train, y_test
    
    def save_processed_data(self, X_train, X_test, y_train, y_test):
        """Save processed data for later use"""
        np.savez('processed_medical_data.npz',
                X_train=X_train, X_test=X_test,
                y_train=y_train, y_test=y_test)
        print("Processed data saved to 'processed_medical_data.npz'")

# Example usage
if __name__ == "__main__":
    preprocessor = MedicalDataPreprocessor()
    
    # Load data
    X, y, feature_names = preprocessor.load_breast_cancer_data()
    
    # Perform EDA
    df = preprocessor.exploratory_data_analysis(X, y, feature_names)
    
    # Prepare for quantum processing
    X_train, X_test, y_train, y_test = preprocessor.prepare_quantum_data(X, y, n_features=8)
    
    # Save processed data
    preprocessor.save_processed_data(X_train, X_test, y_train, y_test)
