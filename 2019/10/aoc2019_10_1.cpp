#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <map>
#include <charconv>


/*
* 
* 
    1. Generer grunnkoordinatene.
        1a. X og Y må være delig på samme heltall.
        1b. Hvis X eller Y er et primtall så må det andre tallet være delig på det. som (9,3) => (3,1)
        1c. 
    2. For hver 8.del.
        2a. Hver 8.del har sitt koordinat multiplier, som (-1,1)
        2b. Bruk grunnkoordianter og multiplier for å lage koordinater 
        2c. Stopp når man går utenfor kartets maksgrenser.

*/
// Skal det være (x,y) som i oppgaven eller (y,x) som [y][x] i lines.

/* Ikke brukt */
std::vector<std::pair<int, int>> makeBaseCoordinates(const int x) {
    std::vector<std::pair<int, int>> coordinates{};

    // Er begge delbar på samme tall
    auto notDividable = [x](int y) {
        for (int i{ 2 }; i < x; ++i) {
            if (x % i == 0 && y % i == 0) {
                return false;
            }
        }
        return true;
    };

    for (int y{ 1 }; y < x; ++y) {
        // Det er her man kan skjekke alle åtte koordinatene som fåes fra en base.
        if (notDividable(y)) {
            coordinates.push_back(std::make_pair(x, y));
        }
    }
    return coordinates;
}

