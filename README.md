# nexus-quantum
A next-generation, intuitive quantum programming language and compiler.

# 🌌 Nexus Quantum Language

![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
![Status](https://img.shields.io/badge/Status-In_Development-orange.svg)
![Compiler](https://img.shields.io/badge/Compiler-Vector_1.0-success.svg)

**Nexus** is a next-generation quantum programming language designed for humans. It bridges the gap between complex quantum physics and modern, intuitive software engineering. 

Compiled by the **Vector Compiler**, Nexus translates elegant, flow-based syntax directly into hardware-ready instructions (like OpenQASM 3.0), abstracting away the boilerplate of traditional quantum programming.

## ✨ Key Features

* **Visual Data Flow (`->`)**: Stop guessing what controls what. Nexus uses intuitive arrows to dictate information flow, rotations (`90>`), and execution pipelines.
* **Quantum RAII (Automatic Uncomputation)**: Say goodbye to manual garbage entanglement. Mark a qubit as `(help)`, and the Vector compiler automatically applies the reverse operations to clean it up at the end of the block.
* **Built-in Error Correction**: Declare logical qubits seamlessly. `qubits(10, protect="Surface")` handles all the underlying physical syndrome measurements automatically.
* **Natural Quantum Arithmetic**: Add quantum registers as easily as classic integers: `q_res = q_num1 + q_num2`. The compiler generates the QFT Adders behind the scenes.
* **Execution Pipelines**: Chain algorithms, simulations, and hardware runs in a single, readable line.

## 🚀 Quick Start: Hello Quantum (Bell State)

Here is how you create a perfectly entangled Bell State in Nexus:

```python
# Create two logical qubits protected from noise
my_qubits = qubits(2, state=0, protect="Surface").

algo:
entangle(q1, q2) {
    P = 2. # Set maximum circuit depth
    
    H(q1).
    q1.q2(CNOT).
}

# The Nexus Execution Pipeline: 
# Algorithm -> Hardware/Simulation -> Results
entangle(my_qubits[0], my_qubits[1]) -> run(1000, "IBM_Brisbane") -> results.
```

## 🛠️ The Vector Compiler

Nexus code is processed by **Vector**, a dedicated compiler that tokenizes, parses, and transpiles Nexus syntax into lower-level quantum assembly languages.

Current compilation pipeline:
1. **Lexer**: Translates Nexus text into language tokens. *(Done)*
2. **Parser**: Builds the Abstract Syntax Tree (AST). *(In Progress)*
3. **Transpiler**: Converts the AST into hardware-specific execution code. *(Planned)*

## 📂 Project Structure

* `docs/` - Official syntax cheat sheets and language documentation.
* `examples/` - Ready-to-run quantum algorithms written in Nexus (Grover, QFT, etc.).
* `src/` - The Vector Compiler source code (Python).
* `nexus_lib/` - The Nexus Standard Library (Built-in states, oracles, and math modules).

## 🤝 Contributing

We are building the future of quantum software. Whether you are a quantum physicist or a classical software developer, your contributions are welcome! 

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
