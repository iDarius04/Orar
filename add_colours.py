#!/usr/bin/env python3
"""Adds colour selection to the planner.
Usage: python3 add_colours.py path/to/index.html
- Personal activities (work, etc.): colour picker in the form.
- Subjects (courses / seminars / labs / English): colour per subject in a new "Culorile materiilor" section.
Colours are saved, synced and exported/imported with the rest of the data.
Creates <file>.bak, then overwrites the file. Aborts untouched if any anchor doesn't match."""
import sys, shutil

CSS = r""".swr{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.sw{width:28px;height:28px;min-width:0;min-height:0;padding:0;border-radius:50%;border:2px solid transparent;line-height:1}
.sw.on{border-color:var(--fg);box-shadow:0 0 0 2px var(--card) inset}
.sw.def{background:var(--card);color:var(--mut);font-size:12px;border-color:var(--ln)}
.sw.def.on{border-color:var(--fg)}
.cr{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:8px}
.cnm{flex:0 0 220px;padding:6px 8px;border-radius:8px;font-weight:600;background:var(--ln)}
.cnm.set{background:hsl(var(--h) var(--s) var(--l))}
@media(max-width:720px){#cc{grid-column:1/-1}.cnm{flex:1 1 100%}#CL{margin:0 12px}.cr{padding:10px;background:var(--card);border-radius:14px}.sw{width:34px;height:34px}}
"""

JS_HELPERS = r"""let HR=44,fh=null;const HUES=[0,20,45,90,130,175,210,250,280,320];
const sw=(cur,extra)=>HUES.map(h=>'<button type="button" class="sw'+(cur===h?' on':'')+'" '+extra+' data-h="'+h+'" aria-label="Culoare '+h+'" style="background:hsl('+h+' 65% 55%)"></button>').join('')+'<button type="button" class="sw def'+(cur==null?' on':'')+'" '+extra+' data-h="" title="Culoare implicită" aria-label="Culoare implicită">✕</button>';
const drawCc=()=>{$('cc').innerHTML='<span class="st">Culoare</span>'+sw(fh,'')};"""

JS_LISTENERS = r"""$('cc').addEventListener('click',e=>{const b=e.target.closest('.sw');if(!b)return;fh=b.dataset.h===''?null:+b.dataset.h;drawCc()});
$('CL').addEventListener('click',e=>{const b=e.target.closest('[data-sc]');if(!b)return;if(b.dataset.h==='')delete S.col[b.dataset.sc];else S.col[b.dataset.sc]=+b.dataset.h;save();render()});"""

CL_RENDER = r"""$('CL').innerHTML=Object.keys(C).map(c=>{const h=S.col[c];return'<div class="cr"><span class="cnm'+(h!=null?' set':'')+'"'+(h!=null?' style="--h:'+h+'"':'')+'>'+C[c]+'</span><span class="swr">'+sw(h==null?null:h,'data-sc="'+c+'"')+'</span></div>'}).join('');"""

# (old, new, expected_count)
EDITS = [
 ("</style></head><body>", CSS + "</style></head><body>", 1),
 ("showC:1,base:{},wp:{},ser:[],one:[],scope:'all'}", "showC:1,col:{},base:{},wp:{},ser:[],one:[],scope:'all'}", 2),
 ("'showC','base','wp'", "'showC','col','base','wp'", 1),
 ("kind:z.kind||q.kind,d,", "kind:z.kind||q.kind,hue:z.hue,d,", 1),
 ("nm:q.name,kind:q.kind,d,", "nm:q.name,kind:q.kind,hue:q.hue,d,", 1),
 ("let HR=44;", JS_HELPERS, 1),
 ("const pr=x.k=='Personal',tip=", "const pr=x.k=='Personal',hu=pr?x.hue:S.col[x.c],tip=", 1),
 ("""style="top:'+((x.s-RS)*HR+1)""", """style="'+(hu!=null?'--h:'+hu+';':'')+'top:'+((x.s-RS)*HR+1)""", 1),
 ("$('P').innerHTML=p;", "$('P').innerHTML=p;" + CL_RENDER, 1),
 ("""<h2 id="ft">Programul meu (muncă etc.)</h2>""",
  """<h2>Culorile materiilor</h2><div id="CL"></div><h2 id="ft">Programul meu (muncă etc.)</h2>""", 1),
 ("""</select></label><span id="cd" style=""", """</select></label><span id="cc" class="swr"></span><span id="cd" style=""", 1),
 ("const flip=c=>setPick(c,1-pk(c,wk));", "drawCc();const flip=c=>setPick(c,1-pk(c,wk));", 1),
 ("function clear(){ed=null;", "function clear(){ed=null;fh=null;drawCc();", 1),
 ("kind:$('ck').value=='work'?'work':'personal',days,s,e}", "kind:$('ck').value=='work'?'work':'personal',days,s,e,hue:fh}", 1),
 ("$('cw').value=q.par||0;", "$('cw').value=q.par||0;fh=z.hue!=null?z.hue:null;drawCc();", 1),
 ("$('PL').addEventListener('click',e=>{const b=e.target.closest('[data-ed]');if(b)edit(+b.dataset.ed)});",
  "$('PL').addEventListener('click',e=>{const b=e.target.closest('[data-ed]');if(b)edit(+b.dataset.ed)});\n" + JS_LISTENERS, 1),
 ("showC:d.showC==0?0:1,base:{},", "showC:d.showC==0?0:1,col:{},base:{},", 1),
 ("for(const c in L)o.base[c]=d.base&&d.base[c]==1?1:0;",
  "for(const c in L)o.base[c]=d.base&&d.base[c]==1?1:0;\nif(d.col&&typeof d.col=='object')for(const c in C){const h=d.col[c];if(h!=null&&isFinite(+h)&&+h>=0&&+h<=360)o.col[c]=+h}", 1),
 ("{name,kind,days:dd,s,e}};", "{name,kind,days:dd,s,e,hue:q.hue==null?null:num(q.hue,0,360,null)}};", 1),
]

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    bad = [(o[:60], src.count(o), n) for o, _, n in EDITS if src.count(o) != n]
    if bad:
        for o, got, n in bad:
            print(f"ANCHOR MISMATCH (found {got}, expected {n}): {o!r}")
        sys.exit("Nothing was changed.")
    for o, new, _ in EDITS:
        src = src.replace(o, new)
    shutil.copyfile(path, path + ".bak")
    open(path, "w", encoding="utf-8").write(src)
    print("Done. Backup:", path + ".bak")

main()
