#include "SM3_simd.h"

#include <iostream>
using std::endl;
using std::cout;
using std::hex;

static inline WORD SIMD_print(__m256i mm_val, size_t pos) {
	WORD temp[8];
	_mm256_store_epi64(temp, mm_val);
	return temp[pos];
}

static inline __m256i SIMD_word_rotate_sll (__m256i mm_val, size_t imm) {
	imm %= 32;
	__m256i mm_sll = _mm256_slli_epi32(mm_val, (uint8_t)imm);
	__m256i mm_srl = _mm256_srli_epi32(mm_val, 32 - (uint8_t)imm);
	return _mm256_or_si256(mm_sll, mm_srl);
}

static inline __m256i SIMD_P0(__m256i mm_val) {
	__m256i mm_sll9 = SIMD_word_rotate_sll(mm_val, 9);
	__m256i mm_sll17 = SIMD_word_rotate_sll(mm_val, 17);
	return _mm256_xor_si256(mm_val, _mm256_xor_si256(mm_sll9, mm_sll17));
}

static inline __m256i SIMD_P1(__m256i mm_val) {
	__m256i mm_sll15 = SIMD_word_rotate_sll(mm_val, 15);
	__m256i mm_sll23 = SIMD_word_rotate_sll(mm_val, 23);
	return _mm256_xor_si256(mm_val, _mm256_xor_epi32(mm_sll15, mm_sll23));
}

static inline __m256i SIMD_FF_0_15(__m256i A, __m256i B, __m256i C) {
	return _mm256_xor_si256(_mm256_xor_si256(A, B), C);
}

static inline __m256i SIMD_FF_16_63(__m256i A, __m256i B, __m256i C) {
	__m256i X = _mm256_and_si256(A, B);
	__m256i Y = _mm256_and_si256(A, C);
	__m256i Z = _mm256_and_si256(B, C);
	return _mm256_or_si256(X, _mm256_or_si256(Y, Z));
}

static inline __m256i SIMD_GG_0_15(__m256i A, __m256i B, __m256i C) {
	return _mm256_xor_si256(_mm256_xor_si256(A, B), C);
}

static inline __m256i SIMD_GG_16_63(__m256i A, __m256i B, __m256i C) {
	__m256i X = _mm256_and_si256(A, B);
	__m256i Y = _mm256_andnot_si256(A, C);
	return _mm256_or_si256(X, Y);
}

void SM3_SIMD_Engine::push_msg(const std::array<const void*, 8>& block_team, size_t blocklen)
{
	this->block_team = block_team;
	this->blocklen = blocklen;
}

void SM3_SIMD_Engine::msg_expansion()
{
	for (size_t t = 0; t < 8; ++t) {
		const WORD* block = (const WORD*)block_team[t];
		if (block == nullptr) {
			for (size_t i = 0; i < 16; ++i) W[i][t] = 0x00000000;
		}
		else {
			for (size_t i = 0; i < 16; ++i) W[i][t] = block[i];
		}
	}

	for (size_t i = 16; i < 68; ++i) {

		// WORD X = W[i - 16] ^ W[i - 9] ^ WORD_ROTATE_LEFT(W[i - 3], 15);
		__m256i X = _mm256_load_si256((__m256i const *)W[i - 16].data());
		__m256i mm_w_i9 = _mm256_load_si256((__m256i const *)W[i - 9].data());
		X = _mm256_xor_si256(X, mm_w_i9);
		__m256i mm_w_i3 = _mm256_load_si256((__m256i const *)W[i - 3].data());
		mm_w_i3 = SIMD_word_rotate_sll(mm_w_i3, 15);
		X = _mm256_xor_si256(X, mm_w_i3);

		// WORD Y = WORD_ROTATE_LEFT(W[i - 13], 7);
		__m256i Y = _mm256_load_si256((__m256i const *)W[i - 13].data());
		Y = SIMD_word_rotate_sll(Y, 7);

		// this->W[i] = P1(X) ^ Y ^ W[i - 6];
		__m256i ANS = _mm256_load_si256((__m256i const *)W[i - 6].data());
		ANS = _mm256_xor_si256(ANS, Y);
		ANS = _mm256_xor_si256(ANS, SIMD_P1(X));

		// Move to W;
		_mm256_store_epi64(W[i].data(), ANS);

	}

	for (size_t i = 0; i < 64; ++i) {

		// W_stroke[i] = W[i] ^ W[i + 4];
		__m256i ANS = _mm256_load_si256((__m256i const *)W[i].data());
		__m256i wi_4 = _mm256_load_si256((__m256i const *)W[i + 4].data());
		ANS = _mm256_xor_si256(ANS, wi_4);

		// Move to W_stroke;
		_mm256_store_epi64(W_stroke[i].data(), ANS);

	}
}

