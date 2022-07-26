#include <iostream>
#include "SM3_tyte.h"
#include "SM3_basic.h"
#include "SM3_naive.h"

using namespace std;

int main() {
	string msg("abc");

	void* blocks = nullptr; size_t blocklen;
	blocks = msg2blocks_with_padding(msg.c_str(), msg.length(), blocklen);

	SM3_Naive_Engine engine;
	engine.msg_expansion((WORD*)blocks);
	engine.compress();

	cout << engine.get_register_str();
	cout << engine.get_IV_str();
}