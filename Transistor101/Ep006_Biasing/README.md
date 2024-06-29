# Transistors 101 episode 6: Biasing and Bootstrapping

## Files

| File name                   | Description                                    |
| --------------------------- | ---------------------------------------------- |
| `README.md`                 | This file                                      |
| follower-biasing.ods        | Spreadsheet for emitter follower calculations  |
| follower-bad-bias.cjs       | CircuitJS model with less-than-ideal biasing   |
| follower-better-bias.cjs    | CircuitJS model with biasing improved          |
| follower-bootstrap.cjs      | CircuitJS model of boostrapped follower        |

## Notes

The video presents three emitter follower circuits and compares their
biasing.

The first follower has the quiescent voltage computed lazily as the
halfway point between the power rails.  It can be seen as a
as a [CircuitJS model](https://tinyurl.com/2khpdd8o).  ([Alternative link](https://www.falstad.com/circuit/circuitjs.html?ctz=CQAgjCAMB0l3BWcAOaAmA7MgnGB-kA2MAFgwTRA0JCRIGZaBTAWjDACgAlcGsQyCBaESvQYIhpBjcVGgJuINGlH1Ky0fyjaSEyrJgKATrzEhsfAdrDxIHAMbnLE6mfGxbEFgmjYshEWxlIlIMUWFoQg4TDRA1JRU3BNtohM0gtLj6GkFMFIBzTPpsooptOwB3TLAM2P5xDgAXOOR0ygZKGv1wIVQBRDJsBAxIQmxsIRhybIRsBnoEEgpsifGQABMmADMAQwBXABtGjir6SDbqjLsABzjz8Ayz0UxKGSgOW6160xVpcpPwK5vnUrJUWhcng99ACOkpIMgQLC0AgcjD4mBXLD4nYeFj2uicjo9OU5MZEfFkTQsSU9PAOIVqVT4gtumCkSjaGgEZT3rcRs8Ofy4lI4v9HBRuRyRLkOe5bMpaNAsOdivCSGBkMgagioiZpUopbosoSyHB6SB9cUaJayg0qkKefqeTdOZKaBLhX8GgB7cAQETaAAeWvYlCQMAgEh6dl9IoDgmD7DAYbkkZ6kY49ARggAYmnBEg2CAAGreo4AZwAFAAFADWAEpM9mQHnRSKpHAhBAc0YmABHPZMAB29gAnhwgA).)

The second follower has the quiescent point chosen better to avoid
clipping of the waveform.  It was calculated using the spreadsheet in
the list above. Its simulation can be seen using a [CircuitJS model](https://tinyurl.com/2qy4yz42). ([Alternative link](https://www.falstad.com/circuit/circuitjs.html?ctz=CQAgjCAMB0l3BWECAstIIEwDZsHZNJ8MAOEPbZEFAZmQFMBaMMAKACVxKxtIRHsKLnz4RCIOiKjQEHEJkxCameYq5QNKUSqkxZAJ3U8+ATm68NYeJFYBjEGeHgKTkengL+eGYMgnINDTYmDQmCHgQAtBshgpKKnGuIMHwrLFqYCYJaoGUojTWrADmqkpBpRJYGjYA7hWZ2ULGUKwALhIkTVnUyuDdovyY0CgEKCzYZiQTgWCS0NgNCJAKJiQEPCRIJiYgACb0AGYAhgCuADatrHUFXY19OqwADhKQty9CmAQS1U9GFjzyLTfERXZzmPiJZq1DpvG73Fp1WgJSBkJHyBB5UFosAuNG9GycPEqbF5TTaarSAw9BIY6kScp8WhwYp03KsqogxG9TC0rBkHmY554V7oyjC+J8SQtex80XJIEC6ruZYqbDQPAkT4YkxjWa0coIGRpeUQ2m+emkkbMkrmtm2jkI8gixXmxU2Z6yxWy5SSn4Ae3AEEEGgAHiQWGAVEgYBABrHWAHxMG+GGI1HpLHwFmbDQyHwAGKZvhIZggABqfouAGcABQABQA1gBKVi5jSF77iQhwfgQfP6egARxO9AAdrYAJ6sIA).)

The third follower has its input impedance greatly raised by using a bootstrap capacitor.  Its component values were also calculated in the spreadsheet. It can also be simulated with a [CircuitJS model](https://tinyurl.com/2h2w8n5y) ([Alternative link](https://www.falstad.com/circuit/circuitjs.html?ctz=CQAgjCAMB0l3BWEBOAbNA7FhBmVCEAOAFlQ1VRDJCWJxoFMBaMMAKACVxKxjiQmqfr36RwIAExj6Y2dASdwyCSBwqwy7lG3ExYFbKjy2AJy0iUPPtrDxIbAMaXw1sOReijdyBJVMM0HzKGrzIhAjEGDj0TISYpkrqEoSJkrra0fAJGioS6TmqeNqohFkA5qnRPJo4CAZQbAAuqiQeIHTq1noCONAaGGAUBBIIg7gy0KhukMSE0WgYkBizyCirACYMAGYAhgCuADaNbADuqjNtUikW9gAO5q6UvvwyDWc4rRY4Fzen7WppMQdSQISj2M7A0r-FQA+xcYEA4GDbRAvT1OQKMzAkaUBFFIHfewVPG4gG1dF-bGgmjJEFgtj3Rb8HEgJmqKSqFGOGkpFlCMQsuR2XxUSY+QakNDEZKLehxdhmfl0qjpKo6RZElXSIpK8lcs5svnpQUMnnKuopNTSfXQ7gE3LpexObGqi55AVeOyRARgPr6HC8VA4UgSfBCAywSDsM5XNpuKyiSkAqFI2ngyrqTT6FLpgru87Mx0Jb7CawlwHaXxZAD2KBV2gAHoRWPoaEYIN0DGxa2562Imy2VEgYB3xF2PtoAGKjsRIFggABq1aOAGcABQABQA1gBKNgTsTTzkcqRwH0gScmBgARz2DAAdg4AJ5sIA).) This follower is the one that was actually breadboarded and tested in the video.

If for whatever reason, [Paul Falstad's server](https://falstad.com/circuit/) is unavailable, Iain Sharp provides an [alternative site](https://lushprojects.com/circuitjs/).  As a last resort, this repository provides the models in text form, and the source code for the simulator is available via a [GitHub project](https://github.com/pfalstad/circuitjs1).



## Video link

[Ep006: Biasing and Bootstrapping](https://youtu.be/TujF9No88jw)

