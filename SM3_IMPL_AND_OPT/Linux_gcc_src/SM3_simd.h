#ifndef SM3_SIMD_H
#define SM3_SIMD_H

#include "SM3_type.h"
#include "SM3_basic.h"
#include <immintrin.h>
#include <array>
#include <vector>
#include <string>

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

typedef std::array<WORD, 8>	SIMD_Buf_t;

class SM3_SIMD_Engine
{
private:
	std::array<const void*, 8> block_team;
	size_t blocklen;
	size_t valid_team;

	std::array<SIMD_Buf_t, 8> IV;
	std::array<SIMD_Buf_t, 68> W;
	std::array<SIMD_Buf_t, 64> W_stroke;

	void msg_expansion();
	void compress();

public:

	void push_msg(const std::array<const void*, 8>& block_team, size_t blocklen);
	void sm3();
	const char* get_hash_str(size_t team);
};

#endif /* SM3_SIMD_H */