
#include "SM3_basic.h"
#include <algorithm>
#include <cstring>

char int2char(uint8_t input)
{
	static const char lookup[] = {
		'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'
	};
	return lookup[input];
}

void* msg2blocks_with_padding(const char* msg, size_t msglen, size_t& blocklen)
{
	size_t fieldslen = msglen + 1 + 8;
	size_t paddinglen = BYTE_PER_BLOCK - (fieldslen % BYTE_PER_BLOCK);
	size_t totallen = fieldslen + paddinglen;

	void* blocks = (void*)malloc(sizeof(uint8_t) * totallen);
	if (blocks == nullptr)	return nullptr;
	blocklen = totallen / BYTE_PER_BLOCK;

	// Message.
	memcpy(blocks, msg, msglen);
	// 0x80 at the end of message.
	*((uint8_t*)blocks + msglen) = 0x80;
	// 8-byte message length.
	uint8_t* lenpad_begin = (uint8_t*)blocks + (totallen - 8);
	uint8_t* lenpad_end = lenpad_begin + 8;
	*((uint64_t*)lenpad_begin) = (uint64_t)msglen * 8;
	std::reverse(lenpad_begin, lenpad_end);
	// 0 for padding.
	memset((uint8_t*)blocks + (msglen + 1), 0x00, paddinglen);

	// Rotate all word for big-endian.
	size_t wordlen = totallen / BYTE_PER_WORD;
	for (size_t i = 0; i < wordlen; ++i) {
		uint8_t* beg = (uint8_t*)((WORD*)blocks + i);
		uint8_t* end = (uint8_t*)((WORD*)blocks + i + 1);
		std::reverse(beg, end);
	}

	return blocks;
}

const char* word2string(const void* buffer, size_t wordlen)
{
	char* output = (char*)malloc(wordlen * 9 + 1);
	if (output == nullptr)	return nullptr;

	// Rotate for small-endian.
	char* rotate_buf = (char*)malloc(wordlen * BYTE_PER_WORD);
	if (rotate_buf == nullptr)	return nullptr;
	memcpy(rotate_buf, buffer, wordlen * BYTE_PER_WORD);
	for (size_t i = 0; i < wordlen; ++i) {
		uint8_t* beg = (uint8_t*)((uint32_t*)rotate_buf + i);
		uint8_t* end = (uint8_t*)((uint32_t*)rotate_buf + i + 1);
		std::reverse(beg, end);
	}

	char* bufpos = output;
	size_t bytelen = wordlen * BYTE_PER_WORD;
	for (size_t i = 0; i < bytelen; ++i) {
		uint8_t byteval = *((uint8_t*)rotate_buf + i);
		*(bufpos++) = int2char((byteval & 0xF0) >> 4);
		*(bufpos++) = int2char(byteval & 0x0F);
		if ((i + 1) % 32 == 0)		*(bufpos++) = '\n';
		else if ((i + 1) % 4 == 0)	*(bufpos++) = ' ';
	}


	*bufpos = '\0';		// end of string.
	return (const char*)output;
}


