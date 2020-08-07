// c++ -o eff eff.cpp `root-config --cflags --glibs`
// ./eff Minosse_data.txt

#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <TApplication.h>
#include <TCanvas.h>
#include <TGraphErrors.h>
#include <TF1.h>
#include <TStyle.h>
#include <TFitResult.h>
#include <TAxis.h>
#include <TLatex.h>

using namespace std;

double retta (double* x, double* par);

int main (int argc, char ** argv) {

	TApplication* myApp = new TApplication ("myApp", NULL, NULL);
	TCanvas* canva = new TCanvas("canva","",100,200,700,500);
	
	string fileInput = argv[1];
	ifstream in (fileInput.c_str());
	if (in.good() == false) {
		cout << "Errore di apertura file" << endl;
		return 1;
	}
	
	double x, y, z, t;
	vector <double> V;
	vector <double> V_th;
	vector <double> N_triple;
	vector <double> N_doppie;
	vector <double> eff;
	vector <double> eff_err;
	
	
	int Ndata = 0;
	while (true) {
		in >> x >> y >> z >> t;
		if (in.eof() == true) break;
		V.push_back( x );
		V_th.push_back( y );
		N_triple.push_back( z );
                N_doppie.push_back( t );
		Ndata++;
	}
	in.close();
	int N = Ndata;
	
        for (int i = 0; i < N; i++ ) {
                eff.push_back( N_triple[i] / N_doppie[i] );     
        }
        
        for (int i = 0; i < N; i++ ) {
                eff_err.push_back( sqrt( eff[i] * ( 1. - eff[i]) / N_doppie[i] ) );     
        }

	
	TGraphErrors* graph = new TGraphErrors;
	for (int i=0; i < N; i++) {
		graph->SetPoint(i, V[i], eff[i] );
		graph->SetPointError(i, 0., eff_err[i] );
	}
	
	graph->GetXaxis()->SetTitle("Voltage[V]");
	graph->GetYaxis()->SetTitle("Efficiency #epsilon");
	graph->SetTitle("");
	graph->SetMarkerStyle(20);
	graph->SetMarkerSize(0.8);
	graph->SetMarkerColor(kRed);

        canva->cd();	
	graph->Draw("AP");	
	canva->Modified();
	canva->Update();

	myApp->Run();

	return 0;

}
