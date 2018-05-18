import sys
if sys.version_info < (3,5):
    raise Exception('Please use Python version 3.5 or greater.')

# useful additional packages
import matplotlib.pyplot as plt
import numpy as np

# useful math functions
from math import pi, cos, acos, sqrt
import random

# importing the QISKit
from qiskit import QuantumProgram
import Qconfig_c as Qconfig

# import basic plot tools
from qiskit.tools.visualization import plot_histogram

Q_program = QuantumProgram()
Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) # set the APIToken and API url

N = 4
# Creating registers
qr = Q_program.create_quantum_register("qr", N)

# for recording the measurement on qr
cr = Q_program.create_classical_register("cr", N)

circuitName = "sharedEntangled"
sharedEntangled = Q_program.create_circuit(circuitName, [qr], [cr])

#Create uniform superposition of all strings of length 2
for i in range(2):
    sharedEntangled.h(qr[i])

#The amplitude is minus if there are odd number of 1s
for i in range(2):
    sharedEntangled.z(qr[i])

#Copy the content of the fist two qubits to the last two qubits
for i in range(2):
    sharedEntangled.cx(qr[i], qr[i+2])

#Flip the last two qubits
for i in range(2,4):
    sharedEntangled.x(qr[i])
#we first define controlled-u gates required to assign phases
from math import pi
def ch(qProg, a, b):
    """ Controlled-Hadamard gate """
    qProg.h(b)
    qProg.sdg(b)
    qProg.cx(a, b)
    qProg.h(b)
    qProg.t(b)
    qProg.cx(a, b)
    qProg.t(b)
    qProg.h(b)
    qProg.s(b)
    qProg.x(b)
    qProg.s(a)
    return qProg

def cu1pi2(qProg, c, t):
    """ Controlled-u1(phi/2) gate """
    qProg.u1(pi/4.0, c)
    qProg.cx(c, t)
    qProg.u1(-pi/4.0, t)
    qProg.cx(c, t)
    qProg.u1(pi/4.0, t)
    return qProg

def cu3pi2(qProg, c, t):
    """ Controlled-u3(pi/2, -pi/2, pi/2) gate """
    qProg.u1(pi/2.0, t)
    qProg.cx(c, t)
    qProg.u3(-pi/4.0, 0, 0, t)
    qProg.cx(c, t)
    qProg.u3(pi/4.0, -pi/2.0, 0, t)
    return qProg


# dictionary for Alice's operations/circuits
aliceCircuits = {}
# Quantum circuits for Alice when receiving idx in 1, 2, 3
for idx in range(1, 4):
    circuitName = "Alice"+str(idx)
    aliceCircuits[circuitName] = Q_program.create_circuit(circuitName, [qr], [cr])
    theCircuit = aliceCircuits[circuitName]

    if idx == 1:
        #the circuit of A_1
        theCircuit.x(qr[1])
        theCircuit.cx(qr[1], qr[0])
        theCircuit = cu1pi2(theCircuit, qr[1], qr[0])
        theCircuit.x(qr[0])
        theCircuit.x(qr[1])
        theCircuit = cu1pi2(theCircuit, qr[0], qr[1])
        theCircuit.x(qr[0])
        theCircuit = cu1pi2(theCircuit, qr[0], qr[1])
        theCircuit = cu3pi2(theCircuit, qr[0], qr[1])
        theCircuit.x(qr[0])
        theCircuit = ch(theCircuit, qr[0], qr[1])
        theCircuit.x(qr[0])
        theCircuit.x(qr[1])
        theCircuit.cx(qr[1], qr[0])
        theCircuit.x(qr[1])

    elif idx == 2:
        theCircuit.x(qr[0])
        theCircuit.x(qr[1])
        theCircuit = cu1pi2(theCircuit, qr[0], qr[1])
        theCircuit.x(qr[0])
        theCircuit.x(qr[1])
        theCircuit = cu1pi2(theCircuit, qr[0], qr[1])
        theCircuit.x(qr[0])
        theCircuit.h(qr[0])
        theCircuit.h(qr[1])

    elif idx == 3:
        theCircuit.cz(qr[0], qr[1])
        theCircuit.swap(qr[0], qr[1])
        theCircuit.h(qr[0])
        theCircuit.h(qr[1])
        theCircuit.x(qr[0])
        theCircuit.x(qr[1])
        theCircuit.cz(qr[0], qr[1])
        theCircuit.x(qr[0])
        theCircuit.x(qr[1])

    #measure the first two qubits in the computational basis
    theCircuit.measure(qr[0], cr[0])
    theCircuit.measure(qr[1], cr[1])

