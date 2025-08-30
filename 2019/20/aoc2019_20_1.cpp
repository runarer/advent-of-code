/* 
* Start by reading maze into a char 2d vector. 
* Fill in dead ends? (from 18). 
* Make a map of connections. From:To
*/


/*
  Find portals. If isupper()

  First two rows, Find isupper. Combine with char under. Get coordiantes from under that one.
  Last two rows, Find isupper. Combine with char under. Get coordiantes from over.
  Left side, First isupper. Combine with next. Get coordiantes for next after.
  Right side, Next last colume, isupper, Combine with next, get coordiantes from before.
*/

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <queue>
#include <map>

class MazeMap 
{
public:
    MazeMap(const std::vector<std::string> &map);
    auto findFastestPath() -> int;
private:
    void printMap();
    void newConnection(std::string portal, std::pair<int, int> coords);
    std::vector<std::string> mazemap;
    std::pair<int, int> start;
    std::pair<int, int> target;
    std::map<std::pair<int, int>, std::pair<int, int>> portals{};
    std::map<std::string, std::pair<int, int>> connections{};

    const int mapH{};
    const int mapW{};
};

MazeMap::MazeMap(const std::vector<std::string>& map) : mapH{ static_cast<int>(map.size()) }, mapW{ static_cast<int>(map[0].size()) }
{
    mazemap = map;    

    /* Find all portals, start and end. */
    /* Top portals */
    for (int i = 2; i < mazemap[0].size()-2; i++) {
        if (isupper(mazemap[0][i])) {
            newConnection({ mazemap[0][i],mazemap[1][i] }, { 2,i });
        }        
    }
    /* Bottom portals */
    for (int i = 2; i < mazemap[0].size()-2; i++) {
        if (isupper(mazemap[mazemap.size()-2][i])) {
            newConnection({ mazemap[mazemap.size() - 2][i],mazemap[mazemap.size() - 1][i] }, { mazemap.size() - 3,i });
        }
    }
    /* Left portals */
    for (int i = 2; i < mazemap.size()-2; i++) {
        if (isupper(mazemap[i][0])) {
            newConnection({ mazemap[i][0],mazemap[i][1] }, { i,2 });
        }
    }
    /* Right portals */
    for (int i = 2; i < mazemap.size() - 2; i++) {
        if (isupper(mazemap[i][mazemap[i].size()-2])) {
            newConnection({ mazemap[i][mazemap[i].size() - 2],mazemap[i][mazemap[i].size() - 1] }, { i,mazemap[i].size() - 3});
        }
    }

    /* Find donut hole. Dette burde kunne løses enklerer og mer elegant. */
    int donutX = 2;
    int donutY = 2;
    for (donutY = 2; donutY < mazemap.size() - 2; donutY++) {
        size_t found = mazemap[donutY].find(" ", 2);
        if (found != std::string::npos && found < mazemap[donutY].size()-2) {
            donutX = found;
            break;
        }
    }    
    
    //std::cout << "\nDonut Hole at: " << donutY << "," << donutX;
    
    /* Top Side of donut hole. */
    for (int i = donutX; mazemap[i][donutX] != '#'; i++) {
        if (isupper(mazemap[donutY][i])) {
            newConnection({ mazemap[donutY][i],mazemap[donutY + 1][i] }, { donutY - 1,i });
        }
    }

    /* Left Side of donut hole. */
    for (int i = donutY; mazemap[i][donutX] != '#'; i++) {
        if (isupper(mazemap[i][donutX])) {
            newConnection({ mazemap[i][donutX],mazemap[i][donutX + 1] }, { i,donutX - 1 });
        }
    }

    int donutW = mazemap[donutY].find("#", donutX);
    if (donutW == std::string::npos) {
        std::cout << "Error";
    }
    donutW--;
    
    /* Right Side of donut hole. */
    for (int i = donutY; mazemap[i][donutW] != '#'; i++) {
        if (isupper(mazemap[i][donutW])) {
            newConnection({ mazemap[i][donutW-1],mazemap[i][donutW] }, { i,donutW + 1 });
        }
    }

    int donutH = 0;
    for (donutH = donutY; mazemap[donutH][donutX] != '#'; donutH++);
    donutH--;
    
    /* Bottom Side of donut hole. */
    for (int i = donutX; mazemap[donutH][i] != '#'; i++) {
        if (isupper(mazemap[donutH][i])) {
            newConnection({ mazemap[donutH-1][i],mazemap[donutH][i] }, { donutH + 1,i });
        }
    }

    //std::cout << "\nDonut Hole W: " << donutW;
    //std::cout << "\nDonut Hole H: " << donutH;
    //std::cout << "\nSize of map " << portals.size() << "\n";

    //for (auto const& [key, value] : portals) std::cout << "\n(" << key.first << "," << key.second << ") -> (" << value.first << "," << value.second << ")";
    //std::cout << "\nStart (" << start.first << "," << start.second << "), Target: (" << target.first << "," << target.second << ")";

    /* Put a wall at start. */
    if (mazemap[start.first+1][start.second] == '.') {
        mazemap[start.first][start.second] = '#';
        start = { start.first + 1, start.second };
    }
    else if (mazemap[start.first - 1][start.second] == '.') {
        mazemap[start.first][start.second] = '#';
        start = { start.first - 1, start.second };
    }
    else if (mazemap[start.first][start.second + 1] == '.') {
        mazemap[start.first][start.second] = '#';
        start = { start.first, start.second + 1};
    }
    else if (mazemap[start.first][start.second - 1] == '.') {
        mazemap[start.first][start.second] = '#';
        start = { start.first, start.second - 1 };
    }

    //printMap();
}

