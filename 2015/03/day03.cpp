#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string_view>
#include <unordered_set>

/* I Dont need the pairs after. So this is not needed*/
namespace std {
template <> struct hash<std::pair<int, int>> {
  size_t operator()(std::pair<int, int> const &Pair) const {
    return std::hash<int>()(Pair.first * 1000000 + Pair.second);
  }
};
} // namespace std

inline int House(int A, int B) { return A * 1000000 + B; }

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

auto Houses(std::string_view Directions) {
  std::unordered_set<int> HousesVisited{House(0, 0)};
  int Height{0};
  int Width{0};

  for (const char &C : Directions) {
    switch (C) {
    case '^':
      ++Height;
      break;
    case '>':
      ++Width;
      break;
    case 'v':
      --Height;
      break;
    case '<':
      --Width;
      break;
    }
    HousesVisited.emplace(House(Height, Width));
  }

  return HousesVisited;
}

auto SplittInstuctions(std::string_view Directions) {
  std::string Santa;
  Santa.reserve(Directions.size() / 2);
  std::string Robot;
  Robot.reserve(Directions.size() / 2);

  int i{0};
  for (const char &C : Directions) {
    if (i % 2 == 0)
      Santa += C;
    else
      Robot += C;
    ++i;
  }
  return std::pair{Santa, Robot};
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
  std::optional<int> Part1{int(Houses(Input).size())};

  // Solve part 2
  auto [SantaInput, RobotInput] = SplittInstuctions(Input);
  std::unordered_set TotalVisited{Houses(SantaInput)};
  std::unordered_set RobotVisited{Houses(RobotInput)};
  TotalVisited.insert(RobotVisited.cbegin(), RobotVisited.cend());
  std::optional<int> Part2{int(TotalVisited.size())};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
