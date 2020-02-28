.PHONY: all

CC=gcc
CFLAGS=-lpthread
BIN_ROUTE=./bin/
SRC_ROUTE=./src/
SRC1=$(SRC_ROUTE)problem1.c
SRC2=$(SRC_ROUTE)problem2.c
BIN1=$(BIN_ROUTE)problem1
BIN2=$(BIN_ROUTE)problem2
OBJ1=problem1
OBJ2=problem2

all: $(OBJ1) $(OBJ2)

$(OBJ1):
		$(CC) -o $(BIN1) $(SRC1) $(CFLAGS)

$(OBJ2):
		$(CC) -o $(BIN2) $(SRC2) $(CFLAGS)