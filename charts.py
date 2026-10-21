import duckdb, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE, GRAY, INK, INK2, SURF = "#2a78d6", "#c9c8c1", "#0b0b0b", "#52514e", "#ffffff"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.edgecolor":"#d8d7d0",
  "axes.labelcolor":INK2,"xtick.color":INK2,"ytick.color":INK,"figure.facecolor":SURF,"axes.facecolor":SURF})
con = duckdb.connect()
con.sql("CREATE TABLE h AS SELECT * FROM read_csv_auto('data/hospitals.csv')")
con.sql("CREATE TABLE c AS SELECT * FROM read_csv_auto('data/hcahps.csv')")

# Chart 1: outcomes, better vs worse than national
rows = con.sql("""SELECT short_name, mort_better+safety_better+readm_better b,
  mort_worse+safety_worse+readm_worse w FROM h ORDER BY (b-w), -w""").fetchall()
fig, ax = plt.subplots(figsize=(4.0,3.0))
for i,(n,b,w) in enumerate(rows):
    col = BLUE if n=="Shannon" else GRAY
    ax.barh(i, b, color=col, height=0.62, edgecolor=SURF, linewidth=1)
    ax.barh(i, -w, color=col, height=0.62, alpha=0.55 if n!="Shannon" else 0.6, edgecolor=SURF, linewidth=1, hatch="////" )
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows])
for t in ax.get_yticklabels():
    if t.get_text()=="Shannon": t.set_fontweight("bold"); t.set_color(BLUE)
ax.axvline(0,color=INK2,lw=0.8); ax.set_xlim(-6.5,6.5)
ax.set_xticks([-6,-4,-2,0,2,4,6]); ax.set_xticklabels(["6","4","2","0","2","4","6"])
ax.set_xlabel("← # worse      # better →", fontsize=8)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.suptitle("Outcome measures vs. national rate", x=0.03, ha="left", fontsize=10, color=INK, fontweight="bold")
fig.tight_layout(); fig.savefig("charts/outcomes.png", dpi=220)

# Chart 2: cleanliness linear score
rows = con.sql("""SELECT short_name, linear_mean FROM c JOIN h USING(facility_id)
  WHERE measure='CLEANLINESS' ORDER BY linear_mean, short_name='Shannon' DESC""").fetchall()
fig, ax = plt.subplots(figsize=(4.0,3.0))
for i,(n,v) in enumerate(rows):
    ax.plot([78,v],[i,i],color="#ecebe6",lw=1.2,zorder=1)
    ax.scatter(v,i,s=60 if n=="Shannon" else 42,color=BLUE if n=="Shannon" else "#9a998f",zorder=3,edgecolor=SURF,linewidth=1.5)
    ax.text(v+0.55, i, str(v), va="center", fontsize=8, color=INK if n=="Shannon" else INK2,
            fontweight="bold" if n=="Shannon" else "normal")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows])
for t in ax.get_yticklabels():
    if t.get_text()=="Shannon": t.set_fontweight("bold"); t.set_color(BLUE)
ax.set_xlim(78,91); ax.set_xticks([80,82,84,86,88,90]); ax.set_xlabel("Linear mean score, 0–100 (axis zoomed)", fontsize=7.5)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.suptitle("Patient-rated cleanliness (HCAHPS)", x=0.03, ha="left", fontsize=10, color=INK, fontweight="bold")
fig.tight_layout(); fig.savefig("charts/cleanliness.png", dpi=220)
print("ok")
