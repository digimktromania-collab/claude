import numpy as np, wave, sys, os
SR=44100; out=sys.argv[1]
rng=np.random.default_rng(7)
def save(name,x):
    x=np.clip(x/ (np.max(np.abs(x))+1e-9)*0.89,-1,1)
    w=wave.open(os.path.join(out,name),'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
def t(d): return np.arange(int(SR*d))/SR
def lp(x,a):  # one-pole lowpass, a in 0..1 per-sample (array or scalar)
    y=np.zeros_like(x); a=np.broadcast_to(a,x.shape); s=0.0
    for i in range(len(x)): s+=a[i]*(x[i]-s); y[i]=s
    return y
# whoosh: noise with sweeping lowpass + bell envelope
d=0.45; tt=t(d); n=rng.standard_normal(len(tt))
sweep=0.02+0.35*np.sin(np.pi*tt/d)**2
env=np.sin(np.pi*tt/d)**1.6
w=lp(n,sweep)-lp(n,sweep*0.25); save('whoosh.wav',w*env)
# pop: short sine with pitch drop
tt=t(0.12); f=900*np.exp(-tt*35)+250; ph=2*np.pi*np.cumsum(f)/SR
save('pop.wav',np.sin(ph)*np.exp(-tt*40))
# click: tiny filtered transient
tt=t(0.04); save('click.wav',lp(rng.standard_normal(len(tt)),0.5)*np.exp(-tt*180)+0.6*np.sin(2*np.pi*2200*tt)*np.exp(-tt*120))
# ding: bell partials
tt=t(1.4); x=sum(a*np.sin(2*np.pi*f*tt)*np.exp(-tt*k) for f,a,k in [(1318,1,3),(2637,.4,5),(3951,.2,7),(1975,.25,4)])
save('ding.wav',x*(1-np.exp(-tt*400)))
# riser: noise + rising tone, 1.2s, ends abruptly
d=1.2; tt=t(d); f=200*(8**(tt/d)); ph=2*np.pi*np.cumsum(f)/SR
n=lp(rng.standard_normal(len(tt)),0.05+0.6*(tt/d)**2)
save('riser.wav',(0.5*np.sin(ph)+n)*(tt/d)**2)
# lo-fi music: 4 chords, ~70bpm loop of 8 bars, rhodes-ish + soft kick/hat + vinyl crackle
bpm=72; beat=60/bpm; bar=4*beat; chords=[[57,60,64,67],[53,57,60,64],[55,59,62,65],[52,55,59,62]] # Am7 Fmaj7 G7ish Em7
total=8*bar; N=int(SR*total); mus=np.zeros(N)
def mf(m): return 440*2**((m-69)/12)
for b in range(8):
    s=int(b*bar*SR); tt=t(bar); ch=chords[b%4]
    for m in ch:
        f=mf(m); tone=np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*3)
        mus[s:s+len(tt)]+=0.18*tone*np.exp(-tt*0.9)*(1+0.15*np.sin(2*np.pi*4*tt))
    bass=np.sin(2*np.pi*mf(ch[0]-24)*tt)*np.exp(-tt*1.2); mus[s:s+len(tt)]+=0.35*bass
    for k in range(4):
        ks=s+int(k*beat*SR); kt=t(0.25)
        if k in (0,2): kf=60+90*np.exp(-kt*30); mus[ks:ks+len(kt)]+=0.6*np.sin(2*np.pi*np.cumsum(kf)/SR)*np.exp(-kt*12)
        if k in (1,3): st=t(0.18); mus[ks:ks+len(st)]+=0.15*rng.standard_normal(len(st))*np.exp(-st*25)
        for h in (0,0.5):
            hs=ks+int(h*beat*SR); ht=t(0.05); mus[hs:hs+len(ht)]+=0.05*np.diff(np.r_[0,rng.standard_normal(len(ht))])*np.exp(-ht*80)
mus=lp(mus,0.25)  # warm it up
crack=np.zeros(N); idx=rng.integers(0,N,400); crack[idx]=rng.standard_normal(400)*0.3
mus+=lp(crack,0.4)+0.004*rng.standard_normal(N)
save('lofi.wav',mus)
