#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <functional>
#include <numeric>

int fuelReq(int mass) {
    int fuel = mass / 3 - 2;
    if (fuel <= 0) {
        return 0;
    }
    return fuel + fuelReq(fuel);
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

    /* Read file */
    std::ifstream infile(argv[1]);
    std::vector<int> ints(std::istream_iterator<int>{infile},
        std::istream_iterator<int>{});

    // for (auto value : ints)
    //     std::cout << value << "\n";

    int sum = std::accumulate(ints.begin(), ints.end(), 0, [](int acc, int value) {
        return acc + fuelReq(value);
        });

    std::cout << sum << std::endl;

    return 1;
}