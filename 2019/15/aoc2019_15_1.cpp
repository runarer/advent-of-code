#include <map>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <string>
#include <ranges>
#include <algorithm>
#include <iterator>
#include <set>

/*
    Need to change memory to map<int,long long>.
    If input is a vector, then add that to map
*/
class Robot
{
public:
    Robot(std::vector<long long> program);
    enum class Direction {north=1,south=2,west=3,east=4};
    int run(int input);
    std::map<std::pair<int,int>,int> exploreMap();    

private:
    std::map<std::size_t, long long> mem{};
    std::vector<long long> io{};
    std::map<std::pair<int, int>,int> map{};
    //std::set<std::pair<int, int>> discovered{};
    int ptr{ 0 };
    int rb{ 0 };
    bool halted{ false };
    //void move(Direction direction,int x, int y);
    int move(Direction direction, int x, int y);
};

Robot::Robot(std::vector<long long> program)
{
    /* Load program to mem, index får nullverdien til size_t og settes til den typen, */
    for (auto index = std::size_t{}; auto & instruction : program) {
        mem[index++] = instruction;
    }

}

int Robot::run(int input) {
    int output{ 0 };

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
            output = mem[pm1 ? pm1 == 2 ? mem[ptr + 1] + rb : ptr + 1 : mem[ptr + 1]];
            //std::cout << output << '\n';
            ptr += 2;
            return output;
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

/* I can change this to find shortest path to 2.
  If all move return 0 return 0 else return smallest + 1.
  If 2 is found, return 1;
  If in map return 0;
*/
int Robot::move(Direction direction, int x, int y) {
    /* Is it in the disovered set, leave if so. */
    std::pair<int, int> pos{ std::make_pair(x, y) };
    if (map.count(pos)) {
        //std::cout << "Exists " << pos.first << " " << pos.second << '\n';
        return 0;
    }

    /* Update map and discovered */
    int newBlock{ run(static_cast<int>(direction)) };
    map[pos] = newBlock;

    /* Found a wall */
    if (newBlock == 0) return 0;

    /* Found the oxygen system */
    if (newBlock == 2) return 1;

    /* Make moves in all directions */
    std::array ret {0,0,0,0};
    ret[0] = move(Direction::north, x, y - 1);
    ret[1] = move(Direction::east, x + 1, y);
    ret[2] = move(Direction::south, x, y + 1);
    ret[3] = move(Direction::west, x - 1, y);

    /* Move the robot back to where it came from */
    switch (direction) {
    case Direction::north:
        run(static_cast<int>(Direction::south));
        break;;
    case Direction::east:
        run(static_cast<int>(Direction::west));
        break;;
    case Direction::south:
        run(static_cast<int>(Direction::north));
        break;
    case Direction::west:
        run(static_cast<int>(Direction::east));
        break;
    }

    /* Find smallest return value that's not zero. */
    std::sort(ret.begin(), ret.end());
    int smallestNonZero{0};
    for (auto n : ret) {
        if (n > smallestNonZero) {
            smallestNonZero = n;
            break;
        }
    }

    return smallestNonZero ? smallestNonZero + 1 : 0;
}

//void Robot::move(Direction direction,int x, int y) {
//    /* Is it in the disovered set, leave if so. */
//    std::pair<int,int> pos{ std::make_pair(x, y) };
//    if (map.count(pos)) {
//        //std::cout << "Exists " << pos.first << " " << pos.second << '\n';
//        return;
//    }
//    
//    /* Update map and discovered */
//    int newBlock{ run(static_cast<int>(direction)) };    
//    map[pos] = newBlock;
//    
//    /* Found a wall */
//    if (newBlock == 0) return;
//
//    /* Make moves in all directions */
//    move(Direction::north, x, y - 1);
//    move(Direction::east, x + 1, y);
//    move(Direction::south, x, y + 1);
//    move(Direction::west, x - 1, y);
//    
//    /* Move the robot back to where it came from */
//    switch (direction) {
//    case Direction::north: 
//        run(static_cast<int>(Direction::south));
//        return;
//    case Direction::east:
//        run(static_cast<int>(Direction::west));
//        return;
//    case Direction::south:
//        run(static_cast<int>(Direction::north));
//        return;
//    case Direction::west:
//        run(static_cast<int>(Direction::east));
//        return;
//    }
//}

std::map<std::pair<int, int>, int> Robot::exploreMap() {

    /* Add starting point to map and discovered */
    map[std::make_pair(0, 0)] = 9;

    /* Make first movements */
    std::array ret{ 0,0,0,0 };
    ret[0] = move(Direction::north, 0, -1);
    ret[1] = move(Direction::east, 1, 0);
    ret[2] = move(Direction::south, 0, 1);
    ret[3] = move(Direction::west, -1, 0);

    for (auto r : ret) {
        std::cout << r << " ";
    }
    std::cout << "\n";

    return map;
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
    std::map<std::pair<int, int>, int> room{ robot.exploreMap() };
    //robot.exploreMap();
    //std::pair<int, int> robotPos{ 0,0 };
    
    int minX{ 0 };
    int minY{ 0 };
    int maxX{ 0 };
    int maxY{ 0 };
    std::vector<std::vector<int>> roomMap{};

    for (auto block : room) {
        
        /* Find dimentions of room */
        if (block.first.first < minX) minX = block.first.first;
        else if (block.first.first > maxX) maxX = block.first.first;
        if (block.first.second < minY) minY = block.first.second;
        else if (block.first.second > maxY) maxY = block.first.second;

        //std::cout << "(" << block.first.first << "," << block.first.second << ") = " << block.second << "\n";
    }

    /* Find dimentions of room */
    int transformX{ abs(minX) };
    int transformY{ abs(minY) };
    int height{ transformY + maxY + 1 };
    int length{ transformX + maxX + 1 };
    std::cout << "Height: " << height << " Length: " << length << "\n";

    roomMap.resize(height);
    for (auto &line : roomMap) {
        line.resize(length,8);
    }    

    /* Draw map */
    for (auto &block : room) {
        roomMap[transformY + block.first.second][transformX + block.first.first] = block.second;
    }

    /* Print Map */
    for (auto &line : roomMap) {
        for (int block : line) {
            switch (block)
            {            
            case 1:
                std::cout << ' ';
                break;
            case 2:
                std::cout << 'X';
                break;
            case 9:
                std::cout << 'S';
                break;
            default:
                std::cout << '#';
                break;
            }
        }
        std::cout << "\n";
    }

    /* Find shortest route to 2, this can be combined with the discovery of the map. As the intcode function as a 2d array.*/

    return 0;
}