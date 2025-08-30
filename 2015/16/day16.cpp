#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <regex>
#include <string>
#include <unordered_map>

std::vector<std::string> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<std::string> FileContent;
  std::string Line;

  while (std::getline(Input, Line))
    FileContent.push_back(Line);

  return FileContent;
}
std::unordered_map<std::string, int> Sue{
    {"children", 3}, {"cats", 7},    {"samoyeds", 2}, {"pomeranians", 3},
    {"akitas", 0},   {"vizslas", 0}, {"goldfish", 5}, {"trees", 3},
    {"cars", 2},     {"perfumes", 1}};

int FindSue(std::vector<std::string> Lines) {
  int RightSue{0};

  for (const auto &Line : Lines) {
    int SueNumber, Fact1Amount, Fact2Amount, Fact3Amount;
    std::string Fact1, Fact2, Fact3;

    const std::regex Pattern{
        R"(Sue (\d+): ([a-z]+): (\d+), ([a-z]+): (\d+), ([a-z]+): (\d+))"};
    std::smatch Match;

    if (std::regex_match(Line, Match, Pattern)) {
      SueNumber = std::stoi(Match[1]);
      Fact1 = Match[2];
      Fact1Amount = std::stoi(Match[3]);
      Fact2 = Match[4];
      Fact2Amount = std::stoi(Match[5]);
      Fact3 = Match[6];
      Fact3Amount = std::stoi(Match[7]);
    }

    if (Sue.contains(Fact1) && Sue[Fact1] != Fact1Amount) {
      continue;
    }
    if (Sue.contains(Fact2) && Sue[Fact2] != Fact2Amount) {
      continue;
    }
    if (Sue.contains(Fact3) && Sue[Fact3] != Fact3Amount) {
      continue;
    }
    RightSue = SueNumber;
  }
  return RightSue;
}

int FindRealSue(std::vector<std::string> Lines) {
  int RightSue{0};

  for (const auto &Line : Lines) {
    int SueNumber, Fact1Amount, Fact2Amount, Fact3Amount;
    std::string Fact1, Fact2, Fact3;

    const std::regex Pattern{
        R"(Sue (\d+): ([a-z]+): (\d+), ([a-z]+): (\d+), ([a-z]+): (\d+))"};
    std::smatch Match;

    if (std::regex_match(Line, Match, Pattern)) {
      SueNumber = std::stoi(Match[1]);
      bool FoundSue{true};

      for (auto It{Match.begin() + 2}; It < Match.end(); It += 2) {
        const std::string Fact{(*It)};
        const int FactAmount{std::stoi(*(It + 1))};
        if (Fact == "cats" || Fact == "trees") {
          if (Sue[Fact] >= FactAmount) {
            FoundSue = false;
          }
        } else if (Fact == "pomeranians" || Fact == "goldfish") {
          if (Sue[Fact] <= FactAmount) {
            FoundSue = false;
          }
        } else if (Sue.contains(Fact) && Sue[Fact] != FactAmount) {
          FoundSue = false;
        }
        if (!FoundSue) {
          break;
        }
      }
      if (!FoundSue)
        continue;
    }

    RightSue = SueNumber;
  }
  return RightSue;
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
  std::optional<int> Part1{FindSue(Input)};

  // Solve part 2
  std::optional<int> Part2{FindRealSue(Input)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
