import time
import matplotlib.pyplot as plt
import numpy as np
from monte_carlo import MonteCarloOption


def plot_monte_carlo_paths(
    mc_engine, n_paths_to_plot=100, save_filename='barrier_paths_visualization.png'
):
    """
    Simulates underlying asset price paths and visualizes Knock-In vs Non-Knock-In trajectories.
    """
    print(
        f"Generating paths and plotting {n_paths_to_plot} trajectories..."
    )
    start_time = time.time()

    paths = mc_engine.generate_paths()

    max_prices = np.max(paths, axis=1)
    knock_in_flags = max_prices >= mc_engine.H

    t = np.arange(0, mc_engine.T_days + 1)

    plt.figure(figsize=(12, 7))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    plotted_ki_count = 0
    plotted_non_ki_count = 0

    np.random.seed(mc_engine.seed)
    random_indices = np.random.choice(paths.shape[0], mc_engine.n_sims, replace=False)

    for i in random_indices:
        current_path = paths[i]

        if knock_in_flags[i]:
            if plotted_ki_count < n_paths_to_plot // 2:
                plt.plot(
                    t,
                    current_path,
                    color='#e74c3c',
                    alpha=0.35,
                    linewidth=1.0,
                    label='_nolegend_'
                    if plotted_ki_count > 0
                    else 'Knock-In (Touched Barrier)',
                )
                plotted_ki_count += 1
        else:
            if plotted_non_ki_count < n_paths_to_plot // 2:
                plt.plot(
                    t,
                    current_path,
                    color='#95a5a6',
                    alpha=0.25,
                    linewidth=1.0,
                    label='_nolegend_'
                    if plotted_non_ki_count > 0
                    else 'Non-Knock-In (Expired Neutral)',
                )
                plotted_non_ki_count += 1

        if plotted_ki_count + plotted_non_ki_count >= n_paths_to_plot:
            break

    plt.axhline(
        y=mc_engine.H,
        color='#c0392b',
        linestyle='--',
        linewidth=2.0,
        label=f'Barrier Price (H = {mc_engine.H:,.0f})',
    )
    plt.axhline(
        y=mc_engine.K,
        color='#27ae60',
        linestyle=':',
        linewidth=1.8,
        label=f'Strike Price (K = {mc_engine.K:,.0f})',
    )
    plt.axhline(
        y=mc_engine.S0,
        color='#2980b9',
        linestyle='-',
        linewidth=1.5,
        label=f'Initial Asset Price (S0 = {mc_engine.S0:,.0f})',
    )

    plt.title(
        'Monte Carlo Path Simulation: Up-and-In Barrier Call Option',
        fontsize=14,
        fontweight='bold',
        pad=15,
    )
    plt.xlabel('Time Steps (Days)', fontsize=11, labelpad=8)
    plt.ylabel('Underlying Asset Price ($S_t$)', fontsize=11, labelpad=8)
    plt.legend(loc='upper left', fontsize=10, framealpha=0.9)
    plt.tight_layout()

    plt.savefig(save_filename, dpi=300)
    elapsed_time = time.time() - start_time
    print(
        f"Plot saved successfully as '{save_filename}' ({elapsed_time:.2f} seconds)"
    )
    plt.close()


if __name__ == "__main__":

    mc = MonteCarloOption(
        S0=15500,
        K=15000,
        H=16000,
        T_days=90,
        r=0.025,
        sigma=0.30,
        n_simulations=10000,
        seed=42,
    )

    plot_monte_carlo_paths(
        mc, n_paths_to_plot=100, save_filename='barrier_paths_visualization.png'
    )