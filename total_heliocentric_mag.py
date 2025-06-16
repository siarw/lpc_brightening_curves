from sys import argv
from typing import Iterable, Union

import numpy as np


def total_heliocentric_mag(
    distance: Union[float, Iterable[float]],
    orbital_arc: str = "inbound",
    oort_group: str = "new",
) -> float:
    """Calculate total heliocentric magnitude as function of heliocentric distance.

    Separates calculation by orbital arc and Oort group using median brightening
    parameters from a sample of 200+ comets.

    Parameters
    ----------
    distance : float or array_like
        Heliocentric distance in au
    orbital_arc : {'inbound', 'outbound'}, optional
        Orbital phase (pre/post-perihelion), default: 'inbound'
    oort_group : {'new', 'int', 'old'}, optional
        Oort dynamical group, default: 'new'

    Returns
    -------
    median_total_mag : float or array_like
        Median total heliocentric magnitude. Convert to apparent magnitude by
        adding 5*log10(observer distance).

    Notes
    -----
    Uses hardcoded values from dictionary `BRIGHTENING_PARS` structured as:
    - Top level: Oort groups ('new', 'int', 'old')
    - Second level: orbital arcs ('inbound', 'outbound')
    - Parameters:
      - k_near: Brightening slope inside transition (3.16 au)
      - k_far: Brightening slope beyond transition
      - k1: Post-perihelion fading slope (outbound only)
      - m1: Magnitude at 1 au (phase-dependent)

    Transition distance stored in `TRANSITION_R` (3.16 au).

    References
    ----------
    Lacerda et al. 2025, A&A, 697, A210
    DOI: 10.1051/0004-6361/202453565

    Author: Pedro Lacerda
    Date: 2025-06-16

    Todo
    ----
    Implement user-specified parameters and transition distance.

    Dependencies
    ------------
    numpy
    typing; python_version < '3.5'
    """

    OORT_GROUPS = ["new", "int", "old"]
    BRIGHTENING_PARS = {
        "new": {
            "inbound": {
                "k_near": 6.7285,  # Near-Sun slope
                "k_far": 12.847,  # Far-Sun slope
                "m1": 8.28,  # Pre-perihelion magnitude at 1 au
            },
            "outbound": {
                "k1": 11.54,  # Post-perihelion fading slope
                "m1": 8.75,  # Post-perihelion magnitude at 1 au
            },
        },
        "int": {
            "inbound": {"k_near": 7.83575, "k_far": 12.524, "m1": 8.96},
            "outbound": {"k1": 12.66, "m1": 9.71},
        },
        "old": {
            "inbound": {"k_near": 13.40275, "k_far": 14.632, "m1": 11.58},
            "outbound": {"k1": 13.21, "m1": 11.57},
        },
    }
    # distance at which slope changes
    TRANSITION_R = 3.16  # au
    transition_log_r = np.log10(TRANSITION_R)

    # if run from CLI, read in arguments
    if len(argv) == 4:
        distance = float(argv[1])
        orbital_arc = argv[2]
        oort_group = argv[3]
    else:
        distance = np.asarray(distance)

    # validate oort_group
    if oort_group not in OORT_GROUPS:
        raise ValueError(f"Invalid oort group: {oort_group}")
    # validate arc
    if orbital_arc not in ["inbound", "outbound"]:
        raise ValueError(f"Invalid arc: {orbital_arc}")

    # log distance (log_r)
    log_r = np.log10(np.asarray(distance))

    if orbital_arc == "inbound":  # pre-perihelion
        mask = log_r < transition_log_r
        k_near = BRIGHTENING_PARS[oort_group]["inbound"]["k_near"]
        m_near = BRIGHTENING_PARS[oort_group]["inbound"]["m1"]
        k_far = BRIGHTENING_PARS[oort_group]["inbound"]["k_far"]
        m_far = m_near + transition_log_r * (k_near - k_far)
        total_mag = np.where(mask, m_near + k_near * log_r, m_far + k_far * log_r)
    else:  # post-perihelion
        k = BRIGHTENING_PARS[oort_group]["outbound"]["k1"]
        m = BRIGHTENING_PARS[oort_group]["outbound"]["m1"]
        total_mag = m + k * log_r
    return total_mag


def main():
    print()
    print("What the function `total_heliocentric_mag` does:")
    print("-----------------------------------------------")
    print(
        """Calculates total heliocentric magnitude as a function of heliocentric
distance, separated by orbital arc and Oort group. The brightening
parameters, currently hardcoded into dictionary `BRIGHTENING_PARS`, are
median values for a sample of over 200 comets. See Lacerda et al. (2025)
for details.  """,
        end="\n\n",
    )
    print("Usage:")
    print("------")
    print(
        """total_heliocentric_mag(distance, orbital_arc, oort_group)""",
        end="\n\n",
    )
    print("Examples:")
    print("---------")
    print(""">>> print(total_heliocentric_mag(5.0, "inbound", "new"))""")
    print("output: ", total_heliocentric_mag(5.0, "inbound", "new"), end="\n\n")
    print(""">>> print(total_heliocentric_mag([1.0, 3.0, 10.0], "inbound", "new"))""")
    print(
        "output: ",
        total_heliocentric_mag([1.0, 3.0, 10.0], "inbound", "new"),
        end="\n\n",
    )
    print(""">>> print(total_heliocentric_mag([2.3, 3.7], "outbound", "old"))""")
    print("output: ", total_heliocentric_mag([2.3, 3.7], "outbound", "old"), end="\n\n")


if __name__ == "__main__":
    main()
