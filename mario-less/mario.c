#include <stdio.h>
#include <cs50.h>

int main(void)
{

int height;
    do
    {
        height = get_int("Enter height of pyramid ");
    }
    while(height<=0);



    for (int i=0; i<height; i++)
    {
        for (int k=0; k<height-i-1; k++)
        {
        printf(" ");
        }
        for (int j=0; j<=i; j++)
        {
            printf("#");

        }

        printf("\n");
    }





}
