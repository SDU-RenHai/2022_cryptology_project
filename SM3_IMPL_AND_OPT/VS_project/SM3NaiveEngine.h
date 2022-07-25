#ifndef SM3_NAIVE_ENGINE_H
#define SM3_NAIVE_ENGINE_H

#include "SM3_tyte.h"

#define IV0  0x7380166f
#define IV1  0x4914b2b9
#define IV2  0x172442d7
#define IV3  0xda8a0600
#define IV4  0xa96f30bc
#define IV5  0x163138aa
#define IV6  0xe38dee4d
#define IV7  0xb0fb0e4e

#define FF_0_15(X, Y, Z)	( (WORD)X ^ (WORD)Y ^ (WORD)Z )
#define FF_16_63(X, Y, Z)	( ((WORD)X & (WORD)Y) | ((WORD)X & (WORD)Z) | ((WORD)Y & (WORD)Z) )

#define GG_0_15(X, Y, Z)	FF_0_15(X, Y, Z)
#define GG_16_63(X, Y, Z)	( ((WORD)X & (WORD)Y) | ((~(WORD)X) & (WORD)Z) )

#define P0(X)	( (WORD)X ^ ((WORD)X << 9) ^ ((WORD)X << 17) )
#define P1(X)	( (WORD)X ^ ((WORD)X << 15) ^ ((WORD)X << 23) )

class SM3NaiveEngine
{

};

#endif // !SM3_NAIVE_ENGINE_H


