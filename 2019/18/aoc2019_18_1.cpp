#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <queue>

class CaveMap 
{
public:
    CaveMap(const std::vector<std::string> &map);
private:
    void printMap();
    void fillDeadEnds(std::vector<std::pair<int, int>>& deadends);
    auto removeDeadEndDoors() -> std::vector<char>;
    void findKeyToKey();
    void findTopLevelItems();
    std::vector<std::string> cavemap;
    std::pair<int, int> start;
    std::vector<std::tuple<char, int, int>> keys;
    std::vector<std::tuple<char, int, int>> doors;
    std::vector < std::vector<int>> keyToKey;
    std::vector<std::pair<char,int>> topLevelKeys{};
    std::vector<char> topLevelDoors{};
    const int mapH{};
    const int mapW{};
};

CaveMap::CaveMap(const std::vector<std::string>& map) : mapH{ static_cast<int>(map.size()) }, mapW{ static_cast<int>(map[0].size()) }
{
    cavemap = map;

    std::vector<std::pair<int, int>> deadends{};

    /* Find all points of interest*/
    for (int i = 1; i < mapH - 1; i++) {
        for (int j = 1; j < mapW - 1; j++) {
            /* Wall */
            if (map[i][j] == '#')
                continue;
            /* Open */
            if (map[i][j] == '.') {
                int wallsNear{ 0 };
                if (map[i][j + 1] == '#') wallsNear++;
                if (map[i][j - 1] == '#') wallsNear++;
                if (map[i + 1][j] == '#') wallsNear++;
                if (map[i - 1][j] == '#') wallsNear++;

                /* Deadend */
                if (wallsNear == 3) {
                    deadends.push_back(std::make_pair(i, j));
                    //cavemap[i][j] = '*';
                }
                /* Hallway */
                //else if (wallsNear == 2) {
                //    deadends.push_back(std::make_pair(i, j));
                //    cavemap[i][j] = '-';
                //}
                /* Cross */
                // else if (wallsNear <= 1) {
                //    deadends.push_back(std::make_pair(i, j));
                //    cavemap[i][j] = '+';
                //}
            }
            /* Door */
            else if (isupper(map[i][j])) {
                doors.push_back(std::make_tuple(map[i][j], i, j));
            }
            /* Key */
            else if (islower(map[i][j])) {
                keys.push_back(std::make_tuple(map[i][j], i, j));
            }
            /* Start */
            else if (map[i][j] == '@') {
                start = std::make_pair(i, j);
            }
        }
    }

    cavemap[start.first][start.second] = '.';

    fillDeadEnds(deadends);
    std::vector<char> uselessKeys = removeDeadEndDoors();
    std::transform(uselessKeys.begin(), uselessKeys.end(), uselessKeys.begin(), tolower);

    std::cout << "Useless keys:  "; for (auto c : uselessKeys) std::cout << c; std::cout << '\n';

    findKeyToKey();
    findTopLevelItems();
    std::cout << "Toplevel keys:  "; for (auto c : topLevelKeys) std::cout << c.first << c.second; std::cout << '\n';
    std::cout << "Toplevel Doors: "; for (auto c : topLevelDoors) std::cout << c; std::cout << '\n';
    printMap();
    
    std::string solution {"iawqtgvsdefykxmnjzopbluhcr"}; // Funnet manuelt.

    int steps = 0;
    for (auto& k : topLevelKeys) {
        if (k.first == solution[0]) {
            steps += k.second;
            break;
        }
    }
    std::cout << "\nWalking:\n";
    for (int i = 0; i < solution.size() - 1; i++) {
        std::cout << "From: " << solution[i] << " to " << solution[i + 1] << " in " << keyToKey[static_cast<int>(solution[i]) - 97][static_cast<int>(solution[i + 1]) - 97] <<" steps\n";
        steps += keyToKey[static_cast<int>(solution[i]) - 97][static_cast<int>(solution[i + 1]) - 97];
    }
    std::cout << "\nSteps: " << steps << std::endl;    

}

