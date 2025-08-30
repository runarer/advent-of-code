#include <string>
#include <sstream>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>
#include <cmath>
#include <boost/multiprecision/cpp_int.hpp>


static inline boost::multiprecision::int128_t mod(boost::multiprecision::int128_t a, boost::multiprecision::int128_t b)
{
    return (a >= 0) ? (a % b) : (b + a % b);
}

enum TokenType { nothing, cut, stack, increment };

std::vector<std::vector<int>> groups{};

auto shuffleDeck(std::vector<std::pair<TokenType, long long>>& actions, long long deck_size) -> std::vector<int> {
    std::vector<int> deck(deck_size, 0);
    for (int i = 0; i < std::size(deck); i++) deck[i] = i;

    for (auto& [token, value] : actions) {
        if (token == cut) {
            //std::cout << "\nCut " << value;            
            if (value < 0)
                value = (int)deck.size() + value;
            std::rotate(deck.begin(), deck.begin() + value, deck.end());
        }
        else if (token == stack) {
            //std::cout << "\nStack";
            std::reverse(deck.begin(), deck.end());
        }
        else if (token == increment) {
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
    return deck;
}


auto fillOutGroups(std::vector<std::pair<TokenType,int>>& actions,long long deck_size) -> std::vector<std::vector<int>> {
    std::vector<std::vector<int>> temp_groups(73, std::vector<int>{});

    for (auto& [token, value] : actions) {
        if (token == increment) {
            if (temp_groups[value].size() > 0) 
                continue;

            temp_groups[value].resize(value);
            long long group_size { deck_size / value };
            
            //int offset{value - deck_size - group_size*value};
            //int last{ group_size * value };
            temp_groups[value][0] = 0;
            
            int prev = 0;
            for (int i = 1; i < value; i++) {
                long long overflow{ group_size * value + prev };
                if (overflow < deck_size)
                    overflow += value;
                prev = overflow % deck_size;
                temp_groups[value][prev] = i;                
                //temp_groups[value].push_back(overflow % deck_size);
                //temp_groups[value].push_back((offset * i) % value);
            }
        }
    }
    return temp_groups;
}

// Parse at get lines,and create "Tokens", a token is a std::pair<char,int>
auto parse(std::vector<std::string>& lines) -> std::vector<std::pair<TokenType, long long>> {
    std::vector<std::pair<TokenType, long long>> tokens{};

    for (std::string& line : lines) {
        TokenType type{ nothing };
        long long value{ 0 };
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
        tokens.push_back({ type,value });
    }

    return tokens;
}

auto cardAt(std::vector<std::pair<TokenType, int>>& instructions, long long deck_size, long long i) -> long long {
    //std::ranges::reverse_view actions{ instructions };

    for (auto& [token, value] : instructions | std::views::reverse) {
        if (token == cut) {
            //std::cout << "\nCut " << value;
            if (value < 0) {
                //i = if (i < | cut | ) deck_(n - 1)[deck_size + cut + i] else deck_(n - 1)[i + cut]
                if (i < std::abs(value)) {
                    i = deck_size + value + i;
                }
                else {                    
                    i = i + value;   
                }
            }
            else {
                //deck_n[i] = if (i < cut) deck_(n - 1)[cut + i] else deck_(n - 1)[i + cut]                
                if (i >= deck_size - value) {
                    i = i - (deck_size - value);
                }
                else {
                    i = i + value;
                }
            }
        }
        else if (token == stack) {
            //std::cout << "\nStack";
            i = deck_size - 1 - i;            
        }
        else if (token == increment) {
            if (i == 0) return 0;
            //std::cout << "\nIncrement " << value;
            long long block_size{ deck_size / value };
            //int round{ groups[value][(int)(i % value)] };
            //std::cout << "\n value: " << value << " and " << i % value;
            i = groups[value][(int)(i % value)] * block_size + i/value;
            //int round { (int)(i/(block_size)) };
            //int offset{ (int)(deck_size - block_size * value) };
            //i = (i % (block_size+1))*value + ((offset * round) % value);

            /* This gives the position of a card after increment by value:
                i = (i * value) % deck_size;
            */
             
            //i = (deck_size - (deck_size / value) * i) % deck_size;
            //if (i < 0) // FORDI C++ ikke gjør modulo riktig.
            //    i += deck_size;
        }
        else {
            std::cout << "\nNothing found";
        }
    }
    return i;
}

auto removeStack(std::vector<std::pair<TokenType, long long>>& instructions, long long deck_size) -> std::vector<std::pair<TokenType, long long>> {
    std::vector<std::pair<TokenType, long long>> newInstructions{};

    for (auto& instruction : instructions) {
        auto& [type, value] = instruction;
        if (type == stack) {
            newInstructions.push_back({increment,deck_size-1});
            newInstructions.push_back({ cut,1 });
        }
        else {
            newInstructions.push_back(instruction);
        }
    }

    return newInstructions;
}

auto simplifyActions(std::vector<std::pair<TokenType, long long>>& actions, long long deck_size) -> std::vector<std::pair<TokenType, long long>> {    

    //long long finalCut{0};
    //long long finalIncrement{1};    
    boost::multiprecision::int128_t finalCut{ 0 };
    boost::multiprecision::int128_t finalIncrement{ 1 };
    
    std::vector<std::pair<TokenType, long long>> instructions{ removeStack(actions,deck_size) };
    
    for (auto& [type, value] : instructions) {
        if (type == cut) {
            //finalCut = (boost::multiprecision::int128_t)(finalCut + value) % deck_size;
            finalCut = mod((finalCut + value), deck_size);
        } 
        else if (type == increment) {
            //finalIncrement = (finalIncrement * value)%deck_size;
            finalIncrement = mod((finalIncrement * value) , deck_size);
            //std::cout << "\nFinal Inc: " << finalIncrement << " and value " << value;
            //finalCut = (boost::multiprecision::int128_t)(finalCut * value) % deck_size;
            finalCut = mod((finalCut * value), deck_size);
        }
        else {
            std::cout << "Stack in simplifyActions" << std::endl;
        }
    }

    return { {increment,(long long)finalIncrement},{cut,(long long)finalCut} };
}

auto iterationTable(std::pair<std::pair<TokenType, long long>,std::pair<TokenType, long long>> actions, long long deck_size, long long iterations) -> std::pair<std::pair<TokenType, long long>, std::pair<TokenType, long long>> {
    std::vector<std::pair<std::pair<TokenType, long long>, std::pair<TokenType, long long>>> table{ actions };
    //for (auto& incT : table) { std::cout << "\nINC1 " << incT.first.second; std::cout << "\nCUT1 " << incT.second.second; }
    /* Create table */
    long long it{1};
    while ((it *= 2) <= iterations) {
        boost::multiprecision::int128_t x{ table.back().first.second };
        boost::multiprecision::int128_t y{ table.back().second.second };
        boost::multiprecision::int128_t x2{ x * x };
        boost::multiprecision::int128_t x2r{ mod(x2 ,deck_size) };
        //boost::multiprecision::int128_t x2r{ x2 % (boost::multiprecision::cpp_int)deck_size };
        //std::cout << "\nx " << x << "|" << x2 << "|" << x2r << "|" << (long long)x2r;

        //table.push_back({ {increment, (long long)((x*x)%deck_size)} , {cut,(long long)( ((x*y)%deck_size) + y) % deck_size}});
        //table.push_back({ {increment, (long long)x2r} , {cut,(long long)(((x * y) % deck_size) + y) % deck_size} });
        table.push_back({ {increment, (long long)x2r} , {cut,(long long) mod( mod(x * y,deck_size) + y, deck_size) } });
        //table.push_back(std::make_pair( std::make_pair(increment, (long long)x2r) , std::make_pair(cut,(long long)(((x * y) % deck_size) + y) % deck_size)));
    }
    //for (auto& incT : table) { std::cout << "\nINC " << incT.first.second; std::cout << "\nCUT " << incT.second.second; }

    /* Do the iteration */
    boost::multiprecision::int128_t incX{ table.back().first.second };
    boost::multiprecision::int128_t cutY{ table.back().second.second};
    
    long long power{ (int)table.size() - 1 };
    long long const two{ 1 };
    long long iterations_left{ iterations - (long long)(two << power) };
    //std::cout << "\nIt left: " << iterations_left << "|"<< (two << power);
    power--;
    
    while (iterations_left > 0) {        
        if (( two << power) <= iterations_left) {
            //std::cout << "\nIterations: " << iterations_left << "|" << (two << power);
            boost::multiprecision::int128_t x{ table[power].first.second };
            boost::multiprecision::int128_t y{ table[power].second.second };
            //incX = (incX * x) % deck_size;
            incX = mod((incX * x) , deck_size);
            //cutY = (((x * cutY) % deck_size) + y) % deck_size;
            cutY = mod(mod(x * cutY, deck_size) + y , deck_size);
            iterations_left -= two << power;
        } else {
            power--;
        }
    }

    return { {increment,(long long)incX} , {cut,(long long)cutY} };
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
    //std::vector<std::pair<TokenType, int>> actions{ {cut,8090 },{cut,75} };
    std::vector<std::pair<TokenType, long long>> actions{ parse(lines) };
    //long long deck_size = 10007; 


    long long deck_size{ 119315717514047 };    
    long long shuffles { 101741582076661 };

    std::cout << "\nDS: " << deck_size << std::endl;

    //groups = fillOutGroups(actions, deck_size);
    //long long ans = cardAt(actions, 10007, 6000);
    //std::cout << "\nAn1: " << ans << std::endl;    
    
    //std::vector<std::pair<TokenType, int>> actions1{ {stack,0} };
    //std::vector<int> deck{shuffleDeck(actions,deck_size)};
    //std::cout << "\nAn1: " << deck[6696] << std::endl;

    //std::vector<std::pair<TokenType, int>> actions2{ {increment,10006}, { cut, 1} };
    std::vector<std::pair<TokenType, long long>> actions2{ simplifyActions( actions, deck_size) };
    //std::cout << "\nINCs " << actions2[0].second; std::cout << "\nCUTs " << actions2[1].second;
    /*
    for (auto& [type, value] : actions2) {
        if (type == cut)
            std::cout << "\nCUT " << value;
        if (type == increment)
            std::cout << "\nINC " << value;
    }*/
    //std::vector<int> deck2{ shuffleDeck(actions2,deck_size) };
    //std::cout << "\nAn2: " << deck2[6696] << std::endl;

   
    /*
    long long a{ actions2[0].second };
    long long b{ actions2[1].second * -1};    
   
    std::vector<int> deck_temp(deck_size, 0);
    for (int i = 0; i < deck_temp.size(); i++) deck_temp[i] = i;
    std::vector<long long> deck3(deck_size,0);
    for (int i = 0; i < deck3.size(); i++) {
        long long temp = (a * deck_temp[i] + b) % deck_size;
       if (temp < 0) 
            temp += deck_size;
        deck3[temp] = deck_temp[i];
    }
    std::cout << "\nAn3: " << deck3[6696] << std::endl;
    
    */
    //std::vector<std::pair <std::pair<TokenType, int>, std::pair<TokenType, int>>> incTable{ iterationTable({actions2[0],actions2[1] }, deck_size, shuffles) };
    std::pair <std::pair<TokenType, long long>, std::pair<TokenType, long long>> iterated{ iterationTable({actions2[0],actions2[1] }, deck_size, shuffles) };
    std::cout << "\nINC a" << iterated.first.second; std::cout << "\nCUT d" << iterated.second.second;

    boost::multiprecision::int128_t toInv{ mod(2020 - -1*iterated.second.second,deck_size) };
    boost::multiprecision::int128_t toMul{ iterated.first.second };
    std::cout << "\nTo Inv" << toInv;

    boost::multiprecision::int128_t inved{ 16910502149740 };
    std::cout << "\nAnsver" << mod(toMul * inved,deck_size);

    /* Reverse the two shuffles */
    /* Cut */ 
    long long pos{ 2020 };
    if (iterated.second.second < 0) {
        if (pos < std::abs(iterated.second.second)) {
            pos = deck_size + iterated.second.second + pos;
        }
        else {
            pos = pos + iterated.second.second;
        }
    }
    else {
        if (pos >= deck_size - iterated.second.second) {
            pos = pos - (deck_size - iterated.second.second);
        }
        else {
            pos = pos + iterated.second.second;
        }
    }    
    std::cout << "\nPosition after reversing cut: " << pos <<std::endl;
    /* Increase */


    /* TEST */
    boost::multiprecision::int128_t startPos{ 2020 };
    startPos = mod((startPos * iterated.first.second),deck_size);

    std::cout << "\nTEST reverse: " << startPos << std::endl;

    startPos = mod((startPos - iterated.second.second) , deck_size);
    if (startPos < 0) 
        startPos += deck_size;
    
    std::cout << "\nTEST cut: " << startPos << std::endl;

    /*
    int cut{ 3 };
    deck_size = 10;
    int startPos{ 9 };
    std::cout << "\nstartPos: " << startPos;
    
    startPos = (startPos - cut) % deck_size;
    if (startPos < 0) 
        startPos += deck_size;
    
    std::cout << " new startPos: " << startPos;
    */
    //for (auto& incT : incTable) { std::cout << "\nINC " << incT.first.second; std::cout << "\nCUT " << incT.second.second; }


    /*
    for (auto& group : groups) {
        std::cout << "\nGroup:";
        for (auto& g : group) std::cout << " " << g;
    }
    */

    //for (int i = 0; i < 10; i++) std::cout << i << " "; std::cout << std::endl;
    /*
    for (int i = 0; i <10; i++) {
        //std::cout << i << "  " << cardAt(actions, deck_size, i) << "\n";
        std::cout << cardAt(actions, deck_size, i) << " ";
    }
    std::cout << std::endl;
    */

    
    //std::cout << "\nAn: 6696|2019" << std::endl;
    //std::cout << "\nOrg: "; for (int i : deck) std::cout << " " << i;

    /*
    std::vector<int> d(10, 0);
    for (int i = 0; i < std::size(d); i++) d[i] = i;
    std::cout << "\nOrg: "; for (int i : d) std::cout << " " << i;
    std::cout << "\nRes: "; for (int i : d) std::cout << " " << i;
    */
    return 0;
}


// 103869742091030 to high
// 32387955094573 to low