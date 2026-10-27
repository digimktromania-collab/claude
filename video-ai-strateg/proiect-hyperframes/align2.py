import json,re,difflib,unicodedata,sys
d=json.load(open(sys.argv[1]))
toks=[];
for c in d: toks+=list(zip(c['tokens'],c['ts']))
words=[]
for t,ts in toks:
    if t.startswith(' ') or not words: words.append([t.strip(),ts,ts])
    else: words[-1][0]+=t; words[-1][2]=ts
asr=[]
for i,(w,s,e) in enumerate(words):
    nxt=words[i+1][1] if i+1<len(words) else e+0.5
    asr.append({'w':w,'s':s,'e':min(nxt,e+0.35)})
def norm(w):
    w=unicodedata.normalize('NFD',w.lower()); w=''.join(c for c in w if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]','',w)
sw=open(sys.argv[2]).read().split()
A=[norm(x['w']) for x in asr]; S=[norm(x) for x in sw]
# fuzzy alignment via DP on similarity
import numpy as np
n,m=len(S),len(A)
sim=lambda a,b: difflib.SequenceMatcher(None,a,b).ratio()
D=np.full((n+1,m+1),1e9); D[0,:]=np.arange(m+1)*0.6; D[:,0]=np.arange(n+1)*0.6; P={}
for i in range(1,n+1):
    for j in range(max(1,i-40),min(m,i+40)+1):
        c=1-sim(S[i-1],A[j-1])
        opts=[(D[i-1,j-1]+c*1.2,'m'),(D[i-1,j]+0.6,'s'),(D[i,j-1]+0.6,'a')]
        D[i,j],P[i,j]=min(opts)
i,j=n,m; match={}
while i>0 and j>0:
    p=P.get((i,j),'s' if i>j else 'a')
    if p=='m':
        if sim(S[i-1],A[j-1])>0.3: match[i-1]=j-1
        i-=1;j-=1
    elif p=='s': i-=1
    else: j-=1
out=[]
for k,w in enumerate(sw):
    if k in match: a=asr[match[k]]; out.append({'w':w,'s':round(a['s'],2),'e':round(a['e'],2),'m':1})
    else: out.append({'w':w,'s':None,'e':None,'m':0})
# interpolate
for k,o in enumerate(out):
    if o['s'] is None:
        p=next((out[x] for x in range(k-1,-1,-1) if out[x]['m']),None); q=next((out[x] for x in range(k+1,len(out)) if out[x]['m']),None)
        s=p['e'] if p else 0; e=q['s'] if q else s+0.4
        o['s']=round(s,2); o['e']=round(max(e,s+0.15),2)
json.dump(out,open(sys.argv[3],'w'),ensure_ascii=False,indent=0)
print(sum(o['m'] for o in out),'/',len(out),'matched')
print(' '.join(f"{o['w']}[{o['s']}]" + ('' if o['m'] else '*') for o in out))
