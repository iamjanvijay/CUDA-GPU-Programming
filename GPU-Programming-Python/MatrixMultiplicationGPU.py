from __future__ import division
from numba import cuda
import numpy
import time
import math

# M1,N1,M2,N2 = (32, 16, 16, 32)
# M1,N1,M2,N2 = (256, 64, 64, 256)
M1,N1,M2,N2 = (256, 512, 512, 256)

# CUDA kernel
@cuda.jit
def matmul(A, B, C):
    """Perform matrix multiplication of C = A * B
    """
    row, col = cuda.grid(2)
    if row < C.shape[0] and col < C.shape[1]:
        tmp = 0.
        for k in range(A.shape[1]):
            tmp += A[row, k] * B[k, col]
        C[row, col] = tmp
        
# Host code

def cpumatmul(A, B, C):
	for row in xrange(0,M1) :
		for col in xrange(0,N2) :
			dotprod = 0
			for k in xrange(0,N1) :
				dotprod += (A[row][k] * B[k][col])
			C[row][col] = dotprod			

# Initialize the data arrays
A = numpy.full((M1, N1), 3, numpy.float) # matrix containing all 3's
B = numpy.full((M2, N2), 4, numpy.float) # matrix containing all 4's

# Copy the arrays to the device
A_global_mem = cuda.to_device(A)
B_global_mem = cuda.to_device(B)

# Allocate memory on the device for the result
C_global_mem = cuda.device_array((M1, N2))

#Allocating memory on the host for cross checking result
C_cpu_mem = numpy.full((M1, N2), 0, numpy.float)

# Configure the blocks
threadsperblock = (16, 16)
blockspergrid_x = int(math.ceil(A.shape[0] / threadsperblock[0]))
blockspergrid_y = int(math.ceil(B.shape[1] / threadsperblock[1]))
blockspergrid = (blockspergrid_x, blockspergrid_y)

#starting clock count
start = time.time()

# Start the kernel 
matmul[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem)

#printing out time used for processing
print "Matrix multiplication on GPU completed in %s seconds." % (time.time() - start)

# Copy the result back to the host
C = C_global_mem.copy_to_host()

# print(C)

#starting clock count
start = time.time()
#computing on CPU
cpumatmul(A, B, C_cpu_mem)
print "Matrix multiplication on CPU completed in %s seconds." % (time.time() - start)

error = 0
for row in xrange(0,M1) :
	for col in xrange(0,N2) :
		error += abs(C_cpu_mem[row][col]-C[row][col])

print "Error in CPU's and GPU's computations :", error		