void MazeMap::newConnection(std::string portal, std::pair<int,int> coords) {
    //std::cout << "\nFound " << portal << " at (" << coords.first << "," << coords.second << ")";
    if (portal == "AA") {
        start = coords;
    }
    else if(portal == "ZZ") {
        target = coords;
    }
    else if (connections.find(portal) == connections.end()) {
        connections.insert(std::make_pair(portal, coords));
    }
    else {
        //std::cout << " Allready found: " << portal;
        portals[connections[portal]] = coords;
        portals[coords] = connections[portal];
        connections.erase(portal);
    }
}

void MazeMap::printMap()
{
    std::cout << "\nCave Map:\n";
    for (auto line : mazemap)
        std::cout << line << '\n';
    std::cout << '\n';
}

auto MazeMap::findFastestPath() -> int {
    // make copy of map for steps.
    std::vector<std::vector<int>> steps(mapH, std::vector<int>(mapW,mapH*mapW));
    std::queue<std::pair<int, int>> next{  };
    next.push(start);
    steps[start.first][start.second] = 1; // We have allready moved one.

    // Walk the cave
    while (!next.empty()) {
        /* Shortest path is allready found. */
        if (next.front() == target) {
            break;
        }
        
        auto [posI, posJ] = next.front();
        next.pop();

        int neighbors[4][2]{ {posI + 1,posJ}, {posI - 1,posJ}, {posI,posJ + 1}, {posI,posJ - 1} };
        int next_steps = steps[posI][posJ] + 1;

        for (auto& [nextI, nextJ] : neighbors) {
            if (mazemap[nextI][nextJ] == '#')
                continue;
            
            if (isupper(mazemap[nextI][nextJ])) {
                auto& portal = portals[{posI, posJ}];
                nextI = portal.first;
                nextJ = portal.second;                
            }

            // Allready a shorter or equal path.
            if (steps[nextI][nextJ] < next_steps)
                continue;
            steps[nextI][nextJ] = next_steps;


            next.push(std::make_pair(nextI, nextJ));
        }
    }
    return steps[target.first][target.second];
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
    std::vector<std::string> lines{};
    while (!infile.eof()) {
        std::string line{};
        if (getline(infile, line)) {
            lines.push_back(line);
        }
    }
    infile.close();

    MazeMap map(lines);
    int steps{ map.findFastestPath() };

    std::cout << "\nShortest Path is: " << steps << std::endl;

    return 0;
}