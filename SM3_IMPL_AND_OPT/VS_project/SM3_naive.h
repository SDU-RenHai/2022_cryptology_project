#ifndef SM3_NAIVE_H
#define SM3_NAIVE_H

#include "SM3_tyte.h"
#include "SM3_basic.h"
#include <array>

#define IV0  0x7380166f
#define IV1  0x4914b2b9
#define IV2  0x172442d7
#define IV3  0xda8a0600
#define IV4  0xa96f30bc
#define IV5  0x163138aa
#define IV6  0xe38dee4d
#define IV7  0xb0fb0e4e

#define T_0_15		0x79cc4519
#define T_16_63		0x7a879d8a

#define FF_0_15(X, Y, Z)	( (WORD)(X) ^ (WORD)(Y) ^ (WORD)(Z) )
#define FF_16_63(X, Y, Z)	( ((WORD)(X) & (WORD)(Y)) | ((WORD)(X) & (WORD)(Z)) | ((WORD)(Y) & (WORD)(Z)) )

#define GG_0_15(X, Y, Z)	( (WORD)(X) ^ (WORD)(Y) ^ (WORD)(Z) )
#define GG_16_63(X, Y, Z)	( ((WORD)(X) & (WORD)(Y)) | ((~(WORD)(X)) & (WORD)(Z)) )

#define P0(X)	( (WORD)(X) ^ WORD_ROTATE_LEFT(X, 9) ^ WORD_ROTATE_LEFT(X, 17) )
#define P1(X)	( (WORD)(X) ^ WORD_ROTATE_LEFT(X, 15) ^ WORD_ROTATE_LEFT(X, 23) )

class SM3_Naive_Engine
{
private:
	std::array<WORD, 8> IV;
	std::array<WORD, 68> W;
	std::array<WORD, 64> W_stroke;
	WORD A, B, C, D, E, F, G, H;

	void msg_expansion(const WORD* block);
	void compress();

public:
	SM3_Naive_Engine();
	
	void sm3(const WORD* input, size_t blocklen);
	void sm3(const char* msg, size_t msglen);
	void sm3(const std::string& msg);

	const std::array<WORD, 8> & get_hash();
	const char* get_hash_str();
};

#endif // !SM3_NAIVE_H


