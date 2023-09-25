Kb=1.38*(10**-23)

V=float(input('volume:'))

N=float(input('Number of particles'))

V=500*2100*float(input('length'))

def moyenne(S):
    S2=[s**2 for s in S]
    return sum(S2)/len(S2)


def temperature(S, mass):
    return (mass/3*Kb)*moyenne(S)


def kinetic_pressure(S, mass):
    return (N/3*V)*mass*moyenne(S)