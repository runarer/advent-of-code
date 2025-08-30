#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <regex>
#include <string>

std::vector<std::string> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<std::string> FileContent;
  std::string Line;

  while (std::getline(Input, Line))
    FileContent.push_back(Line);

  return FileContent;
}

struct Ingredient {
  std::string Name;
  int Capacity;
  int Durability;
  int Flavor;
  int Texture;
  int Calories;
};

auto ParseLines(std::vector<std::string> Lines) {
  std::vector<Ingredient> Ingredients;

  for (const auto &Line : Lines) {
    std::string Name;
    int Capacity, Duration, Flavor, Texture, Calories;

    const std::regex Pattern{
        R"(([a-zA-Z]+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+))"};
    std::smatch Match;

    if (std::regex_match(Line, Match, Pattern)) {
      Name = Match[1];
      Capacity = std::stoi(Match[2]);
      Duration = std::stoi(Match[3]);
      Flavor = std::stoi(Match[4]);
      Texture = std::stoi(Match[5]);
      Calories = std::stoi(Match[6]);
    }

    Ingredients.emplace_back(
        Ingredient{Name, Capacity, Duration, Flavor, Texture, Calories});
  }
  return Ingredients;
}

long long int MaximumScore(const std::vector<Ingredient> &Ingredients,
                           const int Total) {
  long long int MaxScore{0};

  for (int First{97}; First > 0; --First) {
    for (int Second{Total - First - 2}; Second > 0; --Second) {
      for (int Third{Total - First - Second - 1}; Third > 0; --Third) {
        int Forth{Total - First - Second - Third};

        const int Capacity{
            Ingredients[0].Capacity * First + Ingredients[1].Capacity * Second +
            Ingredients[2].Capacity * Third + Ingredients[3].Capacity * Forth};
        const int Durability{Ingredients[0].Durability * First +
                             Ingredients[1].Durability * Second +
                             Ingredients[2].Durability * Third +
                             Ingredients[3].Durability * Forth};
        const int Flavor{
            Ingredients[0].Flavor * First + Ingredients[1].Flavor * Second +
            Ingredients[2].Flavor * Third + Ingredients[3].Flavor * Forth};
        const int Texture{
            Ingredients[0].Texture * First + Ingredients[1].Texture * Second +
            Ingredients[2].Texture * Third + Ingredients[3].Texture * Forth};

        long long int Score = Capacity * Durability * Flavor * Texture;
        if (Capacity < 0 || Durability < 0 || Flavor < 0 || Texture < 0) {
          Score = 0;
        }
        if ((Ingredients[0].Calories * First +
             Ingredients[1].Calories * Second +
             Ingredients[2].Calories * Third +
             Ingredients[3].Calories * Forth) != 500) {
          Score = 0;
        }
        MaxScore = std::max(MaxScore, Score);
      }
    }
  }
  return MaxScore;
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
  std::vector<Ingredient> Ingredients{ParseLines(Input)};

  //  Solve part 1
  std::optional<long long int> Part1{MaximumScore(Ingredients, 100)};

  // Solve part 2
  std::optional<int> Part2{};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
