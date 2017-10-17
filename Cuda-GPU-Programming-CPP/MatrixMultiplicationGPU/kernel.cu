#ifndef Kernel_CU
#define Kernel_CU

#include <bits/stdc++.h>
#include <cuda_runtime.h>
#include "kernel.h"
using namespace std;

__global__ void matrixMultiplicationKernel(float *A, float *B, float *C, int N)
{
	int Col = blockIdx.y*blockDim.y+ threadIdx.y;
	int Row = blockIdx.x*blockDim.x+ threadIdx.x;

	float tmpSum = 0;

	if(Row<N&&Col<N)
	{
		for(int i=0;i<N;i++)
		{
			tmpSum += A[Row*N+i] * B[i*N+Col];
		}
	}
	C[Row*N+Col] = tmpSum;
}

void matrixMultiplication(float *A, float *B, float *C, int N)
{
	dim3 threadsPerBlock(N,N);
	dim3 blocksPerGrid(1,1);
	if(N*N>1024)
	{
		threadsPerBlock.x = 64;
		threadsPerBlock.y = 64;
		blocksPerGrid.x = ceil(double(N)/double(threadsPerBlock.x));
		blocksPerGrid.y = ceil(double(N)/double(threadsPerBlock.y));
	}

	matrixMultiplicationKernel<<<blocksPerGrid, threadsPerBlock>>>(A, B, C, N);
}

#endif
