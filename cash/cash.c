#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;

    //int change = 70;
    int coins = 0;
    int change;
    do
    {
        change = get_int("Change owed: ");
    }
    while (change<0);

    while (change>0)
    {
        if (quarter <= change)
        {
            change-=quarter;
            coins+=1;
        }
        else if (dime <= change)
        {
            change-=dime;
            coins+=1;
        }
        else if (nickel <= change)
        {
            change-=nickel;
            coins+=1;
        }
        else
        {
            change-=penny;
            coins+=1;
        }

    }

    printf("%i\n",coins);

}
