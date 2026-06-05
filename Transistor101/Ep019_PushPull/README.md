# Transistors 101

Please join me in supporting [World Central Kitchen](https://donate.wck.org/team/806315)

## Episode 19: BJT Power Amps 1: Amplifier Classes and Why Push-Pull

Video link (https://youtu.be/1MtjPw3F_sk)

In this episode, we start on a journey to explore building power
amplifiers using BJT's.  This episode is an introduction, introducing
amplifier classes and exploring why practical power amps are almost
all push-pull amps in class AB.

## CircuitJS models demonstrated in the videos

```CircuitJS/AmpClasses.cjs```

Demonstration of the amplifier classes. The first amp can be biased
into Class A, AB, B or C by adjusting the 'Bias Voltage' slider; the
second demonstrates Class D.

```CircuitJS/feedforward.cjs```

Simple 2-transistor emitter follower, with a feed-forward resistor
used to mitigate crossover distortion.  The feed-forward resistor can
be removed to show crossover distortion that stems from the op-amp's
limited slew rate.

```CircuitJS/feedforward2.cjs```

Even with negative feedback, a small op-amp cannot drive the
feed-forward configuration into a low-impedance load.

 1. Cannot drive enough current through feed-forward resistor.
 
 2. Cannot source enough base current to the power transistors.

```CircuitJS/just-2-transistors.cjs```

Simplest possible push-pull follower exhibits unacceptable crossover
distortion.


## KiCAD schematics for breadboarded circuits

```PushPull/PushPull.cjs```

Master container with links to the individual schematics.  See notes
in the individual drawings for construction and demonstration notes.








