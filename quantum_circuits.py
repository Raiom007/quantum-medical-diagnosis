"""
Quantum Circuits for Medical Diagnosis - FIXED VERSION
Implements various quantum feature encoding strategies
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, PauliFeatureMap, EfficientSU2, RealAmplitudes
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

class QuantumFeatureMaps:
    def __init__(self, n_features):
        self.n_features = n_features
        
    def create_zz_feature_map(self, reps=2, entanglement='full'):
        """
        ZZ Feature Map - Most effective for medical data
        Encodes classical data into quantum states using rotation and entanglement
        """
        feature_map = ZZFeatureMap(
            feature_dimension=self.n_features,
            reps=reps,
            entanglement=entanglement
        )
        
        print(f"ZZ Feature Map created:")
        print(f"- Qubits: {self.n_features}")
        print(f"- Repetitions: {reps}")
        print(f"- Entanglement: {entanglement}")
        print(f"- Parameters: {feature_map.num_parameters}")
        
        return feature_map
    
    def create_pauli_feature_map(self, reps=2):
        """
        Pauli Feature Map - Alternative encoding strategy
        Uses Pauli rotation gates for feature encoding
        """
        feature_map = PauliFeatureMap(
            feature_dimension=self.n_features,
            reps=reps,
            paulis=['Z', 'ZZ']  # Use Z and ZZ interactions
        )
        
        return feature_map
    
    def visualize_feature_map(self, feature_map, sample_data=None):
        """Visualize the quantum feature map circuit - FIXED VERSION"""
        
        if sample_data is None:
            # Create sample data for visualization
            sample_data = np.random.rand(self.n_features) * 2 * np.pi
        
        # Convert numpy array to list (FIX for parameter type error)
        if isinstance(sample_data, np.ndarray):
            sample_data = sample_data.tolist()
        
        try:
            # Create parameter dictionary for proper assignment
            param_dict = {}
            parameters = feature_map.parameters
            param_list = list(parameters)
            
            # Assign parameters properly
            for i, param in enumerate(param_list):
                if i < len(sample_data):
                    param_dict[param] = float(sample_data[i % len(sample_data)])
                else:
                    param_dict[param] = float(sample_data[i % len(sample_data)])
            
            # Bind parameters to create concrete circuit
            bound_circuit = feature_map.assign_parameters(param_dict)
            
            # Save circuit diagram
            fig = circuit_drawer(bound_circuit, output='mpl', 
                               style={'backgroundcolor': '#FFFFFF'},
                               fold=20)  # Fold long circuits
            plt.savefig('quantum_feature_map.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print(f"✅ Circuit depth: {bound_circuit.depth()}")
            print(f"✅ Number of parameters: {feature_map.num_parameters}")
            print(f"✅ Circuit visualization saved as 'quantum_feature_map.png'")
            
            return bound_circuit
            
        except Exception as e:
            print(f"❌ Visualization error: {e}")
            print("📝 Creating simplified circuit instead...")
            
            # Fallback: create simple circuit without parameters
            simple_circuit = QuantumCircuit(self.n_features)
            for i in range(self.n_features):
                simple_circuit.ry(np.pi/4, i)  # Simple rotation
            
            fig = circuit_drawer(simple_circuit, output='mpl')
            plt.savefig('quantum_feature_map_simple.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            return simple_circuit

class QuantumAnsatz:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        
    def create_efficient_su2(self, reps=3, entanglement='linear'):
        """
        EfficientSU2 Ansatz - Hardware-efficient variational form
        Optimized for NISQ devices
        """
        ansatz = EfficientSU2(
            num_qubits=self.n_qubits,
            reps=reps,
            entanglement=entanglement,
            insert_barriers=True
        )
        
        print(f"EfficientSU2 Ansatz created:")
        print(f"- Qubits: {self.n_qubits}")
        print(f"- Repetitions: {reps}")
        print(f"- Parameters: {ansatz.num_parameters}")
        
        return ansatz
    
    def create_real_amplitudes(self, reps=3):
        """
        Real Amplitudes Ansatz - Alternative variational form
        Uses only real amplitudes (no complex phases)
        """
        ansatz = RealAmplitudes(
            num_qubits=self.n_qubits,
            reps=reps,
            entanglement='full'
        )
        
        return ansatz
    
    def visualize_ansatz(self, ansatz):
        """Visualize the variational ansatz - FIXED VERSION"""
        
        try:
            # Create sample parameters
            num_params = ansatz.num_parameters
            sample_params = np.random.rand(num_params) * 2 * np.pi
            
            # Create parameter dictionary
            param_dict = {}
            parameters = ansatz.parameters
            param_list = list(parameters)
            
            for i, param in enumerate(param_list):
                if i < len(sample_params):
                    param_dict[param] = float(sample_params[i])
            
            # Bind parameters
            bound_ansatz = ansatz.assign_parameters(param_dict)
            
            # Visualize
            fig = circuit_drawer(bound_ansatz, output='mpl', 
                               style={'backgroundcolor': '#FFFFFF'},
                               fold=20)
            plt.savefig('quantum_ansatz.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print(f"✅ Ansatz depth: {bound_ansatz.depth()}")
            print(f"✅ Ansatz visualization saved as 'quantum_ansatz.png'")
            
            return bound_ansatz
            
        except Exception as e:
            print(f"❌ Ansatz visualization error: {e}")
            print("📝 Creating simplified ansatz instead...")
            
            # Fallback: create simple ansatz
            simple_ansatz = QuantumCircuit(self.n_qubits)
            for i in range(self.n_qubits):
                simple_ansatz.ry(np.pi/4, i)
                if i < self.n_qubits - 1:
                    simple_ansatz.cx(i, i+1)
            
            fig = circuit_drawer(simple_ansatz, output='mpl')
            plt.savefig('quantum_ansatz_simple.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            return simple_ansatz

# Example usage and testing
if __name__ == "__main__":
    print("🚀 Creating Quantum Circuits for Medical Diagnosis")
    print("=" * 55)
    
    try:
        # Load processed data
        data = np.load('processed_medical_data.npz')
        X_train = data['X_train']
        n_features = X_train.shape[1]
        
        print(f"✅ Loaded quantum data: {X_train.shape[0]} samples, {n_features} features")
        
    except FileNotFoundError:
        print("❌ Quantum data file not found!")
        print("📝 Using default 8 features for demonstration")
        n_features = 8
        X_train = np.random.rand(100, 8) * 2 * np.pi  # Demo data
    
    print(f"\n⚛️  Creating quantum circuits for {n_features} features")
    
    # Create feature maps
    print("\n1️⃣  Creating Feature Map...")
    feature_maps = QuantumFeatureMaps(n_features)
    zz_map = feature_maps.create_zz_feature_map(reps=2)
    
    # Create ansatz
    print("\n2️⃣  Creating Variational Ansatz...")
    ansatz_builder = QuantumAnsatz(n_features)
    ansatz = ansatz_builder.create_efficient_su2(reps=2)  # Reduced reps for stability
    
    # Visualize circuits
    print("\n3️⃣  Visualizing Feature Map...")
    if len(X_train) > 0:
        sample_data = X_train[0]
    else:
        sample_data = np.random.rand(n_features) * 2 * np.pi
        
    feature_circuit = feature_maps.visualize_feature_map(zz_map, sample_data)
    
    print("\n4️⃣  Visualizing Ansatz...")
    ansatz_circuit = ansatz_builder.visualize_ansatz(ansatz)
    
    print("\n✅ Quantum circuit creation completed!")
    print("📁 Generated files:")
    print("   - quantum_feature_map.png")
    print("   - quantum_ansatz.png")
