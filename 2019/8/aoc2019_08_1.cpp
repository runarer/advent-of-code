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
    std::string_view lineView{ line };

    size_t minZeros{ 150 };
    size_t minOnes { 0 };
    size_t minTwos { 0 };

    for (int i{ 0 }; i < 15000; i += 150) {
        auto image = lineView.substr(i, 150);
        size_t zeros = std::count(image.begin(), image.end(), '0');
        if (zeros < minZeros) {
            minZeros = zeros;
            minOnes = std::count(image.begin(), image.end(), '1');
            minTwos = 150 - zeros - minOnes;
        }
    }
    
    std::cout << "Minimum zeros layer has: " << minOnes * minTwos << std::endl;

    return 1;
}
