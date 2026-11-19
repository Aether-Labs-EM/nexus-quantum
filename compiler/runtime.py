# compiler/runtime.py

from qiskit import transpile
from qiskit.qasm3 import loads
from qiskit_aer import AerSimulator

class LocalSimulator:
    def __init__(self, qasm_code):
        self.qasm_code = qasm_code

    def run(self, shots=1000):
        try:
            # 1. טעינת קוד ה-QASM למעגל של קיסקיט
            circuit = loads(self.qasm_code)
            
            # 2. הוספת מדידות לכל הקיוביטים (כדי שנוכל לראות תוצאות 0 או 1)
            if circuit.num_clbits == 0:
                circuit.measure_all()
                
            # 3. הפעלת הסימולטור המקומי
            simulator = AerSimulator()
            compiled_circuit = transpile(circuit, simulator)
            job = simulator.run(compiled_circuit, shots=shots)
            
            # 4. שליפת התוצאות
            result = job.result()
            return result.get_counts()
            
        except Exception as e:
            return f"Error: {str(e)}"