while True:
    try:
        dollars = float(input("Change owed: "))
        if dollars >= 0:
            break
    except ValueError:
        pass

cents = round(dollars * 100)
coins = 0
coins += cents // 25
cents %=25
coins += cents // 10
cents %= 10
coins += cents // 5
cents %= 5
coins += cents
print(coins)
