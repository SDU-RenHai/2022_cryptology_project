#ifndef SM3_TYPE_H
#define SM3_TYPE_H

#include <cstdint>
#include <array>

#define BIT_PER_WORD	32
#define WORD_PER_BLOCK	16

typedef uint32_t WORD;
typedef std::array<WORD, WORD_PER_BLOCK> BLOCK;


#endif // !SM3_TYPE_H
