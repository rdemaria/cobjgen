import cobjgen as co

co.set_api_path("./api.so")


class Particle(co.Struct):
    x: co.Double
    px: co.Double

class Particles(co.SOA):
    _element: Particle
    _shape: (8,64)

class ParticlesArray(co.Array):
    _element: Particle
    _shape: (8,64)

class Drift(co.Struct):
    length: co.Double

class Bal(co.Struct):
    normal: co.Double
    skew: co.Double

class Multipole(co.Struct):
    length: co.Double
    hxl: co.Double
    hyl: co.Double
    mult: Bal[None]

class BeamBeam6D(co.Struct):
    charge: co.Double
    sigma: co.Double[4,4]
    weak_closedorbit: co.Double[6]
    kick_corr: co.Double[6]



