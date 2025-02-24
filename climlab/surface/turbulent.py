import numpy as np
from climlab.utils.thermo import qsat
from climlab import constants as const
from climlab.process.energy_budget import EnergyBudget


class SurfaceFlux(EnergyBudget):
    def __init__(self, Cd=3E-3, **kwargs):
        super(SurfaceFlux, self).__init__(**kwargs)
        self.Cd = Cd
        self.heating_rate['Tatm'] = np.zeros_like(self.Tatm)
        newinput = ['U',]
        self.add_input(newinput)
        #  fixed wind speed (for now)
        self.U = 5. * np.ones_like(self.Ts)

    def _compute_heating_rates(self):
        '''Compute energy flux convergences to get heating rates in W/m2.'''
        self._compute_flux()
        self.heating_rate['Ts'] = -self._flux
        # Modify only the lowest model level
        self.heating_rate['Tatm'][..., -1, np.newaxis] = self._flux


class SensibleHeatFlux(SurfaceFlux):
    def __init__(self, Cd=3E-3, **kwargs):
        super(SensibleHeatFlux, self).__init__(Cd=Cd, **kwargs)
        self.init_diagnostic('SHF')

    def _compute_flux(self):
        # this ensure same dimensions as Ts
        #  (and use only the lowest model level)
        Ta = self.Tatm[..., -1, np.newaxis]
        Ts = self.Ts
        DeltaT = Ts - Ta
        #  air density
        rho = const.ps * const.mb_to_Pa / const.Rd / Ta
        #  flux from bulk formula
        self._flux = const.cp * rho * self.Cd * self.U * DeltaT
        self.SHF = self._flux


class LatentHeatFlux(SurfaceFlux):
    def __init__(self, Cd=3E-3, **kwargs):
        super(LatentHeatFlux, self).__init__(Cd=Cd, **kwargs)
        self.init_diagnostic('LHF')

    def _compute_flux(self):
        #  specific humidity at lowest model level
        #  assumes pressure is the last axis
        q = self.q[..., -1, np.newaxis]
        Ta = self.Tatm[..., -1, np.newaxis]
        qs = qsat(self.Ts, const.ps)
        Deltaq = qs - q
        #  air density
        rho = const.ps * const.mb_to_Pa / const.Rd / Ta
        #  flux from bulk formula
        self._flux = const.Lhvap * rho * self.Cd * self.U * Deltaq
        self.LHF = self._flux
