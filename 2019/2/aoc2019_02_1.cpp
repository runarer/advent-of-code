#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

int runProgram(std::vector<int>& intcode) {
    int pos{ 0 };
    while (intcode[pos] != 99) {
        switch (intcode[pos])
        {
        case 1:
            intcode[intcode[pos + 3]] = intcode[intcode[pos + 1]] + intcode[intcode[pos + 2]];
            break;
        case 2:
            intcode[intcode[pos + 3]] = intcode[intcode[pos + 1]] * intcode[intcode[pos + 2]];
            break;
        default:
            return 0;
        }
        pos += 4;
    }
    return 1;
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
    /* Read file into string */
    std::ifstream infile(argv[1]);
    std::string line{};
    std::getline(infile, line);

    /* Parse line at commas and put in vector. */
    auto ints = line | std::views::split(',');    
    std::vector<std::string> instructions(ints.begin(),ints.end());

    /* Transform strings to integers */
    std::vector<int> intcode;
    intcode.resize(instructions.size());
    std::transform(instructions.begin(), instructions.end(), intcode.begin(), [](std::string const& s) { return std::stoi(s); });
    
    /* Change list according to task. */
    intcode[1] = 12;
    intcode[2] = 2;

    /* Run program */
    if (runProgram(intcode)) {
        std::cout << "Succsess: " << intcode[0] << std::endl;
    }
    else {
        std::cout << "Failed" << std::endl;
    }

    //for (auto value : intcode)
    //    std::cout << value << "\n";

    return 1;
}