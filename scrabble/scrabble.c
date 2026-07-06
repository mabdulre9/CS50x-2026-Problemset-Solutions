#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main (void)
{
    int index = 0, total1 = 0, total2 =0;
    int pts [] = {1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10};

    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    for (int i = 0; i < strlen(word1); i++)
    {
        if (isalpha(word1[i]))
        {
            index = (int) toupper(word1[i]) -65;
            total1 += pts[index];
        }

    }
    for (int i = 0; i < strlen(word2); i++)
    {
        if (isalpha(word2[i]))
        {
            index = (int) toupper(word2[i]) -65;
            total2 += pts[index];
        }
    }

    if (total1>total2)
    {
        printf("Player 1 wins!\n");
    }
    else if (total1<total2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }



}
