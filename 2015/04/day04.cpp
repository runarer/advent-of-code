#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>

// This Method needs error handling. Will throw exceptions.
//
// tellg() returnerer posisjonen i streamen. Siden vi har satt den til
// eof med std::ios::ate så kan vi bruke tellg() med en gang
std::string GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName, std::ios::binary | std::ios::ate};
  /*if(!Input.is_open()) {
    throw ;
  }*/

  auto FileSize = Input.tellg();
  Input.seekg(std::ios::beg); // Reset for read
  std::string FileContent(FileSize, 0);
  Input.read(&FileContent[0], FileSize);

  Input.close();

  return FileContent;
}
/*
inline unsigned int F(unsigned int B, unsigned int C, unsigned int D) {
  return (B & C) | (~B & D);
};
inline unsigned int G(unsigned int B, unsigned int C, unsigned int D) {
  return (B & D) | (C & ~D);
}
inline unsigned int H(unsigned int B, unsigned int C, unsigned int D) {
  return B ^ C ^ D;
}
inline unsigned int I(unsigned int B, unsigned int C, unsigned int D) {
  return C ^ (B | ~D);
}
inline unsigned int RotateLeft(unsigned int X, int n) {
  return (X << n) | (X >> (32 - n));
}
*/
uint32_t leftRotate32bits(uint32_t n, std::size_t rotate) {
  return (n << rotate) | (n >> (32 - rotate));
}
/*
void FillChunk(std::string_view Key, std::array<unsigned char, 64> &HashInput) {
  int pos{0};

  // Insert the message
  for (const char &C : Key) {
    HashInput[pos] = C;
    ++pos;
  }

  // Insert 1
  HashInput[pos] = 0x80;

  // The length will not be more than 255.
  // This should be some kind of modulo, but i dont think it matter
  // with short messages.
  unsigned long long int Bits{};
  Bits = (Key.size() * 8) & 0xffffffffffffffff;
  std::memcpy(&HashInput[56], &Bits, sizeof Bits);
}

void MD5(std::string_view Key) {
  // These values are from wikipedia
  std::array s{7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
               5, 9,  14, 20, 5, 9,  14, 20, 5, 9,  14, 20, 5, 9,  14, 20,
               4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
               6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21};

  std::array<unsigned int, 64> K{
      0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a,
      0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
      0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340,
      0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
      0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8,
      0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
      0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa,
      0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
      0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92,
      0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
      0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391};

  unsigned int A{0x67452301};
  unsigned int B{0xefcdab89};
  unsigned int C{0x98badcfe};
  unsigned int D{0x10325476};

  std::cout << std::hex << A << B << C << D << '\n';

  std::array<unsigned char, 64> HashInput{};
  FillChunk(Key, HashInput);

  for (int i{0}; i < 64; ++i) {
    unsigned int F{};
    unsigned int g{};
    if (i <= 15) {
      F = (B & C) | (~B & D);
      g = i;
    } else if (i <= 31) {
      F = (B & D) | (C & ~D);
      g = (5 * i + 1) % 16;

    } else if (i <= 47) {
      F = B ^ C ^ D;
      g = (3 * i + 5) % 16;
    } else {
      F = C ^ (B | ~D);
      g = (7 * i) % 16;
    }
    unsigned int M;
    std::memcpy(&M, &HashInput[g * 4], sizeof M);
    F = F + A + K[i] + M;
    A = D;
    D = C;
    C = B;
    B = B + RotateLeft(F, s[i]);
  }

  // for (const char C : HashInput)
  //   std::cout << C << '\n';
  std::cout << std::hex << A << B << C << D;
}
*/

bool isBigEndian() {
  union {
    uint32_t i;
    std::array<char, 4> c;
  } bint = {0x01020304};
  return bint.c[0] == 1;
}

uint32_t toLittleEndian32(uint32_t n) {
  if (!isBigEndian()) {
    return ((n << 24) & 0xFF000000) | ((n << 8) & 0x00FF0000) |
           ((n >> 8) & 0x0000FF00) | ((n >> 24) & 0x000000FF);
  }
  // Machine works on little endian, no need to change anything
  return n;
}

uint64_t toLittleEndian64(uint64_t n) {
  if (!isBigEndian()) {
    return ((n << 56) & 0xFF00000000000000) | ((n << 40) & 0x00FF000000000000) |
           ((n << 24) & 0x0000FF0000000000) | ((n << 8) & 0x000000FF00000000) |
           ((n >> 8) & 0x00000000FF000000) | ((n >> 24) & 0x0000000000FF0000) |
           ((n >> 40) & 0x000000000000FF00) | ((n >> 56) & 0x00000000000000FF);
  }
  return n;
}

