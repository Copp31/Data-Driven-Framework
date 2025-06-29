import os
import json
from mido import MidiFile, MidiTrack, Message, MetaMessage

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(value, min_value=0, max_value=127):
    return max(min_value, min(value, max_value))

# def enforce_c_major_scale(pitch):
#     c_major_scale = [0, 2, 4, 5, 7, 9, 11]
#     octave = pitch // 12
#     note_in_octave = pitch % 12
#     closest_note = min(c_major_scale, key=lambda n: abs(n - note_in_octave))
#     return octave * 12 + closest_note

class MigrantDataToMIDI:
    def __init__(self, json_path):
        self.json_path = json_path
        self.data = self.load_json()

    def load_json(self):
        with open(self.json_path, 'r') as f:
            return json.load(f)

    def create_midi_from_field(self, field_name, output_midi_path, pitch_range=(40, 100), duration=480, velocity=100):
        if field_name not in self.data:
            print(f"Field {field_name} not found in JSON.")
            return

        values = self.data[field_name]
        if not isinstance(values, dict):
            print(f"Field {field_name} must be a dictionary.")
            return

        val_min = min(values.values())
        val_max = max(values.values())

        midi = MidiFile()
        track = MidiTrack()
        midi.tracks.append(track)

        track.append(MetaMessage('track_name', name=field_name))

        time_cursor = 0
        for i, (key, value) in enumerate(values.items()):
            pitch = clamp(int(map_range(value, val_min, val_max, pitch_range[0], pitch_range[1])))
            # pitch = enforce_c_major_scale(pitch)

            delta_time = 240 if i == 0 else 0  # start on beat, then continue immediately
            track.append(Message('note_on', note=pitch, velocity=velocity, time=delta_time))
            track.append(Message('note_off', note=pitch, velocity=velocity, time=duration))
            time_cursor += delta_time + duration

        midi.save(output_midi_path)
        print(f"MIDI saved to {output_midi_path}")
        
        
