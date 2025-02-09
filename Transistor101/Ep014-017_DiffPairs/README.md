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

## Episode 16: Adding a gain stage to the long-tailed pair

In this episode, we improve on the long-tailed pair by adding a gain stage
to the output, and increase its current handling capability with a push-pull
follower.  Unfortunately, that introduces crossover distortion.

Video link [Adding a gain stage to the long-tailed pair](https://youtu.be/MVIBDuUNORs)

## Episode 17: Taming distortion with negative feedback

In this episode, we tame the distortion that the push-pull stage introduces
by applying negative feedback to our amplifier.  It works well for a gain-of-10
amplifier, but when we try a unity-gain follower, it oscillates!

Video link: (Taming distortion)[https://youtu.be/vlr6OmdUiCc]

## Episode 18: Gain compensation

In this episode, we stabilize the oscillation when we run our amplifier
at unity gain, by adding so-called "gain compensation".  We've succeeded in
reinventing the op-amp.  It's a bad one, but we can now look at the internal
schematic of a commercial op-amp and identify all the pieces.

Video link: (Gain compensation)[https://youtu.be/26Ml7Iz69W0]

## Files


| File name           | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `README.md`         | This file                                             |
| `LongTailedPair/`   | KiCAD files of the circuit demonstrated in episode 14  |
| `LongTailedPair.pdf` | Printable schematic for the demo circuit in episode 14 |
| `LongTailedPair2/`   | KiCAD files of the circuit demonstrated in episode 15  |
| `LongTailedPair2.pdf` | Printable schematic for the demo circuit in episode 15 |
| `LongTailedPair3/`   | KiCAD files of the circuit demonstrated in episode 16  |
| `LongTailedPair3.pdf` | Printable schematic for the demo circuit in episode 16 |
| `LongTailedPair4/`   | KiCAD files of the circuit demonstrated in episode 17  |
| `LongTailedPair4.pdf` | Printable schematic for the demo circuit in episode 17 |
| `LongTailedPair5/`   | KiCAD files of the circuit demonstrated in episode 18  |
| `LongTailedPair5.pdf` | Printable schematic for the demo circuit in episode 18 |

## NOTES

Any matched pair of NPN transistors should work in place of the DMMT5551
used here. MMDT2222A, DMMT3904W, MMDT4401, and PMP4201Y would all be
candidates if the pinouts in the schematic are adjusted appropriately.

2N4401 and 2N4403 can be substituted with most general-purpose NPN and PNP
transistors, respectively.  Appropriate pairs include PN2222A/2N2907,
2N3904/2N3906, 2N5551/2N5401, and BD547/BBD557 (or their surface-mount counterparts).
