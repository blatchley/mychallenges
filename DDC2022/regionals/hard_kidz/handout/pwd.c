#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define LOL(v,n) ((v << n) | (v >> (8 - n)))
#define KEK(a,b) (a ^ b)

#define SIZE (32)
#define PWD_SIZE (256)

const char TARGET[SIZE] = {
    0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00
};

const char IV[SIZE] = {
    0x20,0x4d,0x61,0x78,
    0x69,0x6d,0x75,0x6d,
    0x20,0x43,0x79,0x62,
    0x65,0x72,0x63,0x79,
    0x62,0x65,0x72,0x20,
    0x53,0x65,0x63,0x75,
    0x72,0x69,0x74,0x79,
    0x20,0x49,0x56,0x20
};

const char MAGIC[SIZE] = {
    0x42,0x65,0x74,0x74,
    0x65,0x72,0x20,0x53,
    0x65,0x63,0x75,0x72,
    0x65,0x20,0x48,0x61,
    0x73,0x68,0x20,0x41,
    0x6c,0x67,0x6f,0x72,
    0x69,0x74,0x68,0x6d,
    0x20,0x33,0x30,0x30
};

typedef struct Block {
    uint8_t b[SIZE];
} Block;

void compress(Block *dst, Block *src1, Block *src2) {
#include "mix.cc"
}

void hash(Block *dst, uint8_t data[], size_t len) {
    // initialize
    for (size_t i = 0; i < SIZE; i++)
        dst->b[i] = IV[i];

    // iteratively compress
    for (size_t i = 0; i < len; i += SIZE) {
        Block *src1 = dst;
        Block *src2 = (Block*) &data[i];
        compress(dst, src1, src2);
    }

    // apply final tweak
    for (size_t i = 0; i < SIZE; i++)
        dst->b[i] ^= MAGIC[i];
}

void hex_enc(uint8_t data[], size_t len) {
    for (size_t i = 0; i < len; i++)
        printf("%02x", data[i]);
}

void hex_dec(uint8_t data[], size_t len) {
    unsigned int v;
    for (size_t i = 0; i < len; i++) {
        scanf("%02x", &v);
        data[i] = (uint8_t) (v & 0xff);
    }
}

int main() {
    Block dst;
    uint8_t cmd[PWD_SIZE];

    printf("G1v3 m3 d3m byt35 (exactly %d, h3x c0d3d): ", PWD_SIZE);
    hex_dec(cmd, PWD_SIZE);
    hash(&dst, cmd, PWD_SIZE);

    // Your command will only execute if it hashes to 0!
    // Flag is in flag.txt, in same directory as binary :D
    if (memcmp(&dst.b, TARGET, SIZE) == 0) {
        system(cmd);
    } else {
        printf("LOL, git gut m8: ");
        hex_enc((uint8_t*) &dst.b, SIZE);
    }
}
