#!/bin/env python3

"""
Interdigitated Capacitor Layout Generator for KiCad

This script generates the layout for an interdigitated capacitor based on user-defined parameters.
The generated layout is saved in a KiCad footprint file in the ./idc.pretty directory.

Parameters:
- modulename: The name of the module.
- trackWidth: Width of each track/finger in mm.
- gap: Gap between tracks/fingers in mm.
- totalWidth: Total width of the capacitor in mm.
- fingerLength: Length of each finger in mm. Overwrites the totalWidth parameter.
- numFingers: Number of fingers/tracks.
- layer: The PCB layer the capacitor is on.
- connectingTrackWidth: Width of the connecting horizontal tracks in mm (default: trackWidth).

Usage:
    python3 idcGen.py -h
    # For fixed total width:
    python3 idcGen.py --modulename <name> --trackWidth <width> --gap <gap> --totalWidth <totalWidth> --numFingers <numFingers>
    # For fixed finger length:
    python3 idcGen.py --modulename <name> --trackWidth <width> --gap <gap> --fingerLength <fingerLength> --numFingers <numFingers>
    
Example:
    python3 idcGen.py --modulename IDC --trackWidth 0.8 --gap 0.5 --fingerLength 15 --numFingers 10 --connectingTrackWidth 0.8

Output file path:
    ./idc.pretty/

(c) 2024 by Lionnus Kesting
"""

import os
import argparse
from datetime import datetime


def idcGen(trackWidth, gap, totalWidth, numFingers, fingerLength=None, modulename='IDC', layer='F.Cu', connectingTrackWidth=None):
    """
    Generates the layout for an interdigitated capacitor.

    Parameters:
    - modulename: The name of the module.
    - trackWidth: Width of each track/finger in mm.
    - gap: Gap between tracks/fingers in mm.
    - totalWidth: Total width of the capacitor in mm.
    - fingerLength: Length of each finger in mm. Overwrite the totalWidth parameter.
    - numFingers: Number of fingers/tracks.
    - layer: The PCB layer the capacitor is on.
    - connectingTrackWidth: Width of the connecting horizontal tracks in mm (default: trackWidth).

    Returns:
    - A tuple containing the generated module layout and the dimensions as a string.
    """
    if connectingTrackWidth is None:
        connectingTrackWidth = trackWidth

    dt = datetime.today()  # Get current date and time for timestamp
    seconds = int(dt.timestamp())

    # Calculate the total length and the finger length
    totalHeight = numFingers * (trackWidth + gap) - gap
    if fingerLength is None:
        fingerLength = totalWidth - connectingTrackWidth * 2 - gap
    else: 
        totalWidth = fingerLength + 2 * connectingTrackWidth + gap
    
    # Add info to the header
    mod = ""
    # Add module header
    mod += "(footprint %s (layer %s) (tedit %X)\n" % (modulename, layer, seconds)

    # Add connecting tracks as SMD pads
    mod += "  (pad 1 smd rect (at %f %f) (size %f %f) (layers F.Cu))\n" % (
        connectingTrackWidth/2, totalHeight/2, connectingTrackWidth, totalHeight)
    mod += "  (pad 2 smd rect (at %f %f) (size %f %f) (layers F.Cu))\n" % (
        totalWidth-connectingTrackWidth/2, totalHeight/2, connectingTrackWidth, totalHeight)
    
    # Add fingers as SMD pads
    for n in range(numFingers):
        posX = connectingTrackWidth + (n % 2) * gap
        posY = n * (trackWidth + gap)
        sizeX = fingerLength
        sizeY = trackWidth
        mod += "  (pad %X smd rect (at %f %f) (size %f %f) (layers F.Cu))\n" % (
            n%2 + 1, posX + sizeX / 2, posY + sizeY / 2, sizeX, sizeY)
    mod += ")\n"

    # Print terminal message with dimensions
    dimensions = f"Total Width: {totalWidth}mm, Total Height: {totalHeight}mm"
    print(f"Generated {modulename} with dimensions: {dimensions}")

    return mod, dimensions


def main():
    """Parse arguments and generate the capacitor layout."""
    parser = argparse.ArgumentParser(description="Generate an interdigitated capacitor KiCad layout.")
    parser.add_argument("-m", "--modulename", required=True, help="Module name for the generated capacitor.")
    parser.add_argument("-t", "--trackWidth", required=True, type=float, help="Width of each track/finger in mm.")
    parser.add_argument("-g", "--gap", required=True, type=float, help="Gap between tracks/fingers in mm.")
    parser.add_argument("-w", "--totalWidth", type=float, help="Total width of the capacitor in mm.")
    parser.add_argument("-f", "--fingerLength", type=float, help="Length of each finger in mm. Overwrites the totalWidth parameter.")
    parser.add_argument("-n", "--numFingers", required=True, type=int, help="Number of fingers/tracks.")
    parser.add_argument("-c", "--connectingTrackWidth", type=float, help="Width of the connecting tracks in mm (default: same as trackWidth).")

    args = parser.parse_args()

    # Validate input arguments for logical consistency
    if args.trackWidth <= 0:
        print("Error: Track width must be greater than 0.")
        return

    if args.gap <= 0:
        print("Error: Gap must be greater than 0.")
        return

    if args.numFingers < 2:
        print("Error: Number of fingers must be at least 2.")
        return

    if args.connectingTrackWidth is not None and args.connectingTrackWidth <= 0:
        print("Error: Connecting track width must be greater than 0.")
        return
    
    if args.totalWidth is None and args.fingerLength is None:
        print("Error: Either total width or finger length must be provided.")
        return
    
    if args.totalWidth is not None and args.totalWidth <= 0:
        print("Error: Total width must be greater than 0.")
        return
    
    if args.fingerLength is not None and args.fingerLength <= 0:
        print("Error: Finger length must be greater than 0.")
        return

    # Generate the capacitor layout
    cap, dimensions = idcGen(
        modulename=args.modulename,
        trackWidth=args.trackWidth,
        gap=args.gap,
        totalWidth=args.totalWidth,
        fingerLength=args.fingerLength,
        numFingers=args.numFingers,
        connectingTrackWidth=args.connectingTrackWidth
    )

    # Ensure the output directory exists
    output_dir = './idc.pretty'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct the output filename with parameters for traceability
    if args.fingerLength is not None:
        output_filename = f"{output_dir}/{args.modulename}_tw{args.trackWidth}_ctw{args.connectingTrackWidth}_g{args.gap}_fl{args.fingerLength}_n{args.numFingers}.kicad_mod"
    else:
        output_filename = f"{output_dir}/{args.modulename}_tw{args.trackWidth}_ctw{args.connectingTrackWidth}_g{args.gap}_w{args.totalWidth}_n{args.numFingers}.kicad_mod"
    
    with open(output_filename, 'w') as f:
        f.write("# ----------------------------------------------------\n")
        f.write("# Autogenerated by idcGen.py, written by Lionnus Kesting.\n")
        f.write("# Code available at: https://github.com/lionnus/idc_kicad.\n")
        f.write("# ----------------------------------------------------\n")
        f.write("# Date: %s\n" % datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        f.write("# Parameters: %s\n" % args)
        f.write(f"# {dimensions}\n")
        f.write("# ----------------------------------------------------\n")
        f.write(cap)

    print(f"Layout saved to {output_filename}")


if __name__ == "__main__":
    main()
