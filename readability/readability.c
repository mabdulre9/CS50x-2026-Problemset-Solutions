#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string paragraph = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentences = 0;

    int n = strlen(paragraph);

    for (int i = 0; i < n; i++ )
    {
        if (isalpha(paragraph[i]))
        {
            letters +=1;
        }

        if (paragraph[i] == ' ')
        {
            words +=1;
        }

        if (paragraph[i] == '.' || paragraph[i] == '!' || paragraph[i] == '?' )
        {
            sentences +=1;
        }

    }

    float L = (float) letters/words*100;
    float S = (float) sentences/words*100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index <= 16 && index > 1)
    {
        printf("Grade %d\n", index);
    }
    else if (index >16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }

}
