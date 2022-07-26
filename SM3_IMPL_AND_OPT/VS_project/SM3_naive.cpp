#include "SM3_naive.h"

#include <iostream>
using std::cout;
using std::endl;
using std::hex;

SM3_Naive_Engine::SM3_Naive_Engine()
{
	IV_A = IV0;
	IV_B = IV1;
	IV_C = IV2;
	IV_D = IV3;
	IV_E = IV4;
	IV_F = IV5;
	IV_G = IV6;
	IV_H = IV7;
	A = B = C = D = E = F = G = H = 0;
	W = std::array<WORD, 68>{};
	W_stroke = std::array<WORD, 64>{};
}

void SM3_Naive_Engine::msg_expansion(const WORD* block)
{
	for (size_t i = 0; i < 16; ++i) this->W[i] = block[i];
	for (size_t i = 16; i < 68; ++i) {
		WORD X = W[i - 16] ^ W[i - 9] ^ WORD_ROTATE_LEFT(W[i - 3], 15);
		cout << "W[i-16]: " << hex << W[i - 16] << 
			", W[i-9]: " << hex << W[i - 9] << 
			", W[i-3]: " << hex << W[i - 3] <<
			", W[i-3]<<<15: " << hex << WORD_ROTATE_LEFT(W[i - 3], 15) << endl;
		cout << "X: "<< hex << X << endl;
		WORD Y = WORD_ROTATE_LEFT(W[i - 13], 7);
		cout << "W[i-13]: " << W[i - 13] << ", Y: " << hex << Y << endl;
		this->W[i] = P1(X) ^ Y ^ W[i - 6];
		cout << "W[i-6]: " << W[i - 6] << endl;
		cout << "ANS: " << this->W[i] << endl;
	}
	for (size_t i = 0; i < 64; ++i) this->W_stroke[i] = W[i] ^ W[i + 4];
}

const char* SM3_Naive_Engine::get_W_str()
{
	return word2string((void*)this->W.data(), 68);
}

const char* SM3_Naive_Engine::get_W_stroke_str()
{
	return word2string((void*)this->W_stroke.data(), 64);
}


