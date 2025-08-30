#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <regex>
#include <unordered_map>

std::vector<std::string> GetFileContent(const std::string &FileName) {
  std::ifstream Input{FileName};
  std::vector<std::string> FileContent;
  std::string Line;

  while (std::getline(Input, Line))
    FileContent.push_back(Line);

  return FileContent;
}

struct Reindeer {
  std::string Name;
  int Speed;
  int Duration;
  int Rest;
};

auto ParseLines(std::vector<std::string> Lines) {
  std::vector<Reindeer> Reindeers;

  for (const auto &Line : Lines) {
    std::string Name;
    int Speed, Duration, Rest;

    const std::regex Pattern{
        R"(([a-zA-Z]+) can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds.)"};
    std::smatch Match;

    if (std::regex_match(Line, Match, Pattern)) {
      Name = Match[1];
      Speed = std::stoi(Match[2]);
      Duration = std::stoi(Match[3]);
      Rest = std::stoi(Match[4]);
    }

    Reindeers.emplace_back(Reindeer{Name, Speed, Duration, Rest});
  }
  return Reindeers;
}

int HowFar(const Reindeer &Rein, const int Time) {
  const int BlockDuration{Rein.Duration + Rein.Rest};
  const int BlockDistance{Rein.Speed * Rein.Duration};
  const int CompleteBlocks{Time / BlockDuration};
  const int LastBlockBit{Time % BlockDuration};

  int Distance{};
  if (LastBlockBit >= Rein.Duration) {
    Distance = (CompleteBlocks + 1) * BlockDistance;
  } else {
    Distance = CompleteBlocks * BlockDistance + LastBlockBit * Rein.Speed;
  }
  return Distance;
}

int WinningDistance(const std::vector<Reindeer> &Reindeers,
                    const int RaceDuration) {

  int BestDistance{0};
  for (const auto &Rein : Reindeers) {
    int Distance{HowFar(Rein, RaceDuration)};
    BestDistance = std::max(Distance, BestDistance);
  }

  return BestDistance;
}

int WinningPoints(std::vector<Reindeer> Reindeers, int RaceDuration) {
  std::unordered_map<std::string, int> ReinDistance;
  std::unordered_map<std::string, int> ReinPoints;

  for (int Sec{1}; Sec <= RaceDuration; ++Sec) {
    int LeadingDistance{0};

    // Find Leading Distance
    for (const auto &Rein : Reindeers) {
      int Distance{HowFar(Rein, Sec)};
      ReinDistance[Rein.Name] = Distance;
      LeadingDistance = std::max(LeadingDistance, Distance);
    }

    // Award Points
    for (const auto &Rein : Reindeers) {
      if (ReinDistance[Rein.Name] == LeadingDistance)
        ++ReinPoints[Rein.Name];
    }
  }

  int MostPoints{0};
  for (const auto &[_, Points] : ReinPoints) {
    MostPoints = std::max(MostPoints, Points);
  }
  return MostPoints;
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
  std::vector<Reindeer> Reindeers{ParseLines(Input)};

  //  Solve part 1
  std::optional<int> Part1{WinningDistance(Reindeers, 2503)};

  // Solve part 2
  std::optional<int> Part2{WinningPoints(Reindeers, 2503)};

  if (Part1)
    std::cout << "Part 1: " << *Part1 << std::endl;

  if (Part2)
    std::cout << "Part 2: " << *Part2 << std::endl;
}
