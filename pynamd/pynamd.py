#!/usr/bin/env python3
#
# PyNAMD - MacKerell Toolkit
#
# --------------------------

# Imports
# -------

import scipy.constants as Constants

class PyNAMD(object):

    def __init__(self, file):

        self.__version__ = '0.0.1'

        self.file = open(file, 'r')

    def fetch_simulation_metadata(self, molecular_weight=''):

        lines = self.file.readlines()
        energy_lines = [ line for line in lines if 'ENERGY: ' in line and 'Info' not in line ]
        energy_lines = [ energy_line.split() for energy_line in energy_lines ]
        dihedral_potential_energy = [float(energy_line[3]) for energy_line in energy_lines]
        potential_energies = [float(energy_line[13]) for energy_line in energy_lines]
        pressures = [float(energy_line[16]) for energy_line in energy_lines]
        timestep = [energy_line[1] for energy_line in energy_lines]

        volumes = [float(energy_line[18]) for energy_line in energy_lines]
        temperature = [float(energy_line[12]) for energy_line in energy_lines]

        densities = []

        if molecular_weight:
            densities = [ (((216 * molecular_weight) / (Constants.Avogadro * float(volume))) * (10 ** 24)) for volume in volumes ]

        data = {
            'volumes': volumes,
            'dihedral_potential_energies': dihedral_potential_energy,
            'volumes_per_molecule': '',
            'potential_energies': potential_energies,
            'pressures': pressures,
            'temperature': temperature,
            'timestep': timestep,
        }

        if densities:
            data['density'] = densities

        return data