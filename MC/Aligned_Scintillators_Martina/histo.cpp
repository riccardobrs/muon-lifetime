//
//  histo.cpp
//  Programmi
//
//  Created by Martina D'Aloia on 04/01/2020.
//  Copyright © 2020 Martina D'Aloia. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include "TStyle.h"
#include "TCanvas.h"
#include <TGraphErrors.h>
#include "TH1D.h"
#include "TGraph.h"
#include "TF1.h"
#include "TApplication.h"
#include <iomanip>
//#include "mylib.h"
#include<TRandom.h>
#include <TH2F.h>
#include <TMath.h>
#include "TView3D.h"
#include "TAxis3D.h"
#include "TPolyLine3D.h"
#include "THStack.h"

//c++ -o histo  histo.cpp `root-config --glibs --cflags`



using namespace std;

void DoIt (string filename) {

    gStyle -> SetOptFit(1);
   gStyle->SetOptStat(kTRUE);
    ifstream in (filename.c_str());
    float x;
    float y;
   
    TH1D *gauss = new TH1D ("gauss", "  Geometric Efficiency",100, 0.67,0.72); //
    gauss->GetXaxis()->SetTitle("Efficiency");
    gauss->GetYaxis()->SetTitle("Entries");
    TF1 *f1 = new TF1("f1","gaus"); //0.878329,0.893017);
  
    f1->SetLineColor(kRed);
    f1->SetLineWidth(8);
    
    while(1) {
        in >> x >> y ;
        if (in.eof() == true) break;
       gauss->Fill(x,y);
             gauss->Fit("f1");
        gauss->Draw("SAME HISTO");

    }
   
    in.close();
    
}

int main (int argc, char** argv)  {
    TApplication *myApp = new TApplication ("App", 0, 0);
    
    //stampa a schermo dei parametri passati da riga di comando
    cout << "Numero parametri: argc = "<<argc<<endl;
    cout << "Valori parametri:"<<endl;
    for (int i=0; i<argc; i++) cout << "    argv["<<i<<"] = "<< argv[i] << endl;
    
    //string filename = myApp-> Argv(1); //legge da riga comando
    DoIt ("gauss.txt");
   
    
    cout << "\nPer terminare il programma: CTRL+C "<<endl;
    myApp->Run();
    return 0;
}
