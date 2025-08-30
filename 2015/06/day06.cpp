#include <array>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <optional>
#include <sstream>
#include <string_view>

enum class Action { Off = 0, On, Toggle };

struct Instruction {
  Action Action;
  int FromCol;
  int FromRow;
  int ToCol;
  int ToRow;
};

// This Method needs error handling. Will throw exceptions.
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

// From; en.cpprefrence.com/w/cpp/locale/ctype_char
// I really don't understand this.
// It is extending std::ctype<char>, then changing a bitmap lookup table
struct csv_whitespace : std::ctype<char> {
  static const mask *make_table() {
    // make a copy of the "C" locale table
    static std::vector<mask> v(classic_table(), classic_table() + table_size);
    v[','] |= space; // comma will be classified as whitespace
    // v[' '] &= ~space; // space will not be classified as whitespace
    return &v[0];
  }

  csv_whitespace(std::size_t refs = 0) : ctype(make_table(), false, refs) {}
};

auto ParseCoordinates(std::string_view Coordinates) { return std::pair{0, 0}; }

std::vector<Instruction> ParseInstructions(std::istream &Lines) {
  Lines.imbue(std::locale(Lines.getloc(), new csv_whitespace));
  std::vector<Instruction> Instructions;
  std::string ToggleOrTurn;

  while (Lines >> ToggleOrTurn) {
    std::string Button;

    Action Action = Action::Toggle;

    if (ToggleOrTurn == "turn") {
      Lines >> Button;
      if (Button == "on")
        Action = Action::On;
      else
        Action = Action::Off;
    }

    std::string ThrowAway;
    int FromCol, FromRow, ToCol, ToRow;
    Lines >> FromRow;
    Lines >> FromCol;
    Lines >> ThrowAway;
    Lines >> ToRow;
    Lines >> ToCol;

    Instructions.emplace_back(
        Instruction{Action, FromCol, FromRow, ToCol, ToRow});
  }

  return Instructions;
}

int LitLights(const std::vector<Instruction> &Instructions) {
  std::array<bool, 1000 * 1000> Lights{};

  for (const auto &I : Instructions) {
    for (int Row = I.FromRow; Row <= I.ToRow; ++Row) {
      for (int Col = I.FromCol; Col <= I.ToCol; ++Col) {
        int Coor{Row * 1000 + Col};
        if (I.Action == Action::Toggle) {
          Lights[Coor] = !Lights[Coor];
        } else if (I.Action == Action::On) {
          Lights[Coor] = true;
        } else {
          Lights[Coor] = false;
        }
      }
    }
  }
  return std::ranges::count(Lights, true);
}

int TotalBrightness(const std::vector<Instruction> &Instructions) {
  // std::array<int, 1000 * 1000> Lights{0}; // Ser ut til a dette ble for
  // mye for en array. Tror den ligger på stacken.
  std::vector<int> Lights(1000 * 1000, 0);

  for (const auto &I : Instructions) {
    for (int Row = I.FromRow; Row <= I.ToRow; ++Row) {
      for (int Col = I.FromCol; Col <= I.ToCol; ++Col) {
        int Coor{Row * 1000 + Col};
        if (I.Action == Action::Toggle) {
          Lights[Coor] += 2;
        } else if (I.Action == Action::On) {
          ++Lights[Coor];
        } else {
          if (Lights[Coor] > 0)
            --Lights[Coor];
        }
      }
    }
  }

  return std::reduce(Lights.begin(), Lights.end());
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
  std::vector<Instruction> Instructions{ParseInstructions(InputStream)};

  //  Solve part 1
  std::optional<int> Part1{LitLights(Instructions)};

  // Solve part 2
  std::optional<int> Part2{TotalBrightness(Instructions)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
