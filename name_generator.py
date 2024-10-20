import random

def generate_space_name():
    adjectives = [
        'Cosmic', 'Stellar', 'Galactic', 'Nebulous', 'Celestial', 'Astral', 'Lunar', 'Solar',
        'Interstellar', 'Meteoric', 'Supernova', 'Quantum', 'Orbital', 'Gravitational', 'Wormhole',
        'Hyperdrive', 'Plasma', 'Neutron', 'Antimatter', 'Stardust'
    ]
    nouns = [
        'Voyager', 'Nebula', 'Pulsar', 'Quasar', 'Supernova', 'Comet', 'Asteroid', 'Constellation',
        'Galaxy', 'Starship', 'Cosmos', 'Singularity', 'Warp', 'Nexus', 'Cluster', 'Nova',
        'Eclipse', 'Horizon', 'Zenith', 'Vortex'
    ]
    return f"{random.choice(adjectives)}_{random.choice(nouns)}_{random.randint(1000, 9999)}"