int observableAstroids(const std::vector<std::string> &map, int const x, int const y) {    
    int astroids{ 0 };

    const int mapsize{ static_cast<int>(map.size()) };
    
    // Er begge delbar på samme tall
    auto notDividable = [](int x,int y) {
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
            ++astroids;
            break;
        }
    }

    // Below
    for (int i{ y + 1 }; i < mapsize; ++i) {
        if (map[i][x] != '.') {
            ++astroids;
            break;
        }
    }
    // Left
    for (int i{ x - 1 }; i >= 0; --i) {
        if (map[y][i] != '.') {
            ++astroids;
            break;
        }
    }

    // Right
    for (int i{ x + 1 }; i < mapsize; ++i) {
        if (map[y][i] != '.') {
            ++astroids;
            break;
        }
    }

    // Above left
    // her kan vi treffe både 0 og 0
    for (int i{ y - 1 }, j{ x - 1 }; i >= 0 && j >= 0; --i, --j) {
        if (map[i][j] != '.') {
            ++astroids;
            break;
        }
    }

    // Below Left
    // her kan vi treffe både 0 og mapsize
    for (int i{ y + 1 }, j{ x - 1 }; i < mapsize && j >= 0; ++i, --j) {
        if (map[i][j] != '.') {
            ++astroids;
            break;
        }
    }

    // Above Right
    // her kan vi treffe både mapsize og 0
    for (int i{ y - 1 }, j{ x + 1 }; i >= 0 && j < mapsize; --i, ++j) {
        if (map[i][j] != '.') {
            ++astroids;
            break;
        }
    }

    // Below Right
    // her kan vi treffe både mapsize og mapsize
    for (int i{ y + 1 }, j{ x + 1 }; i < mapsize && j < mapsize; ++i, ++j) {
        if (map[i][j] != '.') {
            ++astroids;
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

    int checkX{ 2 };
    int checkY{ 2 };

    for (int i{ 2 }; i <= largestSide; ++i) {
        for (int j = 1; j < i; j++) {  // Første blir (2,1) 

            // Det er her man kan skjekke alle åtte koordinatene som fåes fra en base.
            if (notDividable(i, j)) {
                if (x == checkX && y == checkY) std::cout << "Checking " << i << " , " << j << "\n";
                // Need to multiply

                //int i{ ii };
                //int j{ jj };

                //for (int m{ 2 }; i <= largestSide; ++m) {
                //    if (x == checkX && y == checkY) {
                //        std::cout << "(" << i << "," << j << ")\n";
                //    }

                    // Trenger ikke endre map, bare slutter å lete i den retningen.
                    // Her er (i,j) som (x,y)                

                    
                    // koordianter som skal skjekkes er map[y+j][x+i]
                    // Kan treffe kant mot høre og bunn

                // (x,y) mot høyre og nedover
                for (int m{ 2 }, coordX{ x + i }, coordY{ y + j }; coordX < mapsize && coordY < mapsize; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 1: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        ++astroids;
                        break;
                    }
                    coordX = x + (i * m);
                    coordY = y + (j * m);
                }
                    
                    /*if (i <= right && j <= below) {
                        if (x == checkX && y == checkY) std::cout << "Block 1: ("<< x+i << "," << y+j << ")\n";
                        if (map[y + j][x + i] != '.')
                            ++astroids;
                    }*/
                
                // (y,x) nedover og mot høyre
                for (int m{ 2 }, coordX{ x + j }, coordY{ y + i }; coordX < mapsize && coordY < mapsize ; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 2: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        ++astroids;
                        break;
                    }
                    coordX = x + (j * m);
                    coordY = y + (i * m);
                }

                    /*if (i <= below && j <= right) {
                        if (x == checkX && y == checkY) std::cout << "Block 2: (" << x + j << "," << y + i << ")\n";
                        if (map[y + i][x + j] != '.')
                            ++astroids;
                    }*/


                // (y,-x) nedeover og mot vestre
                for (int m{ 2 }, coordX{ x - j }, coordY{ y + i}; coordX >= 0 && coordY < mapsize ; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 3: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        ++astroids;
                        break;
                    }
                    coordX = x - (j*m);
                    coordY = y + (i*m);
                }
                 /*   if (i <= below && j <= left) {
                        if (x == checkX && y == checkY) std::cout << "Block 3: (" << x - j << "," << y + i << ")\n";
                        if (map[y + i][x - j] != '.')
                            ++astroids;
                    }*/

                
                // (-x,y) mot vestre og nedover.
                for (int m{ 2 }, coordX{ x - i }, coordY{ y + j }; coordX >= 0 && coordY < mapsize; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 4: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        ++astroids;
                        break;
                    }
                    coordX = x - (i*m);
                    coordY = y + (j*m);
                }
                 /*   if (i <= left && j <= below) {
                        if (x == checkX && y == checkY) std::cout << "Block 4: (" << x - i << "," << y + j << ")\n";
                        if (map[y + j][x - i] != '.')
                            ++astroids;
                    }*/
                // (-x,-y) mot venstre og oppover
                for (int m{ 2 }, coordX{ x - i }, coordY{ y - j }; coordX >= 0 && coordY >= 0; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 5: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        ++astroids;
                        break;
                    }
                    coordX = x - (i*m);
                    coordY = y - (j*m);
                }
                    //if (i <= left && j <= above) { // 3 <= 3 4 <= 4
                    //    if (x == checkX && y == checkY) std::cout << "Block 5: (" << x - i << "," << y - j << ")\n";
                    //    if (map[y - j][x - i] != '.')
                    //        ++astroids;
                    //}
     
     
                // (-y,-x) oppover og mot vestre 
                for (int m{ 2 }, coordX{ x - j }, coordY{ y - i }; coordX >= 0 && coordY >= 0; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 6: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        ++astroids;
                        break;
                    }
                    coordX = x - (j * m);
                    coordY = y - (i * m);
                }
                    /*if (i <= above && j <= left) {
                        if (x == checkX && y == checkY) std::cout << "Block 6: (" << x - j << "," << y - i << ")\n";
                        if (map[y - i][x - j] != '.')
                            ++astroids;
                    }*/
                 
                    
                    // (-y,x) oppover og mot høyre
                for (int m{ 2 }, coordX{ x + j }, coordY{ y - i }; coordX < mapsize && coordY >= 0; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 7: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        ++astroids;
                        break;
                    }
                    coordX = x + (j * m);
                    coordY = y - (i * m);
                }                    
                /*if (i <= above && j <= right) {
                        if (x == checkX && y == checkY) std::cout << "Block 7: (" << x + j << "," << y - i << ")\n";
                        if (map[y - i][x + j] != '.')
                            ++astroids;
                    }*/


                    // (x,-y) mot høyre og oppover
                for (int m{ 2 }, coordX{ x + i }, coordY{ y - j }; coordX < mapsize && coordY >= 0; ++m) {
                    if (x == checkX && y == checkY) std::cout << "Block 8: (" << coordX << "," << coordY << ")\n";
                    if (map[coordY][coordX] != '.') {
                        ++astroids;
                        break;
                    }
                    coordX = x + (i * m);
                    coordY = y - (j * m);
                }                    
                    /*if (i <= right && j <= above) {
                        if (x == checkX && y == checkY) std::cout << "Block 8: (" << x + i << "," << y - j << ")\n";
                        if (map[y - j][x + i] != '.')
                            ++astroids;
                    }*/

                    /*i = ii * m;
                    j = jj * m;
                }*/
            }
        }
    }
    //map[y][x] = '0' + astroids;
    return astroids;
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

    int mapsizeY{ static_cast<int>( lines.size() ) };
    int mapsizeX{ static_cast<int>( lines[0].size() )};
    int maxAstroids{ 0 };

    for (int y{ 0 }; y < mapsizeY; ++y) {
        for (int x{ 0 }; x < mapsizeX; ++x) {
            if (lines[y][x] == '#') {
                // We have an astroid
                int astroids{ observableAstroids(lines, x, y) };
                if (astroids > maxAstroids)
                    maxAstroids = astroids;
            }
        }
    }

    for (auto &line : lines)
        std::cout << line << "\n";

    std::cout << "Max astroids coverage: " << maxAstroids << std::endl;

    return 1;
}