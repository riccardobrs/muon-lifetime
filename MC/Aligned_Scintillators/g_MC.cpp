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
#include <TH2D.h>
#include <TLatex.h>
#include <TMatrixDSym.h>
#include <TRandom3.h>
#include <TStyle.h>

using namespace std;


double mu_distribution(double x) {
    
    return pow(cos(x), 3)*sin(x);
    
}

//Try & Catch method
double rand_TAC(double xMin, double xMax, double yMin,double yMax, TRandom3* rand) {
    
    double x = 0. , y = 0.;
    
    do {
        x = rand->Uniform(xMin,xMax);
        y = rand->Uniform(yMin,yMax);
    } while( y > mu_distribution(x) );
    
    return x;
    
}

double GetX_zfixed(double x0, double z0, double z, double theta, double phi) {
    
    return x0 + (z - z0) * tan(theta) * cos(phi);
    
}

double GetY_zfixed(double y0, double z0, double z, double theta, double phi) {
    
    return y0 + (z - z0) * tan(theta) * sin(phi);
    
}

//MC estimation of geometrical efficiency
double MC(double L, double l, double zup, double zdown, int N_MC, int M, int NBin, string outname) {
    
    double theta;   //zenith
    double phi;     //azimutal
        
    double x1, y1;
    double x3, y3;

    int N_coinc, N_tot;               

    double g;            //geometrical efficiency
    double gmin = 1.;
    double gmax = 0.;
    
    TRandom3 * R = new TRandom3(time(NULL));
    
    TCanvas* canva = new TCanvas();
    TCanvas* c_x = new TCanvas();
    TCanvas* c_y = new TCanvas();
    TCanvas* c_xy_1 = new TCanvas();
    TCanvas* c_xy_2 = new TCanvas();
    TCanvas* c_phi = new TCanvas();
    TCanvas* c_theta = new TCanvas();
    TH1D * histo = new TH1D("Statistical box", "", NBin, 0., 0.);
    TH1D * h_x = new TH1D("x statistical box", "", 50, 0., l);
    TH1D * h_y = new TH1D("y statistical box", "", 50, 0., L);
    TH2D * h_xy = new TH2D("stats", "", 60, 0., l, 160, 0., L);
    TH1D * h_phi = new TH1D("#varphi statistical box", "", 50, 0., 2*M_PI);
    TH1D * h_theta = new TH1D("#theta statistical box", "", 50, 0., M_PI/2);
    TF1 * gauss_distrib;
    TF1 * mu_distrib;
    
    for (int j = 0; j < N_MC; j++) {
        
        //print status
        if (j == N_MC/10)
            cout << "MC generation status: 10%" << endl;
        if (j == N_MC*2/10)
            cout << "MC generation status: 20%" << endl;
        if (j == N_MC*3/10)
            cout << "MC generation status: 30%" << endl;
        if (j == N_MC*4/10)
            cout << "MC generation status: 40%" << endl;
        if (j == N_MC*5/10)
            cout << "MC generation status: 50%" << endl;
        if (j == N_MC*6/10)
            cout << "MC generation status: 60%" << endl;
        if (j == N_MC*7/10)
            cout << "MC generation status: 70%" << endl;
        if (j == N_MC*8/10)
            cout << "MC generation status: 80%" << endl;
        if (j == N_MC*9/10)
            cout << "MC generation status: 90%" << endl;
        if (j == N_MC-1)
            cout << "MC generation status: 100%" << endl << endl;
        
        N_coinc = 0;
        N_tot = 0;
        
        for (int i = 0; i < M; i++) {
            
            //Generate an incoming muon on the upper scintillator
            x1 = R -> Uniform(0., l);
            y1 = R -> Uniform(0, L);
            theta = rand_TAC(0., M_PI/2, 0., 3.*sqrt(3)/16, R);
            phi = R -> Uniform(0., 2 * M_PI);
            
            if (j==0) {
                
                h_x -> Fill(x1);
                h_y -> Fill(y1);
                h_xy -> Fill(x1, y1);
                h_phi -> Fill(phi);
                h_theta -> Fill(theta);
            
            }
                            
            //lower scintillator coords
            x3 = GetX_zfixed(x1, zup, zdown, theta, phi);
            y3 = GetY_zfixed(y1, zup, zdown, theta, phi);
            
            if (x3 >= 0. && x3 <= l && y3 >= 0. && y3 <= L)
                N_coinc++;
            
            N_tot++;
                    
        }
                
        g = ((double)N_coinc) / N_tot;
        
        if (g < gmin)
            gmin = g;
        if (g > gmax)
            gmax = g;
        
        histo -> Fill(g);

    }
    
    histo -> GetXaxis() -> SetTitle("g");
    histo -> GetYaxis() -> SetTitle("Counts");
    h_x -> GetXaxis() -> SetTitle("x [cm]");
    h_x -> GetYaxis() -> SetTitle("Counts");
    h_y -> GetXaxis() -> SetTitle("y [cm]");
    h_y -> GetYaxis() -> SetTitle("Counts");
    h_xy -> GetXaxis() -> SetTitle("x [cm]");
    h_xy -> GetYaxis() -> SetTitle("y [cm]");
    //h_xy -> GetZaxis() -> SetTitle("Counts");
    h_phi -> GetXaxis() -> SetTitle("#varphi [rad]");
    h_phi -> GetYaxis() -> SetTitle("Counts");
    h_phi -> GetXaxis() -> SetTitleSize(0.042);
    h_theta -> GetXaxis() -> SetTitle("#theta [rad]");
    h_theta -> GetYaxis() -> SetTitle("Counts");
    h_theta -> GetXaxis() -> SetTitleSize(0.042);
    
    gauss_distrib = new TF1 ("gauss_distrib", "gaus", gmin, gmax);
    gauss_distrib -> SetParameter(1, 0.81);
    
    gStyle -> SetOptStat(11);
    gStyle -> SetOptFit(1112);
    
    canva -> cd();
    histo -> Draw();
    
    TFitResultPtr fit_result = histo -> Fit("gauss_distrib", "RS", "sames");
    TMatrixDSym covariance_matrix = fit_result -> GetCovarianceMatrix();
    
    g = gauss_distrib -> GetParameter(1);
    
    canva -> Modified();
    canva -> Update();
    canva -> SaveAs(outname.c_str());
    delete histo;
    
    mu_distrib = new TF1 ("mu_distrib", "[0]*cos(x)*cos(x)*cos(x)*sin(x)", 0., M_PI/2);
    mu_distrib -> SetParameter(0, M*3.*sqrt(3)/16);
    mu_distrib -> SetParName(0, "Amp");
    c_theta -> cd();
    h_theta -> Draw();
    TFitResultPtr fit_theta = h_theta -> Fit("mu_distrib", "RS", "sames");
    TMatrixDSym covariance_matrix_mu = fit_theta -> GetCovarianceMatrix();
    c_theta -> Modified();
    c_theta -> Update();
    c_theta -> SaveAs("theta.root");
    delete h_theta;
    
    gStyle -> SetOptStat(10);
    
    c_x -> cd();
    h_x -> Draw();
    c_x -> Modified();
    c_x -> Update();
    c_x -> SaveAs("x.root");
    delete h_x;
    
    c_y -> cd();
    h_y -> Draw();
    c_y -> Modified();
    c_y -> Update();
    c_y -> SaveAs("y.root");
    delete h_y;
    
    c_phi -> cd();
    h_phi -> Draw();
    c_phi -> Modified();
    c_phi -> Update();
    c_phi -> SaveAs("phi.root");
    delete h_phi;
    
    
    h_xy -> SetStats(0);
    
    c_xy_1 -> cd();
    h_xy -> Draw("COLZ");
    c_xy_1 -> Modified();
    c_xy_1 -> Update();
    c_xy_1 -> SaveAs("xy1.root");
    
    c_xy_2 -> cd();
    h_xy -> Draw("0LEGO2Z PFC");
    c_xy_2 -> Modified();
    c_xy_2 -> Update();
    c_xy_2 -> SaveAs("xy2.root");
    
    delete h_xy;
    
    return g;
    
}

