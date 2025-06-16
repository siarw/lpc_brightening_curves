README
======

What does the function `calc_total_heliocentric_mag` do?
--------------------------------------------------------

It calculates total heliocentric magnitude as a function of heliocentric
distance, separated by orbital arc and Oort group. The brightening parameters,
currently hardcoded into dictionary `BRIGHTENING_PARS`, are median values for a
sample of 200+ comets. See Lacerda et al. (2025) for details.  

Installation
------------

The function `calc_total_heliocentric_mag()` is included in the file
`calc_total_heliocentric_mag.py`, which is self-contained.  You can copy the
function `calc_total_heliocentric_mag.py` into your working environment, or
clone the repository into a local directory using:

```bash
git clone https://github.com/siarw/lpc_heliocentric_lightcurves.git
```

Usage
-----

```python
calc_total_heliocentric_mag(distance, orbital_arc, oort_group)
```

Examples
---------

```python
>>> print(calc_total_heliocentric_mag(5.0, "inbound", "new"))
output:  14.20233223070413
```

```python
>>> print(calc_total_heliocentric_mag([1.0, 3.0, 10.0], "inbound", "new"))
output:  [ 8.28       11.49031036 18.06966458]
```

```python
>>> print(calc_total_heliocentric_mag([2.3, 3.7], "outbound", "old"))
output:  [16.34842471 19.07594477]
```

Parameters
----------

`distance` : float or array_like
    Heliocentric distance in au  
`orbital_arc` : {`inbound`, `outbound`}, optional
    Orbital phase (inbound/outbound), default: `inbound`  
`oort_group` : {`new`, `int`, `old`}, optional
    Oort dynamical group, default: `new`

Returns
-------

`median_total_mag` : float or array_like
    Median total heliocentric magnitude. Convert to apparent magnitude by
    adding `5 * np.log10(observer distance)`.

Notes
-----

Uses hardcoded values from dictionary `BRIGHTENING_PARS` structured as:

- Top level: Oort groups (`new`, `int`, `old`)
- Second level: orbital arcs (`inbound`, `outbound`)
- Third level: brightening parameters:
  - `k_near`: Brightening slope inside transition (3.16 au)
  - `k_far`: Brightening slope beyond transition
  - `k1`: Post-perihelion fading slope (outbound only)
  - `m1`: Magnitude at 1 au (phase-dependent)

Transition distance stored in `TRANSITION_R` (3.16 au).

References
----------

If you use this function, please cite:  
Lacerda et al. 2025, A&A, 697, A210 (DOI: 10.1051/0004-6361/202453565)

Todo
----

Implement user-specified parameters and transition distance.

Improvements
------------

If you want to contribute suggestions, here is one way:

1. **Fork the Repository**.  Anyone with a GitHub account can fork this public repository:  Click the "Fork" button in the upper-right corner.  Choose where to fork (your own account or organization).  Wait for the fork to be created. This creates a personal copy of the repository under your account.  
2. **Clone and Edit the Forked Repository**.  Clone your fork to your computer:

```bash
git clone https://github.com/<their-username>/<repository-name>.git
```

Create a new branch for your changes:

```bash
git checkout -b suggestion-branch
```

Make and commit changes:

```bash
git add .
git commit -m "Description of changes"
```

Push your branch to your fork:

```bash
git push origin suggestion-branch
```

3. **Propose Changes via Pull Request**. After pushing changes, open a pull request (PR): Go to the main page of your fork on GitHub.  Click "Compare & pull request" (GitHub may show this automatically after a push).  Select the base repository and branch (the original repository and target branch, e.g., main).  Select your fork and branch as the head repository and branch.  Add a title and description explaining the changes.  Click "Create pull request".  This PR notifies me (the repository owner) that someone wants to merge their changes into your project.

Dependencies
------------

- numpy  
- typing if python_version < '3.5'

Author
------

Pedro Lacerda (2025-06-16)

What does the function `plot_heliocentric_lightcurves` do?
----------------------------------------------------------

It plots the heliocentric light curves corresponding to `BRIGHTENING_PARS` to
produce this plot:

![Heliocentric Light Curves](./heliocentric_lightcurves.png)
