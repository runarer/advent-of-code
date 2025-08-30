#include <algorithm>
#include <cctype>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <optional>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std::string_literals;

template <typename T> void printVecL(std::vector<T> Vec) {
  std::cout << "\n----------------------\n";
  for (const auto &L : Vec)
    std::cout << L << '\n';
  std::cout << "----------------------\n";
}

template <typename T> void printVec(std::vector<T> Vec) {
  std::cout << "\n----------------------\n";
  for (const auto &L : Vec)
    std::cout << L << ' ';
  std::cout << "\n----------------------\n";
}

template <typename T> void printSet(std::unordered_set<T> Vec) {
  std::cout << "\n----------------------\n";
  for (const auto &L : Vec)
    std::cout << L << ' ';
  std::cout << "\n----------------------\n";
}

using RuleTable = std::unordered_map<std::string, std::vector<std::string>>;

auto GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  RuleTable Rules;
  std::string StartingPoint;
  std::string Line;

  while (std::getline(Input, Line)) {
    if (Line == "")
      break;
    std::istringstream is{Line};
    std::string Rule, Ignore, Replacement;
    is >> Rule >> Ignore >> Replacement;
    Rules[Rule];
    Rules[Rule].push_back(Replacement);
  }

  std::getline(Input, StartingPoint);

  return std::pair{Rules, StartingPoint};
}

std::vector<std::string> ParseTokens(std::string_view StartingPoint) {
  std::vector<std::string> Tokens;

  for (auto It{StartingPoint.begin()}; It < StartingPoint.end(); ++It) {
    Tokens.emplace_back(1, *It);
    if ((It + 1) != StartingPoint.end() && std::islower(*(It + 1))) {
      ++It;
      Tokens.back() += (*It);
    }
  }

  return Tokens;
}
using SList = std::vector<std::string>;
int FindOverlap(const std::vector<std::string> &First,
                const std::string &FirstStart,
                const std::vector<std::string> &Second,
                const std::string &SecondEnd) {
  int Overlaps{0};

  for (const auto &F : First) {
    if (!F.starts_with(FirstStart))
      continue;
    for (const auto &S : Second) {
      if (!S.ends_with(SecondEnd))
        continue;

      if (F + SecondEnd == FirstStart + S) {
        ++Overlaps;
      }
    }
  }
  return Overlaps;
}

int CountVariations(const RuleTable &Rules,
                    const std::vector<std::string> &Tokens) {
  std::vector<int> Variations(Tokens.size(), 0);

  auto Var{Variations.begin()};
  auto Cur{Tokens.begin()};
  for (auto Next{Cur + 1}; Next != Tokens.end(); ++Cur, ++Next, ++Var) {
    // A replacement
    if (Rules.contains(*Cur)) {
      //
      if (Rules.contains(*Next)) {
        (*(Var + 1)) -=
            FindOverlap(Rules.at(*Cur), *Cur, Rules.at(*Next), *Next);
      }
      (*Var) += Rules.at(*Cur).size();
    }
  }
  // Add the last one
  if (Rules.contains(*Cur))
    (*Var) += Rules.at(*Cur).size();

  return std::reduce(Variations.begin(), Variations.end());
}

std::unordered_set<std::string>
UsedTokens(const RuleTable &Rules,
           const std::vector<std::string> &StartingPoint) {
  std::unordered_set<std::string> Tokens{StartingPoint.begin(),
                                         StartingPoint.end()};

  for (const auto &[Key, _] : Rules)
    Tokens.insert(Key);
  return Tokens;
}

std::unordered_set<std::string>
EndpointTokens(const RuleTable &Rules,
               const std::vector<std::string> &StartingPoint) {
  std::unordered_set<std::string> Tokens{StartingPoint.begin(),
                                         StartingPoint.end()};

  for (const auto &[Key, _] : Rules)
    Tokens.erase(Key);

  return Tokens;
}

