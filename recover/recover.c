#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        return 2;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    FILE *img = NULL;
    int counter = 0;
    char filename[8];

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {


        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            if (img != NULL)
            {
                fclose(img);
                counter ++;
            }

            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");

        }

        if (img != NULL)
        {
            fwrite(buffer,1,512,img);
        }


    }

    fclose(img);
    fclose(card);
}
