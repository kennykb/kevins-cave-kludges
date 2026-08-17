# Transistors 101

## Episode 21: How Not to Measure Speaker Impedance

[Video link](TBD)

Please help us provide 250 insecticidal nets to prevent malaria! https://www.againstmalaria.com/KevinsCave

In this episode, we explore how to measure the AC impedance of a loudspeaker, as a precursor to designing a power amp to drive it.

This episode was intended as a quick side note to an episode discussing how to drive reactive loads with a class-AB amolifier. It ballooned into an entire side project, because of Kevin's abject incompetence. It's posted as a lessom in improving a bad design to the point where it's usable. Hopefully, you'll be entertained by watching Kevin make and correct several mistakes.

The first attempt to measure speaker impedance has a KiCAD model that cam
be found in the ```SpeakerTestRig``` folder.  (A print of the schematic
is in ```SpeakerTestRig.pdf```.  It failed, because the
circuit as designed demanded an impossible slew rate from the op-amp
and could not keep up at high audio frequencies.

The ```SpeakerTestRigAgain``` folder (and ```SpeakerTestRig.pdf``)
contains an attempt to fix this problem,
using the amplifier built in the previous episode as a driver.  While
the driver output now remains tolerably in phase with the input, the
current monitor drifts out of phase because of the delayed response
of the instrumentation amp.

The ```SpeakerTestRigYetAgain``` folder (and ```SpeakerTestRigYetAgain.pdf```)
are "third time's the charm." They add a second instrumentation amp so that
the delays in monitoring output voltage and output current are equal,
mitigating the phase shift.

```speaker_measurement.py``` is the software used to collect the data
in all the runs.
