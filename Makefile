# # 컴파일러 설정
# CXX = g++
# CXXFLAGS = -Wall -O2 -std=c++17 -I./type -I./util -I./matmul

# # 파일 및 디렉토리 설정
# SRCS = main.cpp util/util.cpp type/bell.cpp type/dcn.cpp matmul/spmm_bell.cpp
# OBJS = $(SRCS:.cpp=.o)
# TARGET = main

# # 기본 규칙
# all: $(TARGET)

# # 타겟 실행 파일 생성 규칙
# $(TARGET): $(OBJS)
# 	$(CXX) $(CXXFLAGS) -o $@ $(OBJS)

# # 개별 소스 파일에 대한 오브젝트 파일 생성 규칙
# %.o: %.cpp
# 	$(CXX) $(CXXFLAGS) -c $< -o $@

# # 클린 규칙
# clean:
# 	rm -f $(OBJS) $(TARGET)

# 컴파일러 설정
CXX = g++
NVCC = nvcc
CXXFLAGS = -Wall -O2 -std=c++17 -I./type -I./util -I./matmul
NVCCFLAGS = -O2 -std=c++17 -I./type -I./util -I./matmul

# 파일 및 디렉토리 설정
SRCS = main.cpp util/util.cpp type/bell.cpp type/dcn.cpp
NVCC_SRCS = matmul/spmm_bell.cpp
OBJS = $(SRCS:.cpp=.o) $(NVCC_SRCS:.cpp=.o)
TARGET = main

# 기본 규칙
all: $(TARGET)

# 타겟 실행 파일 생성 규칙
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS) -lcusparse -lcudart

# g++로 컴파일하는 개별 소스 파일에 대한 오브젝트 파일 생성 규칙
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# nvcc로 컴파일하는 spmm_bell.cpp에 대한 규칙
matmul/spmm_bell.o: matmul/spmm_bell.cpp
	$(NVCC) $(NVCCFLAGS) -c $< -o $@

# 클린 규칙
clean:
	rm -f $(OBJS) $(TARGET)
