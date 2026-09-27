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
* Check basic electric-dipole (E1) selection rules
* Filter transitions by E1 selection rule
* Select an RF transition of interest
* Calculate the corresponding two-laser optical ladder
* Display probe and coupling wavelengths
* Export transition results as a CSV file

## Typical Workflow

For example, to investigate cesium transitions near 18–20 GHz:

1. Select **Cs-133**
2. Set the RF frequency range to **17.6–20.0 GHz**
3. Set the Rydberg-state range to **n = 20–50**
4. Search for transitions
5. Select a candidate Rydberg transition
6. View the corresponding optical ladder

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

The application uses ARC to calculate atomic transition frequencies and wavelengths.

The RF transition search considers the following Rydberg states:

* S1/2
* P1/2
* P3/2
* D3/2
* D5/2
* F5/2
* F7/2

The application does not assume that the upper state has a larger principal quantum number than the lower state. Each unordered pair of states is considered once, avoiding duplicate transitions.

The displayed **E1 Allowed** classification uses the basic electric-dipole selection rules:

* Δl = ±1
* Δj = 0, ±1

This is a basic selection-rule check. Hyperfine structure, magnetic-sublevel selection rules, polarization, transition strengths, and other experimental considerations are not included in this classification.

## Limitations

This tool is intended for exploring candidate transitions and assisting with experimental planning. The calculated transitions should be treated as theoretical predictions from the underlying atomic model rather than experimental measurements.

The optical ladder calculation currently assumes a standard ladder configuration through the P3/2 intermediate state:

```text
Ground → P3/2 → Rydberg
```

Additional effects such as hyperfine structure, Zeeman shifts, AC Stark shifts, Doppler effects, laser linewidth, and experimental geometry are not currently modeled.

## Output

The transition table can be exported as a CSV file for further analysis.

## AI-Assisted Development

Generative AI tools, including OpenAI's ChatGPT, were used during development for programming assistance, debugging, documentation, and code review. The author reviewed and evaluated the resulting code and scientific calculations.

## Development

This project is intended as a research and educational tool for exploring Rydberg-atom transitions and assisting with experimental planning.

Contributions, corrections, and suggestions are welcome.

## License

See the `LICENSE` file for licensing information.
