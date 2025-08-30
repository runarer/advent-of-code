#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <iterator>

/*
    generer alle tall, med 6 for loops. neste for-loop starter på samme som forrige.
*/


int possiblePasswords(int start, int end) {
    int pp{ 0 };

    std::cout << "-----------------\n";
    /* AB */
    for (int a{ 33 }; a <= 66; a += 11) {
        for (int b{ a / 11 }; b <= 9; ++b) {
            for (int c{ b }; c <= 9; ++c) {
                for (int d{ c }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        std::cout << a << b << c << d << e << '\n';
                        ++pp;
                    }
                }
            }
        }
    }

    /* BC */
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ (a + 1) * 11 }; b <= 99; b += 11) {
            if (a == 2 && b == 33) continue;
            for (int c{ b / 11 }; c <= 9; ++c) {
                for (int d{ c }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        std::cout << a << b << c << d << e << '\n';
                        ++pp;
                    }
                }
            }
        }
    }

    /* CD */
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ a + 1 }; b <= 8; ++b) {
            for (int c{ (b + 1) * 11 }; c <= 99; c += 11) {
                for (int d{ c / 11 }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        std::cout << a << b << c << d << e << '\n';
                        ++pp;
                    }
                }
            }
        }
    }

    /* DE */
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ a + 1 }; b <= 7; ++b) {
            for (int c{ b + 1 }; c <= 8; ++c) {
                for (int d{ (c + 1) * 11 }; d <= 99; d += 11) {
                    for (int e{ d / 11 }; e <= 9; ++e) {
                        std::cout << a << b << c << d << e << '\n';
                        ++pp;
                    }
                }
            }
        }
    }

    /* EF */
    for (int a{ 2 }; a <= 5; ++a)
        for (int b{ a + 1 }; b <= 6; ++b)
            for (int c{ b + 1 }; c <= 7; ++c)
                for (int d{ c + 1 }; d <= 8; ++d)
                    for (int e{ (d + 1) * 11 }; e <= 99; e += 11) {
                        std::cout << a << b << c << d << e << '\n';
                        ++pp;
                    }                        
    return pp;
}

bool isValid(std::string const &str) {

    for (int i{ 0 }; i < 5; ++i) {
        if (str[i] == str[i + 1]) {
            // Got a pair
            if (i > 0) {
                //check prefix
                if (str[i - 1] == str[i]) continue;
            }
            if (i < 4) {
                //check suffix
                if (str[i + 2] == str[i]) continue;
            }
            return true; // A real pair
        }
    }

    return false;
}

int main(int argc, char* argv[]) {
    
    /* Read file */
    std::ifstream infile(argv[1]);
    std::vector<std::string> lines(std::istream_iterator<std::string>{infile},
        std::istream_iterator<std::string>{});

    
    int valids{ 0 };
    int invalids{ 0 };
    for (auto line : lines)
        if (isValid(line)) {
            ++valids;
            std::cout << line << " valid" << "\n";

        }            
        else {
            ++invalids;
            std::cout << line << " invalid" << "\n";
        }            

    std::cout << "There are " << valids << " and " << invalids << " invalid passwords\n";

    return 1;
}

