import matplotlib.pyplot as plt
import numpy as np
from total_heliocentric_mag import total_heliocentric_mag

OORT_GROUPS = ["new", "int", "old"]
OORT_LINESTYLES = {
    "new": {"linestyle": "-", "color": "#0C7BDC"},
    "int": {"linestyle": (0, (7, 1.5)), "color": "#FFC20A"},
    "old": {"linestyle": (0, (3, 1.5)), "color": "#FF5733"},
}


def plot_heliocentric_lightcurves():
    """
    Plot median heliocentric distance-dependent brightening slopes for [new, int. and old comets]
    in pre-perihelion and post-perihelion phases.
    The brightening slopes are annotated on the plot in mag/log(au).

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # pre-perihelion, median, heliocentric-distance-dependent brightening slopes
    # for [new, int. and old comets]
    oort_gr_inbound_kr_near = [6.7285, 7.83575, 13.40275]  # inside 3.16 au
    oort_gr_inbound_kr_far = [12.847, 12.524, 14.632]  # outside 3.16 au

    # post-perihelion median global fading parameters for [new, int. and old comets]
    oort_gr_outbound_k1 = [11.54, 12.66, 13.21]  # fading slopes

    oort_groups = ["new", "int", "old"]
    oort_labels = [OORT_GROUPS[i] for i, og in enumerate(oort_groups)]
    oort_linestyles = [OORT_LINESTYLES[oort] for oort in oort_groups]

    r = np.linspace(1, 10, 100)
    x = np.log10(r)
    r_near = np.linspace(3.16, 1, 100)
    r_far = np.linspace(10, 3.16, 100)
    x_near = np.log10(r_near)
    x_far = np.log10(r_far)

    fig, (ax_inbound, ax_outbound) = plt.subplots(1, 2, sharey=True)

    # no space between plot axes
    fig.subplots_adjust(wspace=0)

    for i, og in enumerate(oort_groups):
        ax_inbound.plot(
            x,
            total_heliocentric_mag(r, "inbound", og),
            **oort_linestyles[i],
            label=oort_labels[i],
        )
        ax_outbound.plot(
            x,
            total_heliocentric_mag(r, "outbound", og),
            **oort_linestyles[i],
            label=oort_labels[i],
        )

        # annotate lines with slope value
        annotate_opt_dict = {
            "zorder": 2,
            "fontsize": 9,
            "ha": "center",
            "va": "bottom",
            "backgroundcolor": "white",
            "bbox": dict(
                boxstyle="round,pad=0.2", facecolor="yellow", edgecolor="black"
            ),
        }
        ax_inbound.annotate(
            r"$%.1f$" % oort_gr_inbound_kr_near[i],
            (
                (x_ins_mid := (x_near[0] + x_near[-1]) / 2),
                total_heliocentric_mag(10**x_ins_mid, "inbound", og),
            ),
            **annotate_opt_dict,
        )
        ax_inbound.annotate(
            r"$%.1f$" % oort_gr_inbound_kr_far[i],
            (
                x_out_mid := (x_far[0] + x_far[-1]) / 2,
                total_heliocentric_mag(10**x_out_mid, "inbound", og),
            ),
            **annotate_opt_dict,
        )
        ax_outbound.annotate(
            r"$%.1f$" % oort_gr_outbound_k1[i],
            (
                (x_all_dist_mid := (x[0] + x[-1]) / 2),
                total_heliocentric_mag(10**x_all_dist_mid, "outbound", og),
            ),
            **annotate_opt_dict,
        )

    ax_inbound.set_xlabel(r"$r$ (au)")
    ax_outbound.set_xlabel(r"$r$ (au)")
    ax_inbound.set_ylabel(r"mag")

    # ylim 25,6
    ax_inbound.set_ylim(25, 7.5)
    ax_outbound.set_ylim(25, 7.5)
    # xlim 0, 1
    ax_inbound.set_xlim(1, 0)
    ax_outbound.set_xlim(0, 1)

    ax_inbound.set_title("Pre-Perihelion")
    ax_outbound.set_title("Post-Perihelion")

    # preq x ticks at range(1, 11)
    ax_inbound.axes.xaxis.set_ticks(np.log10(np.array([1, 2, 3, 5, 10])))
    ax_inbound.set_xticklabels(["1", "2", "3", "5", "10"])

    # posq x ticks at range(1, 11)
    ax_outbound.axes.xaxis.set_ticks(np.log10(np.array([2, 3, 5, 10])))
    ax_outbound.set_xticklabels(["2", "3", "5", "10"])

    plt.legend(title="Oort Group")


def main():

    plot_heliocentric_lightcurves()

    plt.show()

    # plt.savefig("heliocentric_lightcurves.pdf", transparent=True, bbox_inches="tight")
    # plt.savefig("heliocentric_lightcurves.png", bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    main()
