"""
Create Quantum-Ready Medical Data
Simple version to ensure data file is created
"""

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

def create_quantum_medical_data():
    """Create quantum-ready medical data file"""
    
    print("🔬 Loading medical data...")
    
    # Load data
    data = load_breast_cancer()
    X, y = data.data, data.target
    
    print(f"Original data shape: {X.shape}")
    
    # Step 1: Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Step 2: Reduce dimensions with PCA (for quantum efficiency)
    pca = PCA(n_components=8)
    X_reduced = pca.fit_transform(X_scaled)
    
    variance_retained = pca.explained_variance_ratio_.sum()
    print(f"✅ Reduced to 8 features, retained {variance_retained:.3f} variance")
    
    # Step 3: Scale for quantum encoding (0 to 2π)
    quantum_scaler = MinMaxScaler(feature_range=(0, 2*np.pi))
    X_quantum = quantum_scaler.fit_transform(X_reduced)
    
    # Step 4: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_quantum, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"✅ Training samples: {X_train.shape[0]}")
    print(f"✅ Testing samples: {X_test.shape[0]}")
    
    # Step 5: Save data
    np.savez('processed_medical_data.npz',
             X_train=X_train, X_test=X_test,
             y_train=y_train, y_test=y_test)
    
    print("✅ Quantum data saved to 'processed_medical_data.npz'")
    
    # Verify file was created
    import os
    if os.path.exists('processed_medical_data.npz'):
        file_size = os.path.getsize('processed_medical_data.npz')
        print(f"✅ File created successfully! Size: {file_size} bytes")
        return True
    else:
        print("❌ Error: File was not created")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("CREATING QUANTUM MEDICAL DATA")
    print("=" * 50)
    
    success = create_quantum_medical_data()
    
    if success:
        print("\n🎯 Ready for quantum machine learning!")
    else:
        print("\n❌ Please check for errors above")
