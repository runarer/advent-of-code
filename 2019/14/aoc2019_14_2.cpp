#include <map>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <ranges>
#include <algorithm>
#include <iterator>
#include <regex>
#include <queue>

/*
    Start with needed["Fuel"] = 1
    Lookup fuel and add its ingredient to needed with right amount.
    So needed is "LMPH"=3 "NQXZM" = 33 "MBXSW"=85  "LWBQL"=15 "SCXQ"=5 "QZNXC"=13 "TFMNM"=6 "MWQTH"=7
    If the amount needed was lower than what is produced, add to surplus.



    One queue of pairs: needed
    One map: surplus
    ore counter

    Populate surplus from reactions map.

    while needed has elements:
        Pop first element

        Is it in surplus?
            If so remove amount from surplus.
            Surplus >= 0.
                Done for this element.
            Surplus < 0.
                Surplus is the new amount needed.
                Set surplus to 0.

        Find out how many times the reaction need to be run.
        Does this create a surplus?
            Add to surplus

        For each ingredient
            If ingredient is "ORE"
                Add amount*timesRun to oreAmount
            Add to needed with amount*timesRun.
*/

typedef std::map<std::string, std::pair<int, std::vector<std::pair<int, std::string>>>> ReactionMap;

long long oreNeed(ReactionMap const& reactions, std::map<std::string, long long> &surplus, const long long amount, const std::string name) {
    std::queue<std::pair<std::string, int>> needed{};
    //std::map<std::string, int> surplus{};
    long long oreAmount{ 0 };

    /* Populate surplus from reactions map */
    /*for (auto reaction : reactions) {
        surplus[reaction.first] = 0;
    }*/

    /* while needed has elements */
    needed.push(std::make_pair(name, amount));
    while (!needed.empty()) {
        /* Grab first element */
        long long amountNeeded{ needed.front().second };
        std::string toProduce{ needed.front().first };
        needed.pop();

        /* Is it ore? */
        if (toProduce == "ORE") {
            oreAmount += amountNeeded;
            continue;
        }

        long long producedPerRound{ reactions.at(toProduce).first };

        /* Is there any surplus */
        long long surplusOfProduct{ surplus.at(toProduce) };
        if (surplusOfProduct > 0) {
            if (surplusOfProduct >= amountNeeded) {
                surplus[toProduce] -= amountNeeded;
                amountNeeded = 0;
            }
            else {
                amountNeeded -= surplusOfProduct;
                surplus[toProduce] = 0;
            }
        }
        if (amountNeeded == 0) continue;

        /* Produce needed */
        long long roundNeeded{ amountNeeded / producedPerRound };
        if (amountNeeded % producedPerRound > 0) {
            ++roundNeeded;
            surplus[toProduce] += producedPerRound - (amountNeeded % producedPerRound);
        }

        /* Add ingredient to production line */
        for (auto ingredient : reactions.at(toProduce).second) {
            // Is ore?
            needed.push(std::make_pair(ingredient.second, ingredient.first * roundNeeded));
        }
    }

    return oreAmount;
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
    std::vector<std::string> lines(std::istream_iterator<std::string>{infile},
        std::istream_iterator<std::string>{});

    ReactionMap reactions{};

    /* Parse each line */
    std::vector<std::pair < int, std::string > > reagents{};
    for (int i{ 0 }; i < lines.size(); ++i) {
        if (lines[i] == "=>") {
            reactions[lines[i + 2]] = std::make_pair(std::stoi(lines[i + 1]), reagents);
            i += 2;
            reagents.clear();
        }
        else {
            auto comma = lines[i + 1].find(',');
            if (comma == std::string::npos) {
                reagents.push_back(std::make_pair(std::stoi(lines[i]), lines[i + 1]));
            }
            else {
                reagents.push_back(std::make_pair(std::stoi(lines[i]), lines[i + 1].substr(0, comma)));
            }
            ++i;
        }
    }

    std::map<std::string, long long> surplus{};    

    /* Populate surplus from reactions map */
    for (auto reaction : reactions) {
        surplus[reaction.first] = 0;
    }

    long long cargoHold{ 1000000000000 };
    long long fuelProduced{ 0 };
    for (int i{1000}; i > 0; i /= 10) {
        while (true) {
            std::map<std::string, long long> oldSurplus{surplus};
            long long oreNeeded{ oreNeed(reactions, surplus, i, "FUEL") };
            //cargoHold -= oreNeed(reactions, surplus, 1000, "FUEL");
            if (oreNeeded <= cargoHold) {
                cargoHold -= oreNeeded;
                fuelProduced += i;
            }
            else {
                surplus = oldSurplus;
                break;
            }
        }
    }
    std::cout << "Fuel produced: " << fuelProduced << "\n";

    return 0;
}


// I can keep surplus between each fuel production.
// then subtract ore from one trillion until it hit negative
// Count the number of runs.
// This might be to slow.

// 3566576 to low, IT WAS ONE OFF!!!!!