#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>
#include <unordered_set>
#include <vector>
/*
 * Poison   42 327 52
 * Recharge 34  98 46
 * Shield   33 187 40
 * Recharge 32 160 37  <- Feil
 * Poison   31 189 34
 * MM       30 338 28
 * Recharge 22 210 22
 * Poison   14 239 16
 * Drain    8      8
 * Drain    2      0
 *
 * Poison->Recharge->Shield->
 * MM/Drain->Poison->Recharge->Shield->
 * */
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

auto GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::string Health, Damage, Ignore;

  Input >> Ignore;
  Input >> Ignore;
  Input >> Health;
  Input >> Ignore;
  Input >> Damage;
  return std::pair{std::stoi(Health), std::stoi(Damage)};
}

constexpr int Dead{1000000};

struct Game {
  int Player;
  int Mana;
  int Armor;
  int Boss;
  int BossDamage;
  int Shield;
  int Poison;
  int Recharge;
};

void PrintGame(Game &GS) {
  std::cout << "- Player has " << GS.Player << " hit points, " << GS.Armor
            << ", " << GS.Mana << " mana\n";
  std::cout << "- Boss has " << GS.Boss << " hit points\n";
}

void StartRound(Game &GameState);
void PlayerRound(Game &GameState);
void BossRound(Game &GameState);
int MagicMissile(Game &GameState);
int Drain(Game &GameState);
int Shield(Game &GameState);
int Poison(Game &GameState);
int Recharge(Game &GameState);

int MagicMissile(Game &GameState) {
  constexpr int Cost = 53;

  PlayerRound(GameState);

  // Cannot afford to cast
  if (GameState.Mana < Cost)
    return Dead;

  // Cast
  std::cout << "Player cast Magic Missile\n";
  GameState.Boss -= 4;
  GameState.Mana -= Cost;
  BossRound(GameState);
  return Cost;
}

int Drain(Game &GameState) {
  constexpr int Cost = 73;
  PlayerRound(GameState);

  // Cannot afford to cast
  if (GameState.Mana < Cost)
    return Dead;

  // Cast
  std::cout << "Player cast Drain\n";
  GameState.Boss -= 2;
  GameState.Player += 2;
  GameState.Mana -= Cost;
  BossRound(GameState);
  return Cost;
}

int Shield(Game &GameState) {
  constexpr int Cost = 113;
  PlayerRound(GameState);

  // Cannot afford to cast
  if (GameState.Mana < Cost)
    return Dead;

  // Cast
  std::cout << "Player cast Shield\n";
  GameState.Armor = 7;
  GameState.Shield = 6;
  GameState.Mana -= Cost;
  BossRound(GameState);
  return Cost;
}

int Poison(Game &GameState) {
  constexpr int Cost = 173;
  PlayerRound(GameState);

  // Cannot afford to cast
  if (GameState.Mana < Cost)
    return Dead;

  // Cast
  std::cout << "Player cast Poison\n";
  GameState.Poison = 6;
  GameState.Mana -= Cost;
  BossRound(GameState);
  return Cost;
}

int Recharge(Game &GameState) {
  constexpr int Cost = 229;
  PlayerRound(GameState);

  // Cannot afford to cast
  if (GameState.Mana < Cost)
    return Dead;

  // Cast
  std::cout << "Player cast Recharge\n";
  GameState.Recharge = 5;
  GameState.Mana -= Cost;
  BossRound(GameState);

  return Cost;
}

void StartRound(Game &GameState) {
  // Recharge
  if (GameState.Recharge > 0) {
    GameState.Mana += 101;
    GameState.Recharge--;
    std::cout << "Recharge provides 101 mana, its timer is now "
              << GameState.Recharge << '\n';
  }

  // Shield active?
  if (GameState.Shield > 0) {
    GameState.Shield--;
    std::cout << "Shield timer is now " << GameState.Shield << '\n';
  }
  if (GameState.Shield == 0)
    GameState.Armor = 0;

  // Poison Active?
  if (GameState.Poison > 0) {
    GameState.Boss -= 3;
    GameState.Poison--;
    std::cout << "Poison deals 3 damage, its timer is now " << GameState.Poison
              << '\n';
  }
}

void PlayerRound(Game &GameState) {
  std::cout << "\n-- Player turn --\n";
  //--GameState.Player;
  PrintGame(GameState);

  // Is player alive?
  if (GameState.Player < 1) {
    std::cout << "Player Died\n";
    return;
  }

  StartRound(GameState);

  // Is the boss dead?
  if (GameState.Boss < 1) {
    std::cout << "Boss is dead\n";
    return;
  }

  // Out of mana means loosing.
  if (GameState.Mana < 53) {
    std::cout << "Player ran out of mana\n";
    return;
  }
}

void BossRound(Game &GameState) {
  std::cout << "\n-- Boss turn --\n";
  PrintGame(GameState);
  StartRound(GameState);

  if (GameState.Boss < 1) {
    std::cout << "Boss is Dead\n";
    return;
  }

  int Damage{std::max(GameState.BossDamage - GameState.Armor, 1)};
  GameState.Player -= Damage;
  std::cout << "Boss attacks for 8 - " << GameState.Armor << " = " << Damage
            << " damage!\n";
}
int PlayHardGame(Game GameState) {
  int MinMana{0};

  --GameState.Player;
  MinMana += Poison(GameState);
  --GameState.Player;
  MinMana += Recharge(GameState);
  --GameState.Player;
  MinMana += Shield(GameState);
  --GameState.Player;
  MinMana += Poison(GameState);
  --GameState.Player;
  MinMana += Recharge(GameState);
  --GameState.Player;
  MinMana += Drain(GameState);
  --GameState.Player;
  MinMana += Poison(GameState);
  --GameState.Player;
  MinMana += Drain(GameState);
  --GameState.Player;
  MinMana += MagicMissile(GameState);

  return MinMana;
}

int PlayGame(Game GameState) {
  int MinMana{0};

  MinMana += Poison(GameState);
  MinMana += Recharge(GameState);
  MinMana += Shield(GameState);
  MinMana += Poison(GameState);
  MinMana += MagicMissile(GameState);
  MinMana += MagicMissile(GameState);
  MinMana += MagicMissile(GameState);
  MinMana += MagicMissile(GameState);
  MinMana += MagicMissile(GameState);

  return MinMana;
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

  auto [BossHealth, BossDamage]{GetFileContent(File.path().string())};

  //   Solve part 1
  Game StartState{50, 500, 0, BossHealth, BossDamage, 0, 0, 0};
  std::optional<int> Part1{PlayGame(StartState)};
  // Solve part 2

  std::optional<int> Part2{PlayHardGame(StartState)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
