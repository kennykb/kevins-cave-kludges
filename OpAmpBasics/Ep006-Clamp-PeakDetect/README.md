# Op-Amp Basics
## Episode 6-7: Three Circuits, One Idea

Video link: [Three circuits, one idea](https://youtu.be/vFuQ36QZQWc)
Video link: [Peak detector torture tester](/storage/kennykb/Videos/OpAmpBasics/Ep06-Rect-Clamp-PeakDet/)
Video link: [Reducing peak detector leakage current](https://youtu.be/QEqsVSCnKNI)
_Please join me in supporting the 'Get Fed Up!' campaign at Save the Children._ [Donate here](http://support.savethechildren.org/goto/KevinsCave)

In episode 6, we take a second look at the precision half-wave rectifier,
elaborate it to voltage clamps and peak detectors, study the effect of
slew rate some more, and discover the phenomenon of voltage droop.

There's a bonus episode where I show the design for the test circuit
used to put the peak detector through its paces.

In episode 7, we tackle the problem of reducing the voltage droop
in the peak detector, and learn many lessons about reducing leakage
cuirrent in high-impedance circuits.  We introduce the op-amp data sheet
parameter of input bias current.

All the schematics of the demo circuits this time fit on a single page,
so they're all bundled together.  There's a second page with the test
rig for the peak detector

| File name           | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `README.md`         | This file                                             |
| `demos/`            | Directory containing KiCAD model with schematics |
| `demos.pdf`         | Printable schematics for the demo circuits |
| `peak_det_tester/`  | Directory containing KiCAD model for test rig |
| `peak_det_tester.pdf` | Printable schematic for the test rig |
