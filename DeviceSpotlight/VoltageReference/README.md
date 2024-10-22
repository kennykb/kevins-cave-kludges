# Bandgap Voltage References

A viewer asked why I don't stock Zener diodes routinely.

I was going to do a quick five-minute reply, but it turned into a deep dive into the workings of IC bandgap voltage references, leading up to building a 7.5 volt low-current supply that achieves 0.1% accuracy over 0-20 mA loads.

The resulting video is [here](https://youtu.be/WHERE).

Schematic is `voltref.pdf`. KiCAD model is available in the `kicad/` subfolder.

The TL431BCLPR part I used has its data sheet [here](https://www.ti.com/lit/ds/symlink/tl431.pdf).
The TI app node on setting the voltage of the reference is [here](https://www.ti.com/lit/an/slva445/slva445.pdf).




