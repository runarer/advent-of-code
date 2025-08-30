#include <string>
#include <sstream>
#include <vector>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>
#include <boost/multiprecision/cpp_int.hpp>

typedef boost::multiprecision::int128_t bigInt;
typedef std::pair<bigInt, bigInt> lfc;

static inline bigInt mod(bigInt a, bigInt b)
{
    return (a >= 0) ? (a % b) : (b + a % b);
}

/* Modular power */
auto modPower(bigInt x, bigInt pow, bigInt m) -> bigInt {
    bigInt answer{ 1 };

    while (pow > 0) {
        if (mod(pow, 2)) {
            answer = mod(answer * x, m);
        }
        pow = pow / 2;
        x = mod(x * x, m);
    }

    return answer;
}

/* Modular inverse */
auto modInverse(bigInt x, bigInt m) -> bigInt {
    return modPower(x, m - 2, m);
}

/* Modular divide */
auto modDiv(bigInt a, bigInt b, bigInt m) -> bigInt {
    return mod(a * modInverse(b, m), m);
}

auto compose(lfc f, lfc g, bigInt m) -> lfc {
    return { mod(f.first*g.first,m),mod(mod(f.second * g.first,m)+g.second,m) };
}

auto composeSelf(lfc f, bigInt k, bigInt m) -> lfc {
    lfc g{ 1,0 };
    while (k > 0) {
        if (mod(k, 2)) {
            g = compose(g, f, m);
        }
        k = k / 2;
        f = compose(f, f, m);
    }
    return g;
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

    bigInt deck_size{ 119315717514047 };    
    bigInt iterations{ 101741582076661 };
    bigInt posToFind{ 2020 };

    /* Base f(x)=ax+b */
    bigInt a{ 1 };
    bigInt b{ 0 };

    /* For each line, get a and b, */
    for (std::string& line : lines) {        
        bigInt c{ 0 };
        bigInt d{ 0 };

        long long value{ 0 };
        if (line[0] == 'c') {
            /* Cut */
            c = 1;
            d = -1 * std::stoi(line.substr(4));
        }
        else if (line[0] == 'd' && line[5] == 'i') {
            /* Stack */
            c = -1;
            d = -1;
        }
        else if (line[0] == 'd' && line[5] == 'w') {
            /* Increment */
            c = std::stoi(line.substr(20));
            d = 0;            
        }
        /* Compose */
        a = mod(a * c, deck_size);
        b = mod(b * c + d, deck_size);
    }

    /* Compose the lfc into it self */
    lfc composedK = composeSelf({ a,b }, iterations, deck_size);

    bigInt answer{ modDiv(mod(posToFind - composedK.second,deck_size),composedK.first,deck_size) };
    std::cout << "The answer is: " << answer << std::endl;
}



// 103869742091030 to high
// 93750418158025 right
// 32387955094573 to low