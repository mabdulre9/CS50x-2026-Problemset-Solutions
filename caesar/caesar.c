#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])

{


    if (argc != 2 )
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    int n = strlen(argv[1]);

    for (int i = 0; i < n; i++)
    {
        if (!(isdigit(argv[1][i])))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int key = atoi(argv[1]);
    string text = get_string("Text: ");
    int m = strlen(text);
    // isalpha islower isupper
    // A-Z --- 65 to 90
    // a-z --- 97 to 122

 printf("ciphertext: ");

    for (int i = 0; i < m; i++)
    {

        if (isupper(text[i]))
        {
            printf("%c" , (((text[i]-65)+key) % 26 )+65);
        }
        else if (islower(text[i]))
        {
            printf("%c" , (((text[i]-97)+key) % 26 )+97);
        }
        else
        {
            printf("%c",text[i]);
        }

    }

printf("\n");

}
