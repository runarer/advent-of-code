#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <map>
#include <charconv>
#include <algorithm>
#include <functional>

/* I have the hits from part one. Change that algorithm to give a list. */
std::vector<std::pair<int,int>> observableAstroids(const std::vector<std::string>& map, int const x, int const y) {
    //int astroids{ 0 };
    std::vector<std::pair<int, int>> astroids{};

    const int mapsize{ static_cast<int>(map.size()) };

    // Er begge delbar på samme tall
    auto notDividable = [](int x, int y) {
        for (int i{ 2 }; i <= y; ++i) {
            if (x % i == 0 && y % i == 0) {
                return false;
            }
        }
        return true;
    };

    /* Find astroids */
    // Above
    for (int i{ y - 1 }; i >= 0; --i) {
        if (map[i][x] != '.') {
            //++astroids;            
            astroids.push_back(std::make_pair(x,i));
            break;
        }
    }

    // Below
    for (int i{ y + 1 }; i < mapsize; ++i) {
        if (map[i][x] != '.') {
            //++astroids;
            astroids.push_back(std::make_pair(x, i));
            break;
        }
    }
    // Left
    for (int i{ x - 1 }; i >= 0; --i) {
        if (map[y][i] != '.') {
            //++astroids;
            astroids.push_back(std::make_pair(i, y));
            break;
        }
    }

    // Right
    for (int i{ x + 1 }; i < mapsize; ++i) {
        if (map[y][i] != '.') {
            //++astroids;
            astroids.push_back(std::make_pair(i, y));
            break;
        }
    }

    // Above left
    // her kan vi treffe både 0 og 0
    for (int i{ y - 1 }, j{ x - 1 }; i >= 0 && j >= 0; --i, --j) {
        if (map[i][j] != '.') {
            //++astroids;
            astroids.push_back(std::make_pair(j, i));
            break;
        }
    }

    // Below Left
    // her kan vi treffe både 0 og mapsize
    for (int i{ y + 1 }, j{ x - 1 }; i < mapsize && j >= 0; ++i, --j) {
        if (map[i][j] != '.') {
            //++astroids;
            astroids.push_back(std::make_pair(j, i));
            break;
        }
    }

    // Above Right
    // her kan vi treffe både mapsize og 0
    for (int i{ y - 1 }, j{ x + 1 }; i >= 0 && j < mapsize; --i, ++j) {
        if (map[i][j] != '.') {
            //++astroids;
            astroids.push_back(std::make_pair(j, i));
            break;
        }
    }

    // Below Right
    // her kan vi treffe både mapsize og mapsize
    for (int i{ y + 1 }, j{ x + 1 }; i < mapsize && j < mapsize; ++i, ++j) {
        if (map[i][j] != '.') {
            //++astroids;
            astroids.push_back(std::make_pair(j, i));
            break;
        }
    }

    //// 8.delene
    // Fin største side
    int largestSide{ x };
    for (int side : { mapsize - y - 1, mapsize - x - 1, y }) {
        if (side > largestSide)
            largestSide = side;
    }

    int checkX{ -1 };
    int checkY{ -1 };

    for (int i{ 2 }; i <= largestSide; ++i) {
        for (int j = 1; j < i; j++) {  // Første blir (2,1) 

            // Det er her man kan skjekke alle åtte koordinatene som fåes fra en base.
            if (notDividable(i, j)) {
                if (x == checkX && y == checkY) std::cout << "Checking " << i << " , " << j << "\n";

                // (x,y) mot høyre og nedover
                for (int m{ 2 }, coordX{ x + i }, coordY{ y + j }; coordX < mapsize && coordY < mapsize; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 1: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        //++astroids;
                        astroids.push_back(std::make_pair(coordX, coordY));
                        break;
                    }
                    coordX = x + (i * m);
                    coordY = y + (j * m);
                }


                // (y,x) nedover og mot høyre
                for (int m{ 2 }, coordX{ x + j }, coordY{ y + i }; coordX < mapsize && coordY < mapsize; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 2: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        //++astroids;
                        astroids.push_back(std::make_pair(coordX, coordY));
                        break;
                    }
                    coordX = x + (j * m);
                    coordY = y + (i * m);
                }


                // (y,-x) nedeover og mot vestre
                for (int m{ 2 }, coordX{ x - j }, coordY{ y + i }; coordX >= 0 && coordY < mapsize; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 3: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        //++astroids;
                        astroids.push_back(std::make_pair(coordX, coordY));
                        break;
                    }
                    coordX = x - (j * m);
                    coordY = y + (i * m);
                }


                // (-x,y) mot vestre og nedover.
                for (int m{ 2 }, coordX{ x - i }, coordY{ y + j }; coordX >= 0 && coordY < mapsize; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 4: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        //++astroids;
                        astroids.push_back(std::make_pair(coordX, coordY));
                        break;
                    }
                    coordX = x - (i * m);
                    coordY = y + (j * m);
                }


                // (-x,-y) mot venstre og oppover
                for (int m{ 2 }, coordX{ x - i }, coordY{ y - j }; coordX >= 0 && coordY >= 0; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 5: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        //++astroids;
                        astroids.push_back(std::make_pair(coordX, coordY));
                        break;
                    }
                    coordX = x - (i * m);
                    coordY = y - (j * m);
                }

                // (-y,-x) oppover og mot vestre 
                for (int m{ 2 }, coordX{ x - j }, coordY{ y - i }; coordX >= 0 && coordY >= 0; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 6: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        //++astroids;
                        astroids.push_back(std::make_pair(coordX, coordY));
                        break;
                    }
                    coordX = x - (j * m);
                    coordY = y - (i * m);
                }


                // (-y,x) oppover og mot høyre
                for (int m{ 2 }, coordX{ x + j }, coordY{ y - i }; coordX < mapsize && coordY >= 0; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 7: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        //++astroids;
                        astroids.push_back(std::make_pair(coordX, coordY));
                        break;
                    }
                    coordX = x + (j * m);
                    coordY = y - (i * m);
                }
                

                // (x,-y) mot høyre og oppover
                for (int m{ 2 }, coordX{ x + i }, coordY{ y - j }; coordX < mapsize && coordY >= 0; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 8: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        //++astroids;
                        astroids.push_back(std::make_pair(coordX, coordY));
                        break;
                    }
                    coordX = x + (i * m);
                    coordY = y - (j * m);
                }
            }
        }
    }
    //map[y][x] = '0' + astroids;
    return astroids;
}

int findAnswer(std::vector<std::pair<int,int>> points, const int x0, const int y0, const int nHit) {
    std::vector< std::pair< double,std::pair<int, int> > > angles;

    std::transform(points.begin(), points.end(), std::back_inserter(angles),
        [x0, y0](std::pair<int, int> coord) -> std::pair<double,std::pair<int, int>> {
            return std::make_pair(atan2(coord.first - x0, coord.second - y0),coord);
        });

    // Sort angles by second in pair
    std::sort(angles.begin(), angles.end(), std::greater());

    return angles[nHit-1].second.first*100 + angles[nHit-1].second.second;
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

    int mapsizeY{ static_cast<int>(lines.size()) };
    int mapsizeX{ static_cast<int>(lines[0].size()) };

    int maxX{ 22 };
    int maxY{ 25 };


    // Create list for maxX,maxY
    std::vector<std::pair<int, int>> astroids{ observableAstroids(lines,maxX,maxY) };

    // Create angle list
    int answer{ findAnswer(astroids,maxX,maxY,200)};

    std::cout << "The answer is " << answer << std::endl;

    return 1;
}