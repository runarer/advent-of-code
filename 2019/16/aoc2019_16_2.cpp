#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <numeric>

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

int createElement(const std::vector<int>& signals, const int element) {
    int newNumber{ 0 };
    //int repeatBlock{ 1 };
    int nInEachBlock{ element + 1 };
    bool negative{ false };

    for (int i{ element }, j{ 1 }; i < signals.size(); ++i, ++j) {
        if (negative) {
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

//std::vector<int> fft(const std::vector<int>& signals, int phases) {
//    std::vector<int> newSignals{};
//    std::vector<int> tempSignals{ signals };
//    newSignals.reserve(signals.size());
//
//    for (int i{ 0 }; i < phases; ++i) {
//        newSignals.clear();
//
//        for (int i{ 0 }; i < signals.size(); ++i) {
//            newSignals.push_back(createElement(tempSignals, i));
//        }
//        tempSignals = newSignals;
//
//        /*for (auto signal : newSignals) {
//            std::cout << signal;
//        }
//        std::cout << '\n';*/
//    }
//    return newSignals;
//}

void fft(std::vector<int>& signals, int phases) {
    //std::vector<int> newSignals{};
    //std::vector<int> tempSignals{ signals };
    //newSignals.reserve(signals.size());

    for (int i{ 0 }; i < phases; ++i) {
        //newSignals.clear();

        for (int i{ 0 }; i < signals.size(); ++i) {
            signals[i] = createElement(signals, i);
        }
        //tempSignals = newSignals;

        /*for (auto signal : newSignals) {
            std::cout << signal;
        }
        std::cout << '\n';*/
    }
    //return newSignals;
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

    /* Calculate offset */
    int offset{ signals[6] };
    for (int i{ 5 }, j{10}; i >= 0; --i, j*=10)
        offset += j * signals[i];
    
    int repeatSignals{ 10000 };
    int signalsSize{ static_cast<int>(signals.size()) };
    int elementsInLastPart{ signalsSize * repeatSignals - offset };
    std::vector<int> repeatedSignals{};    
    repeatedSignals.reserve(elementsInLastPart);

    /* Insert first part */
    //int lastPartOfSignals{ elementsInLastPart % signals.size() };
    for (int i{ signalsSize - (elementsInLastPart % signalsSize) }; i < signalsSize; ++i) {
        repeatedSignals.push_back( signals[i] );
    }

    /* Insert repeated parts */
    for (int i{ 0 }; i < elementsInLastPart/signalsSize; ++i) {
        repeatedSignals.insert(std::end(repeatedSignals),std::begin(signals),std::end(signals));
    }
    //std::cout << repeatedSignals.size() << '\n';

    for (int j{ 0 }; j < 100; ++j) {
        int sum = std::accumulate(repeatedSignals.begin(), repeatedSignals.end(), 0);
        for (int i{ 0 }, prevSignal{ 0 }; i < repeatedSignals.size(); ++i) {
            sum -= prevSignal;
            prevSignal = repeatedSignals[i];
            repeatedSignals[i] = sum % 10;
        }
    }

    for (int i{ 0 }; i < 8; ++i)
        std::cout << repeatedSignals[i];
    std::cout << '\n';


    return 0;
}