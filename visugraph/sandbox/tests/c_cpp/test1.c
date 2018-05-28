#include <stdio.h>

int main() {
    FILE *f = fopen("this_is_a_random_file.txt", "w");
    fprintf(f, "this should not be printing\n");
}