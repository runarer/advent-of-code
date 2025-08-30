#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <regex>
#include <string>

auto GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::string Line;
  int Row{}, Col{};

  if (std::getline(Input, Line)) {

    const std::regex Pattern{
        R"(To continue, please consult the code grid in the manual\.  Enter the code at row (\d+), column (\d+)\.)"};

    std::smatch Match;
    if (std::regex_match(Line, Match, Pattern)) {
      Row = std::stoi(Match[1]);
      Col = std::stoi(Match[2]);
    }
  }
  return std::pair{Row, Col};
}

long long int F(int TRow, int TCol) {
  int Row{1};
  int Col{1};
  int NextStart{1};
  long long int Code{20151125};

  while (Row != TRow || Col != TCol) {
    Code *= 252533;
    Code %= 33554393;
    if (Row == 1) {
      ++NextStart;
      Row = NextStart;
      Col = 1;
    } else {
      ++Col;
      --Row;
    }
  }
  return Code;
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

  std::pair<int, int> Input{GetFileContent(File.path().string())};

  //   Solve part 1
  std::optional<long long int> Part1{F(Input.first, Input.second)};

  // Solve part 2
  std::optional<int> Part2{};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
