// c++ -o logic2scinti logic2scinti.cpp `root-config --cflags --glibs`
// ./logic2scinti logic_data_2scinti.txt

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
	
	double x, y;
	vector <double> delay;
	vector <double> counts;
	
	int Ndata = 0;
	while (true) {
		in >> x >> y;
		if (in.eof() == true) break;
		delay.push_back( x );
		counts.push_back( y );
		Ndata++;
	}
	in.close();
	int N = Ndata;

	TGraphErrors* graph = new TGraphErrors;
	for (int i=0; i < N; i++) {
		graph->SetPoint(i, delay[i], counts[i] );
		graph->SetPointError(i, 0., 1./sqrt(counts[i]) );
	}
	
	graph->GetXaxis()->SetTitle("Delay[ns]");
	graph->GetYaxis()->SetTitle("Counts");
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
