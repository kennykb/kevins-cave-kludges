Transconductance Amplifiers, part 4: High-Current Bidirectional Voltage-Controlled Current Source

Please help me support [World Central Kitchen](https://donate.wck.org/team/806315)!

Video link: [Transconductance Amplifiers, part 4](https://youtu.be/2AUP0A4dkHc)

In this video, we look at improvements to the Howland current source, originally suggested by the analog legend Bob Widlar.
By the end of it, we've built a bidirectional voltage-controlled current source that can drive ±1.2 A, into any load from a short circuit up to a roughly ±10 V compliance limit.

This folder contains KiCAD schematics (and PDF plots of them) for several stages of the test circuit:

`Transconductance4-Widlar-1` - Schematics for the initial test circuit with an INA143 difference amp as the current source.

`Transconductance4-Widlar-2` - Adding a feedback buffer so that the circuit can remain accurate for tiny currents.

`Transconductance4-Widlar-3` - Adding a commercial unity-gain amp to boost the output current (we demonstrate ±60 mA, ±150 mA is possible with better thermal management).

`Transconductance4-Widlar-4` - Adding a pair of power transistors to boost the output current still further. We demonstrate ±1.2 A. At least ±3 A is possible with the same components with better thermal management.
