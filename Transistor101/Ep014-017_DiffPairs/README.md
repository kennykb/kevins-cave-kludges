# Transistors 101
## Episode 14: Differential Pairs: The Heart of Analog Circuits

Video link: [The Differential Pair](https://youtu.be/z4kL78zurwU)

The video discusses the long-tailed pair, the basic circuit that
forms the input of virtually all op-amps and other analog devices.

Video link: [The Differential Pair](https://youtu.be/amhCj044Vio)

## Episode 15: Improving the long-tailed pair

Video link: (Improving the Long-Tailed Pair)[https://youtu.be/MG1PXJ36-GA)

In this second video on differential amplifiers, we improve the basic long-tailed pair, by using a current source instead of a resistor to supply the  tail current.
We also explore the possibility of squeezing out more gain from the amilifier by eliminating the emitter resistors, and discover that, unlike with the common-emitter amplifier, leaving them out doesn't lead to thermal instability.


| File name           | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `README.md`         | This file                                             |
| `LongTailedPair/`   | KiCAD files of the circuit demonstrated in episode 14  |
| `LongTailedPair.pdf` | Printable schematic for the demo circuit in episode 14 |

Any matched pair of NPN transistors should work in place of the DMMT5551
used here. MMDT2222A, DMMT3904W, MMDT4401, and PMP4201Y would all be
candidates if the pinouts in the schematic are adjusted appropriately.
