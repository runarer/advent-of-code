#include <string>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

std::vector<int> runProgram(std::vector<int> intcode, std::vector<int> input) {
    std::vector<int> output{};
    int pointer{ 0 };
    int inputPointer{ 0 };

    while (intcode[pointer] != 99) {
        int parametermode3{ 0 };
        int parametermode2{ 0 };
        int parametermode1{ 0 };
        int instruction{ intcode[pointer] };

        /* Parse instruction */
        if (instruction >= 10000) {
            // Parameter mode 3
            parametermode3 = instruction / 10000;
            instruction %= 10000;
        }
        if (instruction >= 1000) {
            // Parameter mode 2
            parametermode2 = instruction / 1000;
            instruction %= 1000;
        }
        if (instruction >= 100) {
            // Parameter mode 1
            parametermode1 = instruction / 100;
            instruction %= 100;
        }

        switch (instruction)
        {
            // This will only work with parameter mode 'not 0' and 0.
        case 1: // add
            intcode[intcode[pointer + 3]] = intcode[parametermode1 ? pointer + 1 : intcode[pointer + 1]]
                + intcode[parametermode2 ? pointer + 2 : intcode[pointer + 2]];
            pointer += 4;
            break;
        case 2: // multi
            intcode[intcode[pointer + 3]] = intcode[parametermode1 ? pointer + 1 : intcode[pointer + 1]]
                * intcode[parametermode2 ? pointer + 2 : intcode[pointer + 2]];
            pointer += 4;
            break;
        case 3: // read input
            intcode[intcode[pointer + 1]] = input[inputPointer++];
            pointer += 2;
            break;
        case 4: // output
            output.push_back(intcode[parametermode1 ? pointer + 1 : intcode[pointer + 1]]);
            pointer += 2;
            break;
        case 5: // Jump-if-true
            if (intcode[parametermode1 ? pointer + 1 : intcode[pointer + 1]]) {
                pointer = intcode[parametermode2 ? pointer + 2 : intcode[pointer + 2]];
            }
            else {
                pointer += 3;
            }
            break;
        case 6: // Jump-if-false
            if (!(intcode[parametermode1 ? pointer + 1 : intcode[pointer + 1]])) {
                pointer = intcode[parametermode2 ? pointer + 2 : intcode[pointer + 2]];
            }
            else {
                pointer += 3;
            }
            break;
        case 7: // less than
            if ((intcode[parametermode1 ? pointer + 1 : intcode[pointer + 1]])
                < (intcode[parametermode2 ? pointer + 2 : intcode[pointer + 2]]))
            {
                intcode[intcode[pointer + 3]] = 1;
            }
            else {
                intcode[intcode[pointer + 3]] = 0;
            }
            pointer += 4;
            break;
        case 8: // equal to
            if ((intcode[parametermode1 ? pointer + 1 : intcode[pointer + 1]])
                == (intcode[parametermode2 ? pointer + 2 : intcode[pointer + 2]]))
            {
                intcode[intcode[pointer + 3]] = 1;
            }
            else {
                intcode[intcode[pointer + 3]] = 0;
            }
            pointer += 4;
            break;
        default:
            std::cout << " Something went wrong, " << intcode[pointer] << std::endl;
            intcode[pointer] = 99; // Halt
            break;
        }
    }

    return output;
}

int amplifiers(std::vector<int> &intcode, std::array<int,5> setup, int inputSignal) {    
    for (int phase : setup) {
        inputSignal = runProgram(intcode, std::vector<int>{phase, inputSignal})[0];
    }
    return inputSignal;
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
    std::vector<std::string> instructions(ints.begin(), ints.end());

    /* Transform strings to integers */
    std::vector<int> intcode;
    intcode.resize(instructions.size());
    std::transform(instructions.begin(), instructions.end(), intcode.begin(), [](std::string const& s) { return std::stoi(s); });

    /* Run program */
    std::array<int, 5> signals{ 0,1,2,3,4 };
    int maxThrust{ 0 };
    do {
        int thrust{amplifiers(intcode,signals,0)};
        if (thrust > maxThrust) 
            maxThrust = thrust;
    } while (std::next_permutation(signals.begin(), signals.end()));

    std::cout << "Max thrust is: " << maxThrust <<std::endl;

    return 1;
}
