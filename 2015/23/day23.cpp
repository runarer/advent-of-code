#include <array>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>

enum class Inst { hlf = 0, tpl, inc, jmp, jie, jio };
// enum class Registers { a = 0, b = 1 };

struct Instruction {
  Inst Ins;
  int Reg;
  int Offset;
};

// using Instruction = std::tuple<Inst, Registers, int>;
using Instructions = std::vector<Instruction>;

// This Method needs error handling. Will throw exceptions.
//
// tellg() returnerer posisjonen i streamen. Siden vi har satt den til
// eof med std::ios::ate så kan vi bruke tellg() med en gang
Instructions GetFileContent(const std::string &FileName) {
  Instructions Insts{};

  std::ifstream Input{FileName};
  std::string Ins;
  std::string Reg;
  std::string Off;

  while (Input >> Ins) {
    if (Ins == "jmp") {
      Input >> Off;
      Insts.emplace_back(Inst::jmp, 0, std::stoi(Off));
    } else if (Ins == "hlf") {
      Input >> Reg;
      int R{0};
      if (Reg == "b")
        R = 1;
      Insts.emplace_back(Inst::hlf, R, 0);
    } else if (Ins == "inc") {
      Input >> Reg;
      int R{0};
      if (Reg == "b")
        R = 1;
      Insts.emplace_back(Inst::inc, R, 0);
    } else if (Ins == "tpl") {
      int R{0};
      if (Reg == "b")
        R = 1;
      Input >> Reg;
      Insts.emplace_back(Inst::tpl, R, 0);
    } else if (Ins == "jie") {
      Input >> Reg;
      int R{0};
      if (Reg == "b")
        R = 1;

      Input >> Off;
      Insts.emplace_back(Inst::jie, R, std::stoi(Off));
    } else if (Ins == "jio") {
      Input >> Reg;
      int R{0};
      if (Reg == "b")
        R = 1;

      Input >> Off;
      Insts.emplace_back(Inst::jio, R, std::stoi(Off));
    }
  }

  return Insts;
}

int RunInst(Instructions &Ins, uint64_t a, uint64_t b) {
  // auto Pos{Ins.begin()};
  int Pos{0};
  std::array<uint64_t, 2> Regs{a, b};

  // while (Pos != Ins.end()) {
  while (Pos < Ins.size()) {
    // Instruction &I = *Pos;
    Instruction &I = Ins[Pos];
    switch (I.Ins) {
    case Inst::hlf:
      Regs[I.Reg] /= 2;
      ++Pos;
      // std::cout << "hlf " << int(I.Reg) << '\n';
      break;
    case Inst::inc:
      ++Regs[I.Reg];
      ++Pos;
      // std::cout << "inc " << int(I.Reg) << '\n';

      break;
    case Inst::jmp:
      // Pos = std::next(Pos, I.Offset);
      Pos += I.Offset;
      // std::cout << "jmp " << I.Offset << '\n';

      break;
    case Inst::tpl:
      Regs[I.Reg] *= 3;
      ++Pos;
      // std::cout << "tpl " << int(I.Reg) << '\n';

      break;
    case Inst::jie:
      if (Regs[I.Reg] % 2 == 0)
        //  Pos = std::next(Pos, I.Offset);
        Pos += I.Offset;
      else
        ++Pos;
      // std::cout << "jie " << int(I.Reg) << ", " << I.Offset << '\n';

      break;
    case Inst::jio:
      if (Regs[I.Reg] == 1)
        //  Pos = std::next(Pos, I.Offset);
        Pos += I.Offset;
      else
        ++Pos;

      // std::cout << "jio " << int(I.Reg) << ", " << I.Offset << '\n';
      break;
    }
  }
  return Regs[1];
}

void printInst(Instructions &Ins) {
  for (const auto &I : Ins) {
    switch (I.Ins) {
    case Inst::hlf:

      std::cout << "hlf " << int(I.Reg) << '\n';
      break;
    case Inst::inc:
      std::cout << "inc " << int(I.Reg) << '\n';

      break;
    case Inst::jmp:
      std::cout << "jmp " << I.Offset << '\n';

      break;
    case Inst::tpl:
      std::cout << "tpl " << int(I.Reg) << '\n';

      break;
    case Inst::jie:
      std::cout << "jie " << int(I.Reg) << ", " << I.Offset << '\n';

      break;
    case Inst::jio:
      std::cout << "jio " << int(I.Reg) << ", " << I.Offset << '\n';

      break;
    }
  }
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

  Instructions Input{GetFileContent(File.path().string())};

  //  Solve part 1
  std::optional<int> Part1{RunInst(Input, 0, 0)};

  // Solve part 2
  std::optional<int> Part2{RunInst(Input, 1, 0)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
