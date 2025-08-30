#include <map>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <ranges>
#include <algorithm>
#include <iterator>

/*
    Need to change memory to map<int,long long>.
    If input is a vector, then add that to map
*/
class Game
{
public:
    Game(std::vector<long long> program);
    std::vector<int> run(long long input);

private:
    std::map<int, long long> mem{};
    std::vector<long long> io{};
    int ptr{ 0 };
    int rb{ 0 };
    bool halted{ false };
};

Game::Game(std::vector<long long> program)
{
    /* Load program to mem, index får nullverdien til size_t og settes til den typen, */
    for (auto index = std::size_t{}; auto & instruction : program) {
        mem[index++] = instruction;
    }

    /*  */

}

std::vector<int> Game::run(long long input) {
    std::vector<int> output{};
    

    while (mem[ptr] != 99) {
        int pm3{ 0 };
        int pm2{ 0 };
        int pm1{ 0 };
        long long instruction{ mem[ptr] };

        /* Parse instruction */
        if (instruction >= 10000) {
            // Parameter mode 3
            pm3 = instruction / 10000;
            instruction %= 10000;
        }
        if (instruction >= 1000) {
            // Parameter mode 2
            pm2 = instruction / 1000;
            instruction %= 1000;
        }
        if (instruction >= 100) {
            // Parameter mode 1
            pm1 = instruction / 100;
            instruction %= 100;
        }

        switch (instruction)
        {
        case 1: // add
            mem[pm3 == 2 ? mem[ptr + 3] + rb : mem[ptr + 3]] =
                mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]]
                + mem[pm2 ? pm2 == 2 ? mem[ptr + 2] + rb : ptr + 2 : mem[ptr + 2]];
            ptr += 4;
            break;
        case 2: // multi
            mem[pm3 == 2 ? mem[ptr + 3] + rb : mem[ptr + 3]] =
                mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]]
                * mem[pm2 ? pm2 == 2 ? mem[ptr + 2] + rb : ptr + 2 : mem[ptr + 2]];
            ptr += 4;
            break;
        case 3: // read input
            //std::cout << input << '\n';
            mem[pm1 == 2 ? mem[ptr + 1] + rb : mem[ptr + 1]] = input;
            ptr += 2;
            break;
        case 4: // output            
            output.push_back(mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]]);
            //std::cout << output << '\n';            
            ptr += 2;            
            break;
        case 5: // Jump-if-true
            if (mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]]) {
                ptr = mem[pm2 ? pm2 == 2 ? mem[ptr + 2] + rb : ptr + 2 : mem[ptr + 2]];
            }
            else {
                ptr += 3;
            }
            break;
        case 6: // Jump-if-false
            if (!(mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]])) {
                ptr = mem[pm2 ? pm2 == 2 ? mem[ptr + 2] + rb : ptr + 2 : mem[ptr + 2]];
            }
            else {
                ptr += 3;
            }
            break;
        case 7: // less than
            if ((mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]])
                < (mem[pm2 ? pm2 == 2 ? mem[ptr + 2] + rb : ptr + 2 : mem[ptr + 2]]))
            {
                mem[pm3 == 2 ? mem[ptr + 3] + rb : mem[ptr + 3]] = 1;
            }
            else {
                mem[pm3 == 2 ? mem[ptr + 3] + rb : mem[ptr + 3]] = 0;
            }
            ptr += 4;
            break;
        case 8: // equal to
            if ((mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]])
                == (mem[pm2 ? pm2 == 2 ? mem[ptr + 2] + rb : ptr + 2 : mem[ptr + 2]]))
            {
                mem[pm3 == 2 ? mem[ptr + 3] + rb : mem[ptr + 3]] = 1;
            }
            else {
                mem[pm3 == 2 ? mem[ptr + 3] + rb : mem[ptr + 3]] = 0;
            }
            ptr += 4;
            break;
        case 9:
            rb += mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]];
            ptr += 2;
            break;
        default:
            std::cout << " Something went wrong, " << mem[ptr] << std::endl;
            mem[ptr] = 99; // Halt
            break;
        }
    }

    return output;
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
    std::vector<long long> program{};
    program.resize(instructions.size());
    std::transform(instructions.begin(), instructions.end(), program.begin(), [](std::string const& s) { return std::stoll(s); });

    /* Run program */
    Game game{ program };
    std::vector<int> setupOutput{ game.run(0) };
    int minX{ 0 };
    int minY{ 0 };
    int maxX{ 0 };
    int maxY{ 0 };

    // Find dimesions
    for (int i{ 0 }; i < setupOutput.size(); i += 3) {
        if (setupOutput[i] > maxX)
            maxX = setupOutput[i];
        if (setupOutput[i+1] > maxY)
            maxY = setupOutput[i+1];
        //std::cout << "(" << setupOutput[i] << "," << setupOutput[i+1] << ") = " << setupOutput[i+2] << "\n";
    }
    //std::cout << "(" << maxX << "," << maxY << ")" << "\n";

    /* Create map */
    std::vector<std::vector<int>> map{};
    map.resize(maxY+1);
    for (auto &line : map) {
        line.resize(maxX+1);
    }
    for (int i{ 0 }; i < setupOutput.size(); i += 3) {
        map[setupOutput[i+1]][setupOutput[i]] = setupOutput[i + 2];
    }

    int blocks{0};
    blocks = std::count(setupOutput.begin(), setupOutput.end(), 2);

    /* Print map*/
    int blockOnMap{ 0 };
    for (auto& line : map) {
        for (auto& ch : line) {
            std::cout << ch;
        }
        blockOnMap += std::count(line.begin(), line.end(), 2);
        std::cout << '\n';
    }

    // blockOnMap is the answer
    std::cout << blocks << " " << blockOnMap << '\n';


    return 1;
}