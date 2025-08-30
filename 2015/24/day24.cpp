#include <cstdint>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <numeric>
#include <optional>
#include <ranges>
#include <vector>

// Jeg vet ikke hvorfor det fungerer uten å sjekke om resterende tall kan
// kombinerers til to eller tre partisjoner. Tror det har med primtall å gjøre.
//
//

// This Method needs error handling. Will throw exceptions.
// tellg() returnerer posisjonen i streamen. Siden vi har satt den til
// eof med std::ios::ate så kan vi bruke tellg() med en gang
std::vector<int> GetFileContent(const std::string &FileName) {
  std::vector<int> Numbers;

  std::ifstream Input{FileName};
  std::string In;

  while (Input >> In) {
    Numbers.emplace_back(std::stoi(In));
  }

  return Numbers;
}

template <typename T> void PrintVec(const std::vector<T> &Vec) {
  for (const auto &I : Vec)
    std::cout << I << ' ';
  std::cout << '\n';
}
/*
std::vector<int> RemoveElements(const std::vector<int> &C,
                                const std::vector<int> &S) {
  std::vector<int> Left{};
  auto It2{S.begin()};
  for (auto It1{C.begin()}; It1 != C.end(); ++It1) {
    if (It2 != S.end() && *It1 == *It2) {
      ++It2;
    } else {
      Left.emplace_back(*It1);
    }
  }
  return Left;
}
*/

using vii = std::vector<int>::iterator;
/*
bool Combi(const std::vector<int> &Containers, const int Pick, vii Start,
           std::vector<int> &Selected, const int Target) {
  int N_Left{Pick - int(Selected.size())};

  // End state:
  if (N_Left == 0) {
    int Sum{0};
    for (int S : Selected)
      Sum += S;
    if (Sum == Target) {
      // PrintVec(Selected);
      return true;
    }
    return false;
  } else {
    for (vii It = Start; It != Containers.end(); ++It) {
      Selected.push_back(*It);
      if (Combi(Containers, Pick, It + 1, Selected, Target))
        return true;
      Selected.pop_back();
    }
  }
  return false;
}
*/
/*
bool GotSubPartision(std::vector<int> &C, const int StorageSize,
                     const int MinSize) {
  std::vector<int> Temp{};

  for (int I{MinSize}; I < C.size() - MinSize; ++I) {
    if (Combi(C, I, C.begin(), Temp, StorageSize))
      return true;
  }
  return false;
}
*/
/*
void Combinations(
    const std::vector<int> &Containers, const int Pick, vii Start,
    std::vector<int> &Selected, const int Target,
    std::vector<std::pair<uint64_t, std::vector<int>>> &SmallestStorage) {
  int N_Left{Pick - int(Selected.size())};

  // End state:
  if (N_Left == 0) {
    int Sum{0};
    for (int S : Selected)
      Sum += S;
    if (Sum == Target) {
      // What is left need to be made into
      std::vector<int> Left{RemoveElements(Containers, Selected)};
      if (GotSubPartision(Left, Target, Pick)) {
        // std::cout << "------------------------\n";
        // PrintVec(Selected);
        // PrintVec(Left);
        uint64_t Prod{std::reduce(Selected.begin(), Selected.end(), uint64_t(1),
                                  std::multiplies{})};
        // std::cout << Prod << '\n';
        SmallestStorage.emplace_back(Prod, Selected);
      }
    }
  } else {
    for (vii It = Start; It != Containers.end(); ++It) {
      Selected.push_back(*It);
      Combinations(Containers, Pick, It + 1, Selected, Target, SmallestStorage);
      Selected.pop_back();
    }
  }
}
*/

int GetStorageSize(const std::vector<int> &Packages) {
  return std::reduce(Packages.begin(), Packages.end()) / 3;
}

int GetMinPackages(const std::vector<int> &Packages, const int StorageSize) {
  int MinPackages{0};
  int TempSum{0};

  for (auto It{std::views::reverse(Packages).begin()}; TempSum < StorageSize;
       ++It) {
    TempSum += *It;
    ++MinPackages;
  }
  return MinPackages;
}

int GetMaxPackages(const std::vector<int> &Packages, const int StorageSize) {
  int MaxPackages{0};
  int TempSum{0};

  for (auto It{Packages.begin()}; TempSum < StorageSize; ++It) {
    TempSum += *It;
    ++MaxPackages;
  }
  return MaxPackages - 1;
}
/*
uint64_t GetSmallestStorage(std::vector<int> Packages) {
  const int StorageSize{GetStorageSize(Packages)};
  const int MaxPackages{GetMaxPackages(Packages, StorageSize)};
  const int MaxSmallest{int(Packages.size()) / 3};
  const int MinPackages{GetMinPackages(Packages, StorageSize)};

  std::vector<std::pair<uint64_t, std::vector<int>>> SmallestStorage{};
  for (int I{MinPackages}; I <= MaxSmallest; ++I) {
    std::vector<int> Selected{};
    Combinations(Packages, I, Packages.begin(), Selected, StorageSize,
                 SmallestStorage);
    if (SmallestStorage.size()) {
      break;
    }
  }

  uint64_t Max{std::numeric_limits<uint64_t>::max()};
  for (const auto &[Q, S] : SmallestStorage) {
    Max = std::min(Max, Q);
    // std::cout << Q << '|';
    // PrintVec(S);
  }

  return Max;
}
*/

