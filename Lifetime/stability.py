import numpy as np
import ROOT

if __name__ == '__main__':
    
    file_content = np.loadtxt('stability.txt')
    
    out_content_chi2 = file_content[:,:-2]
    np.savetxt('stability_chi2.txt', out_content_chi2, delimiter='\t', fmt='%.6f')
    
    out_content_tau = np.zeros((file_content.shape[0], 3)) #one more column needed
    out_content_tau[:,0:2] = file_content[:,0:2]
    out_content_tau[:,2] = file_content[:,3]
    np.savetxt('stability_tau.txt', out_content_tau, delimiter='\t', fmt='%.6f')
    
    g_chi2 = ROOT.TGraph2D ('stability_chi2.txt')
    g_tau = ROOT.TGraph2D ('stability_tau.txt')
    
    g_chi2.SetTitle('')
    g_chi2.GetXaxis().SetTitle('N bins')
    g_chi2.GetYaxis().SetTitle('Fit range [#mus]')
    g_chi2.GetZaxis().SetTitle('#chi^{2}/NDF')
    g_tau.SetTitle('')
    g_tau.GetXaxis().SetTitle('N bins')
    g_tau.GetYaxis().SetTitle('Fit range [#mus]')
    g_tau.GetZaxis().SetTitle('#tau [#mus]')
    
    f = ROOT.TFile('stability.root', 'RECREATE')
    
    c_chi2 = ROOT.TCanvas()
    c_chi2.cd()
    g_chi2.Draw('SURF1')
    c_chi2.Write('c_chi2_surf1')
    g_chi2.Draw('CONT4Z')
    c_chi2.Write('c_chi2_cont4z')
    
    c_tau = ROOT.TCanvas()
    c_tau.cd()
    g_tau.Draw('SURF1')
    c_tau.Write('c_tau_surf1')
    g_tau.Draw('CONT4Z')
    c_tau.Write('c_tau_cont4z')
    
    f.Close()
