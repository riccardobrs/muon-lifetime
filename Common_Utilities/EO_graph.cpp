// g++ -o EO_graph EO_graph.cpp `root-config --cflags --glibs`

#include <iostream>
#include <cmath>
#include <TApplication.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TAxis.h>
#include <TH1.h>
#include <TF1.h>
#include <TMath.h>
#include <TStyle.h>

using namespace std;

Double_t Est(Double_t *x, Double_t *par)
{
	Double_t value=0;

	value = par[0] * TMath::Power(TMath::Cos(x[0] * 3.14 / 180.0), par[1]);
	return value;
} 
Double_t Ovest(Double_t *x, Double_t *par)
{
	Double_t value=0;

	value = par[0] * TMath::Power(TMath::Cos(x[0] * 3.14 / 180.0), par[1]);
	return value;
} 

int main(int argc, char** argv){
/*
	if (argc < 3){

		cout << "Not enough parameters: ./MyTGraph filename.txt filename.txt" << endl;
		return 1;
	}
*/
	TApplication* myApp = new TApplication("myApp", NULL, NULL);
	TCanvas* myC = new TCanvas("myC","Effetto Est-Ovest", 0, 0, 1500, 700);
	TF1* myFun = new TF1 ("myFun", Est, 0, 89, 2);
	myFun -> SetLineColor (kRed);
	myFun -> SetParameter (0, 1);
	myFun -> SetParameter (1, 2);
	myFun -> SetParName (0, "Ampiezza_Est");
	myFun -> SetParName (1, "Esponente_Est");
	gStyle -> SetOptFit (1111);	
	
	TF1* myFun1 = new TF1 ("myFun1", Ovest, 0, 89, 2);
	myFun1 -> SetLineColor (kBlue);
	myFun1 -> SetParameter (0, 1);
	myFun1 -> SetParameter (1, 2);
	myFun1 -> SetParName (0, "Ampiezza_Ovest");
	myFun1 -> SetParName (1, "Esponente_Ovest");
	gStyle -> SetOptFit (1111);	

	TGraphErrors* myGraph = new TGraphErrors(argv[1]);
	myGraph -> GetXaxis()->SetTitle("Angolo [°]");
	myGraph -> GetYaxis()->SetTitle ("Rate normalizzato [Hz]");
	myGraph -> SetMarkerStyle(20);
	myGraph -> SetMarkerColor(kRed);
	myGraph -> SetMarkerSize(1);
	myGraph -> Fit ("myFun", "R");
	myGraph -> SetTitle("Effetto Est-Ovest");
	
	TGraphErrors* myGraph1 = new TGraphErrors(argv[2]);
	myGraph1 -> GetXaxis()->SetTitle("Angolo [°]");
	myGraph1 -> GetYaxis()->SetTitle ("Rate normalizzato [Hz]");
	myGraph1 -> SetMarkerStyle(20);
	myGraph1 -> SetMarkerColor(kBlue);
	myGraph1 -> SetMarkerSize(1);
	myGraph1 -> Fit ("myFun1", "R");
	myGraph1 -> SetTitle("Effetto Est-Ovest");

	
	myC -> cd();
	myGraph -> Draw("AP");
	myGraph1 -> Draw("P SAME");
	myC -> Update();
	myApp -> Run();
	return 0;
}
