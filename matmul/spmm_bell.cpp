#include <cuda_fp16.h>        // data types
#include <cuda_runtime_api.h> // cudaMalloc, cudaMemcpy, etc.
#include <cusparse.h>         // cusparseSpMM
#include <cstdio>            // printf
#include <cstdlib>           // EXIT_FAILURE
#include "spmm_bell.h"
#include "bell.h"
#include "dcn.h"
using namespace std;

#define CHECK_CUDA(func)                                                       \
{                                                                              \
    cudaError_t status = (func);                                               \
    if (status != cudaSuccess) {                                               \
        std::printf("CUDA API failed at line %d with error: %s (%d)\n",        \
               __LINE__, cudaGetErrorString(status), status);                  \
        return EXIT_FAILURE;                                                   \
    }                                                                          \
}

#define CHECK_CUSPARSE(func)                                                   \
{                                                                              \
    cusparseStatus_t status = (func);                                          \
    if (status != CUSPARSE_STATUS_SUCCESS) {                                   \
        std::printf("CUSPARSE API failed at line %d with error: %s (%d)\n",    \
               __LINE__, cusparseGetErrorString(status), status);              \
        return EXIT_FAILURE;                                                   \
    }                                                                          \
}

const int EXIT_UNSUPPORTED = 2;

void copyFloatToHalf(const float* hA_values, __half* dA_values, int size) {
    // GPU 메모리에 __half 배열 할당
    __half* h_half = new __half[size];  // 호스트 메모리에 __half 배열을 생성
    // float 배열의 값을 __half로 변환
    for (int i = 0; i < size; ++i) {
        h_half[i] = __float2half(hA_values[i]);  // float을 __half로 변환
    }

    // 변환된 __half 배열을 GPU로 복사
    cudaMemcpy(dA_values, h_half, size * sizeof(__half), cudaMemcpyHostToDevice);

    // 호스트 메모리 해제
    delete[] h_half;
}

void copyHalfToFloat(__half* dA_values, float* hA_values, int size) {
    // GPU의 __half 배열을 CPU의 float 배열로 변환하여 복사
    __half* h_half = new __half[size];  // 호스트 메모리에 __half 배열을 생성

    // GPU에서 호스트로 __half 배열 복사
    cudaMemcpy(h_half, dA_values, size * sizeof(__half), cudaMemcpyDeviceToHost);

    // __half 배열을 float으로 변환
    for (int i = 0; i < size; ++i) {
        hA_values[i] = __half2float(h_half[i]);  // __half를 float으로 변환
    }

    // 호스트 메모리 해제
    delete[] h_half;
}

