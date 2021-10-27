from scipy.stats import truncnorm
from scipy.integrate import odeint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def gen_norm_dist(clip_a,clip_b,u=None):
    if u is None:
        u = (clip_a+(clip_b-clip_a)/2)
    std = 1
    a, b = (clip_a - u) / std, (clip_b - u) / std
    return truncnorm(a,b,loc=u)

class DrugAdministration():
    def __init__(self, drug, doses, times, weight):
        self.drug = drug
        self.doses = doses
        self.times = times
        self.weight = weight
        self._Vd = drug._Vd*self.weight
        self._CL = drug._CL*self.weight
        self.F = drug.F
        self._Tmax = drug._Tmax
        self.baseline = 0
        self.dCdt = lambda C,t: self.u(t)/self.Vd - (self.CL/self.Vd)*C

    @property
    def Vd(self):
        return self._Vd

    @property
    def CL(self):
        return self._CL

    @CL.setter
    def CL(self,val):
        self._CL = val

    @property
    def Tmax(self):
        return self._Tmax

    def set_baseline(self,dose,interval):
        self.baseline = self.Css(dose,interval)

    def Css(self,dose,interval):
        auc = (self.F*dose)/(self.CL)
        return auc/interval

    def u(self,t):
        u_bool = (t > self.times) & (t < self.times+self.Tmax)
        if u_bool.any():
            idx = u_bool.values.tolist().index(True)
            return self.F*self.doses.values[idx]/self.Tmax
        else:
            return 0

    def C(self,t,normalize=False):
        c = odeint(self.dCdt,self.baseline,t,tcrit=t).flatten()
        if normalize:
            c = c/self.baseline
        return c

    def plot(self):
        t = np.linspace(0,self.times.max(),1000)
        y = [self.u(tau) for tau in t]
        sns.lineplot(t,y)

    def plot_Cp(self,span=25,C0=0,normalize=False):
        t = np.linspace(0,self.times.max(),1000)
        C = self.C(t,normalize)
        if span is not None:
            C = pd.Series(C).ewm(span).mean()
        df = pd.DataFrame({
            'Time (hrs)':t,
            'Medication':['{}'.format(self.drug._name_)]*len(t),
            'Concentration (mg/L)':C})
        sns.lineplot(data=df,x='Time (hrs)',hue='Medication',y='Concentration (mg/L)')

class Drug(object):
    _weight = 80

    def get_CL(self,wt=80):
        return cls._CL*wt

    def show_Vd(self, wt=None):
        print('Vd: ',cls.Vd,' L/kg')

    def show_CL(self,wt=None):
        print('CL: ', cls._CL, ' L/hour/kg')

    @classmethod
    def __str__(cls):
        return cls._name_


class Levetiracetam(Drug):
    _name_ = 'Levetiracetam'
    F  = 0.96 # percent
    _Vd = 0.70 # L/kg
    _CL = 0.96/1000*60 # L/hour/kg
    _Tmax = 1.5 # Hours

    @classmethod
    def create_administration(cls, doses, times, weight):
        da = DrugAdministration(cls, doses, times, weight)
        return da

class Lamotrigine(Drug):
    _name_ = 'Lamotrigine'
    # https://www.accessdata.fda.gov/drugsatfda_docs/label/2006/020241s10s21s25s26s27,020764s3s14s18s19s20lbl.pdf
    F = 0.98
    CL_dist = gen_norm_dist(0.24*60/1000,1.15*60/1000,0.58) # L/hr/kg
    Tmax_dist = gen_norm_dist(0.5,4.0,2.2) # (1.4-4.8)
    Vd_dist = gen_norm_dist(0.9,1.3)

    _Vd = Vd_dist.mean()
    _CL = CL_dist.mean()
    _Tmax = Tmax_dist.mean()

    @classmethod
    def create_administration(cls, doses, times, weight):
        da = DrugAdministration(cls, doses, times, weight)
        return da

class Pregabalin(Drug):
    _name_ = 'Pregabalin'
    # https://www.accessdata.fda.gov/drugsatfda_docs/label/2018/021446s035,022488s013lbl.pdf
    F = 0.95
    CL_dist = gen_norm_dist(67.0/1000*60,80.9/1000*60) # L/hr

    _Vd = 0.5 # L/kg
    _CL = CL_dist.mean()
    _Tmax = 1.5

    @classmethod
    def create_administration(cls, doses, times, weight):
        da = DrugAdministration(cls, doses, times, weight)
        da.CL = cls._CL
        return da

    @classmethod
    def show_CL(cls,wt=None):
        print('CL: ', cls._CL, ' L/hour')

    @classmethod
    def get_CL(cls,wt=80):
        return cls._CL
