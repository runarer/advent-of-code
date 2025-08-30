#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <optional>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

// This Method needs error handling. Will throw exceptions.
std::vector<std::string> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<std::string> FileContent;
  std::string Line;

  while (std::getline(Input, Line))
    FileContent.push_back(Line);

  return FileContent;
}

using Graph =
    std::unordered_map<std::string, std::unordered_map<std::string, int>>;

auto ParseLine(const std::string &Line) {
  std::string City1;
  std::string City2;
  std::string Ignore;
  int Distance;

  std::istringstream LineS{Line};

  LineS >> City1;
  LineS >> Ignore;
  LineS >> City2;
  LineS >> Ignore;
  LineS >> Distance;

  return std::tuple{City1, City2, Distance};
}

void AddCities(Graph &Cities, const std::string &City1,
               const std::string &City2, int Distance) {
  if (!Cities.contains(City1))
    Cities[City1];
  if (!Cities.contains(City2))
    Cities[City2];

  Cities[City1][City2] = Distance;
  Cities[City2][City1] = Distance;
}

int CalculateDistance(Graph &Cities, std::vector<std::string> &AllCities) {
  int TotalDistance{0};

  for (int i{1}; i < AllCities.size(); ++i) {
    TotalDistance += Cities[AllCities[i - 1]][AllCities[i]];
  }

  return TotalDistance;
}

auto FindRoutes(const std::vector<std::string> &Lines) {
  Graph Cities;
  std::vector<std::string> AllCities;
  int Shortest{std::numeric_limits<int>::max()};
  int Longest{0};

  for (const auto &Line : Lines) {
    auto [City1, City2, Distance]{ParseLine(Line)};
    AddCities(Cities, City1, City2, Distance);
  }

  for (const auto &[City, _] : Cities) {
    AllCities.emplace_back(City);
  }

  do {
    if (AllCities.front() > AllCities.back())
      continue;
    const int Dist{CalculateDistance(Cities, AllCities)};
    if (Dist < Shortest)
      Shortest = Dist;
    if (Dist > Longest)
      Longest = Dist;
  } while (std::next_permutation(AllCities.begin(), AllCities.end()));

  return std::pair{Shortest, Longest};
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

  std::vector<std::string> Input{GetFileContent(File.path().string())};

  //  Solve part 1
  auto [Shortest, Longest]{FindRoutes(Input)};
  std::optional<int> Part1{Shortest};

  // Solve part 2
  std::optional<int> Part2{Longest};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
