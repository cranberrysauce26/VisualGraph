#include <fstream>

int main() {
    std::ofstream fout("a_random_file.txt");
    fout << "YYYYYY\n";
    fout.close();
}