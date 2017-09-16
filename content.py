import random

from blur.markov.node import Node
from blur.markov.graph import Graph
from blur.soft import SoftFloat
from blur import rand

from voice import Voice
from oscillator import Oscillator
from agent import Agent

from frequencies import frequencies


scale_pitches = {
    'gf': frequencies[6],
    'bf': frequencies[10],
    'c': frequencies[0] * 2,
    'df': frequencies[1] * 2,
    'ef': frequencies[3] * 2,
    'f': frequencies[5] * 2
}

main_pitch_weights = [
    (scale_pitches['gf'], 10),
    (scale_pitches['bf'], 7),
    (scale_pitches['df'], 10),
    (scale_pitches['f'], 3),
]

scale_pitch_weights = [
    (scale_pitches['gf'], 5),
    (scale_pitches['bf'], 5),
    (scale_pitches['c'], 7),
    (scale_pitches['df'], 3),
    (scale_pitches['ef'], 1),
    (scale_pitches['f'], 3),
]

detune_weights = [
    (0, 100),
    (2, 40),
    (20, 0),
]

octave_weights = [
    (1/8, 5),
    (1/4, 20),
    (1/2, 10),
    (1, 3),
    (2, 1),
    (4, 0.5),
    (8, 0.1),
]

amp_off = SoftFloat([(-1, 0), (0, 10)])
amp_pp = SoftFloat([(0.001, 1), (0.01, 4)])
amp_p = SoftFloat([(0.01, 1), (0.1, 3)])
amp_mf = SoftFloat([(0.1, 1), (0.2, 3)])
amp_f = SoftFloat([(0.3, 1), (0.4, 2), (0.6, 0)])
amp_ff = SoftFloat([(0.7, 5), (1.1, 0)])

node_off = Node(amp_off)
node_pp = Node(amp_pp)
node_p = Node(amp_p)
node_mf = Node(amp_mf)
node_f = Node(amp_f)
node_ff = Node(amp_ff)

node_off.add_link(node_off, 20000)
node_off.add_link(node_pp, 5)
node_off.add_link(node_p, 4)
node_off.add_link(node_f, 1)
node_off.add_link(node_ff, 1)

node_pp.add_link(node_pp, 6000)
node_pp.add_link(node_off, 30)
node_pp.add_link(node_p, 20)
node_pp.add_link(node_mf, 5)
node_pp.add_link(node_f, 1)

node_p.add_link(node_p, 4000)
node_p.add_link(node_off, 10)
node_p.add_link(node_mf, 1)

node_mf.add_link(node_mf, 1000)
node_mf.add_link(node_off, 20)
node_mf.add_link(node_f, 1)

node_f.add_link(node_f, 50)
node_f.add_link(node_off, 10)
node_f.add_link(node_mf, 2)

node_ff.add_link(node_ff, 100)
node_ff.add_link(node_f, 10)
node_ff.add_link(node_off, 10)

main_nodes = [
    node_off,
    node_pp,
    node_p,
    node_mf,
    node_f
]

agents = []

for i in range(50):
    freq = (rand.weighted_choice(main_pitch_weights)
            * rand.weighted_choice(octave_weights))
    graph = Graph(main_nodes)
    agents.append(Agent(Voice(Oscillator(freq)), graph))

for i in range(70):
    base_freq = (rand.weighted_choice(main_pitch_weights)
                 + rand.pos_or_neg(rand.weighted_rand(detune_weights)))
    freq = base_freq * rand.weighted_choice(octave_weights)
    graph = Graph(main_nodes)
    agents.append(Agent(Voice(Oscillator(freq)), graph))

length = 60 * 12  # Seconds

for agent in agents:
    event_times = [random.uniform(0, length) for i in range(length // 3)]
    for event_time in event_times:
        agent.create_event(event_time)

voices = [agent.voice for agent in agents]

from keyframe import Keyframe
voices.append(Voice(Oscillator(scale_pitches['d'] * (1/4))))
voices[-1].keyframes.append(Keyframe(0, 5))
