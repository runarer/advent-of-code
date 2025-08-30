#include <string>
#include <sstream>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

auto split(std::string str, char delimiter) -> std::vector<std::string> {
    std::string segment;
    std::stringstream ss(str);
    std::vector<std::string> seqlist;

    while (std::getline(ss, segment, delimiter)) {
        seqlist.push_back(segment);
    }

    return seqlist;
}


class Springdroid {
public:
    Springdroid(std::vector<std::string> instructions);
    void runProgram(std::vector<int> input);
    auto jump(std::string& springscript) -> std::pair<int, std::string>;
private:
    std::array<long long, 10000> code{ 0 };
    std::array<long long, 10000> intcode{};
    std::vector<long long> output{ 0 };
};

Springdroid::Springdroid(std::vector<std::string> instructions)
{
    /* Transform strings to integers */
    std::transform(instructions.begin(), instructions.end(), code.begin(), [](std::string const& s) { return std::stoll(s); });
}


void Springdroid::runProgram(std::vector<int> input) {
    int ptr{ 0 };
    int inputPointer{ 0 };
    int rb{ 0 };
    intcode = code;

    while (intcode[ptr] != 99) {
        int pm3{ 0 };
        int pm2{ 0 };
        int pm1{ 0 };
        long long instruction{ intcode[ptr] };

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
            /*intcode[intcode[ptr + 3]] = intcode[pm1 ? ptr + 1 : intcode[ptr + 1]]
                + intcode[pm2 ? ptr + 2 : intcode[ptr + 2]];*/
            intcode[pm3 == 2 ? intcode[ptr + 3] + rb : intcode[ptr + 3]] =
                intcode[pm1 ? pm1 == 2 ? intcode[ptr + 1] + rb : ptr + 1 : intcode[ptr + 1]]
                + intcode[pm2 ? pm2 == 2 ? intcode[ptr + 2] + rb : ptr + 2 : intcode[ptr + 2]];
            ptr += 4;
            break;
        case 2: // multi
            /*intcode[intcode[ptr + 3]] = intcode[pm1 ? ptr + 1 : intcode[ptr + 1]]
                * intcode[pm2 ? ptr + 2 : intcode[ptr + 2]];*/
            intcode[pm3 == 2 ? intcode[ptr + 3] + rb : intcode[ptr + 3]] =
                intcode[pm1 ? pm1 == 2 ? intcode[ptr + 1] + rb : ptr + 1 : intcode[ptr + 1]]
                * intcode[pm2 ? pm2 == 2 ? intcode[ptr + 2] + rb : ptr + 2 : intcode[ptr + 2]];
            ptr += 4;
            break;
        case 3: // read input
            //intcode[intcode[ptr + 1]] = input[inputPointer++];
            intcode[pm1 == 2 ? intcode[ptr + 1] + rb : intcode[ptr + 1]] = input[inputPointer++];
            ptr += 2;
            break;
        case 4: // output
            //output.push_back(intcode[pm1 ? ptr + 1 : intcode[ptr + 1]]);
            output.push_back(intcode[pm1 ? pm1 == 2 ? intcode[ptr + 1] + rb : ptr + 1 : intcode[ptr + 1]]);
            ptr += 2;
            break;
        case 5: // Jump-if-true
            //if (intcode[pm1 ?  ptr + 1 : intcode[ptr + 1]]) {
            //    ptr = intcode[pm2 ? ptr + 2 : intcode[ptr + 2]];
            if (intcode[pm1 ? pm1 == 2 ? intcode[ptr + 1] + rb : ptr + 1 : intcode[ptr + 1]]) {
                ptr = intcode[pm2 ? pm2 == 2 ? intcode[ptr + 2] + rb : ptr + 2 : intcode[ptr + 2]];
            }
            else {
                ptr += 3;
            }
            break;
        case 6: // Jump-if-false
            //if (!(intcode[pm1 ? ptr + 1 : intcode[ptr + 1]])) {
            //    ptr = intcode[pm2 ? ptr + 2 : intcode[ptr + 2]];               
            if (!(intcode[pm1 ? pm1 == 2 ? intcode[ptr + 1] + rb : ptr + 1 : intcode[ptr + 1]])) {
                ptr = intcode[pm2 ? pm2 == 2 ? intcode[ptr + 2] + rb : ptr + 2 : intcode[ptr + 2]];
            }
            else {
                ptr += 3;
            }
            break;
        case 7: // less than
            //if ((intcode[pm1 ? ptr + 1 : intcode[ptr + 1]])
            //    < (intcode[pm2 ? ptr + 2 : intcode[ptr + 2]]))
            if ((intcode[pm1 ? pm1 == 2 ? intcode[ptr + 1] + rb : ptr + 1 : intcode[ptr + 1]])
                < (intcode[pm2 ? pm2 == 2 ? intcode[ptr + 2] + rb : ptr + 2 : intcode[ptr + 2]]))
            {
                intcode[pm3 == 2 ? intcode[ptr + 3] + rb : intcode[ptr + 3]] = 1;
            }
            else {
                intcode[pm3 == 2 ? intcode[ptr + 3] + rb : intcode[ptr + 3]] = 0;
            }
            ptr += 4;
            break;
        case 8: // equal to
            //if ((intcode[pm1 ? ptr + 1 : intcode[ptr + 1]])
            //    == (intcode[pm2 ? ptr + 2 : intcode[ptr + 2]]))
            if ((intcode[pm1 ? pm1 == 2 ? intcode[ptr + 1] + rb : ptr + 1 : intcode[ptr + 1]])
                == (intcode[pm2 ? pm2 == 2 ? intcode[ptr + 2] + rb : ptr + 2 : intcode[ptr + 2]]))
            {
                intcode[pm3 == 2 ? intcode[ptr + 3] + rb : intcode[ptr + 3]] = 1;
            }
            else {
                intcode[pm3 == 2 ? intcode[ptr + 3] + rb : intcode[ptr + 3]] = 0;
            }
            ptr += 4;
            break;
        case 9:
            //pm1 == 2 ? intcode[ptr + 1] + rb :
            rb += intcode[pm1 ? pm1 == 2 ? intcode[ptr + 1] + rb : ptr + 1 : intcode[ptr + 1]];
            ptr += 2;
            break;
        default:
            std::cout << " Something went wrong, " << intcode[ptr] << std::endl;
            intcode[ptr] = 99; // Halt
            break;
        }
    }
}

auto Springdroid::jump(std::string& springscript) -> std::pair<int, std::string>
{
    // convert springscript to std::vector<long long>?
    std::vector<int> script{};
    for (char c : springscript) script.push_back((int)c);

    runProgram(script);

    // check output
    int damage{ 0 };
    for (auto& o : output) {
        if (o > 256) {
            damage = o;
            break;
        }
    }

    std::string asciiOutput{};
    for (long long l : output) asciiOutput.push_back((char)l);

    return { damage, asciiOutput };

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
    std::vector<std::string> instructions = split(line, ',');
    Springdroid springdroid(instructions);

    std::string jumpscript = "NOT C J\nAND D J\nNOT E T\nAND H T\nOR E T\nAND T J\nNOT B T\nAND D T\nOR T J\nNOT A T\nOR T J\nRUN\n";
    auto [succsess, rendering] = springdroid.jump(jumpscript);
    if (succsess) {
        std::cout << "Damage to ship: " << succsess << std::endl;
    }
    else {
        std::cout << "Jump unsuccsessfull\n" << rendering << std::endl;
    }

    return 0;
}
