#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float avg = 0;
            avg = round ((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;

        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed = 0;
    float sepiaGreen = 0;
    float sepiaBlue = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaRed = round(fmin(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue,255));
            sepiaGreen = round(fmin(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue,255));
            sepiaBlue = round(fmin(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue,255));


            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;

        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    int tmpl_red = 0;
    int tmpl_green = 0;
    int tmpl_blue = 0;
    int tmpr_red = 0;
    int tmpr_green = 0;
    int tmpr_blue = 0;

    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width/2; j++)
        {
            tmpl_red = image[i][j].rgbtRed;
            tmpl_green = image[i][j].rgbtGreen;
            tmpl_blue = image[i][j].rgbtBlue;

            tmpr_red = image[i][width - 1 - j].rgbtRed;
            tmpr_green = image[i][width - 1 - j].rgbtGreen;
            tmpr_blue = image[i][width - 1 - j].rgbtBlue;

            image[i][width - 1 - j].rgbtRed = tmpl_red;
            image[i][width - 1 - j].rgbtGreen = tmpl_green;
            image[i][width - 1 - j].rgbtBlue = tmpl_blue;

            image[i][j].rgbtRed = tmpr_red;
            image[i][j].rgbtGreen = tmpr_green;
            image[i][j].rgbtBlue = tmpr_blue;

        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }



    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            float count = 0;

            for (int k = i-1; k < i+2 ; k++)
            {
                for (int l = j - 1; l < j+2; l++)
                {
                    if (k >= 0 && k < height && l >= 0 && l < width)
                    {
                        sumRed += copy[k][l].rgbtRed;
                        sumGreen += copy[k][l].rgbtGreen;
                        sumBlue += copy[k][l].rgbtBlue;
                        count ++;
                    }

                }


            }
            image[i][j].rgbtRed = round(sumRed/count);
            image[i][j].rgbtGreen = round(sumGreen/count);
            image[i][j].rgbtBlue = round(sumBlue/count);



        }
    }

    return;

}
