CC=gcc
CFLAGS=-W -Wall -ansi -pedantic
LDFLAGS=
EXEC=windows
SRC_C=$(wildcard out/*.c) 
SRC_CPP=$(wildcard out/*.cpp)
OBJ=$(SRC_C:.c=.o) $(SRC_CPP:.cpp=.o)

all: $(EXEC)

linux: out/build.so

out/build.so: $(OBJ)
	$(CC) -shared -o $@ $(OBJ)

windows: out/build.dll out/build.lib

out/build.lib: $(OBJ)
	ar -rcs $@ $(OBJ)

out/build.dll: $(OBJ)
	$(CC) -shared -o $@ $(OBJ)
	
%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)