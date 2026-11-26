import sys,json,subprocess,numpy as np
src=sys.argv[1]; thr_off=float(sys.argv[2]) if len(sys.argv)>2 else 8
raw=subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','16000','-af','highpass=f=150,lowpass=f=4000','-f','s16le','-'],capture_output=True).stdout
x=np.frombuffer(raw,np.int16)/32768; hop=160; n=320
rms=np.array([np.sqrt(np.mean(x[i:i+n]**2))+1e-6 for i in range(0,len(x)-n,hop)]); db=20*np.log10(rms)
db=np.convolve(db,np.ones(5)/5,'same')
floor=np.percentile(db,10); thr=floor+thr_off
print('floor',round(floor,1),'thr',round(thr,1),file=sys.stderr)
quiet=db<thr; out=[]; i=0
while i<len(quiet):
    if quiet[i]:
        j=i
        while j<len(quiet) and quiet[j]: j+=1
        s,e=i*0.01,j*0.01
        if e-s>0.3: out.append([round(s,2),round(e,2)])
        i=j
    else: i+=1
json.dump(out,sys.stdout)
