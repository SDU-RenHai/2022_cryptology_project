#define _CRT_SECURE_NO_WARNINGS

#include "SM3_type.h"
#include "SM3_basic.h"
#include "SM3_naive.h"
#include "SM3_simd.h"

#include <fstream>
#include <iostream>
#include <chrono>
#include <filesystem>

using namespace std;
using recursive_directory_iterator = std::filesystem::recursive_directory_iterator;
using namespace std::chrono;

extern string help_str;
extern string wrong_arg;
extern string wrong_no_file;
extern string conflict_arg;
extern string wrong_open_file;

enum {UNCERTAIN, PERFORMANCE, TEST};
int runtype = UNCERTAIN;

const char* output_file = nullptr;
FILE* fp = stdout;

void performance();
void sm3_test(const string& msg);

int main(int argc, char* const argv[]) {
	
	string msg1 = "abc";
	string msg2 = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd";
	sm3_test(msg1);
	sm3_test(msg2);

	performance();
	return 0;
}

void sm3_test(const string& msg)
{
	SM3_Naive_Engine native_engine;
	SM3_SIMD_Engine  simd_engine;
	fprintf(fp, "Use native to hash '%s': \n", msg.c_str());
	native_engine.sm3(msg);
	fprintf(fp, "%s", native_engine.get_hash_str());
	fprintf(fp, "Use SIMD to hash '%s': \n", msg.c_str());
	array<const void*, 8> blocks{};
	size_t blocklen = 0;
	void* block = msg2blocks_with_padding(msg.c_str(), msg.length(), blocklen);
	blocks[0] = (const void*)block;
	simd_engine.push_msg(blocks, blocklen);
	simd_engine.sm3();
	fprintf(fp, "%s", simd_engine.get_hash_str(0));
}

void performance()
{
	for (const auto& dirEntry : recursive_directory_iterator("./test")) {
		if (dirEntry.is_directory() == true)	continue;
		string path_str = dirEntry.path().string();
		fprintf(stdout, "Open and read file %s...\n", path_str.c_str());
		ifstream infile(path_str);

		vector<string> msg_vec;
		string msg;
		while (infile >> msg) {
			msg_vec.push_back(msg);
		}
		fprintf(stdout, "Get %zd messages in total.\n", msg_vec.size());

		// Naive
		unsigned long long duration = 0;
		fprintf(stdout, "Run naive for 100 times...");
		SM3_Naive_Engine naive_engine;
		for (size_t i = 0; i < 100; ++i) {
			for (const auto& m : msg_vec) {
				size_t blocklen = 0;
				auto block = msg2blocks_with_padding(m.c_str(), m.length(), blocklen);
				auto start = high_resolution_clock::now();
				naive_engine.sm3((const WORD*)block, blocklen);
				auto stop = high_resolution_clock::now();
				duration += duration_cast<microseconds>(stop - start).count();
			}
		}
		fprintf(stdout, "Done.   ");
		fprintf(stdout, "Time Duration: %llu(micro_sec)\n", duration);

		// SIMD
		duration = 0;
		fprintf(stdout, "Run SIMD for 100 times...");
		SM3_SIMD_Engine simd_engine;
		for (size_t i = 0; i < 100; ++i) {
			size_t msg_len = msg_vec.size();
			size_t msg_idx = 0;
			while (msg_idx < msg_len) {
				array<const void*, 8> block_team;
				size_t blocklen = 0;
				for (size_t t = 0; t < 8; ++t) {
					block_team[t] = 
						msg2blocks_with_padding(msg_vec[msg_idx].c_str(), msg_vec[msg_idx].length(), blocklen);
					++msg_idx;
				}
				simd_engine.push_msg(block_team, blocklen);
				auto start = high_resolution_clock::now();
				simd_engine.sm3();
				auto stop = high_resolution_clock::now();
				duration += duration_cast<microseconds>(stop - start).count();
			}
		}
		fprintf(stdout, "Done.   ");
		fprintf(stdout, "Time Duration: %llu(micro_sec)\n", duration);
	}
}
