// c++ -o histo_mc histo_mc.cpp `root-config --cflags --glibs`
// ./histo_mc

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
#include <TFile.h>

using namespace std;

// convert from int to string
std::string IntStringConvert(Int_t Number){
  std:: string Result;
  ostringstream Convert;
  Convert << Number;
  Result = Convert.str(); 
  return Result;
}

int main (int argc, char ** argv) {

	TApplication* myApp = new TApplication ("myApp", NULL, NULL);
	TCanvas* c = new TCanvas("","",0,0,300,300);
	gStyle->SetOptStat(11);
    gStyle->SetOptFit(1112);
    
	double tau_plus = 2.197;
	double tau_minus = 2.026;
	//composition of mu+ and mu- at earth surface (i.e. probabilities)
	double p_plus = 0.56;
	double p_minus = 0.44;
	
	//number of events in the dataset
	int N_down = 2289;
	int N_up = 3350;
	double N_events = ( N_up + N_down ) / 2.; 
	int NBin = 50;
	double min_t = 0.;
	double max_t = 11;	
    
    
	//BINNING of the histogram of single bin content
	int N_BIN = 15;
	//creating an array of histograms
	
	string name, title;

	TH1F *h[NBin];

    for(int j=0; j < NBin ;j++) {
		name="hbin_"+IntStringConvert(j+1);
    	title="hbin_ "+IntStringConvert(j+1);
    	h[j]=new TH1F(name.c_str(),title.c_str(),N_BIN,0.,0.);   
	}
		
	int N_MC = 10000; //number of MC simulations performed    
	TRandom3 * R = new TRandom3(time(NULL));
	
	double mean_bin[NBin];
	for (int k = 0; k < NBin; k++) {
		mean_bin[k] = 0.;
	}
	
	
	
	for (int n =0 ; n < N_MC ; n++) {			
		
		TH1D * histo = new TH1D("simulatated histo", "simulatated histo", NBin, min_t, max_t);
		double N_plus = R->Binomial(N_events,p_plus);
		//double N_minus = R->Binomial(N_events,p_minus);
		double N_minus = N_events - N_plus;	
		double entry_plus, entry_minus = 0.;
		
		for ( int i =0 ; i < N_plus ; i++) {
				entry_plus = R->Exp(tau_plus);
				histo->Fill(entry_plus);
			}
			
		for ( int i =0 ; i < N_minus ; i++) {
			entry_minus = R->Exp(tau_minus);
			histo->Fill(entry_minus);
		}

		c->cd();
		histo->Draw();
		//histo->Fit("f");
		c->Update();
		c->Modified();		
		
		for(int j=0; j < NBin ; j++) {
    			h[j]->Fill(histo->GetBinContent(j+1)); 
    			mean_bin[j] += histo->GetBinContent(j+1);  
		}						
		if (n < N_MC - 1) delete histo;			
	}
	
	for(int j=0; j < NBin ;j++) {
		mean_bin[j] = mean_bin[j] / N_MC;
	}

	vector <double> mean_value;
	for(int i =0 ; i < NBin ; i++) {
		mean_value.push_back(mean_bin[i]);	
	}
	
	/*TCanvas *canva_bin[NBin]; 

	for(int j=0 ; j < NBin ; j++) {
		name="canva bin n. "+ IntStringConvert(j);
	    title="canva bin n. "+ IntStringConvert(j);
	    canva_bin[j] = new TCanvas(name.c_str(),title.c_str(),0,0,800,800);   
	}	
	
	//Poisson Fit
	
	
	for(int j=0; j < NBin ;j++) {
		TF1* poiss = new TF1("poiss","[0]*TMath::Poisson(x,[1])",0.,0.);
   		poiss->SetParameter(1,mean_bin[j]);

    	canva_bin[j]->cd();
		h[j]->Draw();
		h[j]->Fit("poiss");
		mean_value.push_back( (int) poiss->GetParameter(0) );
		
		string title = "bin n. " + IntStringConvert(j+1) + ".png";
        canva_bin[j]->SaveAs(title.c_str());
        
		canva_bin[j]->Update();
		canva_bin[j]->Modified();	
				  
	}
	
	for(int j=0; j < NBin ;j++) {
		delete h[j];
		delete canva_bin[j];
	}
	
	*/	
	
	TCanvas* canva = new TCanvas("","",0,0,400,300);
	TH1D * histo_MC = new TH1D("histo", "", NBin, min_t, max_t);
	
	double entries = 0.;		
	for ( int i =0 ; i < NBin ; i++) {
		histo_MC->SetBinContent(i+1, mean_value[i]);
		entries += mean_value[i];	
	}
	histo_MC->SetEntries(entries);
	
	TF1 * f = new TF1("f", "[0]*exp(-x/[1])", min_t, max_t);
	f->SetParName(0,"Amp");
	f->SetParName(1,"tau");
	f->SetParameter(0,N_events);
	f->SetParameter(1,2.2);
	f->SetParameter(0,N_events);
	
	canva->cd();
	histo_MC->Draw();
	//histo_MC->Fit("f");		
	canva->Update();
	canva->Modified();
	
	TFile* tfile = new TFile("MC_histo.root","RECREATE");
	histo_MC->Write();
	f->Write();
	tfile->Write();
	tfile->Close();
	
    myApp->Run();
    return 0;
    
}
