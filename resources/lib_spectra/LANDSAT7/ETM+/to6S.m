
load /users/cabot/Spectral/Solar/nl.dat

rep6S(:,1:2)=nl;

for b=1:5

  R=load(sprintf('spectral_b%d.dat',b));
  rep6S(:,b+2) = interp1(R(:,1)/1000.0,R(:,2),rep6S(:,1)) ;
  
end

id=find(rep6S<0 | isnan(rep6S));
rep6S(id)=0;

save rep6S.dat rep6S /ascii

for b=1:5
    
    i0=min(find(rep6S(:,b+2)));
    i1=max(find(rep6S(:,b+2)));
    
    w0=rep6S(i0,1);
    w1=rep6S(i1,1);
    r =rep6S(i0:i1,b+2);
    
    f=fopen(sprintf('ETM_B%d.dat',b),'wt');
    fprintf(f,'%f %f\n',w0,w1);
    fprintf(f,'%f\n',r);
    fclose(f);
    
end
    
   
