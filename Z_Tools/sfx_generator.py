import numpy as np
from scipy.io.wavfile import write
import os

SAMPLE_RATE = 44100
SFX_DIR = r"d:\WT3D_Project\Z_Tools\Audio\SFX"

if not os.path.exists(SFX_DIR):
    os.makedirs(SFX_DIR)

def normalize(audio):
    audio = np.clip(audio, -1.0, 1.0)
    return np.int16(audio * 32767)

# 1. Cinematic Bass Drop
def make_bass_drop(duration=3.0):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Frequency sweep from 80Hz down to 20Hz exponentially
    freq = 60 * np.exp(-1.5 * t) + 20
    # Phase integration for variable frequency: phi(t) = integral(2pi*f(t))
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    # Base sine wave
    wave = np.sin(phase)
    # Add heavy clipping/saturation for 'Maxskills Impact'
    wave = np.tanh(wave * 2.5) 
    # Envelope (fast attack, exponential decay)
    envelope = np.where(t < 0.05, t/0.05, np.exp(-1.2 * (t - 0.05)))
    return normalize(wave * envelope * 0.9)

# 2. Robotic Glitch Whoosh
def make_glitch_whoosh(duration=2.0):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # White noise base
    noise = np.random.uniform(-1, 1, len(t))
    
    # Filter envelope (Whoosh swell)
    swell_env = np.sin(np.pi * (t / duration)) ** 3
    
    # Glitch chops
    chop_freq = 15 # chops per second
    chop_wave = (np.sign(np.sin(2 * np.pi * chop_freq * t)) + 1) / 2
    
    # Add sudden bursts
    bursts = np.zeros_like(t)
    for i in range(5):
        start = np.random.uniform(0.2, duration-0.2)
        idx_start = int(start * SAMPLE_RATE)
        idx_end = idx_start + int(0.05 * SAMPLE_RATE)
        bursts[idx_start:idx_end] = np.random.uniform(-1, 1, idx_end - idx_start) * 2.0
    
    # Sawtooth Drone
    drone_freq = 200 - 150 * (t/duration) # sweeping down
    drone_phase = 2 * np.pi * np.cumsum(drone_freq) / SAMPLE_RATE
    saw = 2 * (drone_phase / (2 * np.pi) - np.floor(0.5 + drone_phase / (2 * np.pi)))
    
    combined = (noise * swell_env * chop_wave * 0.5) + (bursts * 0.4) + (saw * swell_env * 0.3)
    return normalize(np.tanh(combined * 1.5))

# 3. Metal Impact Riser
def make_metal_impact_riser(duration=4.0):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Riser phase
    riser_duration = 2.5
    t_rise = t[t < riser_duration]
    rise_freq = 200 + 1000 * (t_rise / riser_duration)**2
    rise_phase = 2 * np.pi * np.cumsum(rise_freq) / SAMPLE_RATE
    riser_wave = np.sin(rise_phase) * (t_rise / riser_duration)
    
    # Impact phase
    t_impact = t[t >= riser_duration] - riser_duration
    impact_noise = np.random.uniform(-1, 1, len(t_impact))
    impact_decay = np.exp(-3.0 * t_impact)
    impact_wave = np.tanh(impact_noise * 3.0) * impact_decay
    
    # Sub-boom at impact
    sub_freq = 50 * np.exp(-2 * t_impact) + 20
    sub_phase = 2 * np.pi * np.cumsum(sub_freq) / SAMPLE_RATE
    sub_wave = np.sin(sub_phase) * np.exp(-1.5 * t_impact)
    
    combined_impact = impact_wave * 0.5 + sub_wave * 0.7
    
    # Stitch together
    full_wave = np.zeros_like(t)
    full_wave[:len(riser_wave)] = riser_wave * 0.6
    full_wave[len(riser_wave):] = combined_impact
    
    return normalize(full_wave)

# 4. Cinematic Sweep (Pure Whoosh)
def make_pure_whoosh(duration=1.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    # lowpass simulation via moving average (rough approx)
    # applying window envelope
    window = np.sin(np.pi * (t / duration)) ** 2
    return normalize(noise * window * 0.5)

print("Starting Synthesizer...")
write(os.path.join(SFX_DIR, "1_Cinematic_Bass_Drop.wav"), SAMPLE_RATE, make_bass_drop())
write(os.path.join(SFX_DIR, "2_Robotic_Glitch_Whoosh.wav"), SAMPLE_RATE, make_glitch_whoosh())
write(os.path.join(SFX_DIR, "3_Metal_Impact_Riser.wav"), SAMPLE_RATE, make_metal_impact_riser())
write(os.path.join(SFX_DIR, "4_Pure_Cinematic_Whoosh.wav"), SAMPLE_RATE, make_pure_whoosh())
print(f"B2B Arsenal generated at {SFX_DIR}!")
