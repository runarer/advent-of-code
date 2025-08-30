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
class Robot
{
public:
	Robot(std::vector<long long> program);
	int run(long long input);

private:
	std::map<int, long long> mem{};
	std::vector<long long> io{};	
	int ptr{ 0 };
	int rb{ 0 };
    bool halted{ false };
};

Robot::Robot(std::vector<long long> program)
{
	/* Load program to mem, index får nullverdien til size_t og settes til den typen, */
	for (auto index = std::size_t{}; auto & instruction : program) {
		mem[index++] = instruction;
	}

	/*  */

}

int Robot::run(long long input) {
    int output{};
    bool firstOutput{ true };
    
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
            if (firstOutput) {
                output = 10 * mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]];
                //std::cout << output << '\n';
                firstOutput = false;
                ptr += 2;
            }
            else {
                output += mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]];
                //std::cout << output << '\n';
                ptr += 2;
                return output; // Is this okey?
            }            
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

    return -1;
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
    Robot robot{ program };
    std::map<std::pair<int, int>, int> paintedPanels{};
    int robotDirection{ 0 }; // Dette burde være enum
    std::pair<int, int> robotPos{ 0,0 };

    paintedPanels[robotPos] = 0;

    int output{0};

    while ((output = robot.run( paintedPanels[robotPos] )) != -1) {
        //std::cout << output << " | (" << robotPos.first << "," << robotPos.second <<")\n";
        
        paintedPanels[robotPos] = output / 10;

        if (output % 10) {
            // turn right
            if (robotDirection == 3)
                robotDirection = 0;
            else
                ++robotDirection;
        }
        else {
            //turn left
            if (robotDirection == 0)
                robotDirection = 3;
            else
                --robotDirection;
        }

        //switch (output)
        //{
        //case 0: 
        //    // painted black
        //    paintedPanels[robotPos] = 0;
        //    
        //    // turn left
        //    if (robotDirection == 0)
        //        robotDirection = 3;
        //    else
        //        --robotDirection;
        //    
        //    break;
        //case 1:
        //    // painted black
        //    paintedPanels[robotPos] = 0;
        //    
        //    // turn right
        //    if (robotDirection == 3)
        //        robotDirection = 0;
        //    else
        //        ++robotDirection;
        //    
        //    break;
        //case 10:
        //    // painted white
        //    paintedPanels[robotPos] = 1;
        //    
        //    // turn left
        //    if (robotDirection == 0)
        //        robotDirection = 3;
        //    else
        //        --robotDirection;            
        //    break;
        //case 11:
        //    // painted white
        //    paintedPanels[robotPos] = 1;

        //    // turn right
        //    if (robotDirection == 3)
        //        robotDirection = 0;
        //    else
        //        ++robotDirection;
        //    break;
        //default:
        //    break;
        //}

        switch (robotDirection)
        {
        case 0:
            ++robotPos.second;
            break;
        case 1:
            ++robotPos.first;
            break;
        case 2:
            --robotPos.second;
            break;
        case 3:
            --robotPos.first;
            break;
        default:
            break;
        }

        // Is skiping this safe, is there a default value for non existing map keys?
       /* if (!paintedPanels.count(robotPos)) {
            paintedPanels[robotPos] = 0;
        }*/
    }

    std::cout << paintedPanels.size() << '\n';

    /*for (auto o : paintedPanels) {
        std::cout << o.first.first << "," << o.first.second << '\n';
    }*/

    return 1;
}