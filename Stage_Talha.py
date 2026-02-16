import medkit

from pathlib import Path #permet de faire des chemins
from medkit.io.medkit_json.text import load_text_document

doc = load_text_document(Path("/Users/talhasoylu/Desktop/StageDataScience/stage/pour_talha.json")) #json vers document texte

ents = list(doc.anns.entities) #list permet d'avoir la longueur et 
print("Nb entités:", len(ents)) #nbre d'entités présentes

for e in ents[:30]: #boucle sur 30 premières lignes 
    span = e.spans[0] #span : début et fin 
    print(e.label, "->", doc.text[span.start:span.end]) 

labels = sorted({e.label for e in doc.anns.entities}) #liste par ordre alphabétique les labels 
labels

drug_labels = {"Med"} 

for e in doc.anns.entities: #boucle qui affiche tous les spans en lien avec le label Med
    if e.label in drug_labels:
        span = e.spans[0]
        print(doc.text[span.start:span.end])


import pandas as pd #pour créer un dataframe

def span_text(doc, ann):  #récupère une annotation ann et renvoie le texte correspondant dans le texte 
    s = ann.spans[0]
    return doc.text[s.start:s.end]

def span_center(ann):  #sert à mesurer qui est le plus proche du médicament 
    s = ann.spans[0]
    return (s.start + s.end) / 2

ents_by_label = {}    # Récupère les entités par label
for e in doc.anns.entities:
    ents_by_label.setdefault(e.label, []).append(e)  #append => ajout dans la bonne liste de l'entité 

for k in ents_by_label:  # Mets-les dans l'ordre du texte
    ents_by_label[k].sort(key=lambda x: x.spans[0].start)

meds = ents_by_label.get("Med", [])
dosages = ents_by_label.get("Dosage", [])
freqs = ents_by_label.get("Freq", [])
routes = ents_by_label.get("Route", [])
dates = ents_by_label.get("Date", []) + ents_by_label.get("Date_relative", [])  #les dates 

WINDOW = 80  # +/- 80 caractères autour du médicament (ajuste si besoin)

rows = []
for m in meds:  #une ligne par médicament 
    m_span = m.spans[0]
    m_center = span_center(m)

    def nearest_in_window(cands): #on prends les plus proches du médicament si présent dans la fenêtre 
        best = None
        best_dist = 10**9
        for c in cands:
            c_span = c.spans[0]
            # garde uniquement si dans la fenêtre autour du médicament
            if c_span.end < m_span.start - WINDOW or c_span.start > m_span.end + WINDOW:
                continue
            dist = abs(span_center(c) - m_center)
            if dist < best_dist:
                best = c
                best_dist = dist
        return best

    d = nearest_in_window(dosages) #on récupère les meilleures matchs 
    f = nearest_in_window(freqs)
    r = nearest_in_window(routes)
    dt = nearest_in_window(dates)

    rows.append({  #on crée des dictionnaires plus simple pour faire des dataframes car chaque dic = une ligne et chaque clé = une colonne 
        "Medicament": span_text(doc, m),
        "Dosage": span_text(doc, d) if d else None,
        "Frequence": span_text(doc, f) if f else None,
        "Voie": span_text(doc, r) if r else None,
        "Date": span_text(doc, dt) if dt else None,
        "Start": m_span.start,
        "End": m_span.end,
    })

df = pd.DataFrame(rows).sort_values("Start").reset_index(drop=True) #création du dataframe final avec tri dans l'ordre 

# Export CSV sur le Bureau
out_csv = Path.home() / "Desktop" / "table_medicaments.csv"
df.to_csv(out_csv, index=False, encoding="utf-8-sig")
print("CSV créé :", out_csv)

def show_context(doc, start, end, window=80):
    left = max(0, start - window)
    right = min(len(doc.text), end + window)
    return doc.text[left:right]

for i, row in df.head(3).iterrows():
    print("\n--- ligne", i, "---")
    print("Med:", row["Medicament"], "| Dosage:", row["Dosage"], "| Freq:", row["Frequence"], "| Voie:", row["Voie"], "| Date:", row["Date"])
    print(show_context(doc, int(row["Start"]), int(row["End"]), window=120))