# dictionary for Bob's operations/circuits
bobCircuits = {}
# Quantum circuits for Bob when receiving idx in 1, 2, 3
for idx in range(1,4):
    circuitName = "Bob"+str(idx)
    bobCircuits[circuitName] = Q_program.create_circuit(circuitName, [qr], [cr])
    theCircuit = bobCircuits[circuitName]
    if idx == 1:
        theCircuit.x(qr[2])
        theCircuit.x(qr[3])
        theCircuit.cz(qr[2], qr[3])
        theCircuit.x(qr[3])
        theCircuit.u1(pi/2.0, qr[2])
        theCircuit.x(qr[2])
        theCircuit.z(qr[2])
        theCircuit.cx(qr[2], qr[3])
        theCircuit.cx(qr[3], qr[2])
        theCircuit.h(qr[2])
        theCircuit.h(qr[3])
        theCircuit.x(qr[3])
        theCircuit = cu1pi2(theCircuit, qr[2], qr[3])
        theCircuit.x(qr[2])
        theCircuit.cz(qr[2], qr[3])
        theCircuit.x(qr[2])
        theCircuit.x(qr[3])

    elif idx == 2:
        theCircuit.x(qr[2])
        theCircuit.x(qr[3])
        theCircuit.cz(qr[2], qr[3])
        theCircuit.x(qr[3])
        theCircuit.u1(pi/2.0, qr[3])
        theCircuit.cx(qr[2], qr[3])
        theCircuit.h(qr[2])
        theCircuit.h(qr[3])

    elif idx == 3:
        theCircuit.cx(qr[3], qr[2])
        theCircuit.x(qr[3])
        theCircuit.h(qr[3])

    #measure the third and fourth qubits in the computational basis
    theCircuit.measure(qr[2], cr[2])
    theCircuit.measure(qr[3], cr[3])

a, b = random.randint(1,3), random.randint(1,3) #generate random integers

for i in range(3):
    for j in range(3):
        a = i +1;
        b= j +1;
        # print("The values of a and b are, resp.,", a,b)
        aliceCircuit = aliceCircuits["Alice"+str(a)]
        bobCircuit = bobCircuits["Bob"+str(b)]

        circuitName = "Alice"+str(a)+"Bob"+str(b)
        Q_program.add_circuit(circuitName, sharedEntangled+aliceCircuit+bobCircuit)

        backend = "local_qasm_simulator"
        ##backend = "ibmqx2"

        shots = 1 # We perform a one-shot experiment
        results = Q_program.execute([circuitName], backend=backend, shots=shots)
        answer = results.get_counts(circuitName)
        # print(answer)
        for key in answer.keys():
            aliceAnswer = [int(key[-1]), int(key[-2])]
            bobAnswer   = [int(key[-3]), int(key[-4])]
            if sum(aliceAnswer) % 2 == 0:#the sume of Alice answer must be even
                aliceAnswer.append(0)
            else:
                aliceAnswer.append(1)
            if sum(bobAnswer) % 2 == 1:#the sum of Bob answer must be odd
                bobAnswer.append(0)
            else:
                bobAnswer.append(1)
            break

        print("Alice answer for a = ", a, "is", aliceAnswer)
        print("Bob answer for b = ", b, "is", bobAnswer)

        # if(aliceAnswer[b-1] != bobAnswer[a-1]): #check if the intersection of their answers is the same
        #     print("Alice and Bob lost")
        # else:
        #     print("Alice and Bob won")

        backend = "local_qasm_simulator"
        #backend = "ibmqx2"
        shots = 10 # We perform 10 shots of experiments for each round
        nWins = 0
        nLost = 0
        for a in range(1,4):
            for b in range(1,4):
                # print("Asking Alice and Bob with a and b are, resp.,", a,b)
                rWins = 0
                rLost = 0

                aliceCircuit = aliceCircuits["Alice"+str(a)]
                bobCircuit = bobCircuits["Bob"+str(b)]
                circuitName = "Alice"+str(a)+"Bob"+str(b)
                Q_program.add_circuit(circuitName, sharedEntangled+aliceCircuit+bobCircuit)

                if backend == "ibmqx2":
                    ibmqx2_backend = Q_program.get_backend_configuration('ibmqx2')
                    ibmqx2_coupling = ibmqx2_backend['coupling_map']
                    results = Q_program.execute([circuitName], backend=backend, shots=shots, coupling_map=ibmqx2_coupling, max_credits=3, wait=10, timeout=240)
                else:
                    results = Q_program.execute([circuitName], backend=backend, shots=shots)
                answer = results.get_counts(circuitName)

                for key in answer.keys():
                    kfreq = answer[key] #frequencies of keys obtained from measurements
                    aliceAnswer = [int(key[-1]), int(key[-2])]
                    bobAnswer   = [int(key[-3]), int(key[-4])]
                    if sum(aliceAnswer) % 2 == 0:
                        aliceAnswer.append(0)
                    else:
                        aliceAnswer.append(1)
                    if sum(bobAnswer) % 2 == 1:
                        bobAnswer.append(0)
                    else:
                        bobAnswer.append(1)

                    #print("Alice answer for a = ", a, "is", aliceAnswer)
                    #print("Bob answer for b = ", b, "is", bobAnswer)

                    if(aliceAnswer[b-1] != bobAnswer[a-1]):
                        #print(a, b, "Alice and Bob lost")
                        nLost += kfreq
                        rLost += kfreq
                    else:
                        #print(a, b, "Alice and Bob won")
                        nWins += kfreq
                        rWins += kfreq
        #         print("\t#wins = ", rWins, "out of ", shots, "shots")
        #
        # print("Number of Games = ", nWins+nLost)
        # print("Number of Wins = ", nWins)
        # print("Winning probabilities = ", (nWins*100.0)/(nWins+nLost))
