#include <iostream>
#include "SM3_tyte.h"
#include "SM3_basic.h"
#include "SM3_naive.h"

using namespace std;

int main() {
	string msg("abc");

	void* blocks = nullptr; size_t blocklen;
	blocks = msg2blocks_with_padding(msg.c_str(), msg.length(), blocklen);

	cout << "Padding message: \n";
	const char* blockstr = nullptr;
	blockstr = word2string(blocks, blocklen * WORD_PER_BLOCK);
	cout << blockstr << endl;

	SM3_Naive_Engine engine;
	engine.msg_expansion((WORD*)blocks);

	cout << "Expansion: \n";
	cout << "W_0 to W_67: \n";
	cout << engine.get_W_str() << endl;
	cout << "W_stroke_0 to W_stroke_63: \n";
	cout << engine.get_W_stroke_str() << endl;
}