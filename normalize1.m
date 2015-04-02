function normalize1(filedir)


dBN = 70; 

%% read all sounds
filedir = 'experiment data/SoundsForExperiment';
files = dir([filedir filesep '*.wav']); 

for i=1:length(files), 
    
    fprintf(1,'normalize %s...',files(i).name); 
    
    filename = [filedir filesep files(i).name];
    [x,sr]=wavread(filename); 
    
    
    %% convert to mono
    if(size(x,2)==2)
        x=.5*(x(:,1)+x(:,2));
    end
          
    %% compute dBA
    loudness=sones(x,sr); 
    
    fprintf(1,'sonie %.2fdBA, ',loudness); 
    
    %% normalize
    x=10^((dBN-loudness)/20)*x;
    
    %% check
    loudness=sones(x,sr); 
    fprintf(1,'new sonie %.2fdA, ',loudness); 
    
    
    %% save resampled sound
    filename2 = [filedir filesep 'norm' filesep files(i).name];
    warning off
    wavwrite(x,sr,filename2);
    warning on 
    fprintf(1,'done\n'); 
end


function s = sones(x,sr)
p.fs          = sr;
p.do_sone     = 0;         %% compute dBA
specific_sones = ma_sone(x,p);
sones = max(specific_sones);
s=max(sones);

