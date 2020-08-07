//
//  Gaussiana.c
//  Programmi
//
//  Created by Martina D'Aloia on 23/12/2019.
//  Copyright © 2019 Martina D'Aloia. All rights reserved.
//

#define MAIN_PROGRAM

#include <limits.h>
#include <float.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
//#include <malloc.h>
#include "start.h"
#include "random.h"

#define M_PI 3.14159265358979323846264338327950288

double func (float x) {

return cos(x)*cos(x);

}


int main (void) {
/* DICHIARO LE VARIABILI  */
    int N_sweep=500;
    int N=25000;
    
    
    float eff[N];
    
    float x[N];
    float y[N];
    
    float x1[N];
    float y1[N];
    
    float x2[N];
    float y2[N];
    int n[N_sweep];

   
    FILE *gauss;
  
    
    gauss=fopen("gauss.txt","w+");
   
    
    float theta[N];
    float phi[N];
   // float f[N];
    float f_0[N];
    float L1=80.0;
    float L2=30.0;
    //int count1 =0;
    //int count2=0;
    float h=1.9;
    int i=0;
    int j=0;
    int k=0;
   
  
    for (i=0; i<N_sweep; i++) {
    
    float Nt=0.0;
    float Nd=0.0;

rlxs_init(0,3090+i);     //inizializzazione

ranlxs(x,N);     //generatore di numeri casuali
    
ranlxs(y,N);
    
ranlxs(theta,N);

ranlxs(phi,N);
    
ranlxs(f_0,N);
    
    // printf("x = %f\n",x[i]);    //p=p+1;
        
    
    for(j=0;j<N; j++) {

    
    x[j]=x[j]*L1;

    y[j]=y[j]*L2;

    theta[j]=(theta[j]*M_PI)-0.5*M_PI ;

    phi[j]=(phi[j]*(2*M_PI))-M_PI ;

    f_0[j]=f_0[j]*(3*sqrt(3)/16) ;
        
    }
        
       
        for(j=0;j<N;j++) {
         
 
        if(func(theta[j])<f_0[j]){
            
            
            x1[j]=x[j]+(h/cos(theta[j]))*sin(theta[j])*cos(phi[j]);
            y1[j]=y[j]+(h/cos(theta[j]))*sin(theta[j])*sin(phi[j]);
            x2[j]=x[j]+(2*h/cos(theta[j]))*sin(theta[j])*cos(phi[j]);
            y2[j]=y[j]+(2*h/cos(theta[j]))*sin(theta[j])*sin(phi[j]);
        
            if(x1[j]>=0.0 && x1[j]<=L1 && y1[j]>=0.0 && y1[j]<=L2 && x2[j]>=0.0 && x2[j]<=L1 && y2[j]>=0.0 && y2[j]<=L2){
                
                Nt+=1;
                
                
                
                
            }
            if(x1[j]>=0.0 && x1[j]<=L1 && y1[j]>=0.0 && y1[j]<=L2) {
                Nd+=1;

        
        }
            
        }
    

}

    eff[i]=Nt/Nd;
        
    }
   
    float max;
    max=eff[0];
    for (i=0;i<N_sweep;i++){
        if(eff[i]>max){
            max=eff[i];
        }
    }
    
    printf("max= %f\n",max);
    
    
    float min;
    min=eff[0];
    for (i=0;i<N_sweep;i++){
      if(eff[i]<min){
          min=eff[i];
      }
  }
    
    printf("min= %f\n",min);
    
    float c;
    int bin =500;
    c=(max-min)/bin;
    
    for(i=0;i<N_sweep;i++){
        
        for(k=0;k<bin;k++){
            
        
        if(eff[i]>=min+(k*c) && eff[i]<=min+c*(k+1)){
            n[k]=n[k]+1;
          
            

    }
    }
    }
    float eff_rbin[N];
        for(k=0;k<500;k++){
            eff_rbin[k]=min+c*0.5*(2*k+1);
            fprintf(gauss,"%f %d\n",eff_rbin[k],n[k]);
        }
   
    
    fclose(gauss);
   
    
   
    }

