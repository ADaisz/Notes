CC=gcc
 
CFLAGS_WARN = -Wall
 
DEFINE =
INCLUDE = -I.
 
SOURCES = $(wildcard *.c)
OBJS = $(patsubst %.c,%,$(SOURCES))

All:$(OBJS)

%:%.c
	$(CC) $< -o $@	$(CFLAGS_WARN)
clean:	
	rm -f $(OBJS)
	rm -f $(TARGET)