CC = g++ -O2 -std=c++17 -mavx2 -mavx -mavx512f -mavx512vl

all: linux_run

linux_run: ./Linux_gcc_src/SM3_type.h ./Linux_gcc_src/SM3_basic.h ./Linux_gcc_src/SM3_simd.h ./Linux_gcc_src/SM3_naive.h ./Linux_gcc_src/SM3_basic.cpp ./Linux_gcc_src/SM3_naive.cpp ./Linux_gcc_src/SM3_simd.cpp ./Linux_gcc_src/main.cpp
	$(CC) ./Linux_gcc_src/SM3_type.h ./Linux_gcc_src/SM3_basic.h ./Linux_gcc_src/SM3_simd.h ./Linux_gcc_src/SM3_naive.h ./Linux_gcc_src/SM3_basic.cpp ./Linux_gcc_src/SM3_naive.cpp ./Linux_gcc_src/SM3_simd.cpp ./Linux_gcc_src/main.cpp -o linux_run
	
clean: 
	rm -rf linux_run
