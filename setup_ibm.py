"""
IBM Quantum Account Setup - Qiskit 1.0+ Compatible
Updated for new authentication system
"""

from qiskit_ibm_runtime import QiskitRuntimeService

def setup_ibm_quantum():
    """Setup IBM Quantum account with API token (Qiskit 1.0+ version)"""
    
    # TODO: Replace with your actual API token from IBM Quantum dashboard
    # Get your token from: https://quantum.cloud.ibm.com
    API_TOKEN = "iIvBPKAe3g5poTSkoWPlT3o6arUi8GeVHgD4ZsucxAGA"
    
    try:
        # Save account credentials (new method for Qiskit 1.0+)
        QiskitRuntimeService.save_account(
            token=API_TOKEN,
            overwrite=True
        )
        print("✅ SUCCESS: IBM Quantum account saved!")
        
        # Test the connection
        service = QiskitRuntimeService()
        backends = service.backends('ibm_brisbane')
        
        print(f"✅ Connected successfully!")
        print(f"📡 Available quantum backends: {len(backends)} devices")
        print(f"🖥️  Example backends: {[backend.name for backend in backends[:3]]}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("💡 Make sure you:")
        print("   1. Created free IBM Quantum account")
        print("   2. Copied the correct API token")
        print("   3. Have internet connection")
        return False

if __name__ == "__main__":
    print("🚀 Setting up IBM Quantum Access (Qiskit 1.0+)...")
    print("=" * 50)
    setup_ibm_quantum()
