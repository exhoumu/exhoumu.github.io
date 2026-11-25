#!/usr/bin/env python3
"""育守法務事務所ブログのビルド。
blog/src/*.md（先頭にメタ情報）から blog/*.html と blog/index.html を作り、sitemap.xml も更新する。
メタ情報の書き方（先頭の --- で囲む）:
  title: 記事タイトル
  date: 2026-11-26
  slug: 英数字とハイフン（ファイル名になる）
  description: 検索結果に出る説明（120字以内）
  cta: check / contact / shiryo のどれか（記事の最後の案内）
  status: publish または draft（draftは出力しない）
本文：段落は空行で区切る。「## 」で見出し、「- 」で箇条書き、**太字**、[文字](URL)。
使い方: python3 blog/build.py （リポジトリのルートで実行）
"""
import re, glob, os, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, 'blog')
SITE = 'https://exhoumu.github.io'
OPEN = datetime.date(2026, 12, 1)
SHIRYO = 'https://docs.google.com/forms/d/e/1FAIpQLSfvN-a86iv_raDTc4XyR5IH_K8_LavKqXG-lcxIQ2-PPBE6tA/viewform?usp=pp_url&entry.211899175=%E3%83%96%E3%83%AD%E3%82%B0'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', t)
    return t

def md(body):
    out = []
    for blk in re.split(r'\n\s*\n', body.strip()):
        lines = blk.strip().split('\n')
        if lines[0].startswith('## '):
            out.append(f'<h2>{inline(lines[0][3:])}</h2>')
            lines = lines[1:]
            if not lines: continue
        if all(l.startswith('- ') for l in lines):
            out.append('<ul>' + ''.join(f'<li>{inline(l[2:])}</li>' for l in lines) + '</ul>')
        else:
            out.append('<p>' + '<br>'.join(inline(l) for l in lines) + '</p>')
    return '\n'.join(out)

def parse(path):
    s = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', s, re.S)
    meta = dict(l.split(':', 1) for l in m.group(1).strip().split('\n'))
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    meta['body'] = m.group(2)
    meta['d'] = datetime.date.fromisoformat(meta['date'])
    return meta

