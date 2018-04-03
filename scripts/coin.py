import sys
if sys.version_info < (3,5):
    raise Exception('Please use Python version 3.5 or greater.')

# useful additional packages
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np

# useful math functions
from math import pi, cos, acos, sqrt

# importing the QISKit
from qiskit import QuantumProgram
import Qconfig_c as Qconfig

# import basic plot tools
from qiskit.tools.visualization import plot_histogram

M = 16                   #Maximum number of physical qubits available
numberOfCoins = 8        #This number should be up to M-1, where M is the number of qubits available
indexOfFalseCoin = 3     #This should be 0, 1, ..., numberOfCoins - 1, where we use python indexing

if numberOfCoins < 4 or numberOfCoins >= M:
    raise Exception("Please use numberOfCoins between 4 and ", M-1)
if indexOfFalseCoin < 0 or indexOfFalseCoin >= numberOfCoins:
    raise Exception("indexOfFalseCoin must be between 0 and ", numberOfCoins-1)

Q_program = QuantumProgram()
Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) # set the APIToken and API url

# Creating registers
# numberOfCoins qubits for the binary query string and 1 qubit for working and recording the result of quantum balance
qr = Q_program.create_quantum_register("qr", numberOfCoins+1)
# for recording the measurement on qr
cr = Q_program.create_classical_register("cr", numberOfCoins+1)

circuitName = "QueryStateCircuit"
queryStateCircuit = Q_program.create_circuit(circuitName, [qr], [cr])

N = numberOfCoins
#Create uniform superposition of all strings of length N
for i in range(N):
    queryStateCircuit.h(qr[i])

#Perform XOR(x) by applying CNOT gates sequentially from qr[0] to qr[N-1] and storing the result to qr[N]
for i in range(N):
    queryStateCircuit.cx(qr[i], qr[N])

#Measure qr[N] and store the result to cr[N]. We continue if cr[N] is zero, or repeat otherwise
queryStateCircuit.measure(qr[N], cr[N])

# we proceed to query the quantum beam balance if the value of cr[0]...cr[N] is all zero
# by preparing the Hadamard state of |1>, i.e., |0> - |1> at qr[N]
queryStateCircuit.x(qr[N]).c_if(cr, 0)
queryStateCircuit.h(qr[N]).c_if(cr, 0)

# we rewind the computation when cr[N] is not zero
for i in range(N):
    queryStateCircuit.h(qr[i]).c_if(cr, 2**N)

k = indexOfFalseCoin
# Apply the quantum beam balance on the desired superposition state (marked by cr equal to zero)
queryStateCircuit.cx(qr[k], qr[N]).c_if(cr, 0)

# Apply Hadamard transform on qr[0] ... qr[N-1]
for i in range(N):
    queryStateCircuit.h(qr[i]).c_if(cr, 0)

# Measure qr[0] ... qr[N-1]
# queryStateCircuit.measure(qr, cr) #THIS IS NOT SUPPORTED?
for i in range(N):
    queryStateCircuit.measure(qr[i], cr[i])

backend = "local_qasm_simulator"
#backend = "ibmqx3"
shots = 1 # We perform a one-shot experiment
results = Q_program.execute([circuitName], backend=backend, shots=shots)
answer = results.get_counts(circuitName)
# for key in answer.keys():
#     if key[0:1] == "1":
#         raise Exception("Fail to create desired superposition of balanced query string. Please try again")

plot_histogram(answer)
from collections import Counter
for key in answer.keys():
    normalFlag, _ = Counter(key[1:]).most_common(1)[0] #get most common label
    for i in range(2,len(key)):
        if key[i] != normalFlag:
            print("False coin index is: ", len(key) - i - 1)
