//g++ -o graph graph.cpp `root-config --cflags --glibs`
//./graph data.txt

#include <TLegend.h>
#include <TLine.h>
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
#include <string>
#include <fstream>
#include <iostream>
#include <TMultiGraph.h>

using namespace std;
using namespace TMath;

int main(int argc, char** argv){

	TApplication* myApp = new TApplication ("myApp", NULL, NULL);
	TCanvas* canva = new TCanvas("canva","canva",100,200,700,500);	
	
	
	string fileInput = argv[1];
	ifstream in (fileInput.c_str());
	if (in.good() == false) {
		cout << "Errore di apertura file" << endl;
		return 1;
	}
	
	//lettura del file dati
	
	double x,y,z,a,b;
	double mean;
	vector <double> HV;
	vector <double> th;
	vector <double> count;
	vector <double> count_err;
	
	
	while (true) {
		in >> x >> y >> z >> a >> b;
		if (in.eof() == true) break;
		HV.push_back( x );
		th.push_back( y );
		mean = ( z + a + b ) / 3;
		count.push_back(mean);
		count_err.push_back(sqrt(mean));
	}
	in.close();
	
	
	TMultiGraph* mg = new TMultiGraph();

	TGraphErrors* gr1 = new TGraphErrors();
        gr1->SetName("gr1");
        gr1->SetTitle("");
        gr1->SetMarkerStyle(21);
        gr1->SetDrawOption("AP");
        gr1->SetLineColor(2);
        gr1->SetLineWidth(4);
        gr1->SetFillStyle(0);
        
        
        TGraphErrors* gr2 = new TGraphErrors();
        gr1->SetName("gr2");
        gr1->SetTitle("");
        gr1->SetMarkerStyle(21);
        gr1->SetDrawOption("AP");
        gr1->SetLineColor(2);
        gr1->SetLineWidth(4);
        gr1->SetFillStyle(0);
        
        
        
        int N = HV.size();
        for ( int i = 0; i < N; i++ ) {
                gr1->SetPoint(i, th[i], count[i]);
                gr1->SetPointError(i, 0. , count_err[i]);
        }
        
        for ( int i = 0; i < N; i++ ) {
                gr2->SetPoint(i, th[i], count[i] + 800 );
                gr2->SetPointError(i, 0. , count_err[i]);
        }

        mg->Add(gr1,"PL");
        mg->Add(gr2,"PL");
        
	canva -> cd();
        mg->Draw("A");
        canva->BuildLegend();
        canva -> Update();
        myApp -> Run();
        
        return 0;
}

