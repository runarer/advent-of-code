#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>

std::vector<std::string> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<std::string> FileContent;
  std::string Line;

  while (std::getline(Input, Line))
    FileContent.push_back(Line);

  return FileContent;
}

void printMap(std::vector<bool> Map, int Size) {
  int W{1};
  for (bool M : Map) {
    std::cout << M;
    if (W == Size) {
      W = 1;
      std::cout << '\n';

    } else {
      ++W;
    }
  }
}

std::vector<bool> CreateLightMap(const std::vector<std::string> &Lines) {
  std::vector<bool> Map;
  Map.reserve(Lines.size() * Lines.size());

  for (const auto &Line : Lines) {
    for (const auto &Char : Line) {
      if (Char == '#')
        Map.emplace_back(true);
      else
        Map.emplace_back(false);
    }
  }
  return Map;
}

inline int GetPos(int row, int col, int size) { return row * size + col; }

int GetLitNeighbors(const std::vector<bool> &Map, const int row, const int col,
                    const int size) {
  int Count{0};
  int Size{size - 1};

  // North
  if (row > 0 && Map[GetPos(row - 1, col, size)])
    ++Count;

  // North East
  if (row > 0 && col < Size && Map[GetPos(row - 1, col + 1, size)])
    ++Count;

  // East
  if (col < Size && Map[GetPos(row, col + 1, size)])
    ++Count;

  // South East
  if (col < Size && row < Size && Map[GetPos(row + 1, col + 1, size)])
    ++Count;

  // South
  if (row < Size && Map[GetPos(row + 1, col, size)])
    ++Count;

  // Soth West
  if (row < Size && col > 0 && Map[GetPos(row + 1, col - 1, size)])
    ++Count;

  // West
  if (col > 0 && Map[GetPos(row, col - 1, size)])
    ++Count;

  // North West
  if (col > 0 && row > 0 && Map[GetPos(row - 1, col - 1, size)])
    ++Count;

  return Count;
}

int RunForNRounds(const std::vector<std::string> &Input, const int Rounds,
                  bool StuckLight) {
  std::vector<bool> LightMap{CreateLightMap(Input)};
  std::vector<bool> Temp(LightMap.size(), false);
  const auto Size{Input.size()};

  if (StuckLight) {
    LightMap[GetPos(0, 0, Size)] = true;
    LightMap[GetPos(0, Size - 1, Size)] = true;
    LightMap[GetPos(Size - 1, 0, Size)] = true;
    LightMap[GetPos(Size - 1, Size - 1, Size)] = true;
  }

  for (int Round{0}; Round < Rounds; ++Round) {
    for (int i{0}; i < Size; ++i) {
      for (int j{0}; j < Size; ++j) {
        // std::cout << i << ' ' << j << '\n';
        int Neighbors{GetLitNeighbors(LightMap, i, j, Size)};
        if (LightMap[GetPos(i, j, Size)]) {
          if (Neighbors == 2 || Neighbors == 3) {
            Temp[GetPos(i, j, Size)] = true;
          } else {
            Temp[GetPos(i, j, Size)] = false;
          }
        } else {
          if (Neighbors == 3) {
            Temp[GetPos(i, j, Size)] = true;
          } else {
            Temp[GetPos(i, j, Size)] = false;
          }
        }
      }
    }
    std::swap(LightMap, Temp);
    if (StuckLight) {
      LightMap[GetPos(0, 0, Size)] = true;
      LightMap[GetPos(0, Size - 1, Size)] = true;
      LightMap[GetPos(Size - 1, 0, Size)] = true;
      LightMap[GetPos(Size - 1, Size - 1, Size)] = true;
    }
  }

  int Count{0};
  for (auto L : LightMap) {
    if (L)
      ++Count;
  }

  return Count;
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
  std::optional<int> Part1{RunForNRounds(Input, 100, false)};

  // Solve part 2
  std::optional<int> Part2{RunForNRounds(Input, 100, true)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
