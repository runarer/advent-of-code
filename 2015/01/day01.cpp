#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>
#include <string_view>

// This Method needs error handling. Will throw exceptions.
//
// tellg() returnerer posisjonen i streamen. Siden vi har satt den til
// eof med std::ios::ate så kan vi bruke tellg() med en gang
std::string GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName, std::ios::binary | std::ios::ate};
  /*if(!Input.is_open()) {
    throw ;
  }*/

  auto FileSize = Input.tellg();
  Input.seekg(std::ios::beg); // Reset for read
  std::string FileContent(FileSize, 0);
  Input.read(&FileContent[0], FileSize);

  Input.close();

  return FileContent;
}

int EnterBasement(std::istream &Input) {
  char C;
  int CurrentFloor{0};

  while (Input.get(C)) {
    if (C == '(')
      ++CurrentFloor;
    else if (C == ')') {
      --CurrentFloor;
      if (CurrentFloor < 0)
        break;
    }
  }

  return Input.tellg();
}

int FinalFloor(std::string_view Input) {
  int CurrentFloor{0};

  for (const char C : Input) {
    if (C == '(')
      ++CurrentFloor;
    else if (C == ')')
      --CurrentFloor;
  }

  return CurrentFloor;
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

  std::string Input{GetFileContent(File.path().string())};

  //  Solve part 1
  std::optional<int> Part1{FinalFloor(Input)};

  // Solve part 2
  std::istringstream InputStream{Input};
  std::optional<int> Part2{EnterBasement(InputStream)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
