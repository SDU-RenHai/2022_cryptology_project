#include "SM3_naive.h"

#include <iostream>
using std::cout;
using std::endl;
using std::hex;

SM3_Naive_Engine::SM3_Naive_Engine()
{
	IV = { IV0, IV1, IV2, IV3, IV4, IV5, IV6, IV7 };
	A = B = C = D = E = F = G = H = 0;
	W = std::array<WORD, 68>{};
	W_stroke = std::array<WORD, 64>{};
}

void SM3_Naive_Engine::msg_expansion(const WORD* block)
{
	for (size_t i = 0; i < 16; ++i) this->W[i] = block[i];
	for (size_t i = 16; i < 68; ++i) {
		WORD X = W[i - 16] ^ W[i - 9] ^ WORD_ROTATE_LEFT(W[i - 3], 15);
		WORD Y = WORD_ROTATE_LEFT(W[i - 13], 7);
		this->W[i] = P1(X) ^ Y ^ W[i - 6];
	}
	for (size_t i = 0; i < 64; ++i) this->W_stroke[i] = W[i] ^ W[i + 4];
}

void SM3_Naive_Engine::compress()
{
	WORD SS1, SS2, TT1, TT2;

	A = IV[0]; B = IV[1]; C = IV[2]; D = IV[3];
	E = IV[4]; F = IV[5]; G = IV[6]; H = IV[7];

	for (size_t j = 0; j <= 15; ++j) {
		SS1 = WORD_ROTATE_LEFT(WORD_ROTATE_LEFT(A, 12) + E + WORD_ROTATE_LEFT(T_0_15, j), 7);
		SS2 = SS1 ^ WORD_ROTATE_LEFT(A, 12);
		TT1 = FF_0_15(A, B, C) + D + SS2 + W_stroke[j];
		TT2 = GG_0_15(E, F, G) + H + SS1 + W[j];
		D = C;
		C = WORD_ROTATE_LEFT(B, 9);
		B = A;
		A = TT1;
		H = G;
		G = WORD_ROTATE_LEFT(F, 19);
		F = E;
		E = P0(TT2);
	}

	for (size_t j = 16; j <= 63; ++j) {
		SS1 = WORD_ROTATE_LEFT(WORD_ROTATE_LEFT(A, 12) + E + WORD_ROTATE_LEFT(T_16_63, j), 7);
		SS2 = SS1 ^ WORD_ROTATE_LEFT(A, 12);
		TT1 = FF_16_63(A, B, C) + D + SS2 + W_stroke[j];
		TT2 = GG_16_63(E, F, G) + H + SS1 + W[j];
		D = C;
		C = WORD_ROTATE_LEFT(B, 9);
		B = A;
		A = TT1;
		H = G;
		G = WORD_ROTATE_LEFT(F, 19);
		F = E;
		E = P0(TT2);
	}

	IV[0] ^= A; IV[1] ^= B; IV[2] ^= C; IV[3] ^= D;
	IV[4] ^= E; IV[5] ^= F; IV[6] ^= G; IV[7] ^= H;
}


void SM3_Naive_Engine::sm3(const WORD* input, size_t blocklen)
{
	IV = { IV0, IV1, IV2, IV3, IV4, IV5, IV6, IV7 };

	for (size_t i = 0; i < blocklen; ++i) {
		const WORD* block_begin = (WORD*)input + (i * WORD_PER_BLOCK);
		msg_expansion(block_begin);
		compress();
	}
}

void SM3_Naive_Engine::sm3(const char* msg, size_t msglen)
{
	size_t blocklen;
	void* blocks = msg2blocks_with_padding(msg, msglen, blocklen);
	sm3((const WORD*)blocks, blocklen);
}

void SM3_Naive_Engine::sm3(const std::string& msg)
{
	sm3(msg.c_str(), msg.length());
}

const std::array<WORD, 8>& SM3_Naive_Engine::get_hash()
{
	return IV;
}

const char* SM3_Naive_Engine::get_hash_str()
{
	return word2string(IV.data(), 8);
}
