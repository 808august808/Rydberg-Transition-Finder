import streamlit as st
import pandas as pd
from arc import Rubidium85, Rubidium87, Caesium

# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="Rydberg Transition Finder",
    page_icon="⚛️",
    layout="wide",
)

st.title("⚛️ Rydberg Transition Finder")

st.write(
    """
    Search for alkali Rydberg–Rydberg transitions within an RF
    frequency range and calculate the optical wavelengths needed
    to reach a selected Rydberg state.
    """
)


# ============================================================
# Atom definitions
# ============================================================

ATOMS = {
    "Rb-85": Rubidium85,
    "Rb-87": Rubidium87,
    "Cs-133": Caesium,
}


# Ground states
GROUND_STATES = {
    "Rb-85": (5, 0, 0.5),
    "Rb-87": (5, 0, 0.5),
    "Cs-133": (6, 0, 0.5),
}


# Common intermediate state used for the optical ladder
INTERMEDIATE_STATES = {
    "Rb-85": (5, 1, 1.5),
    "Rb-87": (5, 1, 1.5),
    "Cs-133": (6, 1, 1.5),
}


GROUND_LABELS = {
    "Rb-85": "5S1/2",
    "Rb-87": "5S1/2",
    "Cs-133": "6S1/2",
}


INTERMEDIATE_LABELS = {
    "Rb-85": "5P3/2",
    "Rb-87": "5P3/2",
    "Cs-133": "6P3/2",
}


# ============================================================
# Orbital information
# ============================================================

ORBITAL_LETTERS = {
    0: "S",
    1: "P",
    2: "D",
    3: "F",
    4: "G",
    5: "H",
}


# Rydberg states searched by default.
#
# Each entry is:
#     (l, j)
#
# These are the orbital angular momentum states included
# in the transition search.
RYDBERG_STATES = [
    (0, 0.5),  # S1/2

    (1, 0.5),  # P1/2
    (1, 1.5),  # P3/2

    (2, 1.5),  # D3/2
    (2, 2.5),  # D5/2

    (3, 2.5),  # F5/2
    (3, 3.5),  # F7/2
]


# ============================================================
# Helper functions
# ============================================================

