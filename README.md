# Interdigitated Capacitor Layout Generator for KiCad

This Python script automates the generation of interdigitated capacitor (IDC) layouts for use in KiCad PCB designs. It allows for quick and customizable creation of capacitor layouts based on user-defined dimensions and parameters.

#### Parameters:
The IDC can be generated from the following parameters, also seen in the figure below.

- `-m`, `--modulename`: Name of the generated capacitor module.
- `-t`, `--trackWidth`: Width of each track/finger in mm.
- `-g`, `--gap`: Gap between tracks/fingers in mm.
- `-w`, `--totalWidth`: Total width of the capacitor in mm.
- `-n`, `--numFingers`: Number of fingers/tracks.
- `-c`, `--connectingTrackWidth`: Width of the connecting horizontal tracks in mm (optional).

<img src="docs/parameter_overview.png" alt="IDC Dimensions" title="Interdigitated Capacitor Dimensions" width="80%"/>


## Getting Started

To use this script, you'll need Python 3 installed on your machine. Clone or download this repository to your local machine to get started.

### Prerequisites

- Python 3.x
- KiCad (for importing the generated `.kicad_mod` file)

### Usage

Run the script from the command line with the required parameters. Here is an example command:

```bash
python3 idcGen.py --modulename idc --trackWidth 0.8 --gap 0.5 --totalWidth 15 --numFingers 40 --connectingTrackWidth 0.8
```

## Understanding the `.kicad_mod` File Format

The generated file is in KiCad's module format (`.kicad_mod`). For more information on this format, visit the [KiCad S-expression file format documentation](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html).

## Reference

This generator was inspired by the paper [Fringing Field Capacitive Smart Sensor Based on PCB Technology for Measuring Water Content in Paper Pulp](https://doi.org/10.1155/2020/3905804).

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.
```
