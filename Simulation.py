import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)  # makes results reproducible

# =====================================================================
# 1. UTILITY FUNCTION
# =====================================================================

def calculate_behavioral_utility(cash_payoff, lambda_fear):
    """
    This function converts cash outcomes into percieved utility

    Gains are valued as they are while Losses are penalised quadratically because losses hurt more. 
        cash >= 0: utility = cash
        cash <  0: utility = -lambda * cash^2

    Note: lambda = 0 means losses carry NO weight (a loss feels like $0).
    It is not the risk-neutral case.
    """
  
    if cash_payoff >= 0:
        return float(cash_payoff)
    return float(-lambda_fear * abs(cash_payoff) ** 2)


# =====================================================================
# 2. PAYOFFS TO PLAYER A
# Index order: [A's choice, B's choice, C's choice]; 0 = stay out, 1 = enter.
# Staying out always pays 0, so only the "A enters" cells are filled in.
# =====================================================================

payoff_matrix_A = np.zeros((2, 2, 2)) # creates a 3D grid where each player has 2 options-- enter or stay out. 
payoff_matrix_A[1, 0, 0] = 1000.0   # monopoly: A enters, B and C stay out
payoff_matrix_A[1, 1, 0] = 100.0    # shared market with B
payoff_matrix_A[1, 0, 1] = 100.0    # shared market with C
payoff_matrix_A[1, 1, 1] = -500.0   # overcrowded: all three enter


# =====================================================================
# 3. SIMULATION: Main loop
# =====================================================================

fear_levels = np.linspace(0.0, 0.05, 40)   # 40 values of lambda
SIMULATION_ROUNDS = 500
recorded_entry_rates = []

for lambda_fear in fear_levels:

    total_entries_in_simulation = 0
    p_belief = 0.5   # Each player guesses that there is a 50% chance their rivals enter the market

    for round_idx in range(SIMULATION_ROUNDS):

        # Expected utility of entering, given the belief p_belief
        prob_both_out    = (1 - p_belief) * (1 - p_belief) # neither b nor c enters today
        prob_b_in_c_out  = p_belief * (1 - p_belief) # b enters while c does not
        prob_b_out_c_in  = (1 - p_belief) * p_belief # c enters while b does not
        prob_both_in     = p_belief * p_belief # both players enter

        eu_enter = (
            prob_both_out   * calculate_behavioral_utility(payoff_matrix_A[1, 0, 0], lambda_fear) +
            prob_b_in_c_out * calculate_behavioral_utility(payoff_matrix_A[1, 1, 0], lambda_fear) +
            prob_b_out_c_in * calculate_behavioral_utility(payoff_matrix_A[1, 0, 1], lambda_fear) +
            prob_both_in    * calculate_behavioral_utility(payoff_matrix_A[1, 1, 1], lambda_fear)
        )
        eu_stay_out = 0.0

        # Choice rule (an assumption): if entering looks good, each firm enters
        # with probability 0.8; otherwise with probability 0.1.
        if eu_enter > eu_stay_out:
            choices = np.random.choice([1, 0], size=3, p=[0.8, 0.2])
        else:
            choices = np.random.choice([1, 0], size=3, p=[0.1, 0.9]) #To choose a raondom market situation

        entries_today = np.sum(choices) 
        total_entries_in_simulation += entries_today

        # where there is 80% faith in old possibilities, 20% faith on today's results
        p_belief = 0.8 * p_belief + 0.2 * (entries_today / 3.0)

    recorded_entry_rates.append(total_entries_in_simulation / (3 * SIMULATION_ROUNDS))


# =====================================================================
# 4. RESULTS AND PLOT
# =====================================================================

results = pd.DataFrame({
    'Loss_Aversion_Coefficient': fear_levels,
    'Market_Entry_Probability': recorded_entry_rates
})
print(results.to_string(index=False))          # all 40 rows, for exact numbers
results.to_csv('results.csv', index=False)

plt.figure(figsize=(9, 5))
plt.plot(results['Loss_Aversion_Coefficient'],
         results['Market_Entry_Probability'] * 100,
         marker='o', color='crimson', linewidth=2,
         label='Simulated entry rate')

# --- equilibrium belief p*(lambda), where expected utility = 0 ---
# EU = 1000 - 1800p + (800 - 250000*lambda) * p^2
# These quadratic roots represent theoretical equillibrium- where the market stabalises. 
def p_star(lam):
    roots = np.roots([800 - 250000 * lam, -1800, 1000])
    valid = [r.real for r in roots if abs(r.imag) < 1e-9 and 0 <= r.real <= 1 + 1e-9] # ensures roots are real numbers
    return min(valid) if valid else np.nan # else outputs "not a number"


# Plotting Graphs
plt.plot(fear_levels, [p_star(l) * 100 for l in fear_levels],
         linestyle='--', color='navy', label='Equilibrium belief p*(λ)')
plt.title('Simulated Market Entry Rate vs. Loss Aversion', fontsize=12, fontweight='bold')
plt.xlabel('Loss-aversion coefficient (λ)', fontsize=10)
plt.ylabel('Market entry rate (%)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(0, 100)
plt.legend()
plt.savefig('figure1.png', dpi=300, bbox_inches='tight')   # figure for the write-up
plt.show()
