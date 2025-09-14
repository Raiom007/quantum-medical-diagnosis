"""
Quantum Performance Optimization
"""

import numpy as np
from quantum_classifier import QuantumMedicalClassifier

def optimize_quantum_performance():
    """Try different quantum configurations"""
    
    # Load data
    data = np.load('processed_medical_data.npz')
    X_train, X_test = data['X_train'], data['X_test']
    y_train, y_test = data['y_train'], data['y_test']
    
    print("🧪 Testing Quantum Optimization Strategies...")
    
    # Strategy 1: Fewer features (4 instead of 8)
    print("\n1️⃣ Testing with 4 features...")
    X_train_4 = X_train[:, :4]
    X_test_4 = X_test[:, :4]
    
    qmc1 = QuantumMedicalClassifier(n_features=4)
    qmc1.create_quantum_components(reps_fm=1, reps_ansatz=1)
    
    if qmc1.train_quantum_classifier(X_train_4, y_train):
        y_pred = qmc1.quantum_classifier.predict(X_test_4)
        accuracy = np.mean(y_pred == y_test)
        print(f"✅ 4-feature accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    
    # Strategy 2: Different optimizer
    print("\n2️⃣ Testing with SPSA optimizer...")
    from qiskit_algorithms.optimizers import SPSA
    
    qmc2 = QuantumMedicalClassifier(n_features=6)
    qmc2.create_quantum_components(reps_fm=1, reps_ansatz=1)
    
    # Manually set SPSA optimizer
    from qiskit_machine_learning.algorithms import VQC
    from qiskit.primitives import Sampler
    
    qmc2.quantum_classifier = VQC(
        feature_map=qmc2.feature_map,
        ansatz=qmc2.ansatz,
        optimizer=SPSA(maxiter=50),
        sampler=Sampler()
    )
    
    X_train_6 = X_train[:, :6]
    X_test_6 = X_test[:, :6]
    
    if qmc2.quantum_classifier.fit(X_train_6, y_train):
        y_pred = qmc2.quantum_classifier.predict(X_test_6)
        accuracy = np.mean(y_pred == y_test)
        print(f"✅ SPSA optimizer accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")

if __name__ == "__main__":
    optimize_quantum_performance()
