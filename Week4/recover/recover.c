#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }
    FILE *input = fopen(argv[1], "r");

    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[512];

    int jpg_count = 0;

    FILE *img = NULL;

    char filename[8];

    while (fread(buffer, sizeof(uint8_t), 512, input) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", jpg_count);

            img = fopen(filename, "w");

            if (img == NULL)
            {
                fclose(input);
                return 1;
            }
            jpg_count++;
        }

        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), 512, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }
    fclose(input);
    return 0;
}