def state_label(n, l, j):
    """
    Convert ARC quantum numbers into a spectroscopic label.

    Examples:
        (34, 2, 2.5) -> 34D5/2
        (35, 1, 1.5) -> 35P3/2
    """

    orbital = ORBITAL_LETTERS.get(l, "?")

    two_j = int(round(2 * j))

    if two_j % 2 == 0:
        j_label = str(two_j // 2)
    else:
        j_label = f"{two_j}/2"

    return f"{n}{orbital}{j_label}"


def allowed_e1_transition(l1, j1, l2, j2):
    """
    Check the basic electric-dipole (E1) selection rules:

        Δl = ±1
        Δj = 0, ±1

    Note that this is only the basic E1 selection-rule check.
    Hyperfine, polarization, and magnetic-sublevel selection
    rules are not included here.

    Returns:
        True  -> E1 allowed
        False -> E1 forbidden
    """

    delta_l = abs(l2 - l1)
    delta_j = abs(j2 - j1)

    return (
        delta_l == 1
        and delta_j <= 1
    )


def transition_frequency_ghz(
    atom,
    n1,
    l1,
    j1,
    n2,
    l2,
    j2,
):
    """
    Calculate transition frequency in GHz.

    ARC returns frequency in Hz.
    """

    frequency_hz = atom.getTransitionFrequency(
        n1,
        l1,
        j1,
        n2,
        l2,
        j2,
    )

    return abs(frequency_hz) / 1e9


def transition_wavelength_nm(
    atom,
    n1,
    l1,
    j1,
    n2,
    l2,
    j2,
):
    """
    Calculate transition wavelength in nm.

    ARC returns wavelength in meters.
    """

    wavelength_m = atom.getTransitionWavelength(
        n1,
        l1,
        j1,
        n2,
        l2,
        j2,
    )

    return abs(wavelength_m) * 1e9


# ============================================================
# RF transition search
# ============================================================

def get_rf_transitions(
    atom,
    n_min,
    n_max,
    rf_min_ghz,
    rf_max_ghz,
):
    """
    Search for Rydberg-Rydberg transitions in the requested
    RF frequency range.

    All included Rydberg states are considered.

    E1 selection rules are NOT used to remove transitions from
    the search. Instead, every transition is returned with an
    E1 Allowed flag so the user can filter the results later.

    We intentionally do NOT assume that n2 > n1.

    Duplicate transitions are removed by using each unordered
    pair of states only once.

    State 1 and State 2 describe the two members of the
    transition pair and do not imply energy ordering.
    """

    results = []

    rf_min_hz = rf_min_ghz * 1e9
    rf_max_hz = rf_max_ghz * 1e9

    # --------------------------------------------------------
    # Build complete list of states
    # --------------------------------------------------------

    states = []

    for n in range(n_min, n_max + 1):

        for l, j in RYDBERG_STATES:

            states.append(
                (n, l, j)
            )

    # --------------------------------------------------------
    # Search every unique pair
    # --------------------------------------------------------

    for i, state1 in enumerate(states):

        n1, l1, j1 = state1

        for state2 in states[i + 1:]:

            n2, l2, j2 = state2

            try:

                frequency_hz = atom.getTransitionFrequency(
                    n1,
                    l1,
                    j1,
                    n2,
                    l2,
                    j2,
                )

            except Exception:
                continue

            # ARC can return a signed frequency depending on
            # which state is supplied first.
            frequency_hz = abs(frequency_hz)

            if frequency_hz == 0:
                continue

            # ------------------------------------------------
            # Frequency filter
            # ------------------------------------------------

            if not (
                rf_min_hz
                <= frequency_hz
                <= rf_max_hz
            ):
                continue

            # ------------------------------------------------
            # Calculate RF wavelength
            # ------------------------------------------------

            wavelength_m = (
                299792458.0 / frequency_hz
            )

            # ------------------------------------------------
            # Selection rules
            # ------------------------------------------------

            e1_allowed = allowed_e1_transition(
                l1,
                j1,
                l2,
                j2,
            )

            results.append(
                {
                    "State 1": state_label(
                        n1,
                        l1,
                        j1,
                    ),

                    "State 2": state_label(
                        n2,
                        l2,
                        j2,
                    ),

                    "RF Frequency (GHz)": (
                        frequency_hz / 1e9
                    ),

                    "RF Wavelength (mm)": (
                        wavelength_m * 1e3
                    ),

                    "E1 Allowed": e1_allowed,

                    "n State 1": n1,
                    "l State 1": l1,
                    "j State 1": j1,

                    "n State 2": n2,
                    "l State 2": l2,
                    "j State 2": j2,
                }
            )

    # --------------------------------------------------------
    # Sort results by frequency
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x["RF Frequency (GHz)"]
    )

    return results


# ============================================================
# Optical ladder
# ============================================================

def get_optical_ladder(
    atom,
    species,
    rydberg_state,
):
    """
    Calculate the standard two-laser ladder:

        Ground → P3/2 → Rydberg

    Returns the probe and coupling wavelengths.
    """

    n, l, j = rydberg_state

    ground = GROUND_STATES[species]

    intermediate = INTERMEDIATE_STATES[species]

    # --------------------------------------------------------
    # Probe laser
    #
    # Ground -> P3/2
    # --------------------------------------------------------

    probe_wavelength_nm = transition_wavelength_nm(
        atom,
        *ground,
        *intermediate,
    )

    # --------------------------------------------------------
    # Coupling laser
    #
    # P3/2 -> Rydberg
    # --------------------------------------------------------

    coupling_wavelength_nm = transition_wavelength_nm(
        atom,
        *intermediate,
        n,
        l,
        j,
    )

    return {
        "probe_wavelength_nm": probe_wavelength_nm,

        "coupling_wavelength_nm": (
            coupling_wavelength_nm
        ),
    }


# ============================================================
# Sidebar
# ============================================================

st.sidebar.header("Search Parameters")


species = st.sidebar.selectbox(
    "Atom",
    list(ATOMS.keys()),
)


rf_min = st.sidebar.number_input(
    "Minimum RF frequency (GHz)",
    min_value=0.001,
    max_value=1000.0,
    value=17.6,
    step=0.1,
)


