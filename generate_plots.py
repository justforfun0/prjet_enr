import numpy as np
import matplotlib.pyplot as plt

# Paramètres de la ligne (valeurs calculées dans le rapport)
R = 0.0849  # Ohm/km
L = 0.4576e-3  # H/km
C = 0.0220e-6  # F/km
G = 0.0069e-6  # S/km
f = 50
omega = 2 * np.pi * f

Z = R + 1j * L * omega
Y = G + 1j * C * omega
gamma = np.sqrt(Z * Y)
Zc = np.sqrt(Z / Y)

# Conditions à la charge (x=0)
Vch = 130000 / np.sqrt(3)  # Tension simple (V)
Pch = 80e6 / 3  # Puissance par phase (W)
cos_phi = 0.8
phi = np.arccos(cos_phi)
Ich = Pch / (Vch * cos_phi) * np.exp(-1j * phi)

def get_VI(x):
    V = Vch * np.cosh(gamma * x) + Zc * Ich * np.sinh(gamma * x)
    I = (Vch / Zc) * np.sinh(gamma * x) + Ich * np.cosh(gamma * x)
    return V, I

# 1. Graphique sur 20 km (Comparaison modèles)
x_20 = np.linspace(0, 20, 100)
V_20, I_20 = get_VI(x_20)

# Modèle impédance série (Z_serie = Z * L_tot)
V_serie = Vch + (Z * x_20) * Ich
I_serie = np.full_like(x_20, Ich, dtype=complex)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(x_20, np.abs(V_20)/1000, 'b-', label='Propagatif')
plt.plot(x_20, np.abs(V_serie)/1000, 'r--', label='Série seule')
plt.xlabel('Distance (km)')
plt.ylabel('Tension (kV)')
plt.title('Tension V(x)')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(x_20, np.abs(I_20), 'b-', label='Propagatif')
plt.plot(x_20, np.abs(I_serie), 'r--', label='Série seule')
plt.xlabel('Distance (km)')
plt.ylabel('Courant (A)')
plt.title('Courant I(x)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('/home/ubuntu/rapport_step/images/comparaison_modeles_20km.png')
plt.close()

# 2. Graphique sur 1000 km (Évolution V et I)
x_1000 = np.linspace(0, 1000, 500)
V_1000, I_1000 = get_VI(x_1000)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(x_1000, np.abs(V_1000)/1000, 'b-')
plt.xlabel('Distance (km)')
plt.ylabel('Tension (kV)')
plt.title('Tension V(x) sur 1000 km')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(x_1000, np.abs(I_1000), 'r-')
plt.xlabel('Distance (km)')
plt.ylabel('Courant (A)')
plt.title('Courant I(x) sur 1000 km')
plt.grid(True)
plt.tight_layout()
plt.savefig('/home/ubuntu/rapport_step/images/evolution_VI_1000km.png')
plt.close()

# 3. Rendement en fonction de la longueur
lengths = np.linspace(1, 200, 100)
rendements = []
for l in lengths:
    Vl, Il = get_VI(l)
    Pl = 3 * np.real(Vl * np.conj(Il))
    rendements.append((Pch * 3) / Pl * 100)

plt.figure(figsize=(8, 5))
plt.plot(lengths, rendements, 'g-')
plt.xlabel('Longueur du câble (km)')
plt.ylabel('Rendement (%)')
plt.title('Rendement de la ligne HTB')
plt.grid(True)
plt.savefig('/home/ubuntu/rapport_step/images/rendement_cable.png')
plt.close()
