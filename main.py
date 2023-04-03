imp, ns = __import__, ["(\n);"]
tl = [
    (t, len(t.string.strip()))
    for t in imp("tokenize").tokenize(open("main.py", "rb").readline)
][1:]
nl, nl2, N, gb = (
    *((getattr(imp("tokenize"), i) for i in ("NEWLINE", "NL", "NAME"))),
    getattr(imp("itertools"), "groupby"),
)
import keyword
app, tol = ns.append, 1
tok_lt = {
    nl: lambda z,v: app(";") if ns[-1] != ";" else None,
    nl2: lambda z,v: app("") if ns[-1] != ";" else None,
}
kw = lambda x: x in keyword.kwlist
[
    (
        (t_buf := 0),
        [
            ns.append(''.join(list(gr)[t_buf:]))
            if sp
            else (
                (space := len(list(gr))),
                (old := None),
                [
                    (
                        (t_buf := -1 * b),
                        (tok := tl.pop(0)),
                        (l := tok[1]),
                        (tok := tok[0]),
                        tok_lt.get(
                            tok.type,
                            lambda tok, old: app(" "+tok.string.strip())
                            if (kw(tok.string.strip())) or (old == N and tok.type == N)
                            else app(tok.string.strip()),
                        )(tok, old),
                        (old := tok.type),
                        (space := space - l),
                    )
                    if space >= (b := abs(tl[0][1] - tol))
                    else None
                    for i in range(min(space, len(tl)))
                ],
            )
            for (sp, gr) in gb(line, key=str.isspace)
        ],
        ns.append(ns.pop(-1).rstrip()+"\\\n") if tl else None,
    )
    for line in open("test/outline.txt").readlines()
]
print("".join(ns))
print(exec("".join(ns)))