rf_max = st.sidebar.number_input(
    "Maximum RF frequency (GHz)",
    min_value=0.001,
    max_value=1000.0,
    value=20.0,
    step=0.1,
)


n_min = st.sidebar.number_input(
    "Minimum Rydberg n",
    min_value=5,
    max_value=100,
    value=20,
    step=1,
)


n_max = st.sidebar.number_input(
    "Maximum Rydberg n",
    min_value=5,
    max_value=100,
    value=50,
    step=1,
)


# ------------------------------------------------------------
# Transition filter
# ------------------------------------------------------------

transition_filter = st.sidebar.selectbox(
    "Transition filter",
    [
        "All transitions",
        "E1 allowed only",
        "E1 forbidden only",
    ],
)


search_button = st.sidebar.button(
    "Search",
    type="primary",
)


# ============================================================
# Input validation
# ============================================================

if rf_min >= rf_max:

    st.error(
        "The minimum RF frequency must be less than "
        "the maximum RF frequency."
    )

    st.stop()


if n_min >= n_max:

    st.error(
        "The minimum Rydberg n must be less than "
        "the maximum Rydberg n."
    )

    st.stop()


# ============================================================
# Search
# ============================================================

if search_button:

    with st.spinner(
        "Searching ARC for Rydberg transitions..."
    ):

        try:

            atom = ATOMS[species]()

            transitions = get_rf_transitions(
                atom,
                n_min,
                n_max,
                rf_min,
                rf_max,
            )

        except Exception as e:

            st.error(
                "ARC encountered an error while searching "
                "for transitions."
            )

            st.exception(e)

            st.stop()

    # Store results
    st.session_state["transitions"] = transitions

    st.session_state["species"] = species

    st.session_state["search_rf_min"] = rf_min

    st.session_state["search_rf_max"] = rf_max

    st.session_state["search_n_min"] = n_min

    st.session_state["search_n_max"] = n_max


# ============================================================
# Display search results
# ============================================================

