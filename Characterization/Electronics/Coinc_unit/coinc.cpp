// c++ -o logic_1scinti logic_1scinti.cpp `root-config --cflags --glibs`
// ./logic_1scinti logic_data_1scinti.txt

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

double funz (double* x, double* par) {
  return par[0] / ( 1 + exp( par[1] * (x[0] - par[2] ) ) ) ; 
}

int main (int argc, char ** argv) {

	TApplication* myApp = new TApplication ("myApp", NULL, NULL);
	TCanvas* canva = new TCanvas("canva","",100,200,700,500);
	
	string fileInput = argv[1];
	ifstream in (fileInput.c_str());
	if (in.good() == false) {
		cout << "Errore di apertura file" << endl;
		return 1;
	}
	
	double x, y, z;
	vector <double> delay;
	vector <double> count_forward;
	vector <double> count_delay;
	vector <double> count_forward_err;
	vector <double> count_delay_err;
	vector <double> ratio;
	vector <double> ratio_err;
    vector <double> real_delay;
    vector <double> real_delay_err;

    
    
    int Ndata = 0;
	while (true) {
		if (in.eof() == true) break;
        in >> x >> y >> z;
        Ndata++;
		delay.push_back( x );
		count_forward.push_back( y );
		count_delay.push_back( z );
    }
	in.close();
	int N = Ndata;
    

    
    for (int i = 0; i < N; i++ ) {
        
        ratio.push_back(count_delay[i] / count_forward[i]);
        //ratio_err.push_back(sqrt((ratio[i] * ( 1. - ratio[i])) / count_forward[i]));
        ratio_err.push_back(sqrt(count_delay[i]/(count_forward[i]*count_forward[i] ) +(count_delay[i]*count_delay[i])/(count_forward[i]*count_forward[i]*count_forward[i])));
                                 
                                 
                                 //cout << ratio_err[i] << endl;
    }
    
  
    for (int i = 0; i < N; i++ ){
        real_delay.push_back(1.026*delay[i]-0.65);
        real_delay_err.push_back(sqrt(0.08*0.08+((real_delay[i]*0.003)*(real_delay[i]*0.003))+2*real_delay[i]*(-0.00022)));
        
    }
  
    
    
    TGraphErrors* graph = new TGraphErrors;
    
	for (int i=0; i < N; i++) {
		graph->SetPoint(i, real_delay[i],ratio[i]);
		graph->SetPointError(i,real_delay_err[i], ratio_err[i]);
	}
	
    graph->GetXaxis()->SetTitle("Delay[ns]");
	graph->GetYaxis()->SetTitle("Fraction of coincidences");
	//graph->SetTitle("Logic Unit (signal splitting)");
	graph->SetMarkerStyle(20);
	graph->SetMarkerSize(0.8);
	graph->SetMarkerColor(kRed);
	
	double min = 3.;
	double max = 40;
	
	double nPar = 3;
	TF1* f = new TF1("funz", funz, min, max,nPar);
	f -> SetParameter (0, 1.);
	f -> SetParameter (1,1);
	f -> SetParameter (2,33.);
	f->SetParName(0,"f_0");
	f->SetParName(1,"k");
	f->SetParName(2,"t_0");
	f -> SetLineColor(kBlue);
	
	gStyle->SetOptFit(1112);
	

        canva->cd();
        	
	graph->Draw("AP");
    TFitResultPtr r = graph->Fit("funz", "SR");
            TMatrixDSym covariance_matrix = r -> GetCovarianceMatrix();
            TMatrixDSym correlation_matrix = r -> GetCorrelationMatrix();
        f->Draw("same");
            
        canva->Modified();
        canva->Update();
        
        
        const char * filename = "coinc_unit_result.txt";
            ofstream outfile (filename);
        
        //--------Fit------------------
            outfile << "INTERPOLAZIONE" << endl;
            outfile  << "\nMatrice di covarianza " << endl;
            for (int i = 0; i < nPar; i++) {
              cout << setw(15) << f->GetParName(i);
            }
            outfile  << endl;
           
            for (int i=0; i<nPar; i++) {
                outfile  << f->GetParName(i);
            for (int j=0; j<nPar; j++) {
            double sigma_ij = covariance_matrix(i,j);
            outfile << setw(15)<< sigma_ij;
          }
          outfile << endl;
        }
        
            outfile << "\nMatrice di correlazione " << endl;
            for (int i = 0; i < nPar; i++) {
              outfile << setw(15) << f->GetParName(i);
            }
            outfile << endl;
           
            for (int i=0; i<nPar; i++) {
          outfile << f->GetParName(i);
          for (int j=0; j<nPar; j++) {
            double ro_ij = correlation_matrix(i,j);
            outfile << setw(15) << ro_ij;
          }
          outfile << endl;
        }

        outfile << endl << "VALORI RESTITUITI DA ROOT" << endl;
        outfile << "Gradi di libertà = " << f->GetNDF() << endl;
        outfile << "Chi2 = " << f->GetChisquare() << endl;
        outfile << "Reduced Chi2 = " << f->GetChisquare() / f->GetNDF() << endl;
        outfile << "p-value = " << f->GetProb() << endl;
        
           outfile << "** STIMA PARAMETRI**" << endl;
        outfile << "f_0 = " << f-> GetParameter(0) << " +- " << f -> GetParError(0) << endl;
        outfile << "k = " << f -> GetParameter(1) << " +- " << f -> GetParError(1) << endl;
        outfile << "t_0 = " << f -> GetParameter(2) << " +- " << f -> GetParError(2) << endl;
        

        myApp->Run();

        return 0;

    }

	





