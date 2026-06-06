#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");

    if (input == NULL)
    {
        printf("Cloud not open input file.\n");
        return 1;
    }
    FILE *output = fopen(argv[2], "w");

    if (output == NULL)
    {
        fclose(input);
        printf("Could not create output file.\n");
        return 1;
    }
    float factor = atof(argv[3]);

    uint8_t header[44];

    fread(header, sizeof(uint8_t), 44, input);
    fwrite(header, sizeof(uint8_t), 44, output);

    int16_t sample;

    while (fread(&sample, sizeof(int16_t), 1, input))
    {
        sample = sample * factor;
        fwrite(&sample, sizeof(int16_t), 1, output);
    }
    fclose(input);
    fclose(output);
}
