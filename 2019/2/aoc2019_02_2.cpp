#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

/* Dette er ikke den samme som løste oppgaven. Men den fungerer og er veldig lik. */

bool runProgram(std::vector<int> intcode,int noun, int verb, int succCode) {
    int pos{ 0 };
    intcode[1] = noun;
    intcode[2] = verb;

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
            return false;
        }
        pos += 4;
    }

    return intcode[0] == succCode;
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
 
    /* Run program */
    for(int i{0}; i <= 100; ++i)
        for(int j{0}; j <= 100; ++j)
            if (runProgram(intcode,i,j,19690720)) {
                std::cout << "Succsess: " << ( 100*i + j) << std::endl;
                i = 101;
                break;
            }

    return 1;
}