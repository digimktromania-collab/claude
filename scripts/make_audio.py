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

# ---------------- v2: meaningful sound design ----------------
def tone(f, d, decay, a=1.0):
    tt = t(d); return a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * decay)
def place(buf, x, at):
    s = int(at * SR); buf[s:s + len(x)] += x[:max(0, len(buf) - s)]; return buf
def mf2(m): return 440 * 2 ** ((m - 69) / 12)
# brand sting: bright rising arpeggio + shimmer
b = np.zeros(int(SR * 1.6))
for k, m in enumerate([72, 76, 79, 84]):
    n = tone(mf2(m), 1.3, 3.2) + 0.35 * tone(mf2(m) * 2, 1.3, 5) + 0.15 * tone(mf2(m) * 3, 1.3, 7)
    place(b, n * (1 - np.exp(-t(1.3) * 300)), k * 0.075)
save('sting.wav', b)
# success: two quick bright notes up
s2 = np.zeros(int(SR * 0.9)); place(s2, tone(mf2(79), 0.8, 6) + 0.3 * tone(mf2(91), 0.8, 9), 0); place(s2, tone(mf2(84), 0.8, 5) + 0.3 * tone(mf2(96), 0.8, 8), 0.09)
save('success.wav', s2)
# notification: soft two-tone glass chime
nt = np.zeros(int(SR * 1.2)); place(nt, tone(988, 1.0, 4) + 0.4 * tone(1976, 1.0, 7), 0); place(nt, tone(1319, 1.0, 3.5) + 0.4 * tone(2637, 1.0, 7), 0.13)
save('notify.wav', nt)
# mouse click: two tiny transients (press + release)
mc = np.zeros(int(SR * 0.12)); hit = lambda: lp(rng.standard_normal(int(SR * 0.012)), 0.7) * np.exp(-t(0.012) * 500) + 0.5 * np.sin(2 * np.pi * 3400 * t(0.012)) * np.exp(-t(0.012) * 400)
place(mc, hit(), 0); place(mc, 0.6 * hit(), 0.065)
save('mouseclick.wav', mc)
# send: short upward swoosh
d = 0.32; tt = t(d); n = rng.standard_normal(len(tt)); sw = lp(n, 0.03 + 0.5 * (tt / d) ** 2) * np.sin(np.pi * tt / d) ** 1.2
f = 400 * 6 ** (tt / d); sw += 0.25 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d)
save('send.wav', sw)
# typing: 3s of irregular soft key clicks (loopable)
ty = np.zeros(int(SR * 3.0)); pos = 0.02
while pos < 2.95:
    k = lp(rng.standard_normal(int(SR * 0.02)), 0.45 + 0.2 * rng.random()) * np.exp(-t(0.02) * 260) * (0.6 + 0.4 * rng.random())
    place(ty, k, pos); pos += 0.055 + 0.06 * rng.random()
save('typing.wav', ty)
