import subprocess, numpy as np, sys, soundfile as sf
f=sys.argv[1]; W,H=144,256
raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'fps=30,scale={W}:{H}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
v=np.frombuffer(raw,np.uint8).reshape(-1,H,W).astype(np.float32)
# lower-face region (mouth/jaw) - broad box
reg=v[:, int(H*0.42):int(H*0.62), int(W*0.0):int(W*0.6)]
m=np.abs(np.diff(reg,axis=0)).mean(axis=(1,2)); m=np.concatenate([[0],m])
subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-ac','1','-ar','16000',f+'.wav'])
a,sr=sf.read(f+'.wav'); hop=sr//30
env=np.array([np.sqrt((a[i*hop:(i+1)*hop]**2).mean()) if i*hop<len(a) else 0 for i in range(len(m))])
def z(x): x=x-np.convolve(x,np.ones(15)/15,'same'); return (x-x.mean())/(x.std()+1e-9)
win=300
for st in range(0,len(m)-win,150):
    mm=z(m[st:st+win]); ee=z(env[st:st+win]); best=None
    for lag in range(-20,21):  # lag>0: audio later than video
        if lag>=0: c=np.mean(mm[:win-lag]*ee[lag:])
        else: c=np.mean(mm[-lag:]*ee[:win+lag])
        if best is None or c>best[1]: best=(lag,c)
    print(f"t={st/30:5.1f}s lag={best[0]/30*1000:+5.0f}ms corr={best[1]:.2f}")