void Combinations4(
    const std::vector<int> &Containers, const int Pick, vii Start,
    std::vector<int> &Selected, const int Target,
    std::vector<std::pair<uint64_t, std::vector<int>>> &SmallestStorage) {
  int N_Left{Pick - int(Selected.size())};

  // End state:
  if (N_Left == 0) {
    int Sum{0};
    for (int S : Selected)
      Sum += S;
    if (Sum == Target) {
      // What is left need to be made into
      uint64_t Prod{std::reduce(Selected.begin(), Selected.end(), uint64_t(1),
                                std::multiplies{})};
      SmallestStorage.emplace_back(Prod, Selected);
    }
  } else {
    for (vii It = Start; It != Containers.end(); ++It) {
      Selected.push_back(*It);
      Combinations4(Containers, Pick, It + 1, Selected, Target,
                    SmallestStorage);
      Selected.pop_back();
    }
  }
}
void Combinations3(
    const std::vector<int> &Containers, const int Pick, vii Start,
    std::vector<int> &Selected, const int Target,
    std::vector<std::pair<uint64_t, std::vector<int>>> &SmallestStorage) {
  int N_Left{Pick - int(Selected.size())};

  // End state:
  if (N_Left == 0) {
    int Sum{0};
    for (int S : Selected)
      Sum += S;
    if (Sum == Target) {
      uint64_t Prod{std::reduce(Selected.begin(), Selected.end(), uint64_t(1),
                                std::multiplies{})};
      SmallestStorage.emplace_back(Prod, Selected);
    }
  } else {
    for (vii It = Start; It != Containers.end(); ++It) {
      Selected.push_back(*It);
      Combinations3(Containers, Pick, It + 1, Selected, Target,
                    SmallestStorage);
      Selected.pop_back();
    }
  }
}

uint64_t FourContainer(std::vector<int> Packages) {
  // std::ranges::sort(Packages, std::greater());
  const int StorageSize{std::reduce(Packages.begin(), Packages.end()) / 4};
  const int MaxPackages{GetMaxPackages(Packages, StorageSize)};
  const int MaxSmallest{int(Packages.size()) / 4};
  const int MinPackages{GetMinPackages(Packages, StorageSize)};

  std::vector<std::pair<uint64_t, std::vector<int>>> SmallestStorage{};
  for (int I{MinPackages}; I <= MaxSmallest; ++I) {
    std::vector<int> Selected{};
    Combinations4(Packages, I, Packages.begin(), Selected, StorageSize,
                  SmallestStorage);
    if (SmallestStorage.size()) {
      break;
    }
  }

  // Sort by smallest Q
  std::ranges::sort(SmallestStorage,
                    [](const std::pair<uint64_t, std::vector<int>> &A,
                       const std::pair<uint64_t, std::vector<int>> &B) {
                      return A.first < B.first;
                    });

  return SmallestStorage[0].first;
}

uint64_t ThreeContainer(std::vector<int> Packages) {
  // std::ranges::sort(Packages, std::greater());
  const int StorageSize{std::reduce(Packages.begin(), Packages.end()) / 3};
  const int MaxPackages{GetMaxPackages(Packages, StorageSize)};
  const int MaxSmallest{int(Packages.size()) / 3};
  const int MinPackages{GetMinPackages(Packages, StorageSize)};

  std::vector<std::pair<uint64_t, std::vector<int>>> SmallestStorage{};
  for (int I{MinPackages}; I <= MaxSmallest; ++I) {
    std::vector<int> Selected{};
    Combinations3(Packages, I, Packages.begin(), Selected, StorageSize,
                  SmallestStorage);
    if (SmallestStorage.size()) {
      break;
    }
  }

  // Sort by smallest Q
  std::ranges::sort(SmallestStorage,
                    [](const std::pair<uint64_t, std::vector<int>> &A,
                       const std::pair<uint64_t, std::vector<int>> &B) {
                      return A.first < B.first;
                    });

  return SmallestStorage[0].first;
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

  std::vector<int> Input{GetFileContent(File.path().string())};
  int StorageSize{GetStorageSize(Input)};

  //  Solve part 1
  std::optional<uint64_t> Part1{ThreeContainer(Input)};

  // Solve part 2
  std::optional<uint64_t> Part2{FourContainer(Input)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
