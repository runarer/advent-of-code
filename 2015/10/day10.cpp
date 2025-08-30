#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>

int Play(const std::string StartLine, const int Rounds) {
  std::string Sequence{StartLine};

  for (int i{0}; i < Rounds; ++i) {
    std::string NextSequence;
    for (auto It{Sequence.begin()}; It != Sequence.end();) {
      char Current = (*It);
      int Number{0};

      while (It != Sequence.end() && (*It) == Current) {
        ++Number;
        ++It;
      }
      NextSequence += std::to_string(Number) + Current;
    }
    Sequence = NextSequence;
  }
  return Sequence.size();
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
  std::ifstream InFile{File.path()};
  std::string Input{};

  std::getline(InFile, Input);

  Play("1", 6);
  //  Solve part 1
  std::optional<int> Part1{Play(Input, 40)};

  // Solve part 2
  std::optional<int> Part2{Play(Input, 50)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
