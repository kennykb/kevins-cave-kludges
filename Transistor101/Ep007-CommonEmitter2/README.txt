# Transistors 101 episode 6: Biasing and Bootstrapping

## Files

| File name                   | Description                                    |
| --------------------------- | ---------------------------------------------- |
| `README.md`                 | This file                                      |
| ce-amp-biasing.ods          | Spreadsheet for common-emitter amplifier       |
| ce-amp.cjs                  | CircuitJS model for common emitter amp         |
| ce-amp-bootstrap.cjs        | CircuitJS model for boosttrapped CE amp        |

## Notes

The video presents biasing, input, and output impedance of transistor
current sources and common emitter amplifiers.

Two followers are simulated here.  The first has a simple voltage
divider as the bias network. It can be seen as a [CircuitJS model](https://tinyurl.com/2b3dbatn) ([Alternative link](https://www.falstad.com/circuit/circuitjs.html?ctz=CQAgjCAMB0l3BWEAmAzNALAdkggnMmAGxFYKSpIkhLk0CmAtGGAFAAuIAHMdxl3wFd+UcCEYZoCLsmQIiqIhlRYwWZVCldU-YTmIyy4OCAAm9AGYBDAK4AbdqwDugkHjDJXeDBiisATl4+rmBwApDGcKwA5iFhcRgRSc6u2p7CQiaQAakmGSBYiqKh8KwASq6FRK5EXOGiieCeSZoIKflcSl4efgDGuRHevlxZmvBwEESYnZAYeHgIGGhyYFRSGG2BQ9wm252+ESWlsXtdeyOi2S481flYyBH52YFKjyKvBUWH49kVH1UgD61eoRRo9FowTaAxruTwfEr1FjHaHfSACeGzCEpe5vdGNJ6sfpENFuHqLXywy6wcbzWl0+nzcDQMCoWQ8dTCWmkPBMsAbHLk0mefiDcE0K4gEVCyUiSm-GUCSmJUXNMSNGAQCFSFJ7EyhfFZVgABwV0p8ioIIFQl2NxgN33xF2tyUS1owvARNCw1RYD1EsgA+koA5AA4k8FwQ8z5HIo2AA8wA2xXW5vW5gr7vvJ-aggxgQ2HKPmEHGE-G2C5iYqeh85SkPvla+DWEA).)

The second has a bootstrapped divider to improve its input impedance. This is the circuit actually built and tested in the video.  It can be seen as a [CircuitJS model](https://tinyurl.com/2aw2mrqd) ([Alternative link](https://www.falstad.com/circuit/circuitjs.html?ctz=CQAgjCAMB0l3BWcZYA4BsB2ATNzZsEBOVA9EdcpBSEBAUwFowwAoAFxFPNQBZUu-QQNoRGCaLwDMkTAgRhMkXuiKY5UaAkxrUkLLilgMLcHBAATegDMAhgFcANu1YB3YSCIEPRXryisAE4+fh5gcCJmcKwA5mER8by0yW4eqFLYaeaQQVm0fAKYUuSi8DkASh5FPELoqJG0SeCZyZoIqQVc6P6dXi2sAMY+3ji0fVCaZbggjDDoylJyimC8RF6qSHODeZ6heq0wZZAQ6JJEGdiQMpSoXsoUWrztwb495q9d-qVlsbs93X8uHoJjl3NwqpcPDlgqMIWNvLQFNF3LDxt14f13OjPN5seDoRQmuDsdUJkjopUScVCbQ6g0QE0ESCtLlsWjGQlEfMcnFseFIAI+coDqlYZ15gJOjkhhKPAg9kJkrAyhAUAQZLwwAoitg6pASOBoCtnnQFQJ+PlFVFQQzgZ0-JLFaxKg6PElLZEIE0YBADiz3B99mYidlWAAHBlCe1CIjYARSEHh4P5czhInAhMpJIJzXkD7acjhBAlEC6gD63TLkDLSRIVaNxcI9bAZeYZbY2c8mDzoRYkKLJbwFd4VZrUnl7egTZ9rZbbCAA).)

## Video link

[Ep007: Biasing the Common-Emitter Amplifier ](https://youtu.be/d0mj0i1vkSg)



