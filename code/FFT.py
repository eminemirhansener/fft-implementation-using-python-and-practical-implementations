import cmath
import math
import matplotlib.pyplot as plt
import numpy as np

def FFT(data):

    n = len(data)

    # The DFT of a single point is the point itself.
    if n<=1:
        return data
    
    # Split the signals into even and odd parts
    even = FFT(data[0::2])
    odd = FFT(data[1::2])

    combined = np.zeros(n, dtype=complex)

    for k in range (n // 2):

        # Calculate the Twiddle Factor: W_N^k = e^(-i * 2 * pi * k / n)
        twiddle = cmath.exp(-2j * cmath.pi * k / n)


        # Apply the Butterfly Operation
        # X[k] = E[k] + W_N^k * O[k]
        combined[k] = even[k] + twiddle * odd[k]
        
        # X[k + n/2] = E[k] - W_N^k * O[k]
        combined[k + n // 2] = even[k] - twiddle * odd[k]

    return combined

if __name__ == '__main__':
    f_sampling = 1000
    N = 2**10
    time = np.linspace(0, 1, N, endpoint=False)

    half_N = N//2

    # --- Signal Generation ---
    # Consider the signal as an analog sensor data with noises.
    main_signal = 5
    # Creating a signal with three different frequencies
    freq1, amp1 = 50.5, 2.0   # 50 Hz component
    freq2, amp2 = 280.7, 0.8  # 280 Hz component
    freq3, amp3 = 400.2, 0.6  # 500 Hz component
    sig1 = amp1 * np.sin(2 * np.pi * freq1 * time)
    sig2 = amp2 * np.sin(2 * np.pi * freq2 * time)
    sig3 = amp3 * np.sin(2 * np.pi * freq3 * time)
    # Add Random White Noise
    noise = np.random.normal(0, 0.5, size=N)
    # Combine all components
    signal = main_signal + sig1 + sig2 + sig3 + noise

    # Pre-processing: Detrend the signal by subtracting mean to remove DC offset
    signal_detrended = signal - np.mean(signal)

    # Window the signal using Hanning Method
    window = np.hanning(len(signal_detrended))
    signal_windowed = signal_detrended * window

    # Compute FFT
    spectrum = FFT(signal)
    spectrum_detrended = FFT(signal_detrended)
    spectrum_windowed = FFT(signal_windowed)

    ######### Magnitudes #########
    # Normalized Magnitude
    magnitudes = np.abs(spectrum) / N
    magnitudes[1:] = magnitudes[1:] * 2.0 # Corrected for DC componenet in 0 Hz!
    # Normalized Detrended Magnitude
    magnitudes_detrended = np.abs(spectrum_detrended) * 2.0 / N
    # Normalized Detrended-Windowed Magnitude
    magnitudes_windowed = np.abs(spectrum_windowed) * 2.0 / np.sum(window)

    # Frequency Bins
    frequencies = np.linspace(0, f_sampling / 2, half_N)

    # Signal Plot
    plt.subplot(2, 2, 1)
    plt.title("Time Domain")
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.plot(time, signal, label='Signal', color='red', linestyle='-')
    plt.grid(True)
    plt.legend()

    # FFT Without Detrending / Hanning Window Plot
    plt.subplot(2, 2, 2)
    plt.title("Frequency Domain")
    plt.plot(frequencies, magnitudes[:half_N], label='FFT Spectrum', color='green', linestyle='-')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.legend()

     # FFT With Detrending Plot
    plt.subplot(2, 2, 3)
    plt.title("Frequency Domain with Detrending")
    plt.plot(frequencies, magnitudes_detrended[:half_N], label='FFT Spectrum', color='green', linestyle='-')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.legend()

    # FFT With Detrending / Hanning Window Plot
    plt.subplot(2, 2, 4)
    plt.title("Frequency Domain with Detrending and Hanning Window")
    plt.plot(frequencies, magnitudes_windowed[:half_N], label='FFT Spectrum', color='green', linestyle='-')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()