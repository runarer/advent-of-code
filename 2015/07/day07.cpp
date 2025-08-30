#include <cctype>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>
#include <string>
#include <unordered_map>

// This Method needs error handling. Will throw exceptions.
std::vector<std::string> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<std::string> FileContent;
  std::string Line;

  while (std::getline(Input, Line))
    FileContent.push_back(Line);

  return FileContent;
}

using Wire = std::optional<uint16_t>;

struct Gate {
  enum class Gates { NOT, AND, OR, LSHIFT, RSHIFT, WIRE };
  Gates Type;
  Wire &Output;
  Wire &FirstInput;
  Wire &SecondInput;

  Gate(Gates T, Wire &Out, Wire &In1, Wire &In2)
      : Type{T}, Output{Out}, FirstInput{In1}, SecondInput{In2} {}

  bool Update() {
    bool Updated{false};

    if (FirstInput && SecondInput) {
      switch (Type) {
      case Gates::NOT:
        Output = ~(*SecondInput);
        break;
      case Gates::AND:
        Output = (*FirstInput) & (*SecondInput);
        break;
      case Gates::OR:
        Output = (*FirstInput) | (*SecondInput);
        break;
      case Gates::LSHIFT:
        Output = (*FirstInput) << (*SecondInput);
        break;
      case Gates::RSHIFT:
        Output = (*FirstInput) >> (*SecondInput);
        break;
      case Gates::WIRE:
        if (!Output)
          Output = (*FirstInput);
        break;
      }
      Updated = true;
    }

    return Updated;
  }
  static Gates GetGateType(std::string_view Type) {
    if (Type == "->")
      return Gates::WIRE;
    if (Type == "NOT")
      return Gates::NOT;
    if (Type == "AND")
      return Gates::AND;
    if (Type == "OR")
      return Gates::OR;
    if (Type == "LSHIFT")
      return Gates::LSHIFT;
    return Gates::RSHIFT;
  }
};

bool IsNumber(std::string_view Str) {
  for (const char &C : Str)
    if (!std::isdigit(C))
      return false;
  return true;
}

auto ParseLine(std::istream &Line) {
  std::string MaybeValue;
  std::string FirstInput;
  std::string Operation;
  std::string SecondInput;
  std::string Output;
  std::string Ignore;

  Line >> MaybeValue;
  if (MaybeValue == "NOT") {
    FirstInput = "dummy";
    Operation = MaybeValue;
    Line >> SecondInput;
    Line >> Ignore;
    Line >> Output;
  } else {
    FirstInput = MaybeValue;
    Line >> Operation;
    if (Operation == "->") {
      SecondInput = "dummy";
    } else {
      Line >> SecondInput;
      Line >> Ignore;
    }
    Line >> Output;
  }
  return std::tuple{FirstInput, Gate::GetGateType(Operation), SecondInput,
                    Output};
}

void AddWire(std::unordered_map<std::string, Wire> &Wires,
             const std::string &FirstInput, const std::string &SecondInput,
             const std::string &Output) {
  if (!Wires.contains(FirstInput)) {
    Wires[FirstInput];
    if (IsNumber(FirstInput))
      Wires[FirstInput] = std::stoi(FirstInput);
  }
  if (!Wires.contains(SecondInput)) {
    Wires[SecondInput];
    if (IsNumber(SecondInput))
      Wires[SecondInput] = std::stoi(SecondInput);
  }
  if (!Wires.contains(Output)) {
    Wires[Output];
  }
}

void ParseInstructions(std::vector<Gate> &Gates,
                       std::unordered_map<std::string, Wire> &Wires,
                       const std::vector<std::string> &Lines) {
  for (const auto &Line : Lines) {
    std::istringstream LineStream{Line};
    auto [FirstInput, Operation, SecondInput, Output]{ParseLine(LineStream)};
    AddWire(Wires, FirstInput, SecondInput, Output);
    Gates.emplace_back(
        Gate{Operation, Wires[Output], Wires[FirstInput], Wires[SecondInput]});
  }
}

int RunInstructions(const std::vector<std::string> Input) {
  std::vector<Gate> Gates;
  std::unordered_map<std::string, Wire> Wires{
      {"dummy", std::optional<uint16_t>{0}}};
  ParseInstructions(Gates, Wires, Input);

  while (!Wires["a"]) {
    for (auto &G : Gates)
      G.Update();
  }
  return Wires["a"].value();
}

int ReRunInstructions(const std::vector<std::string> Input,
                      const int Override) {
  std::vector<Gate> Gates;
  std::unordered_map<std::string, Wire> Wires{
      {"dummy", std::optional<uint16_t>{0}}};
  ParseInstructions(Gates, Wires, Input);

  Wires["b"] = Override;

  while (!Wires["a"]) {
    for (auto &G : Gates)
      G.Update();
  }
  return Wires["a"].value();
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
  std::optional<int> Part1{RunInstructions(Input)};

  // Solve part 2
  std::optional<int> Part2{ReRunInstructions(Input, Part1.value())};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
