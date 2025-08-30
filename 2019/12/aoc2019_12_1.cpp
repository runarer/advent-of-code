#include <iostream>

struct Moon
{
	/*int x{};
	int y{};
	int z{};
	int velocity_x{0};
	int velocity_y{0};
	int velocity_z{0};*/
	int pos[3];
	int velocity[3]{ 0,0,0 };
};

int main() {

	Moon test_moons[4]{ {{-1,0,2}},{{2,-10,-7}},{{4,-8,8}},{{3,5,-1}} };
	Moon second_test_moons[4]{ {{-8,-10,0}}, {{5,5,10}}, {{2,-7,3}}, {{9,-8,-3}} };
	Moon real_moons[4]{ {{3,-6,6}},{{10,7,-9 }}, {{ -3,-7,9 }}, {{ -8,0,4 }} };

	Moon *moons = real_moons;

	for (int step{ 0 }; step < 1000; ++step)
	{
		// Caclculate velocity
		for (int i = 0; i < 3; i++)
		{
			for (int j = i+1; j < 4; j++)
			{
				for (int h{ 0 }; h < 3; ++h) {
					if (moons[i].pos[h] > moons[j].pos[h]) {
						--moons[i].velocity[h];
						++moons[j].velocity[h];
					}
					else if (moons[i].pos[h] < moons[j].pos[h]) {
						++moons[i].velocity[h];
						--moons[j].velocity[h];
					}
				}
			}
		}

		// Apply velocity
		for (int i = 0; i < 4; i++)
		{
			for (int h{ 0 }; h < 3; ++h)
			{
				moons[i].pos[h] += moons[i].velocity[h];
			}
		}

		// Print Moons
		/*
		std::cout << "\nAfter " << step << " step:\n";
		for (int i{ 0 }; i < 4; ++i) {			
			std::cout << "pos=<x " << moons[i].pos[0] << " y= " << moons[i].pos[1] << " z= " << moons[i].pos[2]
				<< ", <x= " << moons[i].velocity[0] << " y= " << moons[i].velocity[1] << " z= " << moons[i].velocity[2] << ">\n";
		}
		*/
	}

	// Calculate energies:
	int total_energy{ 0 };
	for (int i{ 0 }; i < 4; ++i) {
		int pot_energy{ abs(moons[i].pos[0]) + abs(moons[i].pos[1]) + abs(moons[i].pos[2]) };
		int kin_energy{ abs(moons[i].velocity[0]) + abs(moons[i].velocity[1]) + abs(moons[i].velocity[2]) };
		total_energy += pot_energy * kin_energy;
	}

	std::cout << "Total energy in system: " << total_energy << '\n';

	return 0;
}