void CaveMap::printMap()
{
    std::cout << "\nCave Map:\n";
    for (auto line : cavemap)
        std::cout << line << '\n';
    std::cout << '\n';
}

void CaveMap::fillDeadEnds(std::vector<std::pair<int, int>>& deadends)
{
    for (auto deadend : deadends) {
        auto [nextI, nextJ] = deadend;
        int wallsNear{ 3 };

        while (wallsNear >= 3) {
            // Fill in deadend
            cavemap[nextI][nextJ] = '#';

            // Find nextI and nextJ
            if (cavemap[nextI][nextJ + 1] != '#') {
                nextJ++;
            }
            else if (cavemap[nextI][nextJ - 1] != '#') {
                nextJ--;
            }
            else if (cavemap[nextI + 1][nextJ] != '#') {
                nextI++;
            }
            else if (cavemap[nextI - 1][nextJ] != '#') {
                nextI--;
            }
            
            // Is it a point of interest?
            if (cavemap[nextI][nextJ] != '.')
                break;
            
            // Find wallsNear
            wallsNear = 0;
            if (cavemap[nextI][nextJ + 1] == '#') wallsNear++;
            if (cavemap[nextI][nextJ - 1] == '#') wallsNear++;
            if (cavemap[nextI + 1][nextJ] == '#') wallsNear++;
            if (cavemap[nextI - 1][nextJ] == '#') wallsNear++;
        }
    }
}

auto CaveMap::removeDeadEndDoors() -> std::vector<char>
{
    std::vector<char> doorsRemoved{};

    for (auto& d : doors) {
        auto [door,nextI, nextJ] = d;

        // Allready removed?
        if (cavemap[nextI][nextJ] == '#')
            continue;

        int wallsNear{ 0 };
        if (cavemap[nextI][nextJ + 1] == '#') wallsNear++;
        if (cavemap[nextI][nextJ - 1] == '#') wallsNear++;
        if (cavemap[nextI + 1][nextJ] == '#') wallsNear++;
        if (cavemap[nextI - 1][nextJ] == '#') wallsNear++;

        if (wallsNear >= 3) {
            doorsRemoved.push_back(door);
        }
        else {
            continue;
        }

        while (wallsNear >= 3) {
            // Fill in deadend
            cavemap[nextI][nextJ] = '#';

            // Find nextI and nextJ
            if (cavemap[nextI][nextJ + 1] != '#') {
                nextJ++;
            }
            else if (cavemap[nextI][nextJ - 1] != '#') {
                nextJ--;
            }
            else if (cavemap[nextI + 1][nextJ] != '#') {
                nextI++;
            }
            else if (cavemap[nextI - 1][nextJ] != '#') {
                nextI--;
            }

            // Is it a point of interest?
            if (cavemap[nextI][nextJ] != '.') {
                if (isupper(cavemap[nextI][nextJ]))
                    doorsRemoved.push_back(cavemap[nextI][nextJ]);
                else
                    break;
            }                

            // Find wallsNear
            wallsNear = 0;
            if (cavemap[nextI][nextJ + 1] == '#') wallsNear++;
            if (cavemap[nextI][nextJ - 1] == '#') wallsNear++;
            if (cavemap[nextI + 1][nextJ] == '#') wallsNear++;
            if (cavemap[nextI - 1][nextJ] == '#') wallsNear++;
        }
    }
    std::cout << "\nDoors removed: ";
    for (auto c : doorsRemoved) 
        std::cout << c;
    std::cout << '\n';

    return doorsRemoved;
}

