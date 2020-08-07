//
//  sci1.cpp
//  Programmi
//
//  Created by Martina D'Aloia on 16/12/2019.
//  Copyright © 2019 Martina D'Aloia. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include "TStyle.h"
#include "TColor.h"
#include "TCanvas.h"
#include <TGraphErrors.h>
#include "TH2D.h"
#include "TGraph.h"
#include "TF1.h"
#include "TApplication.h"
#include <iomanip>
/*#include "mylib.h"*/
#include<TRandom.h>
#include <TH2F.h>
#include <TMath.h>
#include "TView3D.h"
#include "TAxis3D.h"
#include "TPolyLine3D.h"
#include "THStack.h"
using namespace std;

void DoIt (string filename) {

    gStyle -> SetOptFit(1);
   gStyle->SetPalette(55,0);
    ifstream in (filename.c_str());
    float x;
    float y;
    float z;
   THStack *hs = new THStack("hs","Muon Distribution SC2");
    TH2D *sci1 = new TH2D ("sci1", "sci1", 80, 0, 80, 30, 0, 30); //
   
    hs->Add(sci1);
    while(1) {
        in >> x >> y >>z ;
        if (in.eof() == true) break;
        sci1->Fill(x,y,z);

        hs->Draw("0lego2z PFC");
        
       //hs->GetXaxis()->SetTitle("cm");
      //hs->GetYaxis()->SetTitle("cm");

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
    DoIt ("scintillatore2m.txt");
   
    
    cout << "\nPer terminare il programma: CTRL+C "<<endl;
    myApp->Run();
    return 0;
}
