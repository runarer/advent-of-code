#include <cctype>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>

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
int SumNumbers(std::istream &Input) {
  int Sum{0};

  char C;
  bool Negative{false};
  bool Digit{false};
  std::string DigitBuffer;

  while (Input.get(C)) {
    if (C == '-') {
      Negative = true;
    } else if (std::isdigit(C)) {
      DigitBuffer += C;
      Digit = true;
    } else {
      if (Digit) {
        Sum += Negative ? -std::stoi(DigitBuffer) : std::stoi(DigitBuffer);
        Digit = false;
        DigitBuffer.clear();
      }
      Negative = false;
    }
  }

  return Sum;
}

enum class JSONType { Array, Object };

int SumStructure(std::istream &Input, JSONType Type) {
  int Sum{0};

  char C;
  bool Negative{false};
  bool Digit{false};
  std::string DigitBuffer;

  bool R{false}, Re{false}, Red{false};

  while (Input.get(C)) {
    if (C == '-') {
      Negative = true;
    } else if (std::isdigit(C)) {
      DigitBuffer += C;
      Digit = true;
    } else {
      if (Digit) {
        Sum += Negative ? -std::stoi(DigitBuffer) : std::stoi(DigitBuffer);
        Digit = false;
        DigitBuffer.clear();
      }
      Negative = false;

      if (Type == JSONType::Object && (C == 'r' || C == 'R')) {
        R = true;
      } else if (R && (C == 'e' || C == 'E')) {
        Re = true;
      } else if (Re && (C == 'd' || C == 'D')) {
        Red = true;
      } else if (C == '{') {
        Sum += SumStructure(Input, JSONType::Object);
      } else if (C == '}') {
        if (Red)
          Sum = 0;
        break;
      } else if (C == '[') {
        Sum += SumStructure(Input, JSONType::Array);
      } else if (C == ']') {
        break;
      } else {
        R = false;
        Re = false;
      }
    }
  }

  return Sum;
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
  std::istringstream InputStream{Input};

  //  Solve part 1
  std::optional<int> Part1{SumNumbers(InputStream)};

  // Solve part 2
  InputStream.clear();
  InputStream.seekg(0);
  std::optional<int> Part2{SumStructure(InputStream, JSONType::Array)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
