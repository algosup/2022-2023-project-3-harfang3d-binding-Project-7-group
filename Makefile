CC=gcc
CFLAGS=-W -Wall -ansi -pedantic
LDFLAGS=
EXEC=build
SRC_C=$(wildcard out/*.c) 
SRC_CPP=$(wildcard out/*.cpp)
OBJ=$(SRC_C:.c=.o) $(SRC_CPP:.cpp=.o)

all: $(EXEC)

build: out/build.dll out/build.lib

out/build.lib: $(OBJ)
	ar -rcs build.lib $(OBJ)

out/build.dll: $(OBJ)
	$(CC) -shared -o $@ $(OBJ)
	
%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)