float spmm_bell_exe(BELL &A, DCN &B, DCN &C){

    //time measure
    float time=0.0f;
    cudaEvent_t start, stop;

    // // Check compute capability
    // cudaDeviceProp props;
    // CHECK_CUDA( cudaGetDeviceProperties(&props, 0) )
    // if (props.major < 7) {
    //   std::printf("cusparseSpMM with blocked ELL format is supported only "
    //               "with compute capability at least 7.0\n");
    //   return EXIT_UNSUPPORTED;
    // }

    // Device memory management
    int    *dA_columns;
    __half *dA_values, *dB, *dC;


    CHECK_CUDA( cudaMalloc((void**) &dA_columns, A.num_blocks * sizeof(int)) )
    CHECK_CUDA( cudaMalloc((void**) &dA_values,
                                    A.ell_cols * A.num_rows * sizeof(__half)) )
    CHECK_CUDA( cudaMalloc((void**) &dB, B.num_rows * B.num_cols * sizeof(__half)) )
    CHECK_CUDA( cudaMalloc((void**) &dC, C.num_rows * C.num_cols * sizeof(__half)) )

    CHECK_CUDA( cudaMemcpy(dA_columns, A.ellColInd,
                           A.num_blocks * sizeof(int),
                           cudaMemcpyHostToDevice) )

    //change CPU float arr -> GPU half arr
    copyFloatToHalf(A.ellValue, dA_values, A.ell_cols * A.num_rows);
    copyFloatToHalf(B.value, dB, B.num_rows * B.num_cols);
    copyFloatToHalf(C.value, dC, C.num_rows * C.num_cols);


    // CUSPARSE APIs
    cusparseHandle_t     handle = NULL;
    cusparseSpMatDescr_t matA;
    cusparseDnMatDescr_t matB, matC;
    void*                dBuffer    = NULL;
    size_t               bufferSize = 0;
    float alpha           = 1.0f;
    float beta            = 0.0f;

    CHECK_CUSPARSE( cusparseCreate(&handle) )
    // Create sparse matrix A in blocked ELL format
    CHECK_CUSPARSE( cusparseCreateBlockedEll(
                                      &matA,
                                      A.num_rows, A.num_cols, A.ell_blocksize,
                                      A.ell_cols, dA_columns, dA_values,
                                      CUSPARSE_INDEX_32I,
                                      CUSPARSE_INDEX_BASE_ZERO, CUDA_R_16F) )


    // Create dense matrix B
    CHECK_CUSPARSE( cusparseCreateDnMat(&matB, A.num_cols, B.num_cols, B.num_cols, dB,
                                        CUDA_R_16F, CUSPARSE_ORDER_ROW) )
    // Create dense matrix C
    CHECK_CUSPARSE( cusparseCreateDnMat(&matC, A.num_rows, B.num_cols, B.num_cols, dC,
                                        CUDA_R_16F, CUSPARSE_ORDER_ROW) )
    // allocate an external buffer if needed
    CHECK_CUSPARSE( cusparseSpMM_bufferSize(
                                 handle,
                                 CUSPARSE_OPERATION_NON_TRANSPOSE,
                                 CUSPARSE_OPERATION_NON_TRANSPOSE,
                                 &alpha, matA, matB, &beta, matC, CUDA_R_32F,
                                 CUSPARSE_SPMM_ALG_DEFAULT, &bufferSize) )
    CHECK_CUDA( cudaMalloc(&dBuffer, bufferSize) )

    /*time record start*/
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);
    

    // execute SpMM
    CHECK_CUSPARSE( cusparseSpMM(handle,
                                 CUSPARSE_OPERATION_NON_TRANSPOSE,
                                 CUSPARSE_OPERATION_NON_TRANSPOSE,
                                 &alpha, matA, matB, &beta, matC, CUDA_R_32F,
                                 CUSPARSE_SPMM_ALG_DEFAULT, dBuffer) )

    /*time record end*/
    cudaDeviceSynchronize();
    cudaEventRecord(stop,0);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&time,start,stop);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    // destroy matrix/vector descriptors
    CHECK_CUSPARSE( cusparseDestroySpMat(matA) )
    CHECK_CUSPARSE( cusparseDestroyDnMat(matB) )
    CHECK_CUSPARSE( cusparseDestroyDnMat(matC) )
    CHECK_CUSPARSE( cusparseDestroy(handle) )

    // device result check
    // CHECK_CUDA( cudaMemcpy(C.value, dC, C.num_rows * C.num_cols * sizeof(__half),
    //                        cudaMemcpyDeviceToHost) )
    copyHalfToFloat(dC,C.value,C.num_rows * C.num_cols);

    // device memory deallocation
    CHECK_CUDA( cudaFree(dBuffer) )
    CHECK_CUDA( cudaFree(dA_columns) )
    CHECK_CUDA( cudaFree(dA_values) )
    CHECK_CUDA( cudaFree(dB) )
    CHECK_CUDA( cudaFree(dC) )

    return time;
}


float spmm_bell(BELL &lhs, DCN &rhs, DCN &result, int cnt){
    
    float sum=0.0f;
    float mean;
    
    for(int i=0; i<cnt; i++){
        sum += spmm_bell_exe(lhs, rhs, result);
    }

    mean = sum / cnt;
    return mean;
}
