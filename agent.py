from keyframe import Keyframe


class Agent:

    def __init__(self, voice, amplitude_graph):
        self.voice = voice
        self.amplitude_graph = amplitude_graph

    def create_event(self, time):
        amplitude = self.amplitude_graph.pick().value.get()
        self.voice.keyframes.append(Keyframe(time, amplitude))
