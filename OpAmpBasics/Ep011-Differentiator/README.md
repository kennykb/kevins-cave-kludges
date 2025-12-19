# The Op-Amp Differentiator
## Op-Amp Basics, episode 11

Video link: [The Op-Amp Differentiator](https://youtu.be/uv7WyswjEHg)

Please help me in supporting [Médecins Sans Frontières | Doctors without Borders](https://events.doctorswithoutborders.org/campaign/Kevins-Cave)

In this episode, we turn the op-amp integrator on its head and make an op-amp differentiator. We explore the limits of op-amp differentiation, and discover that the most basic differentiator turns into an oscillator! We correct this by rolling off the gain at high frequencies, turning the differentiator into an integrator past some transition frequency.

We put the improved differentiator through some tests, showing how it does output the derivative of its input signal.

As a final demonstration, we put the output of the sine shaper that we built a few episodes ago through our differentiator, and see how it detects that our approximate sine wave is actually a series of line segments.

The CircuitJS model of the integrator can be accessed on
[Paul Falstad's web site](https://www.falstad.com/circuit/circuitjs.html?ctz=CQAgjOB0AMt-CwFMC0B2EAWATDArAJwDMmm0Y20RAHEUSGtiHs9M6mGAFBkEPSYQANjIhqYIcNERokSSgKQieIQWyZa1IXmiEQs6NiIyuAJQZ4mQ6NQtM8aSWzbSmz-ZDxm7wxj7QC+kGiKBRBzp7emASSQupYGsLxbPRgcB4s7rJeAMbCNkmCAYJxgoLIKLYGYOI6QmDRRNBCaIQEGAbk+lwATvyCeKRiEsxDbGnwXADu-aNFgaXdM+KSg4IrUs5cAOaz2pLFDJThXADyw7Gi1NRsIllcAIbg6rYtTGBE1r5MtmAsoSwJvBwuAENMQMomJCsCIIZYls9EvtniNkdBwRRUSoUatHAjMbjJB81Mw8eiZsT7HjKd98UQSW9wJ9bn5yYjXtcccJOejdgTub9sCNGPc+tFYvFrK9kqDYODDmtZuKERtFRtlei8odleqYlhwBxxpACARmgQJNQ8E08JbtB5YCYAPYgPhENwgAAe2HE5Hox1kMnAYhAbi4QA) or at a [shortened URL](https://tinyurl.com/222y6otn).  In addition, it is stored in text form in this directory.


| File Name | Description |
| --------- | ----------- |
| README.md | This file |
| bode.py   | Python script that produced the Bode plots in the video |
| differentiator.cjs | CircuitJS model of the differentiator. |

I didn't trouble to draw the differentiator in KiCAD, so there's
no formal schematic this time, sorry!


