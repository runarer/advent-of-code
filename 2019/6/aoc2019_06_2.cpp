#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

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
    /* Read file into vector of strings */
    std::ifstream infile(argv[1]);
    std::vector<std::string> lines(std::istream_iterator<std::string>{infile},
        std::istream_iterator<std::string>{});

    std::map<std::string, std::string> orbitalMap{};

    /* Parse line at ) and put in map. */
    for (auto line : lines) {
        std::string value = line.substr(0, 3);
        std::string key = line.substr(4);
        orbitalMap[key] = value;
    }

    /* 
        Two vectors. One from YOU to COM and one from SAN to COM. 
        Then start at COM for both and walk down until they no longer match.
        Count whats left minus one for san and you, and add one for last common sat.    
    */
    // Dette kan erstattes av set og bruke views for å fjerne det de har felles.
    std::vector<std::string> youPath{};
    std::vector<std::string> sanPath{};
    std::string you{ "YOU" };
    std::string san{ "SAN" };

    std::string& parent = you;
    while (parent != "COM")
    {
        parent = orbitalMap[parent];
        youPath.push_back(parent);
    }
    std::reverse(youPath.begin(), youPath.end());

    parent = san;
    while (parent != "COM")
    {
        parent = orbitalMap[parent];
        sanPath.push_back(parent);
    }
    std::reverse(sanPath.begin(), sanPath.end());

    int youCount = youPath.size();
    int sanCount = sanPath.size();
    int commonSats{ 0 };
    while (youPath[commonSats] == sanPath[commonSats])
    {
        //std::cout << "We have " << youPath[commonSats] << '\n';
        ++commonSats;
    }
    int transfers{ youCount + sanCount - 2 * commonSats };

    std::cout << "We have " << transfers << " transfers." << std::endl;

    return 1;
}
