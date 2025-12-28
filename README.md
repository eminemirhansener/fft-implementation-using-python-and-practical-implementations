# Advanced Recursive FFT and Signal Analysis

This repository contains a comprehensive implementation of the Fast Fourier Transform (FFT) and a suite of signal pre-processing techniques. It demonstrates the transition from continuous-time signal theory to an efficient digital algorithm, incorporating methods to handle real-world sensor data.

## Table of Contents
- [Advanced Recursive FFT and Signal Analysis](#advanced-recursive-fft-and-signal-analysis)
  - [Table of Contents](#table-of-contents)
  - [Theoretical Foundation](#theoretical-foundation)
    - [Euler’s Formula and Correlation](#eulers-formula-and-correlation)
  - [Digital Sampling and Constraints](#digital-sampling-and-constraints)
  - [The Discrete Fourier Transform (DFT)](#the-discrete-fourier-transform-dft)
  - [The FFT Algorithm](#the-fft-algorithm)
    - [Mathematical Proof of the Split](#mathematical-proof-of-the-split)
    - [The Butterfly Operation](#the-butterfly-operation)
    - [FFT Pseudocode](#fft-pseudocode)
  - [Signal Pre-processing Techniques](#signal-pre-processing-techniques)
    - [1. Detrending (DC Offset Removal)](#1-detrending-dc-offset-removal)
    - [2. Windowing (Hanning Method)](#2-windowing-hanning-method)
      - [Mathematical Definition](#mathematical-definition)
      - [Application and Scaling](#application-and-scaling)
  - [Post-processing and Interpretation](#post-processing-and-interpretation)
  - [Visual Analysis](#visual-analysis)
    - [Time Domain](#time-domain)
    - [Frequency Domain Comparisons](#frequency-domain-comparisons)

---

## Theoretical Foundation

Any physical signal can be represented mathematically as a sum of infinite sinusoids, each with specific frequencies, amplitudes, and phases. The **Continuous-Time Fourier Transform (CTFT)** provides the mechanism to decompose these signals:

$$X(f) = \int_{-\infty}^{\infty} x(t) \cdot e^{-i 2\pi f t} dt$$

### Euler’s Formula and Correlation
The transformation relies on **Euler’s Formula** to represent circular motion in the complex plane:
$$e^{i\theta} = \cos(\theta) + i \sin(\theta)$$



By multiplying the signal with this complex kernel, the operation performs a cross-correlation. The real part (cosine) measures alignment with a cosine wave, while the imaginary part (sine) measures alignment with a sine wave at frequency $f$. If a frequency component exists, the resulting area under the curve is non-zero.

---

## Digital Sampling and Constraints

To process signals in a digital environment, the continuous function $x(t)$ must be converted into a discrete sequence $x[n]$. 

* **Time Discretization**: Time is represented as $t = n \cdot T_s$, where $T_s$ is the sampling period.
* **Nyquist-Shannon Constraint**: To prevent information loss, the sampling frequency ($f_s$) must be at least twice the highest frequency component ($f_{max}$) in the signal.

---

## The Discrete Fourier Transform (DFT)

The DFT discretizes the frequency domain by dividing the range into $N$ equal "bins":

$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-i \frac{2\pi}{N} kn}$$

The term $e^{-i \frac{2\pi}{N} kn}$ is the **Twiddle Factor**, representing a unit circle divided into $N$ parts. While a standard DFT requires $O(N^2)$ operations, the FFT reduces this complexity to $O(N \log N)$.



---

## The FFT Algorithm

The algorithm uses a divide-and-conquer strategy by splitting the input into even and odd samples.

### Mathematical Proof of the Split
By separating terms where $n = 2m$ (even) and $n = 2m+1$ (odd), the sum becomes:
$$X[k] = \sum_{m=0}^{N/2-1} x[2m] W_{N/2}^{mk} + W_N^k \sum_{m=0}^{N/2-1} x[2m+1] W_{N/2}^{mk}$$

### The Butterfly Operation
Using the symmetry of the unit circle, where $W_N^{k+N/2} = -W_N^k$, we calculate two outputs from one multiplication:
* $X[k] = E[k] + W_N^k \cdot O[k]$
* $X[k + N/2] = E[k] - W_N^k \cdot O[k]$



### FFT Pseudocode
```text
FUNCTION FFT(data):
    N = length(data)
    IF N <= 1: RETURN data
    
    Even = FFT(data at even indices)
    Odd = FFT(data at odd indices)
    
    FOR k FROM 0 TO (N/2 - 1):
        Twiddle = exp(-i * 2 * PI * k / N)
        Result[k] = Even[k] + Twiddle * Odd[k]
        Result[k + N/2] = Even[k] - Twiddle * Odd[k]
        
    RETURN Result

```
---

## Signal Pre-processing Techniques

To improve accuracy when analyzing noisy or non-ideal sensor data, the following steps are implemented:

### 1. Detrending (DC Offset Removal)
Real-world signals often have a non-zero mean, known as a **DC Offset**. This creates a large spike at 0 Hz in the frequency domain, which can obscure small low-frequency components. Detrending is achieved by calculating the average value of the signal and subtracting it from every sample.

### 2. Windowing (Hanning Method)

Real-world signals often have discontinuities at the boundaries of the sampling window, which causes **Spectral Leakage**. Windowing is used to smooth these transitions.

#### Mathematical Definition
The Hanning window $w[n]$ tapers the signal to zero at both ends using a cosine-based function:

$$w[n] = 0.5 \left( 1 - \cos\left( \frac{2\pi n}{N-1} \right) \right)$$



#### Application and Scaling
The time-domain signal is multiplied by the window before the FFT calculation:
$$x_{windowed}[n] = x[n] \cdot w[n]$$

Since windowing reduces the overall signal energy, the magnitudes are normalized by the sum of the window weights to maintain amplitude accuracy:
$$\text{Corrected Magnitude} = \frac{|X[k]|}{\sum w[n]} \times 2$$

---

## Post-processing and Interpretation

After computing the FFT, the raw complex numbers must be converted into physical magnitudes.

* **Magnitude Calculation**: The absolute value of the complex result is taken.
* **Normalization**: The magnitude is divided by $N$. For all bins except the DC component (0 Hz), the value is multiplied by 2.0 to account for the energy in the negative frequency spectrum.
* **Frequency Mapping**: The index of each bin is mapped to a physical frequency using the sampling rate: $Freq = (k \cdot f_s) / N$.

---

## Visual Analysis



### Time Domain
The raw signal represents composite data from DC Component + multiple oscillators combined with random white noise.

![FFT Signal Analysis Results](output.png)

---

### Frequency Domain Comparisons
* **Raw Spectrum**: Shows significant noise and a large DC spike at 0 Hz.
* **Detrended Spectrum**: The 0 Hz spike is removed, revealing the primary frequency components.
* **Windowed Spectrum**: Frequency peaks become narrower and more distinct, with reduced spectral leakage from the noise floor.