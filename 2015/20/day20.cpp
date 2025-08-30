#include <array>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>
#include <unordered_set>
#include <vector>
template <typename T> void printVecL(std::vector<T> Vec) {
  std::cout << "\n----------------------\n";
  for (const auto &L : Vec)
    std::cout << L << '\n';
  std::cout << "----------------------\n";
}

template <typename T> void printVec(std::vector<T> Vec) {
  std::cout << "\n----------------------\n";
  for (const auto &L : Vec)
    std::cout << L << ' ';
  std::cout << "\n----------------------\n";
}

template <typename T, int N> void printArray(std::array<T, N> Vec) {
  std::cout << "\n----------------------\n";
  for (const auto &L : Vec)
    std::cout << L << ' ';
  std::cout << "\n----------------------\n";
}

template <typename T> void printSet(std::unordered_set<T> Vec) {
  std::cout << "\n----------------------\n";
  for (const auto &L : Vec)
    std::cout << L << ' ';
  std::cout << "\n----------------------\n";
}

auto GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::string Line;

  std::getline(Input, Line);

  return std::stoi(Line);
}

long long int GiftsForHouse(long long int N) {
  long long int Gifts{1};

  int Two{2};
  while (N >= 4) {
    if (N % 2 == 0) {
      Two *= 2;
      N /= 2;
      if (N == 2) {
        Two *= 2;
        N = 0;
      }
    } else {
      break;
    }
  }

  if (Two > 2) {
    Gifts *= (Two - 1);
  }

  int Z{3};
  int Zeds{Z};
  while (N >= Z * Z) {
    if (N % Z == 0) {
      Zeds *= Z;
      N /= Z;
      if (N == Z) {
        Zeds *= Z;
        Gifts *= (Zeds - 1) / (Z - 1);
        N = 0;
        break;
      }
      if (N > Z && N < Z * Z) {
        Gifts *= (Zeds - 1) / (Z - 1);
      }
    } else {
      if (Zeds > Z) {
        // We have a factor
        Gifts *= (Zeds - 1) / (Z - 1);
      }
      Z += 2;
      Zeds = Z;
    }
  }

  if (N > 1) {
    Gifts *= ((N * N) - 1) / (N - 1);
  }
  return Gifts;
}

int MinHouses(const int MinGifts) {
  int House{0};

  for (int i{MinGifts / 8}; i < (MinGifts / 2); i += 2) {
    long long int Gifts{GiftsForHouse(i)};
    if (Gifts >= MinGifts) {
      House = i;
      break;
    }
  }

  return House;
}

auto GetGifts(int HouseNr) {
  long long int Gifts{0};

  for (int i{1}; i * i <= HouseNr; ++i) {
    if (HouseNr % i == 0) {
      //  Check i and N/i
      if (i * 50 > HouseNr)
        Gifts += i;

      int Par{HouseNr / i};
      if (Par != i && Par * 50 > HouseNr)
        Gifts += Par;
    }
  }

  return Gifts * 11;
}

int MinHouseAtElven(int Start, int MinGifts) {
  int House{0};

  for (int i{Start}; i < (MinGifts); ++i) {
    long long int Gifts{GetGifts(i)};
    if (Gifts >= MinGifts) {
      House = i;
      break;
    }
  }

  return House;
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
  int Input{GetFileContent(File.path().string())};

  //   Solve part 1
  std::optional<int> Part1{MinHouses(Input / 10)};

  // Solve part 2
  std::optional<int> Part2{MinHouseAtElven(Part1.value(), Input)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
