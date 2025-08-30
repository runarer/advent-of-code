#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>

std::vector<int> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<int> FileContent;
  std::string Line;

  while (std::getline(Input, Line))
    FileContent.push_back(std::stoi(Line));

  return FileContent;
}

auto SplittContainers(std::vector<int> Containers, int MaxValue) {
  std::vector<int> Fillers;
  std::vector<int> Base;

  std::sort(Containers.begin(), Containers.end());

  int Sum{0};
  for (int C : Containers) {
    Sum += C;
    if (Sum >= 150) {
      Base.emplace_back(C);
    } else {
      Fillers.emplace_back(C);
    }
  }
  return std::pair{Base, Fillers};
}

void DoSomething(std::vector<int> &Combination) {
  std::cout << '\n';
  for (int C : Combination) {
    std::cout << C << ' ';
  }
}

using vii = std::vector<int>::iterator;
void Combinations(const std::vector<int> &Containers, const int Pick,
                  const int MaxVolum, vii Start, std::vector<int> &Selected,
                  std::vector<int> &Counts) {
  int N_Left{Pick - int(Selected.size())};

  int Sum{0};
  for (int S : Selected)
    Sum += S;

  if (Sum > MaxVolum)
    return;
  if (Sum == MaxVolum) {
    ++Counts[MaxVolum];
    return;
  }

  // End state:
  if (N_Left == 0) {
    ++Counts[Sum];
  } else {
    for (vii It = Start; It != Containers.end(); ++It) {
      Selected.push_back(*It);
      Combinations(Containers, Pick, MaxVolum, It + 1, Selected, Counts);
      Selected.pop_back();
    }
  }
}

auto CountCombinations(std::vector<int> Containers, int MaxVolum) {
  auto [Base, Fillers]{SplittContainers(Containers, MaxVolum)};

  std::vector<int> CountFillers(MaxVolum + 1, 0); // Largest + 1, 0);
  std::vector<int> Selected{};

  for (int i{1}; i <= Fillers.size(); ++i) {
    Combinations(Fillers, i, MaxVolum, Fillers.begin(), Selected, CountFillers);
  }

  int MaxContainers{0};
  for (int Sum{0}; Sum < MaxVolum; ++MaxContainers) {
    Sum += Base[MaxContainers];
  }
  --MaxContainers;

  std::vector<int> BaseCounts(MaxVolum + 1, 0);
  Selected.clear();
  for (int i{1}; i <= MaxContainers; ++i) {
    Combinations(Base, i, MaxVolum, Base.begin(), Selected, BaseCounts);
  }

  int Count{BaseCounts[MaxVolum]};
  for (int i{1}; i < MaxVolum; ++i) {
    Count += CountFillers[i] * BaseCounts[MaxVolum - i];
  }
  return Count;
}

int FewestContainers(std::vector<int> Containers, int MaxVolum) {
  std::vector<int> Count(MaxVolum + 1, 0);
  std::vector<int> Selected{};

  int i{0};
  for (; i <= Containers.size(); ++i) {
    Combinations(Containers, i, MaxVolum, Containers.begin(), Selected, Count);
    if (Count[MaxVolum] > 0)
      break;
  }

  return Count[MaxVolum];
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

  //  Solve part 1
  std::optional<int> Part1{CountCombinations(Input, 150)};

  // Solve part 2
  std::optional<int> Part2{FewestContainers(Input, 150)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
