# This script computes the MFCC features for automatic speech recognition
#
# You need to complete the part indicated by #### so that the code can produce
# sensible results.
#
# Ning Ma (n.ma@sheffield.ac.uk)
#

import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import numpy as np
from scipy.fftpack import dct

def freq2mel(freq):
	"""Convert Frequency in Hertz to Mels

	Args:
		freq: A value in Hertz. This can also be a numpy array.

	Returns
		A value in Mels.
	"""
	return 2595 * np.log10(1 + freq / 700.0)

def mel2freq(mel):
	"""Convert a value in Mels to Hertz

	Args:
		mel: A value in Mels. This can also be a numpy array.

	Returns
		A value in Hertz.
	"""
	return 700 * (10 ** (mel / 2595.0) - 1)


""" Main Program
"""

# Read waveform
fs_hz, signal = wav.read('SA1.wav')
signal_length = len(signal)

# Define parameters
preemph = 0.97				# pre-emphasis coeefficient
frame_length_ms = 25		# frame length in ms
frame_step_ms = 10			# frame shift in ms
low_freq_hz = 0				# filterbank low frequency in Hz
high_freq_hz = 8000			# filterbank high frequency in Hz
nyquist = fs_hz / 2.0;		# Check the Nyquist frequency
if high_freq_hz > nyquist:
	high_freq_hz = nyquist
num_filters = 26			# number of mel-filters
num_ceps = 12				# number of cepstral coefficients (excluding C0)
cep_lifter = 22				# Cepstral liftering order
eps = 0.001					# Floor to avoid log(0)

# Pre-emphasis
#### emphasised = ...

# Compute number of frames and padding
frame_length = int(round(frame_length_ms / 1000.0 * fs_hz));
frame_step = int(round(frame_step_ms / 1000.0  * fs_hz));
num_frames = int(np.ceil(float(signal_length - frame_length) / frame_step))
print("number of frames is {}".format(num_frames))
pad_signal_length = num_frames * frame_step + frame_length
pad_zeros = np.zeros((pad_signal_length - signal_length))
pad_signal = np.append(emphasised, pad_zeros)

# Find the smallest power of 2 greater than frame_length
NFFT = 1<<(frame_length-1).bit_length(); 

# Compute mel-filters
mel_filters = np.zeros((NFFT // 2 + 1, num_filters))
#### ...


# Compute MFCCs
# Here you can choose either the off-line mode, i.e. save all the frames in a
# matrix and process them in one go, or the online mode, i.e. compute MFCCs 
# frame by frame.

# Hamming window
win = np.hamming(frame_length)

# Compute lifter
lift = 1 + (cep_lifter / 2.0) * np.sin(np.pi * np.arange(num_ceps) / cep_lifter)

# Pre-allocation
feat_powspec = np.zeros((num_frames, NFFT//2+1))
feat_fbank = np.zeros((num_frames, num_filters))
feat_mfcc = np.zeros((num_frames, num_ceps))

# Here we compute MFCCs frame by frame
for t in range(0, num_frames):

	# Framing
	#### frame = ...

	# Apply the Hamming window
	frame = frame * win

	# Compute magnitude spectrum 
	#### magspec = ...

	# Compute power spectrum
	#### powspec = ...

	# Save power spectrum features
	feat_powspec[t, :] = powspec;

	# Compute log mel spectrum
	#### fbank = 

	# Save fbank features
	feat_fbank[t, :] = fbank

	# Apply DCT to get num_ceps MFCCs, omit C0
	#### mfcc = ...

	# Liftering
	mfcc *= lift

	# Save mfcc features
	feat_mfcc[t, :] = mfcc

# Log-compress power spectrogram
feat_powspec[feat_powspec< eps] = eps
feat_powspec = np.log(feat_powspec)


print("=== Before normalisation")
print("mfcc mean = {}".format(np.mean(feat_mfcc, axis=0)))
print("mfcc std = {}".format(np.std(feat_mfcc, axis=0)))

# Cepstral mean and variance normalisation
#### feat_mfcc_z = ...

print("=== After normalisation")
print("mfcc mean = {}".format(np.mean(feat_mfcc_z, axis=0)))
print("mfcc std = {}".format(np.std(feat_mfcc_z, axis=0)))

# Plotting power spectrogram vs mel-spectrogram
plt.figure(1)
siglen = len(signal) / np.float(fs_hz);
plt.subplot(211)
plt.imshow(feat_powspec.T, origin='lower', aspect='auto', extent=(0,siglen,0,fs_hz/2000), cmap='gray_r')
plt.title('Power Spectrogram')
plt.gca().get_xaxis().set_ticks([])
plt.gca().set_yticklabels(['',1,2,3,4,5,6,7,8])
plt.ylabel('Frequency (kHz)')

plt.subplot(212)
freq_bins = freq_bins.astype(int)
plt.imshow(feat_fbank.T, origin='lower', aspect='auto', extent=(0,siglen,0,num_filters), cmap='gray_r')
plt.yticks([0,5,10,15,20,26])
plt.gca().set_yticklabels(['',freq_bins[5],freq_bins[10],freq_bins[16],freq_bins[21],freq_bins[27]])
plt.title('Mel-filter Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')

# Plotting MFCCs with CMN
plt.figure(2)
plt.subplot(211)
plt.imshow(feat_mfcc.T, origin='lower', aspect='auto', extent=(0,siglen,1,num_ceps), cmap='gray_r')
plt.title('MFCC without mean and variance normalisation')

plt.subplot(212)
plt.imshow(feat_mfcc_z.T, origin='lower', aspect='auto', extent=(0,siglen,1,num_ceps), cmap='gray_r')
plt.title('MFCC with mean and variance normalisation')

plt.show()