def head(title, desc, url, depth='../'):
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/ogp.jpg">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{depth}img/favicon.png">
<link rel="apple-touch-icon" href="{depth}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500&amp;family=Noto+Serif+JP:wght@400;600&amp;display=swap">
<link rel="stylesheet" href="{depth}css/site.css">
<style>
.bl{{padding:64px 0 88px}}
.bl .eb{{margin:0;font-size:12px;letter-spacing:.2em;color:#7A6230}}
.bl h1{{font-family:'Noto Serif JP',serif;font-weight:600;font-size:32px;line-height:1.6;letter-spacing:.04em;margin:10px 0 6px}}
.bl .date{{font-size:13px;color:#355269;margin:0 0 36px}}
.art{{font-size:16.5px;line-height:2.05}}
.art p{{margin:0 0 1.5em}}
.art h2{{font-family:'Noto Serif JP',serif;font-weight:600;font-size:22px;line-height:1.6;margin:2.4em 0 .9em;padding-bottom:10px;border-bottom:1px solid #D9D2BF}}
.art ul{{margin:0 0 1.5em;padding-left:1.3em}}
.art li{{margin:.3em 0}}
.art a{{color:#0D1B42}}
.cta{{margin:56px 0 0;background:#0D1B42;color:#F7F4EA;padding:30px 32px}}
.cta p{{margin:0 0 16px;line-height:1.9}}
.cta a.b{{display:inline-flex;align-items:center;min-height:46px;padding:0 24px;background:#F7F4EA;color:#0D1B42;text-decoration:none;font-weight:500;letter-spacing:.06em}}
.cta small{{display:block;margin-top:12px;color:#B8C2D6;font-size:12.5px}}
.by{{margin:40px 0 0;display:flex;gap:18px;align-items:center;border-top:1px solid #D9D2BF;padding-top:24px}}
.by img{{width:72px;height:72px;object-fit:cover;border-radius:50%}}
.by p{{margin:0;font-size:14px;line-height:1.8}}
.list{{list-style:none;margin:0;padding:0;border-top:1px solid #D9D2BF}}
.list li{{border-bottom:1px solid #D9D2BF}}
.list a{{display:block;padding:24px 4px;text-decoration:none;color:#0D1B42}}
.list .t{{font-family:'Noto Serif JP',serif;font-weight:600;font-size:20px;line-height:1.6}}
.list .d{{font-size:13px;color:#355269}}
.list .x{{font-size:14.5px;color:#355269;margin-top:4px;line-height:1.8}}
.back{{margin:40px 0 0;font-size:14px}}
@media (max-width:640px){{.bl{{padding:40px 0 64px}}.bl h1{{font-size:24px}}.art{{font-size:16px}}.cta{{padding:24px 20px}}}}
</style>
</head>
<body>
<div class="ik">
  <header class="hd">
    <div class="wrap">
      <a class="logo" href="{depth}index.html"><small>社会保険労務士事務所</small><span>育守法務事務所</span></a>
      <nav class="nav" aria-label="メインメニュー">
        <a href="{depth}index.html#strength">強み</a>
        <a href="{depth}index.html#service">支援内容</a>
        <a href="{depth}price.html">料金</a>
        <a href="{depth}blog/">ブログ</a>
        <a href="{depth}index.html#profile">代表紹介</a>
        <a class="btn" href="{depth}index.html#contact">お問い合わせ</a>
      </nav>
    </div>
  </header>
  <main class="bl">
    <div class="wrap narrow">
'''

FOOT = '''    </div>
  </main>
  <footer class="ft">
    <div class="wrap">
      <div class="cols">
        <div>
          <p style="margin: 0; font-size: 12px; letter-spacing: 0.2em; color: #C9B78A">社会保険労務士事務所</p>
          <p class="serif" style="margin: 4px 0 0; font-weight: 600; font-size: 24px; letter-spacing: 0.14em">育守法務事務所</p>
          <dl>
            <dt>所在地</dt><dd>北海道札幌市厚別区</dd>
            <dt>対応エリア</dt><dd>訪問：札幌市および近郊　／　オンライン：全国</dd>
            <dt>代表</dt><dd>社会保険労務士　稲石 楓季</dd>
            <dt>メール</dt><dd><a href="mailto:ex.houmu@gmail.com">ex.houmu@gmail.com</a></dd>
            <dt>営業時間</dt><dd>平日 10:00〜19:00（土日祝休み）</dd>
          </dl>
        </div>
        <nav aria-label="フッターメニュー">
          <a href="../index.html">トップ</a>
          <a href="../price.html">顧問契約と料金</a>
          <a href="./">ブログ</a>
          <a href="../policy.html#ai">AIの活用と情報管理</a>
          <a href="../policy.html">プライバシーポリシー</a>
          <a href="../index.html#contact">お問い合わせ</a>
        </nav>
      </div>
      <p style="margin: 48px 0 0; font-size: 12px; color: #B8C2D6">© 2026 育守法務事務所</p>
    </div>
  </footer>
</div>
</body>
</html>
'''

def cta(kind, d):
    pre = '<small>※ ご相談の受付は、2026年12月1日の開業日から始めます。</small>' if d < OPEN else ''
    if kind == 'check':
        return f'<div class="cta"><p>会社の労務管理の状況と、使えるかもしれない助成金の目安が、30秒で分かります。会社名や連絡先の入力はいりません。</p><a class="b" href="../check.html">30秒チェックを始める</a>{pre}</div>'
    if kind == 'shiryo':
        return f'<div class="cta"><p>事務所案内と「顧問契約で変わること」をまとめた資料を、PDFでお送りします。</p><a class="b" href="{SHIRYO}">資料請求（PDF）</a>{pre}</div>'
    return f'<div class="cta"><p>人事や労務のことで気になることがあれば、お気軽にご相談ください。</p><a class="b" href="../index.html#contact">ご相談・お問い合わせ</a>{pre}</div>'

BY = '<div class="by"><img src="../img/inaishi.jpg" alt="稲石 楓季"><p><strong>稲石 楓季</strong>（いないし ふうき）<br>社会保険労務士。育守法務事務所 代表。社会保険労務士法人で3年間、実務を経験。</p></div>'

def ymd(d): return f'{d.year}年{d.month}月{d.day}日'

def main():
    posts = [parse(p) for p in glob.glob(os.path.join(B, 'src', '*.md'))]
    posts = [p for p in posts if p.get('status', 'publish') == 'publish']
    posts.sort(key=lambda p: (p['d'], p['slug']), reverse=True)
    for f in glob.glob(os.path.join(B, '*.html')):
        os.remove(f)
    for p in posts:
        url = f"{SITE}/blog/{p['slug']}.html"
        h = head(f"{p['title']}｜育守法務事務所", p['description'], url)
        h += f'      <p class="eb">BLOG</p>\n      <h1>{inline(p["title"])}</h1>\n      <p class="date">{ymd(p["d"])}</p>\n'
        h += f'      <div class="art">\n{md(p["body"])}\n      </div>\n      {cta(p.get("cta","contact"), p["d"])}\n      {BY}\n      <p class="back"><a href="./">← ブログの一覧へ</a></p>\n' + FOOT
        open(os.path.join(B, p['slug'] + '.html'), 'w', encoding='utf-8').write(h)
    items = ''.join(f'<li><a href="{p["slug"]}.html"><div class="d">{ymd(p["d"])}</div><div class="t">{inline(p["title"])}</div><div class="x">{html.escape(p["description"])}</div></a></li>' for p in posts)
    if not items:
        items = '<li style="padding:24px 4px;color:#355269">記事は準備中です。</li>'
    idx = head('ブログ｜育守法務事務所', '札幌の社会保険労務士事務所「育守法務事務所」のブログ。人事労務・助成金・組織づくりのことを書いています。', f'{SITE}/blog/')
    idx += f'      <p class="eb">BLOG</p>\n      <h1>ブログ</h1>\n      <p class="date">人事労務・助成金・組織づくりのこと、開業準備の記録を書いています。</p>\n      <ul class="list">{items}</ul>\n' + FOOT
    open(os.path.join(B, 'index.html'), 'w', encoding='utf-8').write(idx)
    # sitemap
    sm = os.path.join(ROOT, 'sitemap.xml')
    s = open(sm, encoding='utf-8').read()
    s = re.sub(r'\s*<url><loc>https://exhoumu\.github\.io/blog/[^<]*</loc>.*?</url>', '', s)
    today = datetime.date.today().isoformat()
    add = f'\n  <url><loc>{SITE}/blog/</loc><lastmod>{today}</lastmod></url>' + ''.join(f'\n  <url><loc>{SITE}/blog/{p["slug"]}.html</loc><lastmod>{p["date"]}</lastmod></url>' for p in posts)
    s = s.replace('\n</urlset>', add + '\n</urlset>')
    open(sm, 'w', encoding='utf-8').write(s)
    print(f'{len(posts)} 件を公開用に出力しました')

if __name__ == '__main__':
    main()
