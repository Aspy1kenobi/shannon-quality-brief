import duckdb
con = duckdb.connect()
sql = open("queries.sql").read()
for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
    body = "\n".join(l for l in stmt.splitlines() if not l.strip().startswith("--")).strip()
    if not body: continue
    r = con.sql(body)
    if r is not None: r.show(max_width=200)