void RemoveFakeRules(RuleTable &Rules,
                     const std::unordered_set<std::string> &ApprovedTokens) {
  for (auto &[Rule, Replacements] : Rules) {
    std::vector<std::string> NewRules{};
    for (auto &Repl : Replacements) {
      std::vector<std::string> Tokens{ParseTokens(Repl)};
      // This should be done with set comparing.
      bool Approved{true};
      for (const auto &Token : Tokens)
        if (!ApprovedTokens.contains(Token)) {
          Approved = false;
          break;
        }
      if (Approved)
        NewRules.emplace_back(Repl);
    }
    Rules[Rule] = NewRules;
  }
}

std::unordered_map<std::string, std::string> FlipRules(const RuleTable &Rules) {
  std::unordered_map<std::string, std::string> FlippedRules{};

  for (const auto &[To, Froms] : Rules) {
    for (const auto &From : Froms) {
      FlippedRules[From] = To;
    }
  }

  return FlippedRules;
}

auto SplittRules(const std::unordered_map<std::string, std::string> &Rules) {
  std::unordered_map<std::string, std::string> SimpleRules{};
  std::unordered_map<std::string, std::string> AdvancedRules{};

  for (const auto &[Rule, Repl] : Rules) {
    if (Rule.find("Rn") == std::string::npos) {
      SimpleRules[Rule] = Repl;
    } else {
      AdvancedRules[Rule] = Repl;
    }
  }

  return std::pair{SimpleRules, AdvancedRules};
}

auto ReduceSimple(std::unordered_map<std::string, std::string> Rules,
                  std::string_view Line) {

  auto It{Line.begin()};
  std::string Temp{*It};
  ++It;
  if (It != Line.end() && std::islower(*It)) {
    Temp += (*It);
    ++It;
  }

  int Steps{};
  std::cout << "RR: " << Temp << std::endl;
  for (; It != Line.end(); ++It) {
    Temp += (*It);

    if (std::next(It) != Line.end() && std::islower(*std::next(It))) {
      Temp += (*std::next(It));
      ++It;
    }
    std::cout << Temp << std::endl;
    Temp = Rules[Temp];
    ++Steps;
  }

  return std::pair{Temp, Steps};
}

int FindAndReplace(std::string &L, const std::string &Find,
                   std::string_view Replace) {
  int Replaced{0};
  bool NotDone{true};
  std::vector<std::string> Terms{"Rn" + Find, "Ar" + Find};

  for (const auto &Term : Terms) {
    auto Pos = L.find(Term);
    while (Pos != std::string::npos) {
      L.replace(Pos + 2, Find.size(), Replace);
      ++Replaced;
      Pos = L.find(Term);
    }
  }
  return Replaced;
}

int CountSteps(const RuleTable &Rules, std::string Line) {
  int Steps{0};

  std::unordered_map<std::string, std::string> FlippedRules{FlipRules(Rules)};
  auto [SimpleRules, AdvancedRules] = SplittRules(FlippedRules);

  // Some simple replacements
  bool NotDone{true};
  while (NotDone) {
    NotDone = false;
    for (const auto &[Rule, Repl] : AdvancedRules) {
      int Replaced = FindAndReplace(Line, Rule, Repl);
      if (Replaced != 0) {
        NotDone = true;
        Steps += Replaced;
      }
    }
  }
  std::cout << Line << std::endl;

  return Steps;
}

int CountWithTokens(const std::vector<std::string> Tokens) {
  const int Steps{int(Tokens.size()) - 1};
  const int64_t Rn{std::ranges::count(Tokens, "Rn")};
  const int64_t Ar{std::ranges::count(Tokens, "Ar")};
  const int64_t Y{std::ranges::count(Tokens, "Y")};

  return Steps - Rn - Ar - 2 * Y;
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

  auto [Rules, StartingPoint]{GetFileContent(File.path().string())};
  auto Tokens{ParseTokens(StartingPoint)};

  //   Solve part 1
  std::optional<int> Part1{CountVariations(Rules, Tokens)};

  // Solve part 2
  std::unordered_set<std::string> All{UsedTokens(Rules, Tokens)};
  RemoveFakeRules(Rules, All);
  std::unordered_map<std::string, std::string> FlippedRules{FlipRules(Rules)};

  std::cout << StartingPoint << std::endl;
  std::optional<int> Part2{CountWithTokens(Tokens)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
