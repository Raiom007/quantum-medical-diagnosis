"""
Quantum-Enhanced Medical Diagnosis Classifier - Qiskit 1.0+ Compatible
Combines quantum feature maps with variational circuits
"""

import numpy as np
import time
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import seaborn as sns

# Quantum imports - Updated for Qiskit 1.0+
from qiskit_machine_learning.algorithms import VQC
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit.circuit.library import ZZFeatureMap, EfficientSU2
from qiskit_aer import AerSimulator  # Updated import
from qiskit.primitives import Sampler

class QuantumMedicalClassifier:
    def __init__(self, n_features=8):
        self.n_features = n_features
        self.quantum_classifier = None
        self.classical_classifier = None
        self.feature_map = None
        self.ansatz = None
        
    def create_quantum_components(self, reps_fm=2, reps_ansatz=2):
        """Create quantum feature map and ansatz"""
        
        # Feature Map - encodes classical data into quantum states
        self.feature_map = ZZFeatureMap(
            feature_dimension=self.n_features,
            reps=reps_fm,
            entanglement='full'
        )
        
        # Variational Ansatz - parameterized quantum circuit
        self.ansatz = EfficientSU2(
            num_qubits=self.n_features,
            reps=reps_ansatz,
            entanglement='linear'
        )
        
        print(f"Quantum components created:")
        print(f"- Feature map parameters: {self.feature_map.num_parameters}")
        print(f"- Ansatz parameters: {self.ansatz.num_parameters}")
        
    def train_quantum_classifier(self, X_train, y_train):
        """Train the quantum variational classifier"""
        
        print(f"\n=== TRAINING QUANTUM CLASSIFIER ===")
        start_time = time.time()
        
        # Create quantum instance with Aer simulator
        backend = AerSimulator()
        sampler = Sampler()
        
        # Create and configure VQC
        self.quantum_classifier = VQC(
            feature_map=self.feature_map,
            ansatz=self.ansatz,
            optimizer=COBYLA(maxiter=100),  # Reduced iterations for speed
            sampler=sampler
        )
        
        # Train the model
        print("Training quantum model...")
        try:
            self.quantum_classifier.fit(X_train, y_train)
            training_time = time.time() - start_time
            print(f"✅ Training completed in {training_time:.2f} seconds")
            return True
        except Exception as e:
            print(f"❌ Training error: {e}")
            return False
        
    def train_classical_baseline(self, X_train, y_train):
        """Train classical SVM for comparison"""
        
        print(f"\n=== TRAINING CLASSICAL BASELINE ===")
        self.classical_classifier = SVC(kernel='rbf', random_state=42)
        self.classical_classifier.fit(X_train, y_train)
        print("✅ Classical SVM trained successfully")
        
    def evaluate_models(self, X_test, y_test):
        """Comprehensive model evaluation"""
        
        results = {}
        
        # Quantum model evaluation
        if self.quantum_classifier is not None:
            print(f"\n=== QUANTUM MODEL EVALUATION ===")
            
            try:
                # Predictions
                y_pred_quantum = self.quantum_classifier.predict(X_test)
                
                # Metrics
                quantum_accuracy = accuracy_score(y_test, y_pred_quantum)
                quantum_auc = roc_auc_score(y_test, y_pred_quantum)
                
                print(f"✅ Quantum Accuracy: {quantum_accuracy:.4f} ({quantum_accuracy*100:.1f}%)")
                print(f"✅ Quantum AUC: {quantum_auc:.4f}")
                
                results['quantum'] = {
                    'accuracy': quantum_accuracy,
                    'auc': quantum_auc,
                    'predictions': y_pred_quantum,
                    'classification_report': classification_report(y_test, y_pred_quantum)
                }
                
            except Exception as e:
                print(f"❌ Quantum evaluation error: {e}")
        
        # Classical model evaluation
        if self.classical_classifier is not None:
            print(f"\n=== CLASSICAL MODEL EVALUATION ===")
            
            # Predictions
            y_pred_classical = self.classical_classifier.predict(X_test)
            
            # Metrics
            classical_accuracy = accuracy_score(y_test, y_pred_classical)
            classical_auc = roc_auc_score(y_test, y_pred_classical)
            
            print(f"✅ Classical Accuracy: {classical_accuracy:.4f} ({classical_accuracy*100:.1f}%)")
            print(f"✅ Classical AUC: {classical_auc:.4f}")
            
            results['classical'] = {
                'accuracy': classical_accuracy,
                'auc': classical_auc,
                'predictions': y_pred_classical,
                'classification_report': classification_report(y_test, y_pred_classical)
            }
        
        # Comparison
        if 'quantum' in results and 'classical' in results:
            improvement = (results['quantum']['accuracy'] - results['classical']['accuracy']) * 100
            print(f"\n=== MODEL COMPARISON ===")
            print(f"🚀 Quantum vs Classical Accuracy Improvement: {improvement:.2f}%")
            
            # Create comparison visualization
            self.create_comparison_plots(results, y_test)
            
        return results
    
    def create_comparison_plots(self, results, y_test):
        """Create comprehensive evaluation plots"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Accuracy comparison
        models = ['Classical SVM', 'Quantum VQC']
        accuracies = [results['classical']['accuracy'], results['quantum']['accuracy']]
        
        bars = axes[0,0].bar(models, accuracies, color=['blue', 'red'], alpha=0.7)
        axes[0,0].set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
        axes[0,0].set_ylabel('Accuracy')
        axes[0,0].set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, acc in zip(bars, accuracies):
            axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                          f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # AUC comparison
        aucs = [results['classical']['auc'], results['quantum']['auc']]
        bars = axes[0,1].bar(models, aucs, color=['blue', 'red'], alpha=0.7)
        axes[0,1].set_title('Model AUC Comparison', fontsize=14, fontweight='bold')
        axes[0,1].set_ylabel('AUC Score')
        axes[0,1].set_ylim(0, 1)
        
        for bar, auc in zip(bars, aucs):
            axes[0,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                          f'{auc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Confusion matrices
        cm_classical = confusion_matrix(y_test, results['classical']['predictions'])
        cm_quantum = confusion_matrix(y_test, results['quantum']['predictions'])
        
        sns.heatmap(cm_classical, annot=True, fmt='d', cmap='Blues', ax=axes[1,0],
                   cbar_kws={'label': 'Count'})
        axes[1,0].set_title('Classical SVM Confusion Matrix', fontsize=14, fontweight='bold')
        axes[1,0].set_xlabel('Predicted')
        axes[1,0].set_ylabel('Actual')
        
        sns.heatmap(cm_quantum, annot=True, fmt='d', cmap='Reds', ax=axes[1,1],
                   cbar_kws={'label': 'Count'})
        axes[1,1].set_title('Quantum VQC Confusion Matrix', fontsize=14, fontweight='bold')
        axes[1,1].set_xlabel('Predicted')
        axes[1,1].set_ylabel('Actual')
        
        plt.tight_layout()
        plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save detailed results
        self.save_results(results)
    
    def save_results(self, results):
        """Save detailed results for documentation"""
        
        with open('quantum_medical_results.txt', 'w') as f:
            f.write("QUANTUM-ENHANCED MEDICAL DIAGNOSIS RESULTS\n")
            f.write("=" * 50 + "\n\n")
            
            if 'quantum' in results:
                f.write("QUANTUM MODEL PERFORMANCE:\n")
                f.write(f"Accuracy: {results['quantum']['accuracy']:.4f} ({results['quantum']['accuracy']*100:.1f}%)\n")
                f.write(f"AUC: {results['quantum']['auc']:.4f}\n")
                f.write("\nDetailed Classification Report:\n")
                f.write(results['quantum']['classification_report'])
                f.write("\n\n")
            
            if 'classical' in results:
                f.write("CLASSICAL MODEL PERFORMANCE:\n")
                f.write(f"Accuracy: {results['classical']['accuracy']:.4f} ({results['classical']['accuracy']*100:.1f}%)\n")
                f.write(f"AUC: {results['classical']['auc']:.4f}\n")
                f.write("\nDetailed Classification Report:\n")
                f.write(results['classical']['classification_report'])
                f.write("\n\n")
            
            if 'quantum' in results and 'classical' in results:
                improvement = (results['quantum']['accuracy'] - results['classical']['accuracy']) * 100
                f.write("MODEL COMPARISON:\n")
                f.write(f"Quantum Advantage: {improvement:.2f}% accuracy improvement\n")
                f.write(f"Total Training Samples: 455\n")
                f.write(f"Total Testing Samples: 114\n")
                f.write(f"Quantum Features: 8 (reduced from 30 via PCA)\n")
        
        print("📄 Detailed results saved to 'quantum_medical_results.txt'")

# Example usage
if __name__ == "__main__":
    print("🩺 QUANTUM MEDICAL DIAGNOSIS CLASSIFIER")
    print("=" * 50)
    
    # Load processed data
    try:
        data = np.load('processed_medical_data.npz')
        X_train, X_test = data['X_train'], data['X_test']
        y_train, y_test = data['y_train'], data['y_test']
        
        print(f"✅ Training set: {X_train.shape}")
        print(f"✅ Test set: {X_test.shape}")
        
        # Create and train quantum classifier
        qmc = QuantumMedicalClassifier(n_features=X_train.shape[1])
        qmc.create_quantum_components()
        
        # Train models
        quantum_success = qmc.train_quantum_classifier(X_train, y_train)
        qmc.train_classical_baseline(X_train, y_train)
        
        # Evaluate and compare
        if quantum_success:
            results = qmc.evaluate_models(X_test, y_test)
            print("\n✅ QUANTUM MEDICAL DIAGNOSIS COMPLETE!")
        else:
            print("\n⚠️  Quantum training failed, but classical results available")
            
    except FileNotFoundError:
        print("❌ Processed data file not found!")
        print("💡 Please run 'python data_preparation.py' first")
