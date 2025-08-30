#include <string>
#include <vector>
#include <map>
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
    /* Read file into vector of strings */
    std::ifstream infile(argv[1]);
    std::vector<std::string> lines(std::istream_iterator<std::string>{infile},
        std::istream_iterator<std::string>{});

    std::map<std::string, std::string> orbitalMap{};

    /* Parse line at ) and put in map. */
    for (auto line : lines) {
        std::string value = line.substr(0, 3);
        std::string key = line.substr(4);
        orbitalMap[key] = value;
    }

    int count{ 0 };
    for (auto sat : orbitalMap) {
        ++count;
        std::string &parent = sat.second;
        while (parent !="COM")
        {
            ++count;
            parent = orbitalMap[sat.second];
        }
    }

    std::cout << "We have " << count << " orbits." << std::endl;

    return 1;
}
