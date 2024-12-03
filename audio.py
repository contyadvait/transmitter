import pyaudio
import wave
import threading
import time

audio = pyaudio.PyAudio()
stream = None
frames = []
is_recording = False
sample_rate = 44100
channels = 1
chunk = 1024
format = pyaudio.paInt16
recording_thread = None

def _record():
    global stream, frames, is_recording
    
    stream = audio.open(
        format=format,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk
    )

    while is_recording:
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

def start_recording(output_filename="recording.wav"):
    """Start recording audio to the specified file"""
    global frames, is_recording, recording_thread
    
    frames = []
    is_recording = True

    recording_thread = threading.Thread(target=_record)
    recording_thread.start()

def stop_recording():
    global is_recording, frames, recording_thread
    
    is_recording = False
    if recording_thread and recording_thread.is_alive():
        recording_thread.join()
    
    if frames:
        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

if __name__ == "__main__":
    print("Starting recording...")
    start_recording("test.wav")
    time.sleep(5)
    print("Stopping recording...")
    stop_recording()