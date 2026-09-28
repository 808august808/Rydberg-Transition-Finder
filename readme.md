# ⚛️ Rydberg Transition Finder

Interactive tool for exploring alkali Rydberg–Rydberg transitions and determining the corresponding optical ladder.

The application uses the [ARC (Alkali Rydberg Calculator)](https://arc-alkali-rydberg-calculator.readthedocs.io/) package for atomic-structure calculations.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rydberg-transition-finder.streamlit.app)

[▶ Launch Web App](https://rydberg-transition-finder.streamlit.app)

## Features

* Select **Rb-85, Rb-87, or Cs-133**
* Search for Rydberg–Rydberg transitions within a specified RF frequency range
* Specify a range of principal quantum numbers, `n`
* Calculate RF transition frequencies and wavelengths
* Assign a unique **transition ID** to each result for easy identification
* Check basic electric-dipole (E1) selection rules
* Filter transitions by E1 selection rule
* Calculate RF coupling quantities, including Rabi frequency and relative RF coupling strength
* Select an RF transition of interest
* Calculate the corresponding two-laser optical ladder
* Display probe and coupling wavelengths
* Export transition results as a CSV file

## Typical Workflow

For example, to investigate cesium transitions near 18–20 GHz:

1. Select **Cs-133** and set the RF range to **17.6–20.0 GHz**
2. Set the Rydberg-state range to **n = 20–50** and search
3. Review candidate transitions and their IDs
4. Select a transition from the table using the **transition selector**
5. Optionally enter an **RF electric-field strength** to calculate the Rabi frequency
6. View the optical ladder and RF coupling information

The table displays **relative coupling strength** regardless of whether an RF field strength is provided.

For Cs-133, the optical ladder is calculated as:

```text
6S1/2
  ↓ Probe
6P3/2
  ↓ Coupling
Rydberg state
  ↓ RF
Rydberg state
```

The application reports the wavelengths required for the probe and coupling lasers.

## Transition Search

The application searches combinations of supported Rydberg states within the user-defined principal quantum number and RF-frequency ranges.

Each transition is assigned a unique **ID** within the displayed search results. The ID provides an easy way to identify and select a particular transition.

The application considers each pair of states only once, so the same transition is not displayed multiple times simply because the order of the two states is reversed.

## RF Coupling Information

For a selected transition, the application provides information describing the coupling between the RF field and the Rydberg states.

This includes quantities such as:

* RF transition frequency
* RF wavelength
* RF transition dipole matrix element
* Relative RF coupling strength
* Rabi frequency, when an RF electric-field strength is provided

The **relative coupling strength** allows transitions to be compared without specifying an RF field amplitude. The calculated Rabi frequency additionally depends on the applied RF electric-field amplitude and the calculated atomic transition properties.

These quantities are intended to assist with evaluating candidate transitions for RF/Rydberg-atom experiments. They should not be interpreted as direct measurements of an experimental RF field.

## Electric-Dipole Selection Rules

The displayed **E1 Allowed** classification uses basic electric-dipole selection rules:

* Δl = ±1
* Δj = 0, ±1

This is a basic selection-rule check. Hyperfine structure, magnetic-sublevel selection rules, polarization, transition strengths, and other experimental considerations are not included in this classification.

A transition being classified as E1 allowed does not by itself indicate that it will be experimentally strong or easy to observe.

## Optical Ladder

The optical ladder calculation currently assumes a standard two-photon ladder configuration through the P3/2 intermediate state:

```text
Ground → P3/2 → Rydberg
```

For Cs-133, this corresponds to:

```text
6S1/2 → 6P3/2 → Rydberg state
```

The application calculates the corresponding probe and coupling wavelengths for the selected Rydberg states.

## Supported Rydberg States

The RF transition search considers the following orbital states:

* S1/2
* P1/2
* P3/2
* D3/2
* D5/2
* F5/2
* F7/2

The application does not assume that the upper state has a larger principal quantum number than the lower state. Each unordered pair of states is considered once, avoiding duplicate transitions.

## Installation

### Requirements

* Python 3.10 or newer
* pip

### 1. Clone the repository

```bash
git clone https://github.com/808august808/Rydberg-Transition-Finder.git
cd Rydberg-Transition-Finder
```

### 2. Create a virtual environment

On Windows:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the application

```powershell
streamlit run app.py
```

The application should open automatically in your browser.

If it does not, open:

```text
http://localhost:8501
```

## Scientific Notes

The application uses ARC to calculate atomic energies and transition properties for the selected alkali atom.

The RF transition frequency is determined from the calculated energy difference between the two Rydberg states.

The optical wavelengths are similarly calculated from the relevant energy differences in the assumed optical ladder.

The RF coupling and Rabi-frequency calculations are based on the atomic transition properties provided by the underlying atomic model and the RF electric-field parameters used by the application.

## Limitations

This tool is intended for exploring candidate transitions and assisting with experimental planning. The calculated quantities should be treated as theoretical predictions from the underlying atomic model rather than experimental measurements.

The application does not currently model several effects that can be important in an experimental Rydberg-atom system, including:

* Hyperfine structure
* Zeeman shifts
* AC Stark shifts
* Doppler effects
* Laser linewidth and frequency noise
* Magnetic-sublevel populations
* Polarization-dependent transition strengths
* Experimental beam geometry
* RF standing-wave or spatial-field effects
* Detailed vapor-cell effects

The E1 classification is therefore only a basic selection-rule check and should not be considered a complete prediction of experimental transition strength.

The calculated RF Rabi frequency and coupling quantities also depend on the assumed RF electric-field amplitude and atomic model. Experimental field calibration and geometry are not independently determined by the application.

## Output

The transition table can be exported as a CSV file for further analysis.

A transition can be selected from the table using its **transition ID** and the transition selector to view its associated optical ladder and RF information.

## Development

This project is intended as a research and educational tool for exploring Rydberg-atom transitions and assisting with experimental planning.

Generative AI tools, including OpenAI's ChatGPT, were used during development for programming assistance, debugging, documentation, and code review. The author reviewed and evaluated the resulting code and scientific calculations.

Contributions, corrections, and suggestions are welcome.

## License

See the `LICENSE` file for licensing information.
