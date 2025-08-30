#include <array>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <optional>
#include <vector>

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
    v['x'] |= space; // comma will be classified as whitespace
    // v[' '] &= ~space; // space will not be classified as whitespace
    return &v[0];
  }

  csv_whitespace(std::size_t refs = 0) : ctype(make_table(), false, refs) {}
};

struct Gift {
  int Length;
  int Height;
  int Width;
};

std::vector<Gift> ExtractData(std::istream &Input) {
  std::vector<Gift> Gifts;

  Input.imbue(std::locale(Input.getloc(), new csv_whitespace));

  int Length;
  int Height;
  int Width;

  while (Input >> Length >> Height >> Width) {
    Gifts.emplace_back(Gift{Length, Height, Width});
  }

  return Gifts;
}

int WrappingNeeded(const Gift &Gift) {
  std::array Sides{Gift.Length * Gift.Height, Gift.Length * Gift.Width,
                   Gift.Width * Gift.Height};

  int Extra{std::min(Sides[0], Sides[1])};
  Extra = std::min(Extra, Sides[2]);

  return Extra + (Sides[0] + Sides[1] + Sides[2]) * 2;
}

int RibbonNeeded(const Gift &Gift) {
  return 2 * (std::min(Gift.Length, Gift.Width) +
              std::min(std::max(Gift.Length, Gift.Width), Gift.Height)) +
         Gift.Length * Gift.Width * Gift.Height;
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

  std::ifstream InputStream{File.path()};
  std::vector<Gift> Data{ExtractData(InputStream)};

  //  Solve part 1
  std::optional<int> Part1{std::accumulate(
      Data.cbegin(), Data.cend(), 0,
      [](int sum, const Gift &cur) { return sum + WrappingNeeded(cur); })};

  // Solve part 2
  std::optional<int> Part2{std::accumulate(
      Data.cbegin(), Data.cend(), 0,
      [](int sum, const Gift &cur) { return sum + RibbonNeeded(cur); })};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
