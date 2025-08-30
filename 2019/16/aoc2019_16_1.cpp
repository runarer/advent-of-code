#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

//std::vector<int> repeatingPattern(const int elements) {
//    std::vector<int> pattern{};
//    pattern.resize(elements * 4 - 1);
//
//    /*for (int i{ 0 }; i < elements - 1; ++i) {
//        pattern[i] = 0;
//    }*/
//
//    for (int i{ elements - 1 }; i < elements * 2 - 1 ; ++i) {
//        pattern[i] = 1;
//    }
//
//    /*for (int i{ elements * 2 - 1 }; i < elements * 3 - 1; ++i) {
//        pattern[i] = 0;
//    }*/
//
//    for (int i{ elements * 3 - 1 }; i < elements * 4 - 1; ++i) {
//        pattern[i] = -1;
//    }
//
//    return pattern;
//}

int createElement(const std::vector<int> &signals, const int element) {
    int newNumber{ 0 };
    //int repeatBlock{ 1 };
    int nInEachBlock{ element + 1 };
    bool negative{ false };

    for (int i{ element },j{1}; i < signals.size();++i,++j) {
        if(negative) {
            newNumber -= signals[i];
        }
        else {
            newNumber += signals[i];
        }

        /* New block? */
        if (j % (nInEachBlock) == 0) {
            //Skip one block as it is 0 multiplier
            //repeatBlock += 2;
            i += nInEachBlock;
            negative = !negative;
        }        
    }
    return abs(newNumber) % 10;
}

std::vector<int> fft(const std::vector<int> &signals, int phases) {
    std::vector<int> newSignals{};
    std::vector<int> tempSignals{signals};
    newSignals.reserve(signals.size());

    for (int i{ 0 }; i < phases; ++i) {
        newSignals.clear();

        for (int i{ 0 }; i < signals.size(); ++i) {
            newSignals.push_back(createElement(tempSignals, i));
        }        
        tempSignals = newSignals;
        
        /*for (auto signal : newSignals) {
            std::cout << signal;
        }
        std::cout << '\n';*/
    }
    return newSignals;
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

    /* Transform chars in string to integers */
    std::vector<int> signals{};
    signals.resize(line.size());
    std::transform(line.begin(), line.end(), signals.begin(), [](char s) -> int { return s - '0'; });

    /* Run program */
    std::vector<int> test{1, 2, 3, 4, 5, 6, 7, 8};
    std::vector<int> newSignal{ fft(signals,100) };

    for (int i{ 0 }; i < 8; ++i)
        std::cout << newSignal[i];
    std::cout << '\n';
  

    return 0;
}