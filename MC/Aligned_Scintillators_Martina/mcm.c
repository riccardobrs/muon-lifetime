

#define MAIN_PROGRAM
#include <limits.h>
#include <float.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "start.h"
#include "random.h"

#define M_PI 3.14159265358979323846264338327950288
/* FUNZIONE DISTRIBUZIONE ANGOLO TETA */
double func (float x) {

return cos(x)*cos(x);

}


int main (void) {
/* DICHIARO LE VARIABILI  */
    int N_sweep=500;
    int N=25000;
    int L1=80;
    int L2=30;
    
    float eff=0.0;
    float eff2[N];
    float sigma2;
   

    
    float x[N];
    float y[N];

    float x1[N];
    float y1[N];

    float x2[N];
    float y2[N];
    float sum=0.0;
    float sum2=0.0;
    float mean;
    float mean2;
    float sigma;
    float var;

    
    int scint1[L1][L2];
    int scint2[L1][L2];
    int scint3[L1][L2];
   
    /* DICHIARO I FILE */

    FILE *sci1;
    FILE *sci2;
    FILE *sci3;
    
    sci1=fopen("scintillatore1m.txt","w+");
    sci2=fopen("scintillatore2m.txt","w+");
    sci3=fopen("scintillatore3m.txt","w+");
    
    float theta[N];
    float phi[N];
   
    float f_0[N];
    
   
    float h=1.9;
    int i=0;
    int j=0;
    int k=0;
    int t=0;
    
    for(i=0;i<L1;i++) {
        for(k=0;k<L2;k++) {
            scint1[i][j]=0;
            scint2[i][j]=0;
            scint3[i][j]=0;
        }
    }
    
    for (i=0; i<N_sweep; i++) {
    
    float Nt=0.0;
    float Nd=0.0;

rlxs_init(0,3090+i);     //inizializzazione

ranlxs(x,N);     //generatore di numeri casuali
    
ranlxs(y,N);
    
ranlxs(theta,N);

ranlxs(phi,N);
    
ranlxs(f_0,N);
    
  
        
    
    for(j=0;j<N; j++) {

    
    x[j]=x[j]*L1;

    y[j]=y[j]*L2;

    theta[j]=(theta[j]*M_PI)-0.5*M_PI ;

    phi[j]=(phi[j]*(2*M_PI))-M_PI ;

    f_0[j]=f_0[j]*(3*sqrt(3)/16) ;
        
    }
        
        for(j=0;j<N;j++){
      
        for(k=0;k<L1; k++){
            
            if(x[j]>=(L1/L1)*(k) && x[j]<=(L1/L1)*(k+1)){
                
                for (t=0;t<L2; t++){
                
              
                    if(y[j]>=(L2/L2)*(t) && y[j]<=(L2/L2)*(t+1)){
                       
                        scint1[k][t] +=1;
                        
                        
                    }
                    
                
                }
            }
            


    }
            }
        
        for(j=0;j<N;j++) {
         
 
        if(func(theta[j])<f_0[j]){
            
            
            x1[j]=x[j]+(h/cos(theta[j]))*sin(theta[j])*cos(phi[j]);
            y1[j]=y[j]+(h/cos(theta[j]))*sin(theta[j])*sin(phi[j]);
            x2[j]=x[j]+(2*h/cos(theta[j]))*sin(theta[j])*cos(phi[j]);
            y2[j]=y[j]+(2*h/cos(theta[j]))*sin(theta[j])*sin(phi[j]);
        
            if(x1[j]>=0.0 && x1[j]<=L1 && y1[j]>=0.0 && y1[j]<=L2 && x2[j]>=0.0 && x2[j]<=L1 && y2[j]>=0.0 && y2[j]<=L2){
                
                Nt+=1;
                
                for(k=1;k<=L1; k++){
                   
                    if (x2[j]>(L1/L1)*(k-1) && x2[j]<(L1/L1)*k){
                        
                        for (t=1;t<=L2; t++){
                        if(y2[j]>(L2/L2)*(t-1) && y2[j]<(L2/L2)*t){
                    
                                
                                scint3[k-1][t-1]+=1;
                                
                                }
                        }
                    }
                }
                
                
            }
            if(x1[j]>=0.0 && x1[j]<=L1 && y1[j]>=0.0 && y1[j]<=L2) {
                Nd+=1;

         for(k=1;k<=L1; k++){
            
                    if(x1[j]>(L1/L1)*(k-1) && x1[j]<(L1/L1)*k){
                        
                        for (t=1;t<=L2; t++){

                            if(y1[j]>(L2/L2)*(t-1) && y1[j]<(L2/L2)*t) {
                                
                               scint2[k-1][t-1]+=1;
                                

                            }
                          
                            
                        }
                    }
            
                }
        }

    


        

 
        
}
    

}

    eff=Nt/Nd;
    sum+=eff;
    eff2[i]=eff*eff;
    sum2+=eff2[i];
   //printf("eff= %f\n",eff);
   //fprintf(dati,"%f  %d\n",eff,i);
   

}
    
    
    for(i=0;i<L1;i++) {
        for(k=0;k<L2;k++) {
            fprintf(sci1,"%d  %d  %d\n", i,k,scint1[i][k]);
            fprintf(sci2,"%d  %d  %d\n", i,k,scint2[i][k]);
            fprintf(sci3,"%d  %d  %d\n", i,k,scint3[i][k]);
            
        }
    }
    
    fclose(sci1);
    fclose(sci2);
    fclose(sci3);
    mean=sum/N_sweep;
    mean2=sum2/N_sweep;
    sigma=mean2-(mean*mean);
    sigma2=sigma/mean;
  

    var=sqrt(sigma);
    printf("mean= %f\n",mean);
    printf("var= %f\n",var);
    printf("errore relativo= %f\n",sigma2);
   
    }

