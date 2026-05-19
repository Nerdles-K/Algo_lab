def is_within_budget(selection, costs, budget):
    total = 0
    for i in selection:
        total += costs[i]
    return total <= budget

def maximize_reach_exact(budget, costs, reaches):
    n = len(costs)

    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = costs[i - 1]
        reach = reaches[i - 1]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]

            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + reach)

    selected = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            selected.append(i - 1)
            b -= costs[i - 1]

    selected.reverse()
    return dp[n][budget], selected


def maximize_reach_greedy(budget, costs, reaches):
    n = len(costs)

    order = sorted(range(n), key=lambda i: reaches[i] / costs[i], reverse=True)

    selected = []
    total_cost = 0
    total_reach = 0

    for i in order:
        if total_cost + costs[i] <= budget:
            selected.append(i)
            total_cost += costs[i]
            total_reach += reaches[i]

    return total_reach, selected


def run_test(name, budget, costs, reaches):
    print(f"=== {name} ===")
    print("budget =", budget)
    print("costs  =", costs)
    print("reaches=", reaches)

    exact_reach, exact_sel = maximize_reach_exact(budget, costs, reaches)
    greedy_reach, greedy_sel = maximize_reach_greedy(budget, costs, reaches)

    print("Exact  -> reach:", exact_reach, ", selected users:", exact_sel,
          ", valid:", is_within_budget(exact_sel, costs, budget))
    print("Greedy -> reach:", greedy_reach, ", selected users:", greedy_sel,
          ", valid:", is_within_budget(greedy_sel, costs, budget))


if __name__ == "__main__":
    run_test(
        "Edge Test 1: Empty input",
        budget=10,
        costs=[],
        reaches=[]
    )

    run_test(
        "Edge Test 2: Zero budget",
        budget=0,
        costs=[2, 3, 4],
        reaches=[10, 20, 30]
    )

    run_test(
        "Edge Test 3: Nothing fits",
        budget=3,
        costs=[5, 6, 7],
        reaches=[10, 20, 30]
    )

    run_test(
        "Edge Test 4: Single user",
        budget=5,
        costs=[5],
        reaches=[12]
    )

    run_test(
        "Edge Test 5: Greedy fails",
        budget=5,
        costs=[1, 5],
        reaches=[2, 9]
    )