void SM3_SIMD_Engine::sm3()
{
	IV[0] = { IV0, IV0, IV0, IV0, IV0, IV0, IV0, IV0 };
	IV[1] = { IV1, IV1, IV1, IV1, IV1, IV1, IV1, IV1 };
	IV[2] = { IV2, IV2, IV2, IV2, IV2, IV2, IV2, IV2 };
	IV[3] = { IV3, IV3, IV3, IV3, IV3, IV3, IV3, IV3 };
	IV[4] = { IV4, IV4, IV4, IV4, IV4, IV4, IV4, IV4 };
	IV[5] = { IV5, IV5, IV5, IV5, IV5, IV5, IV5, IV5 };
	IV[6] = { IV6, IV6, IV6, IV6, IV6, IV6, IV6, IV6 };
	IV[7] = { IV7, IV7, IV7, IV7, IV7, IV7, IV7, IV7 };

	for (size_t i = 0; i < blocklen; ++i) {
		msg_expansion();
		compress();
		for (size_t t = 0; t < 8; ++t) {
			if (block_team[t] != nullptr)
				block_team[t] = (const WORD*)block_team[t] + WORD_PER_BLOCK;
		}
	}
}

void SM3_SIMD_Engine::compress()
{
	__m256i SS1, SS2, TT1, TT2;

	__m256i mmA = _mm256_load_si256((__m256i const *)IV[0].data());
	__m256i mmB = _mm256_load_si256((__m256i const *)IV[1].data());
	__m256i mmC = _mm256_load_si256((__m256i const *)IV[2].data());
	__m256i mmD = _mm256_load_si256((__m256i const *)IV[3].data());
	__m256i mmE = _mm256_load_si256((__m256i const *)IV[4].data());
	__m256i mmF = _mm256_load_si256((__m256i const *)IV[5].data());
	__m256i mmG = _mm256_load_si256((__m256i const *)IV[6].data());
	__m256i mmH = _mm256_load_si256((__m256i const *)IV[7].data());

	for (size_t j = 0; j <= 15; ++j) {

		// SS1 = WORD_ROTATE_LEFT(WORD_ROTATE_LEFT(A, 12) + E + WORD_ROTATE_LEFT(T_0_15, j), 7);
		__m256i A_sll_12 = SIMD_word_rotate_sll(mmA, 12);
		__m256i T_sll_j = SIMD_word_rotate_sll(_mm256_set1_epi32(T_0_15), j);
		SS1 = mmE;
		SS1 = _mm256_add_epi32(SS1, _mm256_add_epi32(A_sll_12, T_sll_j));
		SS1 = SIMD_word_rotate_sll(SS1, 7);

		// SS2 = SS1 ^ WORD_ROTATE_LEFT(A, 12);
		SS2 = _mm256_xor_epi32(SS1, A_sll_12);

		// TT1 = FF_0_15(A, B, C) + D + SS2 + W_stroke[j];
		TT1 = SIMD_FF_0_15(mmA, mmB, mmC);
		TT1 = _mm256_add_epi32(TT1, mmD);
		TT1 = _mm256_add_epi32(TT1, SS2);
		TT1 = _mm256_add_epi32(TT1, _mm256_load_si256((__m256i const *)W_stroke[j].data()));

		// TT2 = GG_16_63(E, F, G) + H + SS1 + W[j];
		TT2 = SIMD_GG_0_15(mmE, mmF, mmG);
		TT2 = _mm256_add_epi32(TT2, mmH);
		TT2 = _mm256_add_epi32(TT2, SS1);
		TT2 = _mm256_add_epi32(TT2, _mm256_load_si256((__m256i const *)W[j].data()));

		// D = C;
		mmD = mmC;
		mmC = SIMD_word_rotate_sll(mmB, 9);
		mmB = mmA;
		mmA = TT1;
		mmH = mmG;
		mmG = SIMD_word_rotate_sll(mmF, 19);
		mmF = mmE;
		mmE = SIMD_P0(TT2);
	}

	for (size_t j = 16; j <= 63; ++j) {

		// SS1 = WORD_ROTATE_LEFT(WORD_ROTATE_LEFT(A, 12) + E + WORD_ROTATE_LEFT(T_16_63, j), 7);
		SS1 = mmE;
		__m256i A_sll_12 = SIMD_word_rotate_sll(mmA, 12);
		__m256i T_sll_j = SIMD_word_rotate_sll(_mm256_set1_epi32(T_16_63), j);
		SS1 = _mm256_add_epi32(SS1, _mm256_add_epi32(A_sll_12, T_sll_j));
		SS1 = SIMD_word_rotate_sll(SS1, 7);

		// SS2 = SS1 ^ WORD_ROTATE_LEFT(A, 12);
		SS2 = _mm256_xor_epi32(SS1, A_sll_12);

		// TT1 = FF_16_63(A, B, C) + D + SS2 + W_stroke[j];
		TT1 = SIMD_FF_16_63(mmA, mmB, mmC);
		TT1 = _mm256_add_epi32(TT1, mmD);
		TT1 = _mm256_add_epi32(TT1, SS2);
		TT1 = _mm256_add_epi32(TT1, _mm256_load_si256((__m256i const *)W_stroke[j].data()));

		// TT2 = GG_16_63(E, F, G) + H + SS1 + W[j];
		TT2 = SIMD_GG_16_63(mmE, mmF, mmG);
		TT2 = _mm256_add_epi32(TT2, mmH);
		TT2 = _mm256_add_epi32(TT2, SS1);
		TT2 = _mm256_add_epi32(TT2, _mm256_load_si256((__m256i const *)W[j].data()));

		// D = C;
		mmD = mmC;
		mmC = SIMD_word_rotate_sll(mmB, 9);
		mmB = mmA;
		mmA = TT1;
		mmH = mmG;
		mmG = SIMD_word_rotate_sll(mmF, 19);
		mmF = mmE;
		mmE = SIMD_P0(TT2);

	}

	_mm256_store_epi64(IV[0].data(), _mm256_xor_epi32(mmA, _mm256_load_si256((__m256i const *)IV[0].data())));
	_mm256_store_epi64(IV[1].data(), _mm256_xor_epi32(mmB, _mm256_load_si256((__m256i const *)IV[1].data())));
	_mm256_store_epi64(IV[2].data(), _mm256_xor_epi32(mmC, _mm256_load_si256((__m256i const *)IV[2].data())));
	_mm256_store_epi64(IV[3].data(), _mm256_xor_epi32(mmD, _mm256_load_si256((__m256i const *)IV[3].data())));
	_mm256_store_epi64(IV[4].data(), _mm256_xor_epi32(mmE, _mm256_load_si256((__m256i const *)IV[4].data())));
	_mm256_store_epi64(IV[5].data(), _mm256_xor_epi32(mmF, _mm256_load_si256((__m256i const *)IV[5].data())));
	_mm256_store_epi64(IV[6].data(), _mm256_xor_epi32(mmG, _mm256_load_si256((__m256i const *)IV[6].data())));
	_mm256_store_epi64(IV[7].data(), _mm256_xor_epi32(mmH, _mm256_load_si256((__m256i const *)IV[7].data())));
}

const char* SM3_SIMD_Engine::get_hash_str(size_t team)
{
	std::array<WORD, 8> rlt{ IV[0][team], IV[1][team], IV[2][team], IV[3][team], 
		IV[4][team], IV[5][team], IV[6][team], IV[7][team] };
	return word2string(rlt.data(), 8);
}