void CaveMap::findKeyToKey()
{
    keyToKey = std::vector<std::vector<int>>(keys.size(), std::vector<int>(keys.size()) );
    std::queue<std::pair<int, int>> next{};
    // a is 97 in ascii

    // For each key in keys, do a BFS for all other keys.
    for (auto& key : keys) {
        auto& [door, startI, startJ] = key;
        next.push(std::make_pair(startI, startJ));
        std::vector<std::vector<int>> steps(mapH, std::vector<int>(mapW, mapH*mapW) );
        steps[startI][startJ] = 0;
        
        std::vector<int>& toKeys = keyToKey[static_cast<int>(door) - 97];

        // Walk the whole cave.
        // Will not find itself, its ok, as it is initialized to 0
        while (!next.empty()) {
            auto [posI,posJ] = next.front();
            next.pop();
            
            int neighbors[4][2]{ {posI + 1,posJ}, {posI - 1,posJ}, {posI,posJ + 1}, {posI,posJ - 1} };
            int next_steps = steps[posI][posJ] + 1;
                        
            for (auto& [nextI, nextJ] : neighbors) {
                if (cavemap[nextI][nextJ] == '#')
                    continue;
                
                // Allready a shorter or equal path.
                if (steps[nextI][nextJ] < next_steps)
                    continue;

                next.push(std::make_pair(nextI, nextJ));
                steps[nextI][nextJ] = next_steps;
                if (islower(cavemap[nextI][nextJ])) {
                    toKeys[static_cast<int>(cavemap[nextI][nextJ]) - 97] = next_steps;
                }
            }
        }
    }
    
    //std::cout << "From y to t: " << keyToKey[static_cast<int>('y') - 97][static_cast<int>('t') - 97] << '\n';
    
}

void CaveMap::findTopLevelItems()
{
    //From @ find all keys and Doors, while treating doors as walls.
    std::queue<std::pair<int, int>> next{};
    next.push(std::make_pair(start.first, start.second));
    std::vector<std::vector<int>> steps(mapH, std::vector<int>(mapW, mapH * mapW));
    steps[start.first][start.second] = 0;    

    // Walk the cave
    while (!next.empty()) {
        auto [posI, posJ] = next.front();
        next.pop();

        int neighbors[4][2]{ {posI + 1,posJ}, {posI - 1,posJ}, {posI,posJ + 1}, {posI,posJ - 1} };
        int next_steps = steps[posI][posJ] + 1;

       for (auto& [nextI, nextJ] : neighbors) {
            if (cavemap[nextI][nextJ] == '#')
                continue;            

            // Allready a shorter or equal path.
            if (steps[nextI][nextJ] < next_steps)
                continue;
            steps[nextI][nextJ] = next_steps;

            if (isupper(cavemap[nextI][nextJ])) {
                if (std::find(topLevelDoors.begin(), topLevelDoors.end(), cavemap[nextI][nextJ]) == topLevelDoors.end())
                    topLevelDoors.push_back(cavemap[nextI][nextJ]);
                continue;
            }

            next.push(std::make_pair(nextI, nextJ));            
            if (islower(cavemap[nextI][nextJ])) {
                bool allreadyFound = false;
                for (auto& foundKey : topLevelKeys) {
                    if (foundKey.first == cavemap[nextI][nextJ])
                        allreadyFound = true;
                }
                if (!allreadyFound)
                    topLevelKeys.push_back(std::make_pair(cavemap[nextI][nextJ], next_steps));
            }
        }
    }    
}

int main(int argc, char* argv[]) {

    /* Handle input, a file name */
    if (argc <= 1)
    {
        if (!argv[0])
            std::cout << "Usage: <program name> <input file>" << std::endl;
        else
            std::cout << "Usage: " << argv[0] << " <input file>" << std::endl;
        return 1;
    }

    /* Read file */
    std::ifstream infile(argv[1]);
    std::vector<std::string> lines(std::istream_iterator<std::string>{infile},
        std::istream_iterator<std::string>{});

    CaveMap map(lines);

    for (auto& line : lines)
        std::cout << line << "\n";

    return 1;
}