//retrieve var_name value from config file
string ReadConfig(string filename, string var_name) {
    
    ifstream ConfigFile;
    string line;
    string value = "";
    
    ConfigFile.open(filename);
    
    if (not ConfigFile.is_open()) {
            cout << "An error occured while opening config.txt" << endl;
            return 0;
    }
    
    while (getline(ConfigFile, line)) {
        
        if (line.find(var_name) != string::npos) {
            
            value = line.replace(0, 6, "");
            cout << "Found " << var_name << " = " << value << endl;
            break;
            
        }
    }
    
    ConfigFile.close();
    
    return value;
    
}

//write output file
void WriteOutput(string filename, string s) {
    
    ofstream OutFile;
    
    OutFile.open(filename, ofstream::out);
    OutFile << s << endl;

    OutFile.close();
    
    return;

}

int main (int argc, char ** argv) {
    
    string config = "config.txt";
    
    double L = stod(ReadConfig(config, "L"));           //scintillator length
    double l = stod(ReadConfig(config, "l"));           //scintillator width
    double zup = stod(ReadConfig(config, "zup"));       //upper scintillator height
    double zdown = stod(ReadConfig(config, "zdown"));   //lower scintillator height
    
    int M = stod(ReadConfig(config, "Muons"));          //number of muons
    int N_MC = stod(ReadConfig(config, "N_MC"));        //number of MC simulations
    int NBin = stod(ReadConfig(config, "NBin"));        //number of bins in the histogram
    
    double g = MC(L, l, zup, zdown, N_MC, M, NBin, "g.root");
    
    stringstream outresults;
    
    cout << endl << "****************" << endl << endl;
    cout << "g (MC) = " << g << endl;
    
    outresults << endl << "g (MC) = " << g << endl;
    WriteOutput("g.txt", outresults.str());
    
    return 0;
    
}
