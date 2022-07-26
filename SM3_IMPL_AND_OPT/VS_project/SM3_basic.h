#ifndef SM3_BASIC_H
#define SM3_BASIC_H

#include "SM3_tyte.h"
#include <string>

#define WORD_ROTATE_LEFT(X, len)  (((WORD)(X) << len) | ((WORD)(X) >> (32 - len)))

char int2char(uint8_t input);

void* msg2blocks_with_padding(const char* msg, size_t msglen, size_t& blocklen);

const char* word2string(const void* buffer, size_t wordlen);

#endif // !SM3_BASIC_H
