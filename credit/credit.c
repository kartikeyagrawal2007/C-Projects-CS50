#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card = get_long("Number: ");

    int count = 0;
    long temp = card;
    while (temp > 0)
    {
        temp = temp / 10;
        count++;
    }

    long start = card;

    while (start >= 100)
    {
        start /= 10;
    }

    int first = start / 10;

    int sum1 = 0;
    int sum2 = 0;

    temp = card;
    while (temp > 0)
    {
        int digit = (temp / 10) % 10;
        int multiply = digit * 2;

        if (multiply > 9)
        {
            sum1 += (multiply % 10) + 1;
        }
        else
        {
            sum1 += multiply;
        }
        temp = temp / 100;
    }

    temp = card;

    while (temp > 0)
    {
        sum2 += temp % 10;
        temp /= 100;
    }

    int total = sum1 + sum2;

    if (total % 10 == 0)
    {
        if ((start == 34 || start == 37) && count == 15)
        {
            printf("AMEX\n");
        }
        else if (start >= 51 && start <= 55 && count == 16)
        {
            printf("MASTERCARD\n");
        }
        else if (first == 4 && (count == 13 || count == 16))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
