import sys
sys.path.append("../")

from qiskit import QuantumProgram, QISKitError, RegisterSizeError

# Create a QuantumProgram object instance.
Q_program = QuantumProgram()
backend = 'local_qasm_simulator'

try:
    # Create a Quantum Register called "qr" with 2 qubits.
    qr = Q_program.create_quantum_register("qr", 4)
    # Create a Classical Register called "cr" with 2 bits.
    cr = Q_program.create_classical_register("cr", 4)
    # Create a Quantum Circuit called "qc" involving the Quantum Register "qr"
    # and the Classical Register "cr".
    qc = Q_program.create_circuit("circuit", [qr], [cr])

    qc.h(qr[0])
    qc.h(qr[1])
    qc.ccx(qr[0], qr[1], qr[2])
    qc.cx(qr[0], qr[3])
    qc.cx(qr[1], qr[3])
    # qc.measure(qr[0], cr[3])
    # qc.measure(qr[1], cr[2])
    # qc.measure(qr[2], cr[1])
    # qc.measure(qr[3], cr[0])

    qc.measure(qr, cr)


    # result = Q_program.execute(["circuit"], backend=backend, shots=1024, seed=1)
    result = Q_program.execute("circuit")
    print(result)
    print(result.get_data("circuit"))

except QISKitError as ex:
    print('There was an error in the circuit!. Error = {}'.format(ex))
except RegisterSizeError as ex:
    print('Error in the number of registers!. Error = {}'.format(ex))
