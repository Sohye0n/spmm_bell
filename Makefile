# 컴파일러 설정
CXX = g++
CXXFLAGS = -Wall -O2 -std=c++17 -I./type -I./util

# 파일 및 디렉토리 설정
SRCS = main.cpp util/util.cpp type/bell.cpp type/dcn.cpp
OBJS = $(SRCS:.cpp=.o)
TARGET = main

# 기본 규칙
all: $(TARGET)

# 타겟 실행 파일 생성 규칙
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS)

# 개별 소스 파일에 대한 오브젝트 파일 생성 규칙
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# 클린 규칙
clean:
	rm -f $(OBJS) $(TARGET)
