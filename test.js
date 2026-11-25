// Rulează: node test.js  (verifică merge-ul de sync și curățarea datelor de buget din index.html)
const fs=require('fs'),h=fs.readFileSync(__dirname+'/index.html','utf8'),sc=h.slice(h.lastIndexOf('<script>')+8,h.lastIndexOf('</script>'));
const cut=(a,b)=>{const i=sc.indexOf(a),j=sc.indexOf(b,i);if(i<0||j<0)throw new Error('lipsește: '+a);return sc.slice(i,j)};
const code=cut('let RT=0;const J=','const save=')+cut('const MDEF=','const ymk=')+cut('function cleanMoney','function mitems')+';return{m3,cleanMoney,mnum}';
const {m3,cleanMoney,mnum}=new Function('S','pack','UID','localStorage',code)({},()=>({}),'u',{getItem:()=>null});
let n=0;const ok=(c,m)=>{n++;if(!c){console.error('EȘUAT:',m);process.exit(1)}},J=JSON.stringify;
const b={one:[{id:1},{id:2}],exam:{x:1},money:{tx:[{id:5,amt:1}]}},l={one:[{id:1},{id:3}],exam:{x:1,y:1},money:{tx:[{id:5,amt:1},{id:6,amt:2}]}},r={one:[{id:1},{id:2},{id:4}],exam:{},money:{tx:[{id:5,amt:9}]}};
ok(J(m3(b,l,r))==J({one:[{id:1},{id:3},{id:4}],exam:{y:1},money:{tx:[{id:5,amt:9},{id:6,amt:2}]}}),'merge: adăugări + ștergeri din ambele părți');
ok(m3({a:1},{a:2},{a:3}).a==2,'conflict: câștigă varianta locală');
ok(J(m3({z:[{id:1,n:'a'}]},{z:[{id:1,n:'a'}]},{z:[]}))==J({z:[]}),'ștergere pe server fără modificare locală');
ok(J(m3({z:[{id:1,n:'a'}]},{z:[{id:1,n:'b'}]},{z:[]}))==J({z:[{id:1,n:'b'}]}),'editarea locală bate ștergerea de pe server');
ok(mnum('12,5')==12.5&&mnum('-1')==null&&mnum('abc')==null&&mnum(1e10)==null,'mnum');
const c=cleanMoney({b:{'2026-11':'3000','x':5,'2026-12':-1},tx:[{id:1,d:'2026-11-03',amt:10,cat:'groc',note:'a'},{d:'2026-13-xx',amt:5},{d:'2026-11-04',amt:-3}],rec:[{amt:50,from:'2026-11',name:'chirie',cat:'bills'}],cats:[{id:'a',name:'X',color:'roșu',sav:1,lim:'100'}],rate:'30',carry:{'2026-12':20},roll:{'2026-11':{t:'b',a:5,id:1},'2026-10':{t:'q',a:5}}});
ok(J(Object.keys(c.b))=='["2026-11"]'&&c.tx.length==1&&c.rec.length==1,'cleanMoney elimină intrările invalide');
ok(c.cats[0].color=='#90a4ae'&&c.cats[0].lim==100&&c.rate==30&&c.carry['2026-12']==20&&c.roll['2026-11'].t=='b'&&!c.roll['2026-10'],'cleanMoney: categorii, tarif, report');
console.log('OK · '+n+' verificări');
