import sherpa_onnx, soundfile as sf, json, sys
d=sys.argv[1]
r=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d+'/encoder.int8.onnx',decoder=d+'/decoder.int8.onnx',joiner=d+'/joiner.int8.onnx',tokens=d+'/tokens.txt',model_type='nemo_transducer',num_threads=4)
a,sr=sf.read(sys.argv[2],dtype='float32')
out=[]; seg=20*sr; i=0
# chunk ~20s with overlap handled by cutting at quiet points
import numpy as np
pos=0
while pos<len(a):
    end=min(len(a),pos+seg)
    if end<len(a):
        w=a[end-3*sr:end]; e=np.convolve(w**2,np.ones(1600)/1600,'same'); end=end-3*sr+int(np.argmin(e))
    s=r.create_stream(); s.accept_waveform(sr,a[pos:end]); r.decode_stream(s)
    res=s.result
    out.append({'off':pos/sr,'text':res.text,'tokens':list(res.tokens),'ts':[t+pos/sr for t in res.timestamps]})
    pos=end
json.dump(out,open(sys.argv[3],'w'),ensure_ascii=False,indent=0)
for o in out: print(round(o['off'],2),o['text'])
