DATA_B9 = {
"T692": {
"python": r"""
def find_combinations_count(amount, coins, check_from_index):
    if amount == 0:
        return 1
    elif amount < 0 or len(coins) == check_from_index:
        return 0
    else:
        with_first_coin = find_combinations_count(amount - coins[check_from_index], coins, check_from_index)
        without_first_coin = find_combinations_count(amount, coins, check_from_index + 1)
        return with_first_coin + without_first_coin
""",
"c": r"""
int find_combinations_count(int amount, const int *coins, int coins_len, int check_from_index) {
    if (amount == 0) return 1;
    else if (amount < 0 || coins_len == check_from_index) return 0;
    else {
        int with_first_coin = find_combinations_count(amount - coins[check_from_index], coins, coins_len, check_from_index);
        int without_first_coin = find_combinations_count(amount, coins, coins_len, check_from_index + 1);
        return with_first_coin + without_first_coin;
    }
}
""",
"csharp": r"""
public static class CoinCounter
{
    public static int FindCombinationsCount(int amount, int[] coins, int checkFromIndex)
    {
        if (amount == 0) return 1;
        if (amount < 0 || coins.Length == checkFromIndex) return 0;
        int withFirstCoin = FindCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
        int withoutFirstCoin = FindCombinationsCount(amount, coins, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}
"""
}
}