void *hash_bs(const void *input_bs, uint64_t input_size) {
  // input_bs er typeløs, vi kaster om til byte.
  auto *input = static_cast<const uint8_t *>(input_bs);

  // Samme som fra wikipedia.
  std::array<uint32_t, 64> s = {
      7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
      5, 9,  14, 20, 5, 9,  14, 20, 5, 9,  14, 20, 5, 9,  14, 20,
      4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
      6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21};

  std::array<uint32_t, 64> K = {
      3614090360, 3905402710, 606105819,  3250441966, 4118548399, 1200080426,
      2821735955, 4249261313, 1770035416, 2336552879, 4294925233, 2304563134,
      1804603682, 4254626195, 2792965006, 1236535329, 4129170786, 3225465664,
      643717713,  3921069994, 3593408605, 38016083,   3634488961, 3889429448,
      568446438,  3275163606, 4107603335, 1163531501, 2850285829, 4243563512,
      1735328473, 2368359562, 4294588738, 2272392833, 1839030562, 4259657740,
      2763975236, 1272893353, 4139469664, 3200236656, 681279174,  3936430074,
      3572445317, 76029189,   3654602809, 3873151461, 530742520,  3299628645,
      4096336452, 1126891415, 2878612391, 4237533241, 1700485571, 2399980690,
      4293915773, 2240044497, 1873313359, 4264355552, 2734768916, 1309151649,
      4149444226, 3174756917, 718787259,  3951481745};

  // The initial 128-bit state
  uint32_t a0 = 0x67452301, A = 0;
  uint32_t b0 = 0xefcdab89, B = 0;
  uint32_t c0 = 0x98badcfe, C = 0;
  uint32_t d0 = 0x10325476, D = 0;

  // Step 1: Process the bytestring.
  // Compute padded message size for memory allocation.
  uint64_t padded_message_size = 0;
  if (input_size % 64 < 56) {
    // Hvis vi er under 56, så betyr det at det er plass til bit_size i siste
    // block
    padded_message_size = input_size + 64 - (input_size % 64);
  } else {
    // Ikke plass i siste block, vi må legge til en block til.
    padded_message_size = input_size + 128 - (input_size % 64);
  }

  // Her ligger meldingen lagret.
  std::vector<uint8_t> padded_message(padded_message_size);

  // Legg til den orginale meldingen. input er en peker, input + input_size
  // blir også en peker.
  std::copy(input, input + input_size, padded_message.begin());

  // Legg til en 1 etterfulgt av 0'er.
  // Gjort en liten modifikasjon.
  padded_message[input_size] = 1 << 7; // 1000000
  for (uint64_t i = input_size + 1; i % 64 != 56; i++) {
    padded_message[i] = 0;
  }

  // We add the 64-bit size of message.
  // Must be little endian.
  uint64_t input_bitsize_le = toLittleEndian64(input_size * 8);
  for (uint64_t i = 0; i < 8; i++) {
    padded_message[padded_message_size - 8 + i] =
        (input_bitsize_le >> (56 - 8 * i)) & 0xff;
  }

  std::array<uint32_t, 16> blocks{};

  for (uint32_t chunk = 0; chunk * 64 < padded_message_size; chunk++) {
    // First build the 16 32-bits blocks from chunk.
    for (uint8_t bid = 0; bid < 16; bid++) {
      blocks[bid] = 0;
      // Having to build a 32-bit word from 4-bit words
      // Add each and shift them to the left.
      for (uint8_t cid = 0; cid < 4; cid++) {
        blocks[bid] =
            (blocks[bid] << 8) + padded_message[chunk * 64 + bid * 4 + cid];
      }
    }
    A = a0;
    B = b0;
    C = c0;
    D = d0;

    // Main "Hash" loop
    for (uint8_t i = 0; i < 64; i++) {
      uint32_t F = 0, g = 0;
      if (i < 16) {
        F = (B & C) | ((~B) & D);
        g = i;
      } else if (i < 32) {
        F = (D & B) | ((~D) & C);
        g = (5 * i + 1) % 16;
      } else if (i < 48) {
        F = B ^ C ^ D;
        g = (3 * i + 5) % 16;
      } else {
        F = C ^ (B | (~D));
        g = (7 * i) % 16;
      }
      F += A + K[i] + toLittleEndian32(blocks[g]);

      A = D;
      D = C;
      C = B;
      B += leftRotate32bits(F, s[i]);
    }
    a0 += A;
    b0 += B;
    c0 += C;
    d0 += D;
  }

  // Build signature from state
  auto *sig = new uint8_t[16];
  for (uint8_t i = 0; i < 4; i++) {
    sig[i] = (a0 >> (8 * i)) & 0xFF;
    sig[i + 4] = (b0 >> (8 * i)) & 0xFF;
    sig[i + 8] = (c0 >> (8 * i)) & 0xFF;
    sig[i + 12] = (d0 >> (8 * i)) & 0xFF;
  }
  return sig;
}

std::string sig2hex(void *sig) {
  const char *hexChars = "0123456789abcdef";
  auto *intsig = static_cast<uint8_t *>(sig);
  std::string hex = "";
  // Tar en og en byte, tar de fire første og gjør om til et tall mellom 0-15
  // Bruker dette til å slå opp i hexChars for riktig hex tegn.
  for (uint8_t i = 0; i < 16; i++) {
    hex.push_back(hexChars[(intsig[i] >> 4) & 0xF]);
    hex.push_back(hexChars[(intsig[i]) & 0xF]);
  }
  return hex;
}

void *hash(const std::string &message) {
  return hash_bs(&message[0], message.size());
}

int FindNumber(const std::string &Input, const std::string &Start) {
  int Number{0};
  std::string Hex{};
  do {
    ++Number;
    std::string ToCheck{Input + std::to_string(Number)};

    void *Signature = hash(ToCheck);
    Hex = sig2hex(Signature);

  } while (!Hex.starts_with(Start));
  std::cout << Hex << std::endl;
  return Number;
}

int main(int argc, char *argv[]) {
  if (argc <= 1) {
    std::cerr << "Usage: " << argv[0] << " <input file>" << std::endl;
    return 1;
  }

  std::filesystem::directory_entry File{argv[1]};
  if (!File.exists()) {
    std::cerr << argv[1] << " is not a file. " << std::endl;
    return 1;
  }

  //  std::string Input{GetFileContent(File.path().string())};

  std::string Input{};
  std::ifstream InFile{File.path()};
  std::getline(InFile, Input);

  //  Solve part 1
  std::optional<int> Part1{FindNumber(Input, "00000")};

  // Solve part 2
  std::optional<int> Part2{FindNumber(Input, "000000")};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
