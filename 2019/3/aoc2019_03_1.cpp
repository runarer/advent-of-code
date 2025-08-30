#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>


class Wire {
protected:
    std::vector<std::pair<int, std::pair<int, int>>> horizontal{};
    std::vector< std::pair<int, std::pair<int, int>>> vertical{};

public:
    Wire(const std::string& wires) {
        auto dirs = wires | std::views::split(',');
        std::vector<std::string> directions(dirs.begin(),dirs.end());

        /* I know half is horizontal and half is vertical */
        horizontal.reserve(directions.size() / 2 + 1);
        vertical.reserve(directions.size() / 2 + 1);
        
        /* Populate horizontal and vertical */
        //std::cout << "\n\n--- Wire ---\n";
        int last_horizontal{ 0 };
        int last_vertical{ 0 };
        for (std::string const& d : directions) {
            int current = std::stoi(&d[1]);

            switch (d[0])
            {
            case 'R':
                horizontal.push_back(std::pair{ last_vertical,std::pair{ last_horizontal,last_horizontal + current } });
                last_horizontal += current;
                break;
            case 'L':
                horizontal.push_back(std::pair{ last_vertical,std::pair{ last_horizontal - current,last_horizontal } });
                last_horizontal -= current;
                break;
            case 'U':
                vertical.push_back(std::pair{ last_horizontal,std::pair{ last_vertical, last_vertical + current } });
                last_vertical += current;
                break;
            case 'D':
                vertical.push_back(std::pair{ last_horizontal,std::pair{ last_vertical - current, last_vertical } });
                last_vertical -= current;
                break;
            default:
                std::cout << " Something went wrong!\n";
                break;
            }
        }
    }

    friend std::vector < std::pair<int, int>> findIntersections(Wire& firstWire, Wire& secondWire);
};

std::vector<std::pair<int, int>> findIntersections(Wire& firstWire, Wire& secondWire) {
    std::vector<std::pair<int, int>> intersections{};

    /* Compare firstWire.horizontal with secondWire.vertical */
    for (auto horizontal : firstWire.horizontal)
        for (auto vertical : secondWire.vertical)
            if ((vertical.second.first <= horizontal.first) &&
                (horizontal.first <= vertical.second.second) &&
                (horizontal.second.first <= vertical.first) &&
                (vertical.first <= horizontal.second.second))
                intersections.push_back(std::pair{ horizontal.first,vertical.first });

    /* Compare firstWire.vertical with secondWire.horizontal */
    for (auto horizontal : secondWire.horizontal)
        for (auto vertical : firstWire.vertical)
            if ((vertical.second.first <= horizontal.first) &&
                (horizontal.first <= vertical.second.second) &&
                (horizontal.second.first <= vertical.first) &&
                (vertical.first <= horizontal.second.second))
                intersections.push_back(std::pair{ horizontal.first,vertical.first });

    return intersections;
}

int shortestDistance(std::vector < std::pair<int, int>>& points) {

    auto distance = points | std::views::filter([](auto& p) { return p != std::pair{ 0, 0 }; })
        | std::views::transform([](auto& po) { return abs(po.first) + abs(po.second); });

    return *std::min_element(distance.begin(),distance.end());
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
    /* Read file into strings */
    std::ifstream infile(argv[1]);
    std::string firstLine{};
    std::string secondLine{};
    std::getline(infile, firstLine);
    std::getline(infile, secondLine);

    /* Create objects */
    Wire firstWire(firstLine);
    Wire secondWire(secondLine);

    auto intersections = findIntersections(firstWire, secondWire);
    int shortest = shortestDistance(intersections);

    std::cout << "Shortest: " << shortest << std::endl;

    return 1;
}
