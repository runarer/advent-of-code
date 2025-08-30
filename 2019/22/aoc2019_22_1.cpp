#include <string>
#include <sstream>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

enum TokenType { nothing, cut, stack, increment};

// Parse at get lines,and create "Tokens", a token is a std::pair<char,int>
auto parse(std::vector<std::string>& lines) -> std::vector<std::pair<TokenType,int>> {    
    std::vector<std::pair<TokenType, int>> tokens{};

    for (std::string& line : lines) {
        TokenType type {nothing};
        int value{ 0 };
        if (line[0] == 'c') {
            type = cut;
            value = std::stoi(line.substr(4));
        }
        else if (line[0] == 'd' && line[5] == 'i') {
            type = stack;
        }
        else if (line[0] == 'd' && line[5] == 'w') {
            type = increment;
            value = std::stoi(line.substr(20));
        }
        tokens.push_back({type,value});
    }

    return tokens;
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
    std::vector<std::string> lines{};
    while (!infile.eof()) {
        std::string line{};
        if (getline(infile, line)) {
            lines.push_back(line);
        }
    }
    infile.close();
    
    /* Parse lines and put in vector. */
    std::vector<std::pair<TokenType, int>> actions{ parse(lines) };
    
    std::vector<int> deck(10007,0);
    for (int i = 0; i < std::size(deck); i++) deck[i] = i;

    for (auto& [token, value] : actions) {
        if (token == cut) {
            //std::cout << "\nCut " << value;            
            if (value < 0)
                value = (int)deck.size() + value;                        
            std::rotate(deck.begin(), deck.begin() + value, deck.end());
        } else if (token == stack) {
            //std::cout << "\nStack";
            std::reverse(deck.begin(), deck.end());            
        } else if(token == increment) {
            //std::cout << "\nIncrement " << value;
            auto incrementedDeck = deck;
            int i = 0;
            for (auto& card : deck) {
                incrementedDeck[i] = card;
                i += value;
                i %= deck.size();
            }
            deck = incrementedDeck;
        }
        else {
            std::cout << "\nNothing found";
        }        
    }
    
    auto it = std::find(deck.begin(), deck.end(), 2019);
    if (it != deck.end()) 
        std::cout << "\nAnswer: " << it - deck.begin() << std::endl;
    else
        std::cout << "\nAnswer not found" << std::endl;
    std::cout << "\nAn: " << deck[6696] << "|" << deck[it- deck.begin()] << std::endl;
    //std::cout << "\nOrg: "; for (int i : deck) std::cout << " " << i;

    /*
    std::vector<int> d(10, 0);
    for (int i = 0; i < std::size(d); i++) d[i] = i;
    std::cout << "\nOrg: "; for (int i : d) std::cout << " " << i;
    std::cout << "\nRes: "; for (int i : d) std::cout << " " << i;
    */
    return 0;
}
