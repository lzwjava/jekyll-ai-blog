import torch
import torchaudio


import matplotlib.pyplot as plt
import requests
from torchaudio.utils import download_asset

SAMPLE_GSM = download_asset("tutorial-assets/steam-train-whistle-daniel_simon.gsm")
SAMPLE_WAV = download_asset(
    "tutorial-assets/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav"
)
SAMPLE_WAV_8000 = download_asset(
    "tutorial-assets/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042-8000hz.wav"
)

print(SAMPLE_WAV)

metadata = torchaudio.info(SAMPLE_WAV)
print(metadata)

gsm_metadata = torchaudio.info(SAMPLE_GSM)
print(gsm_metadata)

wav_8000_metadata = torchaudio.info(SAMPLE_WAV_8000)
print(wav_8000_metadata)


def _hide_seek(obj):
    class _wrapper:
        def __init__(self, obj):
            self.obj = obj

        def read(self, n):
            return self.obj.read(n)

    return _wrapper(obj)


url = "https://download.pytorch.org/torchaudio/tutorial-assets/steam-train-whistle-daniel_simon.wav"
with requests.get(url, stream=True) as response:
    metadata = torchaudio.info(response.raw)
    # metadata = torchaudio.info(_hide_seek(response.raw))

print("hide_seek")
print(metadata)

waveform, sample_rate = torchaudio.load(SAMPLE_WAV)

print(waveform)
print(sample_rate)


def plot_waveform(waveform, sample_rate):
    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape
    print(num_channels, num_frames)

    time_axis = torch.arange(0, num_frames) / sample_rate

    print(time_axis)

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].plot(time_axis, waveform[c], linewidth=1)
        axes[c].grid(True)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c + 1}")

    figure.suptitle("waveform")
    # plt.show()


plot_waveform(waveform, sample_rate)


def plot_specgram(waveform, sample_rate, title="Spectrogram"):
    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].specgram(waveform[c], Fs=sample_rate)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c + 1}")
    figure.suptitle(title)
    plt.show()


plot_specgram(waveform, sample_rate)
