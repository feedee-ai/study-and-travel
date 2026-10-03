# Немецкие версии: копия hf/ каждого ролика с заменой текста (подложки те же).
import os, shutil, sys
COMMON = {
 '>DM TO BOOK<': '>TERMIN PER DM<',
 '>KERATIN · HAIR BOTOX · HAIR RECOVERY<': '>KERATIN · HAARBOTOX · HAARREGENERATION<',
 '>TREATMENTS<': '>BEHANDLUNGEN<',
 '>KERATIN<': '>KERATIN<',
 '>HAIR BOTOX<': '>HAARBOTOX<',
 '>HAIR RECOVERY<': '>HAARREGENERATION<',
}
V = {
 '01-desire': {
  '>Your hair is<': '>Ihr Haar begleitet<', '>with you every day.<': '>Sie jeden Tag.<',
  '>It deserves to<': '>Es verdient<', '>look its best.<': '>nur das Beste.<',
  '>Smooth.<': '>Glatt.<', '>Silky.<': '>Seidig.<', '>Glossy.<': '>Glänzend.<',
  '>Hair treatments<': '>Haarbehandlungen,<', '>tailored to your hair.<': '>abgestimmt auf Ihr Haar.<',
  '>Keratin<': '>Keratin<', '>Hair botox<': '>Haarbotox<', '>Hair recovery<': '>Haarregeneration<',
  '>Your hair.<': '>Ihr Haar.<', '>Your space.<': '>Ihr Zuhause.<',
 },
 '02-pain': {
  '>Dry?<': '>Trocken?<', '>Frizzy?<': '>Kraus?<', '>Hard to manage?<': '>Schwer zu bändigen?<',
  '>It doesn’t have<': '>Das muss<', '>to be this way.<': '>nicht so sein.<',
  '>Smooth.<': '>Glatt.<', '>Silky.<': '>Seidig.<', '>Glossy.<': '>Glänzend.<',
  '>Hair treatments<': '>Haarbehandlungen,<', '>tailored to<': '>abgestimmt<', '>your hair.<': '>auf Ihr Haar.<',
  '>HAIR<br>RECOVERY<': '>HAAR-<br>REGENERATION<',
  '>Love your<br>hair again.<': '>Lieben Sie Ihr<br>Haar wieder.<',
 },
 '03-private': {
  '>What if your<': '>Was wäre, wenn<', '>hair treatment<': '>Ihre Haarbehandlung<', '>came to you?<': '>zu Ihnen käme?<',
  '>Premium hair care.<': '>Premium-Haarpflege.<', '>Without leaving<': '>Ohne Ihr Zuhause<', '>your space.<': '>zu verlassen.<',
  '>Healthier.<': '>Gesünder.<', '>Smoother.<': '>Glatter.<', '>More beautiful hair.<': '>Schöneres Haar.<',
  '>We come to you.<': '>Wir kommen zu Ihnen.<',
 },
 '04-time': {
  '>Beautiful hair<': '>Schönes Haar<', '>shouldn’t take<': '>braucht nicht<', '>an hour<': '>jeden Morgen<', '>every morning<': '>eine Stunde<',
  '>Less frizz.<': '>Weniger Frizz.<', '>Less styling.<': '>Weniger Styling.<',
  '>More time<': '>Mehr Zeit<', '>for you.<': '>für Sie.<',
  '>Smooth<': '>Glatt<', '>Easy to manage<': '>Pflegeleicht<', '>Glossy<': '>Glänzend<',
  '>Take back<br>your mornings.<': '>Ihre Morgen<br>gehören Ihnen.<',
 },
}
for name, rep in V.items():
    src = f'{name}/hf'; dst = f'de/{name}/hf'
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(src, dst)
    p = f'{dst}/index.html'; s = open(p).read()
    for a, b in {**rep, **COMMON}.items():
        if a in s: s = s.replace(a, b)
        elif a not in COMMON: print('MISSING', name, a); sys.exit(1)
    s = s.replace('<html>', '<html lang="de">', 1)
    EXTRA = {'03-private': '  .end .kicker { font-size: 58px; letter-spacing: .12em; padding-left: .12em; }\n',
             '02-pain': '  #p3 { font-size: 56px; letter-spacing: .1em; }\n',
             '01-desire': ''}
    if EXTRA.get(name): s = s.replace('</style>', EXTRA[name] + '</style>', 1)
    open(p, 'w').write(s)
    print('ok', name)
