#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>

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

  // Løst på papir.
  // Solve part 1
  std::optional<std::string> Part1{"cqjxxyzz"};

  // Solve part 2
  std::optional<std::string> Part2{"cqkaabcc"};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
