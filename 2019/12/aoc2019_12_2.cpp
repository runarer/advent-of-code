#include <iostream>
#include <algorithm>
#include <array>

/* 
	Alle x,y eller z synker og øker uavhengig av hverandre. 
	Så isteden for å finne når en måne repiterer posisjon kan jeg
	finne når x,y og z repiterer seg.
*/

struct Moon
{
	int pos[3];
	int velocity[3]{ 0,0,0 };
};

int main() {

	Moon test_moons[4]{ {{-1,0,2}},{{2,-10,-7}},{{4,-8,8}},{{3,5,-1}} };
	Moon second_test_moons[4]{ {{-8,-10,0}}, {{5,5,10}}, {{2,-7,3}}, {{9,-8,-3}} };
	Moon real_moons[4]{ {{3,-6,6}},{{10,7,-9 }}, {{ -3,-7,9 }}, {{ -8,0,4 }} };

	Moon* moons = real_moons;
	Moon first_pos[4]{moons[0],moons[1], moons[2], moons[3] };

	bool new_pos{ true };
	long long step{ 0 };
	long long repeat[4]{ 0,0,0,0 };

	std::array<int,3> steps{ 0,0,0 };
	
	// Calculate steps for all x velocity to hit 0 again	
	while (true) {
		++step;
		for (int i{ 0 }; i < 3; ++i) {
			for (int j{ i + 1 }; j < 4; ++j)
			{
				if (moons[i].pos[0] > moons[j].pos[0]) {
					--moons[i].velocity[0];
					++moons[j].velocity[0];
				}
				else if (moons[i].pos[0] < moons[j].pos[0]) {
					++moons[i].velocity[0];
					--moons[j].velocity[0];
				}
			}
		}

		// Apply velocity
		for (int i{0}; i < 4; i++)
		{
			moons[i].pos[0] += moons[i].velocity[0];
		}

		// Is it 0?		
		if (moons[0].velocity[0] == 0 && moons[1].velocity[0] == 0 && moons[2].velocity[0] == 0 && moons[3].velocity[0] == 0)
			break;		
	}
	steps[0] = step;
	std::cout << "X repeat at: " << step << "\n";
	

	step = 0;
	while (true) {
		++step;
		for (int i{ 0 }; i < 3; ++i) {
			for (int j{ i + 1 }; j < 4; ++j)
			{
				if (moons[i].pos[1] > moons[j].pos[1]) {
					--moons[i].velocity[1];
					++moons[j].velocity[1];
				}
				else if (moons[i].pos[1] < moons[j].pos[1]) {
					++moons[i].velocity[1];
					--moons[j].velocity[1];
				}
			}
		}
		// Apply velocity
		for (int i = 0; i < 4; i++)
		{
			moons[i].pos[1] += moons[i].velocity[1];
		}

		if (moons[0].velocity[1] == 0 && moons[1].velocity[1] == 0 && moons[2].velocity[1] == 0 && moons[3].velocity[1] == 0)
			break;
	}
	steps[1] = step;
	std::cout << "Y repeat at: " << step << "\n";
	

	step = 0;
	while (true) {
		++step;
		for (int i{ 0 }; i < 3; ++i) {
			for (int j{ i + 1 }; j < 4; ++j)
			{
				if (moons[i].pos[2] > moons[j].pos[2]) {
					--moons[i].velocity[2];
					++moons[j].velocity[2];
				}
				else if (moons[i].pos[2] < moons[j].pos[2]) {
					++moons[i].velocity[2];
					--moons[j].velocity[2];
				}
			}
		}
		// Apply velocity
		for (int i = 0; i < 4; i++)
		{
			moons[i].pos[2] += moons[i].velocity[2];
		}

		if (moons[0].velocity[2] == 0 && moons[1].velocity[2] == 0 && moons[2].velocity[2] == 0 && moons[3].velocity[2] == 0)
			break;
	}
	steps[2] = step;
	std::cout << "Z repeat at: " << step << "\n";
	
	std::sort(steps.begin(),steps.end(), std::greater());

	// This find halfway
	step = steps[0];
	while (step % steps[1] || step % steps[2]) {		
		step += steps[0];
	}
	
	std::cout << "Repeat after: " << step * 2 << '\n';

	return 0;
}

