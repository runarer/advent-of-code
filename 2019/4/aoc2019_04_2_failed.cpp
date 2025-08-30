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

    /* AB */
    for (int a{ 33 }; a <= 66; a += 11) {
        for (int b{ (a / 11)+1 }; b <= 9; ++b) {
            for (int c{ b }; c <= 9; ++c) {
                for (int d{ c }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        //std::cout << "Number: " << a << b << c << d << e << '\n';
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
            for (int c{ (b / 11)+1 }; c <= 9; ++c) {
                for (int d{ c }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        //std::cout << "Number: " << a << b << c << d << e << '\n';
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
                for (int d{ (c / 11)+1 }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        //std::cout << "Number: " << a << b << c << d << e << '\n';
                        ++pp;
                    }
                }
            }
        }
    }

    /* DE *//*
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ a + 1 }; b <= 7; ++b) {
            for (int c{ b + 1 }; c <= 8; ++c) {
                for (int d{ (c + 1) * 11 }; d <= 99; d += 11) {
                    for (int e{ (d / 11)+1 }; e <= 9; ++e) {
                        ++pp;
                    }
                }
            }
        }
    }*/
    /* DE */
    //int permuts{ 0 };
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ a + 1 }; b <= 7; ++b) {
            for (int c{ b + 1 }; c <= 7; ++c) {
                for (int d{ (c + 1) * 11 }; d <= 88; d += 11) {
                    for (int e{ (d / 11) + 1 }; e <= 9; ++e) {
                        //std::cout << "Number: " << a << b << c << d << e << '\n';
                        ++pp;
                    }
                }
            }
        }
    }
    for (int a{ 333 }; a <= 666; a += 111) {
        for (int d{ (a / 111 + 1) * 11 }; d <= 88; d += 11) {
            for (int e{ (d / 11) + 1 }; e <= 9; ++e) {
                //std::cout << "Number: " << a << d << e << '\n';
                ++pp;
            }
        }
    }

    /* EF */
    for (int a{ 2 }; a <= 5; ++a)
        for (int b{ a + 1 }; b <= 6; ++b)
            for (int c{ b + 1 }; c <= 7; ++c)
                for (int d{ c + 1 }; d <= 8; ++d)
                    for (int e{ (d + 1) * 11 }; e <= 99; e += 11)
                        //std::cout << "Number: "<< a << b << c << d << e << '\n';
                        ++pp;
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ (a + 1) * 111 }; b <= 888; b += 111) {
            if (a == 2 && b == 333) continue;
            for (int e{ (b / 111 + 1) * 11 }; e <= 99; e += 11) {
                //std::cout << "Number: " << a << b << e << '\n';
                ++pp;
            }
        }
    }
    for (int a{ 333 }; a <= 666; a += 111) {
        for (int b{ (a / 111 + 1) }; b <= 9; ++b) {
            for (int e{ (b + 1) * 11 }; e <= 99; e += 11) {
                //std::cout << "Number: " << a << b << e << '\n';
                ++pp;
            }
        }
    }
    return pp;
}

int main(int argc, char* argv[]) {
    int start{ 234208 };
    int end{ 765869 };

    int pp{ possiblePasswords(start,end) };
    std::cout << "There are " << pp << " possible password.\n";



    return 1;
}
