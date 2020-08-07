import ROOT
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    xml_to_root = ROOT.TFile ('luglio_2_misura_2.root', 'READ')
    
    dir_u = 'Event15483' #up decay
    dir_d = 'Event10392' #down decay
    dir_r1 = 'Event3740'  #rejected event
    dir_r2 = 'Event1839'  #rejected event
    
    g0_u = ROOT.TGraph()
    g1_u = ROOT.TGraph()
    g0_d = ROOT.TGraph()
    g1_d = ROOT.TGraph()
    g0_r1 = ROOT.TGraph()
    g1_r1 = ROOT.TGraph()
    g0_r2 = ROOT.TGraph()
    g1_r2 = ROOT.TGraph()
    
    ROOT.gDirectory.cd(dir_u)
    ROOT.gDirectory.GetObject("channel0", g0_u)
    ROOT.gDirectory.GetObject("channel1", g1_u)
    
    ROOT.gDirectory.cd('../'+dir_d)
    ROOT.gDirectory.GetObject("channel0", g0_d)
    ROOT.gDirectory.GetObject("channel1", g1_d)
    
    ROOT.gDirectory.cd('../'+dir_r1)
    ROOT.gDirectory.GetObject("channel0", g0_r1)
    ROOT.gDirectory.GetObject("channel1", g1_r1)
    
    ROOT.gDirectory.cd('../'+dir_r2)
    ROOT.gDirectory.GetObject("channel0", g0_r2)
    ROOT.gDirectory.GetObject("channel1", g1_r2)
    
    xml_to_root.Close()
    
    dx = 1./244
    
    x0_u = np.array(g0_u.GetX())
    y0_u = np.array(g0_u.GetY())
    x1_u = np.array(g1_u.GetX())
    y1_u = np.array(g1_u.GetY())
    
    plt.figure()
    ax1 = plt.subplot(211)
    ax1.plot(x0_u, y0_u, label='channel 0')
    ax1.plot(x1_u, y1_u, 'r', label='channel 1')
    ax1.set(xlim=[10.75, 11.25])
    leg1 = ax1.legend()
    plt.grid(True)
    ax2 = plt.subplot(212)
    ax2.plot(x0_u[:-1], np.diff(y0_u)/dx, label='channel 0')
    ax2.plot(x1_u[:-1], np.diff(y1_u)/dx, 'r', label='channel 1')
    ax2.set(xlim=[10.75, 11.25])
    leg2 = ax2.legend()
    plt.xlabel('t [$\mu$s]')
    plt.grid(True)
    plt.show()
    
    x0_d = np.array(g0_d.GetX())
    y0_d = np.array(g0_d.GetY())
    x1_d = np.array(g1_d.GetX())
    y1_d = np.array(g1_d.GetY())
    
    plt.figure()
    ax1 = plt.subplot(211)
    ax1.plot(x0_d, y0_d, label='channel 0')
    ax1.plot(x1_d, y1_d, 'r', label='channel 1')
    ax1.set(xlim=[8.5, 11.5])
    leg1 = ax1.legend()
    plt.grid(True)
    ax2 = plt.subplot(212)
    ax2.plot(x0_d[:-1], np.diff(y0_d)/dx, label='channel 0')
    ax2.plot(x1_d[:-1], np.diff(y1_d)/dx, 'r', label='channel 1')
    ax2.set(xlim=[8.5, 11.5])
    leg2 = ax2.legend()
    plt.xlabel('t [$\mu$s]')
    plt.grid(True)
    plt.show()
    
    x0_r1 = np.array(g0_r1.GetX())
    y0_r1 = np.array(g0_r1.GetY())
    x1_r1 = np.array(g1_r1.GetX())
    y1_r1 = np.array(g1_r1.GetY())
    
    fig1, ax1 = plt.subplots()
    ax1.plot(x0_r1, y0_r1, label='channel 0')
    ax1.plot(x1_r1, y1_r1, 'r', label='channel 1')
    leg1 = ax1.legend()
    plt.xlabel('t [$\mu$s]')
    plt.grid(True)
    plt.show()
    
    x0_r2 = np.array(g0_r2.GetX())
    y0_r2 = np.array(g0_r2.GetY())
    x1_r2 = np.array(g1_r2.GetX())
    y1_r2 = np.array(g1_r2.GetY())
    
    fig2, ax2 = plt.subplots()
    ax2.plot(x0_r2, y0_r2, label='channel 0')
    ax2.plot(x1_r2, y1_r2, 'r', label='channel 1')
    leg2 = ax2.legend()
    plt.xlabel('t [$\mu$s]')
    plt.grid(True)
    plt.show()
