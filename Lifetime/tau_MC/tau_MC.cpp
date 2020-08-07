// c++ -o tau_MC tau_MC.cpp `root-config --cflags --glibs`
// ./tau_MC

#include <cmath>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <TAxis.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TFitResult.h>
#include <TH1D.h>
#include <TLatex.h>
#include <TMatrixDSym.h>
#include <TRandom3.h>
#include <TStyle.h>
#include <TApplication.h>

using namespace std;

double max_deviation(vector <double> v, double M) {
    
    double err = 0.;
    
    for (int i=0; i < v.size(); i++) {
        
        if (err < abs(v[i] - M))
            err = abs(v[i] - M);
        
    }
    
    return err;

}


int main (int argc, char ** argv) {

	TApplication* myApp = new TApplication ("myApp", NULL, NULL);
	TCanvas* c = new TCanvas();
	gStyle->SetOptStat(11);
    gStyle->SetOptFit(1112);
    
	double tau_plus = 2.197e-06;
	double tau_minus = 2.026e-06;
	//composition of mu+ and mu- at earth surface (i.e. probabilities)
	double p_plus = 0.56;
	double p_minus = 0.44;
	int N_events = 45000; //number of events in the dataset
	int NBin = 50;
	
	
	
	
	
	vector <double> tau_syst;
	vector <double> tau_syst_err;
	
	double maxt = 11e-06;
	TF1 * f = new TF1("f", "[0]*exp(-x/[1])", 0.5e-06, maxt);
	f->SetParName(0,"Amp");
	f->SetParName(1,"tau");	
	f->SetParameter(1,2.2e-06);
	
	
    int N_MC = 5000; //number of MC simulations performed    
	TRandom3 * R = new TRandom3(time(NULL));
	
	vector <double> entries;
	
	int N_syst = 9;
	for ( int k = 0; k < N_syst; k++ ) {
	
		vector <double> tauMC_value;
		vector <double> tauMC_err;
	
		if (k == 0) { // N_plus + 2%  N_minus - 2% 
			p_plus = 0.56 * 1.02;
			p_minus = 0.44 * 0.98;
		}
		if (k == 1) { // N_plus - 2% N_minus + 2% 
			p_plus = 0.56 * 0.98;
			p_minus = 0.44 * 1.02;
		}
		if (k == 2) { // N_plus + 5%  N_minus - 5% 
			p_plus = 0.56 * 1.05;
			p_minus = 0.44 * 0.95;
		}
		if (k == 3) { // N_plus - 5% N_minus + 5% 
			p_plus = 0.56 * 0.95;
			p_minus = 0.44 * 1.05;
		}
		if (k == 4) { // N_plus + 8%  N_minus - 8% 
			p_plus = 0.56 * 1.08;
			p_minus = 0.44 * 0.92;
		}
		if (k == 5) { // N_plus - 8% N_minus + 8% 
			p_plus = 0.56 * 0.92;
			p_minus = 0.44 * 1.08;
		}
		if (k == 6) { // N_plus + 10%  N_minus - 10% 
			p_plus = 0.56 * 1.10;
			p_minus = 0.44 * 0.90;
		}
		if (k == 7) { // N_plus - 10% N_minus + 10% 
			p_plus = 0.56 * 0.90;
			p_minus = 0.44 * 1.10;
		}
		
		for (int j =0 ; j < N_MC ; j++) {			
		
			TH1D * histo = new TH1D("simulatated histo", "simulatated histo", NBin, 0., 0.);
			double N = R->Poisson(N_events);
			double N_plus = R->Binomial(N,p_plus);
			double N_minus = R->Binomial(N,p_minus);
			
			
			double entry_plus, entry_minus = 0.;
			for ( int i =0 ; i < N_plus ; i++) {
				entry_plus = R->Exp(tau_plus);
				histo->Fill(entry_plus);
			}
			
			for ( int i =0 ; i < N_minus ; i++) {
				entry_minus = R->Exp(tau_minus);
				histo->Fill(entry_minus);
			}
		        
		        			
		
		f->SetParameter(0, N_plus + N_minus);
		f->SetParameter(1,2.2e-06);
		c->cd();
		histo->Draw();
		histo->Fit("f", "R"); 
		
		
		tauMC_value.push_back(f->GetParameter(1));
		tauMC_err.push_back(f->GetParError(1));
		
		c->Update();
		c->Modified();
		
		delete histo;
		}
	
	
		NBin = 25;
		TH1D * tau_histo = new TH1D("Statistical box", "MC histo", NBin, 0., 0.);
		tau_histo -> GetXaxis() -> SetTitle("#tau_{MC} [#mus]");
    	tau_histo -> GetYaxis() -> SetTitle("Counts");
    	tau_histo -> GetXaxis() -> SetTitleSize(0.042);
    
		
		
		for ( int i =0 ; i < tauMC_value.size() ; i++) {
			tau_histo->Fill(tauMC_value[i]/1e-06);
		}		
		
		//TF1 * f_gaus = new TF1("f_gaus", "[0]*exp(-0.5*((x-[1])/[2])**2)", 1.9e-06, 2.3e-06 );
		TF1 * f_gaus = new TF1("f_gaus", "gaus", 1.9e-06, 2.3e-06 );
		f_gaus->SetParName(0,"Amp");
		f_gaus->SetParName(1,"mean");
		f_gaus->SetParName(2,"sigma");
		f_gaus->SetParameter(0,457);
		f_gaus->SetParameter(1,2.1);
		f_gaus->SetParameter(2,6.9e-03);
		
		c->cd();
		tau_histo->Draw();
		tau_histo->Fit("f_gaus", "L");
		c->Update();
		c->Modified();
		
		tau_syst.push_back(f_gaus->GetParameter(1));
		tau_syst_err.push_back(f_gaus->GetParError(1));
		entries.push_back(tau_histo->GetEntries());		
	}	
	
	const char * filename = "tau_MC_results.txt";
	ofstream outfile (filename);
	
	double max_dev = max_deviation(tau_syst, tau_syst[8]);
	
	for ( int i = 0; i < tau_syst.size(); i++ ) {		
	cout << "tau[" << i << "] = ( " << tau_syst[i] /1e-06 << " +- " << tau_syst_err[i] /1e-06 << ") e-06 s" << endl;	
	}
	cout << "Max Deviation: " << max_dev << endl;
	
	outfile << "Range Fit 0.5 - 11" << endl;
	outfile << "tau_MC = ( " << tau_syst[8] /1e-06 << " +- " << tau_syst_err[8] /1e-06 << ") e-06 s" << endl; 
	for ( int i = 0; i < tau_syst.size() -1; i++ ) {		
	outfile<< "tau_syst[" << i << "] = ( " << tau_syst[i] /1e-06 << " +- " << tau_syst_err[i] /1e-06 << ") e-06 s" << endl;	
	}
	outfile << "Max Deviation: " << max_dev << endl;
	
    myApp->Run();
    return 0;
    
}
