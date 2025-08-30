#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

/* 
    1. Extends the Wire class with a travel vector, steps and coordiantes. 
    2. Make a friend function that calculate steps to intersection
    3. Run through all intersections and calculate steps for both wires, add them.
    4. Find smallest from point 3.

    1. Change Wire class to a path <<int,int>,<int,int>>, first is from and second is to. first is x and second is y for inner pairs.
    2. Use filter to get horizontal and vertical. Look for matching first.x and second.x.
    3. When we find an intersection, calculate steps by walking the path.

    Muligheter for å gjøre dette mer effektivt. Utregninger gjøres flere ganger.
*/


class Wire {
protected:
    std::vector<std::pair<int, std::pair<int, int>>> horizontal{};
    std::vector< std::pair<int, std::pair<int, int>>> vertical{};
    std::vector< std::pair<int, int>> path{};

public:
    Wire(const std::string& wires) {
        auto dirs = wires | std::views::split(',');
        std::vector<std::string> directions(dirs.begin(), dirs.end());

        /* I know half is horizontal and half is vertical */
        horizontal.reserve(directions.size() / 2 + 1);
        vertical.reserve(directions.size() / 2 + 1);
        path.reserve(directions.size());

        /* Populate horizontal and vertical */
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

            path.push_back(std::make_pair(last_horizontal, last_vertical));
        }
    }

    int steps(const int y, const int x) {
        int steps{ 0 };
        std::pair<int, int> last{ 0,0 };

        for (auto part : path) {
            // is the intersection in this part
            if ( !((x < last.first && x < part.first) || (x > last.first && x > part.first)
                || (y < last.second && y < part.second) || (y > last.second && y > part.second))) {
                steps += mDist(last.first,last.second,x,y);
                break;
            }
            // if not, add number to steps.
            steps += mDist(last.first, last.second, part.first, part.second);
            last = part;
        }

        return steps;
    }

private:
    int mDist(const int fromX, const int fromY, const int toX, const int toY) {
        return abs(fromX-toX)+abs(fromY-toY);
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
            {
                if( horizontal.first || vertical.first)
                    intersections.push_back(std::pair{ horizontal.first,vertical.first });
            }

    /* Compare firstWire.vertical with secondWire.horizontal */
    for (auto horizontal : secondWire.horizontal)
        for (auto vertical : firstWire.vertical)
            if ((vertical.second.first <= horizontal.first) &&
                (horizontal.first <= vertical.second.second) &&
                (horizontal.second.first <= vertical.first) &&
                (vertical.first <= horizontal.second.second))
            {
                if (horizontal.first || vertical.first)
                    intersections.push_back(std::pair{ horizontal.first,vertical.first });
            }

    return intersections;
}

int shortestToIntersection(std::vector < std::pair<int, int>>& points, Wire &firstWire, Wire &secondWire) {
    int shortest = firstWire.steps(points[0].first,points[0].second) + secondWire.steps(points[0].first, points[0].second);

    for (auto p : points | std::views::drop(1)) {
        int temp = firstWire.steps(p.first, p.second) + secondWire.steps(p.first, p.second);
        if (temp < shortest)
            shortest = temp;
    }

    return shortest;
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
    int shortest = shortestToIntersection(intersections,firstWire,secondWire);

    std::cout << "Shortest: " << shortest << std::endl;

    return 1;
}
