import matplotlib.pyplot as plt
import numpy as np
from monte_carlo import MonteCarloOption
from delta_hedging import DeltaHedgingSimulator

def plot_pnl_distribution(summary: dict, save_path: str = "hedging_pnl_distribution.png"):
    """
    Plots the histogram of hedging PnL errors across simulated paths and saves as an image.
    """
    pnls = summary["all_pnls"]
    mean_pnl = summary["mean_pnl"]
    std_pnl = summary["std_pnl"]

    plt.figure(figsize=(10, 6))

    # 1. PnL Histogram
    plt.hist(
        pnls, bins=25, color="skyblue", edgecolor="black", alpha=0.7, label="Hedging PnL"
    )

    # 2. Reference Lines: Zero Benchmark & Mean PnL
    plt.axvline(0, color="red", linestyle="--", linewidth=1.8, label="Zero PnL Benchmark")
    plt.axvline(
        mean_pnl, color="green", linestyle="-", linewidth=2.0, label=f"Mean PnL ({mean_pnl:,.2f} KRW)"
    )

    # 3. ±1 Standard Deviation Range (Shaded)
    plt.axvspan(
        mean_pnl - std_pnl,
        mean_pnl + std_pnl,
        color="grey",
        alpha=0.15,
        label=f"±1 Std Dev ({std_pnl:,.2f} KRW)",
    )

    # 4. Chart Labels & Style
    plt.title("Multi-Path Delta Hedging PnL Error Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Final Hedging Error / PnL (KRW)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.legend(loc="upper right", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    
    # Save chart image and display
    plt.savefig(save_path, dpi=300)
    print(f"\nPlot successfully saved as '{save_path}'")
    plt.show()

if __name__ == "__main__":
    # 1. Base option configuration
    mc = MonteCarloOption(
        S0=15500, K=15000, H=16000, T_days=90, r=0.025, sigma=0.30, n_simulations=2000, seed=42
    )

    # 2. Run multi-path hedging simulation across 100 paths
    num_paths = 100
    all_paths = mc.generate_paths()[:num_paths]
    simulator = DeltaHedgingSimulator(mc)
    summary = simulator.simulate_multi_path_hedging(all_paths)

    # 3. Render visual plot
    plot_pnl_distribution(summary)