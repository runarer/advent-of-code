#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <optional>
#include <string>
#include <unordered_set>
#include <vector>

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

enum class Attrib { Cost = 0, Damage = 1, Armor = 2 };

struct Equipment {
  std::string Name;
  int Cost;
  int Damage;
  int Armor;
};

// using EquipmentList = std::unordered_map<std::string, std::array<int, 3>>;

using EquipmentList = std::vector<Equipment>;
/*
EquipmentList Weapons{{"Dagger", {8, 4, 0}},
                      {"Shortsword", {10, 5, 0}},
                      {"Warhammer", {25, 6, 0}},
                      {"Longsword", {40, 7, 0}},
                      {"Greataxe", {74, 8, 0}}};

EquipmentList Armor{{"Leather", {13, 0, 1}},
                    {"Chainmail", {31, 0, 2}},
                    {"Splintmail", {53, 0, 3}},
                    {"Bandedmail", {75, 0, 4}},
                    {"Platemail", {102, 0, 5}}};

EquipmentList Rings{{"Damage + 1", {25, 1, 0}},  {"Damage + 2", {50, 2, 0}},
                    {"Damage + 3", {100, 3, 0}}, {"Defense + 1", {20, 0, 1}},
                    {"Defense + 2", {40, 0, 2}}, {"Defense + 3", {80, 0, 3}}};
*/

EquipmentList Weapons{{"Dagger", 8, 4, 0},
                      {"Shortsword", 10, 5, 0},
                      {"Warhammer", 25, 6, 0},
                      {"Longsword", 40, 7, 0},
                      {"Greataxe", 74, 8, 0}};

EquipmentList Armors{{"Unarmored", 0, 0, 0},   {"Leather", 13, 0, 1},
                     {"Chainmail", 31, 0, 2},  {"Splintmail", 53, 0, 3},
                     {"Bandedmail", 75, 0, 4}, {"Platemail", 102, 0, 5}};

EquipmentList Rings{{"Damage + 1", 25, 1, 0},  {"Damage + 2", 50, 2, 0},
                    {"Damage + 3", 100, 3, 0}, {"Defense + 1", 20, 0, 1},
                    {"Defense + 2", 40, 0, 2}, {"Defense + 3", 80, 0, 3}};

struct Monster {
  int Health;
  int Damage;
  int Armor;
};

struct Player {
  int Health{100};
  int Damage{0};
  int Armor{0};
  int GoldSpent{0};

  Player(Equipment Weapon, Equipment Chest, std::optional<Equipment> Ring1,
         std::optional<Equipment> Ring2) {
    GoldSpent += Weapon.Cost;
    GoldSpent += Chest.Cost;
    if (Ring1)
      GoldSpent += Ring1->Cost;
    if (Ring2)
      GoldSpent += Ring2->Cost;

    Damage += Weapon.Damage;
    Damage += Chest.Damage;
    if (Ring1)
      Damage += Ring1->Damage;
    if (Ring2)
      Damage += Ring2->Damage;

    Armor += Weapon.Armor;
    Armor += Chest.Armor;
    if (Ring1)
      Armor += Ring1->Armor;
    if (Ring2)
      Armor += Ring2->Armor;
  }

  // Equipment Weapon;
  // Equipment Armor;
  // std::optional<Equipment> Ring1;
  // std::optional<Equipment> Ring2;
};

void PrintPlayer(Player &M) {
  std::cout << "\n----------------------\n";
  std::cout << "Player H: " << M.Health << " D: " << M.Damage
            << " A: " << M.Armor << " G: " << M.GoldSpent << '\n';
  std::cout << "\n----------------------\n";
}

void PrintMonster(Monster &M) {
  std::cout << "\n----------------------\n";
  std::cout << "Monster H: " << M.Health << " D: " << M.Damage
            << " A: " << M.Armor << '\n';
  std::cout << "\n----------------------\n";
}

bool Fight(Player Player, Monster Boss) {

  int PlayerDmg{Player.Damage - Boss.Armor};
  PlayerDmg = std::max(PlayerDmg, 1);
  int BossDmg{Boss.Damage - Player.Armor};
  BossDmg = std::max(BossDmg, 1);

  while (Player.Health > 0 && Boss.Health > 0) {
    Boss.Health -= PlayerDmg;
    if (Boss.Health < 1)
      break;
    Player.Health -= BossDmg;
  }

  return Player.Health > 0;
}

int LowestCostVictory(Monster Boss) {
  int Gold{std::numeric_limits<int>::max()};

  for (const auto &Weapon : Weapons) {
    for (const auto &Armor : Armors) {
      // No Rings
      Player CurrentPlayer{Weapon, Armor, {}, {}};
      if (Fight(CurrentPlayer, Boss)) {
        if (CurrentPlayer.GoldSpent < Gold) {
          Gold = CurrentPlayer.GoldSpent;
        }
      }

      for (const auto &Ring1 : Rings) {
        for (const auto &Ring2 : Rings) {
          if (Ring1.Name == Ring2.Name) {
            CurrentPlayer = Player{Weapon, Armor, Ring1, {}};
          } else {
            CurrentPlayer = Player{Weapon, Armor, Ring1, Ring2};
          }
          if (Fight(CurrentPlayer, Boss)) {
            if (CurrentPlayer.GoldSpent < Gold) {
              Gold = CurrentPlayer.GoldSpent;
            }
          }
        }
      }
    }
  }

  return Gold;
}

int HighestCostVictory(Monster Boss) {
  int Gold{0};

  for (const auto &Weapon : Weapons) {
    for (const auto &Armor : Armors) {
      // No Rings
      Player CurrentPlayer{Weapon, Armor, {}, {}};
      if (!Fight(CurrentPlayer, Boss)) {
        if (CurrentPlayer.GoldSpent > Gold) {
          Gold = CurrentPlayer.GoldSpent;
          PrintPlayer(CurrentPlayer);
        }
      }

      for (const auto &Ring1 : Rings) {
        for (const auto &Ring2 : Rings) {
          if (Ring1.Name == Ring2.Name) {
            CurrentPlayer = Player{Weapon, Armor, Ring1, {}};
          } else {
            CurrentPlayer = Player{Weapon, Armor, Ring1, Ring2};
          }
          if (!Fight(CurrentPlayer, Boss)) {
            if (CurrentPlayer.GoldSpent > Gold) {
              Gold = CurrentPlayer.GoldSpent;
              PrintPlayer(CurrentPlayer);
            }
          }
        }
      }
    }
  }

  return Gold;
}

auto GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::string Health, Damage, Armor, Ignore;

  Input >> Ignore;
  Input >> Ignore;
  Input >> Health;
  Input >> Ignore;
  Input >> Damage;
  Input >> Ignore;
  Input >> Armor;
  return Monster{std::stoi(Health), std::stoi(Damage), std::stoi(Armor)};
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

  Monster Boss{GetFileContent(File.path().string())};

  //   Solve part 1
  std::optional<int> Part1{LowestCostVictory(Boss)};

  // Solve part 2

  std::optional<int> Part2{HighestCostVictory(Boss)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
