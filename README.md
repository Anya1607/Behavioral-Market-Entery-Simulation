# Behavioral-Market-Entery-Simulation

A computational behavioral economics simulation modeling a three-firm market entry game under varying levels of **loss aversion**. Drawing from Kahneman and Tversky’s **Prospect Theory**, this project explores how escalating psychological sensitivity to financial losses suppresses market participation compared to a purely rational baseline.

---

## Overview & Economic Model

In a competitive market with three symmetric firms (A, B, and C), each firm decides simultaneously whether to **Enter (`1`)** or **Stay Out (`0`)**:

| Market Scenario | Player A's Choice | Rivals' Choices | Cash Payoff |
| :--- | :---: | :---: | :---: |
| **Monopoly** | Enter | Both Stay Out | **+$1,000** |
| **Duopoly (Shared)** | Enter | One Enters, One Out | **+$100** |
| **Overcrowded Crash** | Enter | Both Enter | **-$500** |
| **Outside Option** | Stay Out | Any | **$0** |

### Core Mechanics
* **Quadratic Loss Penalty:** Positive gains are evaluated linearly ($Utility(x) = x$), while financial losses are penalized quadratically and multiplied by the fear factor (lambda): ($U(x) = -\lambda x^2$) to reflect intensifying psychological aversion to losses.
* **Adaptive Belief Updating:** Firms adjust their expectations of rival entry over 500 simulated rounds using exponential smoothing (where`80%` is prior belief + `20%` is observed daily entry rate or future belief).
* **Theoretical Equilibrium ($p^*$):** Derived by setting expected behavioral utility to zero, solving the quadratic equation to map the tipping point where potential gains balance loss-averse penalties.

---

## Simulation Results

The graph shows that as the loss-aversion coefficient ($\lambda$) increases, the psychological penalty of a market crash heavily outweighs monopoly gains, sharply depressing market participation:

![Simulated Market Entry Rate vs. Loss Aversion](Screenshot%202026-11-21%20at%2011.06.16%20PM.png)

* **Fearless Baseline ($\lambda = 0.000$):** Without downside fear, firms enter at an aggressive **79.3%** rate.
* **Moderate Loss Aversion ($\lambda \approx 0.010$):** Entry rates drop to **41.2%** as loss penalties scale.
* **High Loss Aversion ($\lambda = 0.050$):** Severe fear of overcrowding drives participation down to **27.1%**, tightly tracking the theoretical equilibrium curve $p^*(\lambda)$.


### Conclusion & Key Takeaway
The close alignment between the simulated entry rates (red) and the analytical equilibrium curve $p^*(\lambda)$ (navy) demonstrates that **adaptive, experience-based learning converges toward theoretical behavioral equilibrium**. Even without explicit knowledge of the underlying utility equations, boundedly rational firms updating their beliefs through trial and error naturally settle around the exact market-entry tipping point predicted by prospect theory. Ultimately, the model illustrates how even modest levels of psychological loss aversion are sufficient to deter aggressive market entry and mitigate overcrowding.

---

## How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Anya1607/Behavioral-Market-Entery-Simulation.git](https://github.com/Anya1607/Behavioral-Market-Entery-Simulation.git)
   cd Behavioral-Market-Entery-Simulation