if "transitions" in st.session_state:

    transitions = st.session_state["transitions"]

    species = st.session_state["species"]

    search_rf_min = st.session_state[
        "search_rf_min"
    ]

    search_rf_max = st.session_state[
        "search_rf_max"
    ]

    search_n_min = st.session_state[
        "search_n_min"
    ]

    search_n_max = st.session_state[
        "search_n_max"
    ]

    st.header(
        "Rydberg–Rydberg Transitions"
    )


    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not transitions:

        st.warning(
            "No Rydberg–Rydberg transitions were found "
            "in the selected frequency and n ranges."
        )

        st.write(
            f"""
            Search range:

            **{species}**

            **{search_rf_min:g}–{search_rf_max:g} GHz**

            **n = {search_n_min}–{search_n_max}**
            """
        )

        st.info(
            """
            Try increasing the n range or changing the RF
            frequency range.
            """
        )

        st.stop()


    # ========================================================
    # Apply transition filter
    # ========================================================

    if transition_filter == "All transitions":

        filtered_transitions = transitions

    elif transition_filter == "E1 allowed only":

        filtered_transitions = [
            t
            for t in transitions
            if t["E1 Allowed"]
        ]

    else:  # E1 forbidden only

        filtered_transitions = [
            t
            for t in transitions
            if not t["E1 Allowed"]
        ]


    # --------------------------------------------------------
    # Count transition types
    # --------------------------------------------------------

    e1_count = sum(
        t["E1 Allowed"]
        for t in transitions
    )

    non_e1_count = (
        len(transitions) - e1_count
    )


    st.write(
        f"""
        Found **{len(transitions)}** transitions in the
        requested RF and n ranges.

        **{e1_count}** satisfy the basic E1 selection rules
        and **{non_e1_count}** do not.
        """
    )


    st.write(
        f"Showing **{len(filtered_transitions)}** "
        f"transitions using the selected filter."
    )


    if not filtered_transitions:

        st.warning(
            "No transitions match the selected filter."
        )

        st.stop()


    # ========================================================
    # Convert results to DataFrame
    # ========================================================

    display_data = []

    for i, transition in enumerate(
        filtered_transitions
    ):

        display_data.append(
            {
                "ID": i,

                "State 1": (
                    transition["State 1"]
                ),

                "State 2": (
                    transition["State 2"]
                ),

                "RF Frequency (GHz)": round(
                    transition[
                        "RF Frequency (GHz)"
                    ],
                    6,
                ),

                "RF Wavelength (mm)": round(
                    transition[
                        "RF Wavelength (mm)"
                    ],
                    4,
                ),

                "E1 Selection Rule": (
                    "Allowed"
                    if transition["E1 Allowed"]
                    else "Forbidden"
                ),
            }
        )


    df = pd.DataFrame(
        display_data
    )


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )


    # ========================================================
    # Select transition
    # ========================================================

    st.header(
        "Optical Ladder"
    )


    transition_options = {}

    for i, transition in enumerate(
        filtered_transitions
    ):

        e1_label = (
            "E1"
            if transition["E1 Allowed"]
            else "non-E1"
        )

        label = (
            f"{transition['State 1']} ↔ "
            f"{transition['State 2']} "
            f"("
            f"{transition['RF Frequency (GHz)']:.6f}"
            f" GHz, {e1_label})"
        )

        transition_options[i] = label


    selected_id = st.selectbox(
        "Select an RF transition",
        options=list(
            transition_options.keys()
        ),
        format_func=lambda x:
            transition_options[x],
    )


    selected = filtered_transitions[
        selected_id
    ]


    # ========================================================
    # Selected RF transition
    # ========================================================

    st.subheader(
        "Selected RF Transition"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "State 1",
            selected["State 1"],
        )


    with col2:

        st.metric(
            "State 2",
            selected["State 2"],
        )


    with col3:

        st.metric(
            "RF Frequency",
            (
                f"{selected['RF Frequency (GHz)']:.6f}"
                " GHz"
            ),
        )


    with col4:

        st.metric(
            "E1 Selection Rule",
            (
                "Allowed"
                if selected["E1 Allowed"]
                else "Forbidden"
            ),
        )


    # ========================================================
    # Calculate optical ladder
    # ========================================================

    atom = ATOMS[species]()


    rydberg_state = (
        selected["n State 2"],
        selected["l State 2"],
        selected["j State 2"],
    )


    try:

        ladder = get_optical_ladder(
            atom,
            species,
            rydberg_state,
        )

    except Exception as e:

        st.error(
            "Could not calculate the optical ladder "
            "for the selected Rydberg state."
        )

        st.exception(e)

        st.stop()


    # ========================================================
    # Optical wavelengths
    # ========================================================

    st.subheader(
        "Required Optical Lasers"
    )


    ground_label = (
        GROUND_LABELS[species]
    )

    intermediate_label = (
        INTERMEDIATE_LABELS[species]
    )

    rydberg_label = (
        selected["State 2"]
    )


    ladder_data = pd.DataFrame(
        [
            {
                "Laser": "Probe",

                "Transition": (
                    f"{ground_label} → "
                    f"{intermediate_label}"
                ),

                "Wavelength (nm)": round(
                    ladder[
                        "probe_wavelength_nm"
                    ],
                    6,
                ),
            },

            {
                "Laser": "Coupling",

                "Transition": (
                    f"{intermediate_label} → "
                    f"{rydberg_label}"
                ),

                "Wavelength (nm)": round(
                    ladder[
                        "coupling_wavelength_nm"
                    ],
                    6,
                ),
            },
        ]
    )


    st.dataframe(
        ladder_data,
        use_container_width=True,
        hide_index=True,
    )


    # ========================================================
    # Ladder diagram
    # ========================================================

    st.subheader(
        "Ladder System"
    )


    st.markdown(
        f"""
        ### {ground_label}

        ↓ **Probe:** \
        {ladder["probe_wavelength_nm"]:.3f} nm

        ### {intermediate_label}

        ↓ **Coupling:** \
        {ladder["coupling_wavelength_nm"]:.3f} nm

        ### {rydberg_label}

        ↓ **RF:** \
        {selected["RF Frequency (GHz)"]:.6f} GHz

        ### {selected["State 1"]}
        """
    )


    # ========================================================
    # Export
    # ========================================================

    st.subheader(
        "Export"
    )


    csv = df.to_csv(
        index=False
    )


    st.download_button(
        label="Download displayed transitions as CSV",

        data=csv,

        file_name=(
            "rydberg_transitions.csv"
        ),

        mime="text/csv",
    )