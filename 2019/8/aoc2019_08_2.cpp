#include <string>
#include <string_view>
#include <vector>
#include <array>
#include <deque>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

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
    /* Read file into string */
    std::ifstream infile(argv[1]);
    std::string line{};
    std::getline(infile, line);

    /* Use a view for read only operations. */
    //std::string_view lineView{ line };
    
    std::string finalImage{ line.substr(0,150) };
    for (int i{ 0 }; i < 150; ++i) {
        if (finalImage[i] == '2') {
            for (int j{ 150 }; j < 15000; j += 150) {
                if (line[j + i] != '2') {
                    finalImage[i] = line[j + i];
                    break;
                }
            }
        }
    }

    std::string_view finalView{ finalImage };
    for (int i{ 0 }; i < 6; ++i) {
        std::cout << finalView.substr(i*25, 25) << '\n';
    }

    return 1;
}
