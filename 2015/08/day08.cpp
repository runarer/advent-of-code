#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <optional>
#include <string>
#include <string_view>
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

int DecodeLine(std::string_view Line) {
  int NChars{int(Line.size()) - 2};

  for (auto It{Line.begin()}; It < Line.end(); ++It) {
    if ((*It) == '\\') {
      if ((*(It + 1)) == 'x') {
        It = It + 2;
        NChars -= 2;
      }
      ++It;
      --NChars;
    }
  }
  return NChars;
}

int EncodeLine(std::string_view Line) {
  int NChars{int(Line.size()) + 4};

  for (auto It{Line.begin()}; It < Line.end(); ++It) {
    if ((*It) == '\\') {
      if ((*(It + 1)) == 'x') {
        It = It + 2;
      } else {
        ++NChars;
      }
      ++It;
      ++NChars;
    }
  }
  return NChars;
}

int DecodeLines(const std::vector<std::string> &Lines) {
  return std::reduce(Lines.begin(), Lines.end(), 0, [](int n, std::string S) {
    return n + (int(S.size()) - DecodeLine(S));
  });
}

int EncodeLines(const std::vector<std::string> &Lines) {
  return std::reduce(Lines.begin(), Lines.end(), 0, [](int n, std::string S) {
    return n + (EncodeLine(S) - int(S.size()));
  });
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
  std::optional<int> Part1{DecodeLines(Input)};

  // Solve part 2
  std::optional<int> Part2{EncodeLines(Input)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
