imp, ns = __import__, ["(\n);"]
app, tol = ns.append, 1
nl,nl2,N,S,gb,kw, nt= (
    *((getattr(imp("tokenize"), i) for i in ("NEWLINE", "NL", "NAME", "STRING"))),
    getattr(imp("itertools"), "groupby"), getattr(imp("keyword"), "iskeyword"), getattr(imp("collections"), "namedtuple")
)
old, *tl = imp("tokenize").tokenize(open("main.py", "rb").readline)
tok_lt = {
    nl: lambda z,v: app(";") if ns[-1] != ";" else None,
    nl2: lambda z,v: app("") if ns[-1] != ";" else None,
}
toktup = nt("t", ["string", "type"])
partok = lambda tok, sp: (ts:=''.join(tok.string.split(" ")),splpt:=ts.find(".") if tok.type == N else space-3, septok:="" if tok.type == N else "\"", toktup(string=ts[:splpt]+septok, type=tok.type), toktup(string=("\"" if tok.type == S else "")+ts[splpt:], type=tok.type))[3:]
[
    (
        (t_buf := 0),
        (trl := False),
        [
            app(''.join(list(gr)[t_buf:]))
            if sp
            else (
                (space := len(list(gr))),
                [
                    (
                        (t_buf := -1 * b),
                        (tok := tl.pop(0)),
                        (pt:=partok(tok, space)),
                        (cs := (pt[0].string,tl.insert(0, pt[1]) if len(pt[1].string)>0 else None)[0] if tok.type in (N,S) and ("." in tok.string and len(tok.string)>=space) else ' '.join(tok.string.split())),
                        (l := len(cs)),
                        tok_lt.get(
                            tok.type,
                            lambda tok, old: app(" "+cs)
                            if kw(cs) or (old.type == N and tok.type == N)
                            else app(cs),
                        )(tok, old),
                        (old := tok),
                        (space := space - l),
                    )
                    if (space >= (b := len(' '.join(tl[0].string.split())) - tol))
                    else None
                    for i in range(min(space, len(tl)))
                ],
            )
            for (sp, gr) in gb(line, key=str.isspace)
        ],
        ns.append(ns.pop(-1).rstrip()+"\\\n") if (tl and not trl) else None,
    )
    for line in open("test/outline.txt").readlines()
]
print("".join(ns))
print(exec("".join(ns)))