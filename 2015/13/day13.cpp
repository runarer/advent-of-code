#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <regex>
#include <unordered_map>

using HappinessTable =
    std::unordered_map<std::string, std::unordered_map<std::string, int>>;

std::vector<std::string> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<std::string> FileContent;
  std::string Line;

  while (std::getline(Input, Line))
    FileContent.push_back(Line);

  return FileContent;
}

auto ParseLine(std::string Line) {
  std::string Name1, Name2, GainLoss;
  int Points;

  std::regex Pattern{
      R"(([a-zA-Z]+) would (lose|gain) (\d+) happiness units by sitting next to ([a-zA-Z]+).)"};
  std::smatch Match;

  if (std::regex_match(Line, Match, Pattern)) {
    Name1 = Match[1];
    Name2 = Match[4];
    Points = std::stoi(Match[3]);
    if (Match[2] == "lose")
      Points *= -1;
  }

  return std::tuple{Name1, Name2, Points};
}

int MaxHappiness(std::vector<std::string> Lines) {
  HappinessTable Happiness;
  for (const auto &Line : Lines) {
    auto [Name1, Name2, Points]{ParseLine(Line)};
    Happiness[Name1][Name2] = Points;
  }

  std::vector<std::string> GuestList;
  for (const auto &[Key, _] : Happiness) {
    GuestList.emplace_back(Key);
  }
  std::sort(GuestList.begin(), GuestList.end());

  int MaxPoints{0};
  do {
    if (GuestList.front() > GuestList.back())
      break;
    int CurPoints{Happiness[GuestList.front()][GuestList.back()]};
    CurPoints += Happiness[GuestList.back()][GuestList.front()];
    for (int i{0}; i < GuestList.size() - 1; ++i) {
      CurPoints += Happiness[GuestList[i]][GuestList[i + 1]];
      CurPoints += Happiness[GuestList[i + 1]][GuestList[i]];
    }
    if (CurPoints > MaxPoints)
      MaxPoints = CurPoints;
  } while (std::next_permutation(GuestList.begin(), GuestList.end()));

  return MaxPoints;
}

int MaxHappinessWithMe(std::vector<std::string> Lines) {
  HappinessTable Happiness;
  for (const auto &Line : Lines) {
    auto [Name1, Name2, Points]{ParseLine(Line)};
    Happiness[Name1][Name2] = Points;
  }

  std::vector<std::string> GuestList;
  for (const auto &[Key, _] : Happiness) {
    GuestList.emplace_back(Key);
  }
  for (const auto &Guest : GuestList) {
    Happiness[Guest]["Me"] = 0;
    Happiness["Me"][Guest] = 0;
  }
  GuestList.emplace_back("Me");
  std::sort(GuestList.begin(), GuestList.end());

  int MaxPoints{0};
  do {
    if (GuestList.front() > GuestList.back())
      break;
    int CurPoints{Happiness[GuestList.front()][GuestList.back()]};
    CurPoints += Happiness[GuestList.back()][GuestList.front()];
    for (int i{0}; i < GuestList.size() - 1; ++i) {
      CurPoints += Happiness[GuestList[i]][GuestList[i + 1]];
      CurPoints += Happiness[GuestList[i + 1]][GuestList[i]];
    }
    if (CurPoints > MaxPoints)
      MaxPoints = CurPoints;
  } while (std::next_permutation(GuestList.begin(), GuestList.end()));

  return MaxPoints;
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
  std::optional<int> Part1{MaxHappiness(Input)};

  // Solve part 2
  std::optional<int> Part2{MaxHappinessWithMe(Input)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
