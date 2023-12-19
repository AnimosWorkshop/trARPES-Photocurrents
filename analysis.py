import eddington as edd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


xerr = 0.02
yerr = 0.02


def csvtodata(df:pd.DataFrame=pd.read_csv('data.csv')) -> edd.FittingData:
    data = {
        'x': list(df['x']),
        'y': list(df['y']),
        'dx': [xerr] * len(df.index),
        'dy': [yerr] * len(df.index)
    }
    return edd.FittingData(data, x_column='x', y_column='y', xerr_column='dx', yerr_column='dy')


def pc_fitfunc(a, x):
    return a[0] * np.sin(2 * x) + a[1] * np.sin(4 * x) + a[2] * np.cos(4 * x) + a[3]


def pc_derfunc(a, x):
    return 2 * a[0] * np.cos(2 * x) + 4 * a[1] * np.cos(4 * x) - 4 * a[2] * np.sin(4 * x)


def pc_func() -> edd.FittingFunction:
    return edd.FittingFunction(fit_func=pc_fitfunc, n=4, name="PC Harmonic", x_derivative=pc_derfunc)


def plot_result(df:pd.DataFrame, fit_res: edd.FittingResult):
    fig, ax = plt.subplots()
    plt.title("Photocurrents in Bi2Se3 - I = f(α)")

    x = np.linspace(0, np.pi, 1000)
    line, = ax.plot(x, pc_fitfunc(fit_res.a, x))

    ax.set_xlabel("Polarization [rad]")
    ax.set_ylabel("Current [arb. units]")
    fig.subplots_adjust(bottom=0.2)

    # Textboxes
    plt.annotate('C=' + "%.2f" % fit_res.a[0], xy=(0,0), xytext=(0.2, 0.075), xycoords='figure fraction')
    plt.annotate('L1=' + "%.2f" % fit_res.a[1], xy=(0, 0), xytext=(0.4, 0.075), xycoords='figure fraction')
    plt.annotate('L2=' + "%.2f" % fit_res.a[2], xy=(0, 0), xytext=(0.6, 0.075), xycoords='figure fraction')
    plt.annotate('D=' + "%.2f" % fit_res.a[3], xy=(0, 0), xytext=(0.8, 0.075), xycoords='figure fraction')
    plt.annotate('x2red=' + "%.2f" % fit_res.chi2_reduced, xy=(0, 0), xytext=(0.35, 0.025), xycoords='figure fraction')
    plt.annotate('pval=' + "%.2f" % fit_res.p_probability, xy=(0, 0), xytext=(0.65, 0.025), xycoords='figure fraction')

    # Hlines
    ax.axvline(x=0, color='g', linestyle=':', linewidth=2)
    ax.axvline(x=np.pi / 2, color='g', linestyle=':', linewidth=2)
    ax.axvline(x=np.pi, color='g', linestyle=':', linewidth=2)
    ax.axvline(x=np.pi / 4, color='b', linestyle=':', linewidth=2)
    ax.axvline(x=3 * np.pi / 4, color='r', linestyle=':', linewidth=2)

    # Data points
    plt.scatter(df['x'], df['y'])

    abslim = abs(fit_res.a[0]) + abs(fit_res.a[1]) + abs(fit_res.a[2])
    plt.ylim(fit_res.a[3] - abslim * 1.15, fit_res.a[3] + abslim * 1.15)

    plt.show()


def main():
    df = pd.read_csv('data.csv')
    fit_result = edd.fitting.fit(csvtodata(df), pc_func(), np.zeros(4), use_x_derivative=True)
    print(fit_result)
    plot_result(df, fit_result)


if __name__ == '__main__':
    main()