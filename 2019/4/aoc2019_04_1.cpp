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
        for (int b{ a / 11 }; b <= 9; ++b) {
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

    /*
    for (int c{ 3 }; c <= 9; c++) {
        int variants{ 0 };
        std::cout << "\nStart of: " << c << '\n';

        for (int d{ c }; d <= 9; d++)
            for (int e{ d }; e <= 9; e++)
                for (int f{ e }; f <= 9; f++) {
                    //std::cout << 33 << c << d << e << f << '\n';
                    ++variants;
                }

        pp += (c < 6 ? c - 2 : 4) * variants;
    }*/
    //std::cout << "\nPP: " << pp << '\n';
    
    /* BC *//*
    int mulTimes{ 0 };
    for (int d{ 4 }; d <= 9; d++) {
        int variantsAfter{ 0 };
        //std::cout << "\nStart of: " << d << '\n';
        for (int e{ d }; e <= 9; e++)
            for (int f{ e }; f <= 9; f++) {
                //std::cout << 244 << d << e << f << '\n';
                ++variantsAfter;
            }

        mulTimes += (d < 7 ? d - 2 : 5);
        //std::cout << "\nVariants in: " << d << " - " << variantsAfter << " and multi " << mulTimes << '\n';
        pp += mulTimes * variantsAfter;
    }*/
    //std::cout << "\nPP: " << pp << '\n';

    
    /*
    mulTimes = 0;
    for (int e{ 4 }; e <= 9; ++e) {
        int variantsAfter{ 0 };
        
        for (int f{ e }; f <= 9; f++) {
            //std::cout << 2344 << e << f << '\n';
            ++variantsAfter;
        }

        mulTimes += e - 3;
        if (e == 9) --mulTimes; // Pga 78 som kommer før 99 ikke skal med
        pp += mulTimes * variantsAfter;
    }    */

    /* AB */

    /* BC */
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ (a + 1) * 11 }; b <= 99; b += 11) {
            if (a == 2 && b == 33) continue;
            for (int c{ b / 11 }; c <= 9; ++c) {
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
                for (int d{ c / 11 }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        //std::cout << "Number: " << a << b << c << d << e << '\n';
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
                    for (int e{ (d + 1) * 11 }; e <= 99; e += 11)
                        //std::cout << "Number: "<< a << b << c << d << e << '\n';
                        ++pp;
    return pp;
}

int permutations(int digits,int length) {
    if (length < 1) return 0;
    if (length > digits) return 0;
    if (length == digits) return 1;
    if (length == 1) return digits;

    int perms{ 0 };
    int loops = (digits - length) + 1;
    for (int i{ 1 }; i <= loops; ++i) {
        perms += permutations(--digits, length - 1);
    }
    return perms;
}

int main(int argc, char* argv[]) {
    int start{ 234208 };
    int end{ 765869 };

    int pp{ possiblePasswords(start,end) };
    std::cout << "There are " << pp << " possible password.\n";

     /*
    int permuts{ 0 };
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ a + 1 }; b <= 7; ++b) {
            for (int c{ b + 1 }; c <= 8; ++c) {
                for (int d{ (c + 1)*11 }; d <= 99; d += 11) {
                    for (int e{ d / 11 }; e <= 9; ++e) {
                        std::cout << "Number: " << a << b << c << d << e << '\n';
                        ++permuts;
                    }                        
                }                
            }                
        }            
    }*/
    
    /*
    int permuts{ 0 };
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ a + 1 }; b <= 8; ++b) {
            for (int c{ (b + 1)*11 }; c <= 99; c += 11) {
                for (int d{ c / 11 }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        std::cout << "Number: " << a << b << c << d << e << '\n';
                        ++permuts;
                    }                        
                }                
            }                
        }            
    }*/
    /*
    int permuts{ 0 };
    for (int a{ 2 }; a <= 6; ++a) {
        for (int b{ (a + 1)*11 }; b <= 99; b += 11) {
            if (a == 2 && b == 33) continue;
            for (int c{ b / 11 }; c <= 9; ++c ) {
                for (int d{ c  }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        std::cout << "Number: " << a << b << c << d << e << '\n';
                        ++permuts;
                    }
                }
            }
        }
    }*/
    /*
    int permuts{ 0 };
    for (int a{ 33 }; a <= 66; a += 11) {
        for (int b{ a / 11 }; b <= 9; ++b) {
            for (int c{ b }; c <= 9; ++c) {
                for (int d{ c }; d <= 9; ++d) {
                    for (int e{ d }; e <= 9; ++e) {
                        std::cout << "Number: " << a << b << c << d << e << '\n';
                        ++permuts;
                    }
                }
            }
        }
    }*/
    //int perm = permutations(5, 2);
    //std::cout << "For taking 2 from 5 leves: " << permuts << " permutations\n";
    
    return 1;
}

//23456 4 5
//23456 1 5
