import sbml2pydstool
import numpy as np
from matplotlib import pyplot as plt
from PyDSTool import args
from PyDSTool import ContClass
from PyDSTool import Generator

# convert SBML to PyDSTool object
c = sbml2pydstool.Converter("ca.xml")

# configure model
DSargs = args(name=c.sbmlmodel.getName())
DSargs.pars = c.pars
DSargs.varspecs = c.varspecs
DSargs.ics = c.icdict

# Integral curves
DSargs.tdomain = [0,30]
ode = Generator.Vode_ODEsystem(DSargs)
traj = ode.compute('polarization')              # integrate ODE
pts  = traj.sample(dt=0.1)                      # Data for plotting

# PyPlot commands
plt.plot(pts['t'], pts['v'])
plt.xlabel('time')                              # Axes labels
plt.ylabel('voltage')                           # ...
plt.ylim([0,65])                                # Range of the y axis
plt.title(ode.name)                             # Figure title from model name
plt.figure()
plt.savefig("fig1.png")

# The system described by Eq. (Ca) is bistable. This can be easily seen integrating trajectories with different initial conditions:
for i, v0 in enumerate(np.linspace(-80,80,20)):
    ode.set( ics = { 'v': v0 } )                # Initial condition
    # Trajectories are called pol0, pol1, ...
    # sample them on the fly to create Pointset tmp
    tmp = ode.compute('pol%3i' % i).sample()    # or specify dt option to sample to sub-sample
    plt.plot(tmp['t'], tmp['v'])
plt.xlabel('time')
plt.ylabel('voltage')
plt.title(ode.name + ' multi ICs')
plt.savefig("fig2.png")

# Bifurcation diagrams
# Prepare the system to start close to a steady state
ode.set(pars = {'p_i': -220} )       # Lower bound of the control parameter 'i'
ode.set(ics =  {'v': -170} )       # Close to one of the steady states present for i=-220

PC = ContClass(ode)

PCargs = args(name='EQ1', type='EP-C')     # 'EP-C' stands for Equilibrium Point Curve. The branch will be labeled 'EQ1'.
PCargs.freepars     = ['p_i']                    # control parameter(s) (it should be among those specified in DSargs.pars)
PCargs.MaxNumPoints = 450                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 2
PCargs.MinStepSize  = 1e-5
PCargs.StepSize     = 2e-2
PCargs.LocBifPoints = 'LP'                     # detect limit points / saddle-node bifurcations
PCargs.SaveEigen    = True                     # to tell unstable from stable branches

PC.newCurve(PCargs)
PC['EQ1'].forward()
PC['EQ1'].display(['p_i','v'], stability=True, figure=3)        # stable and unstable branches as solid and dashed curves, resp.
plt.savefig("fig3.png")

# The information of the equilibrium curve can be accessed via the info() method:
PC['EQ1'].info()

# We can obtain detailed information about a particular special point calling the getSpecialPoint method. For instance, limit point LP2 has the following properties:
print(PC['EQ1'].getSpecialPoint('LP2'))

# We now want to know the location of the limit points change as we vary the calcium conductance, i.e., the parameter gca. We start from one of the limit points, say LP2, 
PCargs = args(name='SN1', type='LP-C')
PCargs.initpoint    = 'EQ1:LP2'
PCargs.freepars     = ['p_i', 'gca']
PCargs.MaxStepSize  = 2
PCargs.LocBifPoints = ['CP']
PCargs.MaxNumPoints = 200
PC.newCurve(PCargs)
PC['SN1'].forward()
PC['SN1'].backward()
PC['SN1'].display(['p_i','gca'], figure=4)
plt.savefig('fig4.png')
plt.show()
