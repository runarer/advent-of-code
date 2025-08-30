#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>
#include <string_view>

/* I Dont need the pairs after. So this is not needed*/

// This Method needs error handling. Will throw exceptions.
std::vector<std::string> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<std::string> Lines;
  std::string Line;

  while (std::getline(Input, Line)) {
    Lines.push_back(Line);
  }

  Input.close();

  return Lines;
}

bool NiceString(std::string_view Line) {
  bool Double{false};
  bool BadWord{false};
  int Vowels{0};

  char Previous{0};
  for (const char C : Line) {
    switch (C) {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
      ++Vowels;
      break;

    // Bad strings
    case 'b':
      if (Previous == 'a')
        BadWord = true;
      break;
    case 'd':
      if (Previous == 'c')
        BadWord = true;
      break;
    case 'q':
      if (Previous == 'p')
        BadWord = true;
      break;
    case 'y':
      if (Previous == 'x')
        BadWord = true;
      break;
    }
    if (BadWord)
      break;

    if (C == Previous)
      Double = true;

    Previous = C;
  }

  return Double && !BadWord && (Vowels >= 3);
}
bool SpacedRepeat(std::string_view Line) {
  char Previous{Line[1]};
  char PreviousPrevious{Line[0]};

  for (auto It = Line.begin() + 2; It != Line.end(); ++It) {
    if (*It == PreviousPrevious)
      return true;

    PreviousPrevious = Previous;
    Previous = *It;
  }

  return false;
}

bool Pair(std::string_view Line) {
  char First{Line[0]};
  char Second{Line[1]};

  for (auto It = Line.begin() + 2; It != Line.end() - 1; ++It) {

    for (auto It2 = It + 1; It2 != Line.end(); ++It2) {
      if (Second == *It2 && First == *(It2 - 1))
        return true;
    }

    First = Second;
    Second = *It;
  }

  return false;
}

bool NewNiceString(std::string_view Line) {
  return SpacedRepeat(Line) && Pair(Line);
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
  std::optional<int64_t> Part1{std::ranges::count_if(Input, NiceString)};

  // Solve part 2
  std::optional<int64_t> Part2{std::ranges::count_if(Input, NewNiceString)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
