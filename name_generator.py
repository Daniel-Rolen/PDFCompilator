import random

def generate_space_name():
    adjectives = ['Cosmic', 'Stellar', 'Galactic', 'Nebulous', 'Celestial', 'Astral', 'Lunar', 'Solar']
    nouns = ['Voyager', 'Nebula', 'Pulsar', 'Quasar', 'Supernova', 'Comet', 'Asteroid', 'Constellation']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}"
