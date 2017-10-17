#ifndef Device_Array
#define Device_Array

#include <bits/stdc++.h>
#include <cuda_runtime.h>

using namespace std;

template<class T>
class devArray
{
//private Functions
private :
	void allocate(size_t size)
	{
		cudaError_t result = cudaMalloc((void**)&start_, size * sizeof(T));
		if (result != cudaSuccess)
		{
			start_ = end_ = 0;
			throw runtime_error("Failed to allocate memory on Device");
		}
		end_ = start_ + size;
	}
	void free()
	{
		if(start_ != 0)
		{
			cudaFree(start_);
			start_ = end_ = 0;
		}
	}

//private Data members
	T* start_;
	T* end_;

//public functions
public :
	// Constructors
	explicit devArray() : start_(0), end_(0)
	{
	}
	explicit devArray(size_t size)
	{
		allocate(size);
	}

	// Destructor
	~devArray()
	{
		free();
	}

	// resize vector
	void resize(size_t size)
	{
		free();
		allocate(size);
	}

	// get size of vector
	size_t getSize() const
	{
		return end_-start_;
	}

	// get Data
	const T* getData() const
	{
		return start_;
	}

	T* getData()
	{
		return start_;
	}

	// set
	void set(const T* src, size_t size)
	{
		size_t min_ = min(size, getSize());
		cudaError_t result = cudaMemcpy(start_, src, min_*sizeof(T), cudaMemcpyHostToDevice );
		if(result!=cudaSuccess)
		{
			throw runtime_error("Failed to copy to device memory.");
		}
	}

	//get
	void get(T* dest, size_t size)
	{
		size_t min_ = min(size, getSize());
		cudaError_t result = cudaMemcpy(dest, start_, min_ * sizeof(T), cudaMemcpyDeviceToHost);
		if(result!=cudaSuccess)
		{
			throw runtime_error("Failed to copy to Host memory.");
		}
	}
};
#endif
