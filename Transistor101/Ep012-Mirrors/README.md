# Transistors 101
## Episode 12: They Do It with Mirrors

The video discusses a simple current mirror,
a circuit that regulates its output terminal
to carry the same current as its input terminal.

Video link: [They Do It with Mirrors](https://youtu.be/amhCj044Vio)

CircuitJS link: [Mirror simulation](https://www.falstad.com/circuit/circuitjs.html?ctz=CQAgjCAMB0l3BWcMBMcUHYMGZIA4UA2ATmIxEMJCQUmoFMBaMMAKGhAGUBPAW1-oAXAE4BLAMYB1UQBsAzgHsAdgFlRw4QuFQQ2ECl0gAkgoCug6vvDGADiAAsOiADUAOnb0Q6AFWEBDJTlROUEtAFEZXlc5MGiUaOxXYV8AoJDwyOjYmISklMDg0OEIqLl7aPK5eOT-AvTizLLohCyoV2jmdrlILp6suC6AE3oAMz9TGUFovrlO6d6usAHo4bGJqe6uuc35-pnV8cnd2djjmaX90cPBVnsl8AQ0ahQ8B8fqe0cIHn4hMSlZIpVOpNNoeidprBEGAUGBiHcEAgwPZiNgEMR4rMYAgsCwMAhCJB7NhPnh4XsVld1m0IZssdAcRg8QSiST7GTKhdKWtJjTOnTGNiMIQ8IS4UiiKQEJyBnIDtTwfywAhoNhCSzCNg4ZQYR0hTgMChsGSXrDPhgKXKqZNWAAlB54RzsujKx0ObAGOh0ewuz06bGsPzIH0gPBwcBgNWh8PEB4gZhIC7wL3QFGkE1EbBZ5Ek8gwNOkQtFovIZOsADuwboeDAVAurxrVEgrDAGEcZKo+IMxBhodr1iTKaQRiUNnMIAAwqYNPQlDdKz2DBg3UsQ8vHM3tB2QIbq8QqIQCU5B3bQ-uKEft4TXl6HL7-VAGRWz52ntuu1Bn9vGy-Q+zPwA5r+joNueeBhv6z71n2dZwK8i6fpW0EISwboIc2Fioe24Ywv+Ya3hAjDENAwo1sSar2IQxJGnmDJYNgWD2OiuAkKKsF0PKNraLh8GEuAKD-ksAlOPArBATxyDCRJSxHl6UECa8678f+u6IRGbr4RGUaac2SFgGhvYSeh8l4f2Rm9rpym8b6-7GXYyGGXBkmOHocniU5QlfB5kCyZ+3GEP2Sm1v2IEiS2hrgAFVDbsFVD7re5CMPYDIGPczB+tiIAADIKH4gwgM4CiTH4AH0FBUU7k8sU7m6lnVaF9Xns2DEuhV6KpRVqleJ+LXgExVDtX1R5dZBSGIgYg3Ikeg11f1lU2YpTzNgARjB1B8ZGsJaXmrAAB7IL2hKpUarzqg4+iOAA8jYjB+LwNjRFOM5ztEnCiEoADWe2RfgDhkOA+LkLQ3oXZO07CLOGxqBoWhQQgbrOg6TpNewIDSPIyjQ6CAByAAK2M6HoBh6CY479n6Rj2RuOjOIw4CvBAEDY-kaRFCUWScpyLTCMztSsxkpTIlkhBZBaPMs4UAui1kLQxHgSS86kksNILFoxGr+ltFkCzHFy3LXLrOs7DEyxWjyGznEb5ym5xFuLFbiw29aNx3HQJ3tuTxqODgdZo4CmMgloeME+C2TgvqqHMsQopookJvgrbNLZIwKAoKqTGQBi+mQGq2Yi90dHCrgWrIjnPZ4BrsqJ6HepQj5MJwsaPkvGyjyQoyDHSgQxCQAFKCopa1fa3S+qd+y-e9zCA-x-r6yngJeHngv8GfA+IbpQ+AaVsvoYQTv26WQJgVukfnbvIfiNKQpdAfs2oj6Lg3vvEaIo7ufj7wAgz4v4pz93Gfnpv6PzfgYVOEVb7f0wEuZ+UD5qfntGApcTxEEUAireEMFl-RPm3pfZ+EoQE9QwG7fBH4UA4gAdYOS29yEEKIL9CB29rwUGEnQ06slWDaFYReKgXDVIulEow+hyCmEQIQUwwgLCmE0PQfeW8AZ7KdSqoaRadBXKAQBi8OBrZNG30-EAA) [Tiny URL](https://tinyurl.com/2643fer7)

## Episode 13: More Current Mirrors

The follow-on video explores more current mirrors, starting with
stabilizing the mirror with emitter resistors, and moving on to
exploring the Widlar asymmetric mirror, the basic 3-transistor
Wilson mirror, and the symmetric Wilson mirror.

Video link: [https://youtu.be/IXL2RSe3bcI]

| File name           | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `README.md`         | This file                                             |
| `kevin-parts/`      | Directory of part models needed in KiCAD model        |
| `mirror-sim.cjs`    | CircuitJS model for the mirror simulation             |
| `mirror-tester/`    | Directory containing KiCAD model for the test circuit |
| `mirror-tester.pdf` | Printable schematic for the test circuit              |

There was no oscilloscope or function generator software for this episode.
I saved the scope traces to a USB stick and did all the analysis in a
spreadsheet.

You'll have to tweak the KiCAD files to use the footprints and
schematic symbols that appear in the `kevin-parts` directory.
I haven't found a good way to share KiCAD models that contain
parts that don't come out of the box with KiCAD.
