# Transistors 101, episode 9
## The quest for gain, part 2: Voltage gain

## Files

| File name           | Description                                       |
| ------------------- | ------------------------------------------------- |
| `README.md`         | This file                                         |
| `MoreVGain/`        | KiCAD files for the breadboarded circuits         |
| `MoreVGain.pdf`     | Printable schematics of the breadboarded circuits |

## Notes

The video presents a series of botched attempts to extract the
greatest possible voltage gain from a single-stage transistor
amplifier. It explores why you can't just put in a tiny emitter
resistor, because of unstable biasing. It fixes the DC bias point,
by bypassing the emitter resistor, and demonstrates the distortion
that you get at higher gains.

There are no CircuitJS simulations this time. We're dealing with
real-world components with real-world tolerances, temperature 
sensitivity, nonlinear behaviour -- things a circuit simulator
usually doesn't model (at least without a lot of extra work).
We went straight to the breadboard.

## Video link

[Ep009: The Quest for Voltage Gain](https://youtu.be/oWepMBOTbpU)
