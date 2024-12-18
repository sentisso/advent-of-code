#include <iostream>
#include <unordered_set>
#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>

#define OBSTACLE '#'

typedef std::vector<char> Grid;
typedef std::pair<size_t, size_t> Vector;
typedef std::pair<size_t, Vector> GuardPos;

constexpr size_t getPos(size_t i, size_t j, size_t width) {
	return i * width + j;
}

std::vector<char> readGrid(const std::string& filename, size_t& height, size_t& width) {
	std::ifstream file(filename);
	if (!file) {
		throw std::runtime_error("Could not open file: " + filename);
	}

	std::vector<char> grid;
	std::string line;
	width = 0;
	height = 0;

	// Read lines and expand grid dynamically
	while (std::getline(file, line)) {
		width = line.length();

		grid.insert(grid.end(), line.begin(), line.end());
		height++;
	}

	return grid;
}

std::pair<size_t, Vector> findGuard(const Grid& grid, size_t height, size_t width) {
	char val;
	size_t pos;

	for (size_t i = 0; i < height; i++) {
		for (size_t j = 0; j < width; j++) {
			pos = getPos(i, j, width);
			val = grid[pos];

			switch (val) {
				case '^':
					return {pos, {-1, 0}};
				case '>':
					return {pos, {0, 1}};
				case 'v':
					return {pos, {1, 0}};
				case '<':
					return {pos, {0, -1}};
				default:
					break;
			}
		}
	}

	throw std::runtime_error("Guard not found in grid");
}

size_t simulateGuard(const Grid& grid, size_t currPos, Vector currVec) {
	std::unordered_set<GuardPos> uniqueVisits;
	std::unordered_set<int>
}

int main() {
	size_t height, width;
	Grid grid = readGrid("input.txt", height, width);

	auto [pos, guard] = findGuard(grid, height, width);

    return 0;
}