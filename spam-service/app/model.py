import os, joblib, numpy as np
from scipy.sparse import hstack
from catboost import CatBoostClassifier

ART = os.getenv("ARTIFACTS_DIR","artifacts")

class SpamCascade:
    def __init__(self):
        self.layer1 = joblib.load(f"{ART}/layer1_logreg.joblib")
        self.vec_word, self.vec_char = joblib.load(f"{ART}/tfidf.joblib")
        cfg = joblib.load(f"{ART}/config.joblib")
        self.top_idx=cfg["top_idx"]; self.META_COLS=cfg["META_COLS"]
        self.TAU_LOW=cfg["TAU_LOW"]; self.TAU_HIGH=cfg["TAU_HIGH"]; self.TAU_FINAL=cfg["TAU_FINAL"]
        self.layer2 = CatBoostClassifier(); self.layer2.load_model(f"{ART}/layer2_catboost.cbm")

    def predict(self, texts, metas):
        meta = np.array([[m[c] for c in self.META_COLS] for m in metas], dtype=float)
        X = hstack([self.vec_word.transform(texts), self.vec_char.transform(texts)]).tocsr()
        s1 = self.layer1.predict_proba(X)[:,1]
        final = s1.copy(); source = np.array(["layer1"]*len(texts), dtype=object)
        idx = np.where((s1>=self.TAU_LOW)&(s1<=self.TAU_HIGH))[0]
        if len(idx):
            top = X[idx][:, self.top_idx].toarray()
            s2 = self.layer2.predict_proba(np.hstack([meta[idx], s1[idx].reshape(-1,1), top]))[:,1]
            final[idx]=s2; source[idx]="layer2"
        label = (final>=self.TAU_FINAL).astype(int)
        return final, label, source
