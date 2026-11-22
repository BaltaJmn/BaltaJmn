#!/usr/bin/env python3
"""Builds the apps page served at https://baltajmn.dev/ (GitHub Pages) and the GitHub profile README from one list.

Only apps that are on sale go in APPS. When one goes on sale or is pulled, edit APPS and run `python3 build.py`.
Store links carry the same campaign format as conCampana() in gk/control/lib.mjs:
App Store ct=<source>-<campaign>, Google Play referrer utm_source=<source>&utm_campaign=<ct>.
Usage: python3 build.py [--test]
"""
import html, sys, urllib.parse
from datetime import date

PT = 129564006
KEY = 'e9b79d4f4468824f180e2a6f114d8f0c'  # IndexNow, public by design
SITE = 'https://baltajmn.dev/'

# name, one line, website, App Store id, Google Play package
APPS = [
    ('FlowTime', 'Pomodoro and flow timer: your break adapts to how long you worked, and you can focus with friends.',
     'https://flowtime.baltajmn.dev/', 6819302003, 'com.baltajmn.flowtime'),
    ('Chroma', 'Photo a day diary: one photo and one color each day, shared with friends if you want.',
     'https://color.baltajmn.dev/', 6819301462, 'com.baltajmn.color'),
    ('Quilt', 'Habit tracker that turns your year into a quilt, one patch a day, with streaks and friends.',
     'https://quilt.baltajmn.dev/', 6819302953, 'com.baltajmn.habit'),
    ('MoodTraker', 'Year in pixels mood tracker: one tap a day fills your year with colors.',
     'https://mood.baltajmn.dev/', 6819302341, 'com.baltajmn.mood'),
    ('Sleeper', 'Bedtime calculator that sets your alarm for the end of a sleep cycle.',
     'https://sleeper.baltajmn.dev/', 6820568314, 'com.baltajmn.sleeper'),
    ('Test4Test', "Developers test each other's apps to meet Google Play's rule of 12 testers for 14 days.",
     'https://testers.baltajmn.dev/', None, 'com.baltajmn.test4test'),
    ('Bobbin', 'Bullet journal with rapid logging, bullets and migration by hand. Your journal stays on your phone.',
     'https://bullet.baltajmn.dev/', 6828976187, None),
    ('Allocute', 'Federal sentencing guidelines calculator: offense level, criminal history and range, with citations.',
     'https://allocute.baltajmn.dev/', 6835876912, None),
    ('Clearwell', 'See-through Home Screen icons and widgets cut from your own wallpaper.',
     'https://clearwell.baltajmn.dev/', 6833337250, None),
    ('Drumwell', 'Drum tuner that shows the pitch at every lug and which tension rods to turn.',
     'https://drumwell.baltajmn.dev/', 6833335973, None),
    ('Globelet', 'Turns photos, panoramas and videos into tiny planets you can spin and save.',
     'https://globelet.baltajmn.dev/', 6835494363, None),
    ('Klarat', 'Practice for the Swedish citizenship test: 431 questions with an explanation for every answer.',
     'https://klarat.baltajmn.dev/', 6836669918, None),
    ('Lane Judge', 'Pinewood derby race manager: heat chart, standings and a finish line camera.',
     'https://lanejudge.baltajmn.dev/', 6836730721, None),
    ('Lapmend', 'Trims and merges Apple Health workouts you forgot to stop or that got split in two.',
     'https://lapmend.baltajmn.dev/', 6835494207, None),
    ('Regwell', 'FAR/AIM: all of 14 CFR, the AIM and the Pilot/Controller Glossary, offline and kept current.',
     'https://regwell.baltajmn.dev/', 6833383062, None),
    ('Shushwell', 'A rhythmic shush for your baby that keeps going with the screen locked and gets louder when baby cries.',
     'https://shushwell.baltajmn.dev/', 6833074761, None),
    ('Stepback', 'Rehearse the cosmetology, esthetics or nail tech state board practical exam with a timed proctor.',
     'https://stepback.baltajmn.dev/', 6836683872, None),
    ('Tilewell', 'Phonics letter tiles for teaching reading and spelling, with a voice for every sound.',
     'https://tilewell.baltajmn.dev/', 6833336538, None),
    ('Whistlepost', 'Tells you the railroad, subdivision and milepost where you stand, and the nearest crossing.',
     'https://whistlepost.baltajmn.dev/', 6836772563, None),
]


def ct(source, campaign=''):
    return '-'.join(x for x in (source, campaign) if x).lower()


def apple(app_id, source, campaign=''):
    return f'https://apps.apple.com/app/apple-store/id{app_id}?pt={PT}&ct={ct(source, campaign)}&mt=8'


def play(pkg, source, campaign=''):
    ref = urllib.parse.quote(f'utm_source={source}&utm_campaign={ct(source, campaign)}', safe='')
    return f'https://play.google.com/store/apps/details?id={pkg}&referrer={ref}'


def links(app, source, campaign=''):
    _, _, web, app_id, pkg = app
    out = [('Website', web)]
    if app_id:
        out.append(('App Store', apple(app_id, source, campaign)))
    if pkg:
        out.append(('Google Play', play(pkg, source, campaign)))
    return out


def page():
    e = html.escape

    def section(title, apps):
        rows = ''.join(
            f'<li><h3>{e(a[0])}</h3><p>{e(a[1])}</p><p class="links">'
            + ' '.join(f'<a href="{e(u)}">{e(t)}</a>' for t, u in links(a, 'web', 'hub')) + '</p></li>\n'
            for a in apps)
        return f'<h2>{title}</h2>\n<ul>\n{rows}</ul>\n'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Apps by BaltaJmn</title>
<link rel="canonical" href="{SITE}">
<meta name="description" content="{len(APPS)} small apps for iPhone and Android by BaltaJmn, an independent developer in Spain: focus timer, habit and mood trackers, drum tuner, pilot rules, phonics tiles and more.">
<style>
:root {{ color-scheme: light dark; --fg: #1c1c1e; --muted: #5f5f66; --line: #e4e4e8; --link: #0a58ca; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fg: #f2f2f4; --muted: #a8a8b0; --line: #2e2e33; --link: #7ab3ff; }} }}
body {{ font: 17px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: var(--fg); max-width: 720px; margin: 0 auto; padding: 32px 20px; }}
h1 {{ font-size: 2em; margin: 0 0 4px; }}
h2 {{ font-size: 1.1em; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; margin: 40px 0 8px; }}
h3 {{ font-size: 1.15em; margin: 0; }}
ul {{ list-style: none; padding: 0; margin: 0; }}
li {{ padding: 14px 0; border-bottom: 1px solid var(--line); }}
li p {{ margin: 2px 0; }}
.links a {{ margin-right: 14px; }}
a {{ color: var(--link); }}
.lede, footer {{ color: var(--muted); }}
footer {{ margin-top: 40px; font-size: .9em; }}
</style>
</head>
<body>
<h1>Apps by BaltaJmn</h1>
<p class="lede">Small, focused apps for iPhone and Android, made by an independent developer in Spain.</p>
{section('iPhone and Android', [a for a in APPS if a[3] and a[4]])}{section('iPhone', [a for a in APPS if a[3] and not a[4]])}{section('Android', [a for a in APPS if a[4] and not a[3]])}<footer>Made by Baltasar Jimenez Rincon, Spain. <a href="https://github.com/BaltaJmn">GitHub</a></footer>
</body>
</html>
'''


def readme():
    rows = '\n'.join(f'- **{a[0]}**: {a[1]} ' + ' | '.join(f'[{t}]({u})' for t, u in links(a, 'github')) for a in APPS)
    return f'''# BaltaJmn

Independent app developer in Spain. Small, focused apps for iPhone and Android.

All apps: [baltajmn.dev]({SITE})

{rows}
'''


def test():
    assert apple(1, 'web', 'hub') == 'https://apps.apple.com/app/apple-store/id1?pt=129564006&ct=web-hub&mt=8'
    assert play('a.b', 'web', 'hub') == 'https://play.google.com/store/apps/details?id=a.b&referrer=utm_source%3Dweb%26utm_campaign%3Dweb-hub'
    assert play('a.b', 'github').endswith('utm_source%3Dgithub%26utm_campaign%3Dgithub')
    p = page()
    assert p.count('<li>') == len(APPS) and '&amp;ct=web-hub&amp;mt=8' in p and 'ct=github' not in p
    r = readme()
    assert r.count('\n- **') == len(APPS) and 'ct=web-hub' not in r
    assert all(ord(c) < 128 for c in p + r), 'ASCII only'
    print('test ok')


if __name__ == '__main__':
    if '--test' in sys.argv:
        test(); sys.exit()
    open('index.html', 'w').write(page())
    open('README.md', 'w').write(readme())
    open('robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
    open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                   f'<url><loc>{SITE}</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n</urlset>\n')
    open(f'{KEY}.txt', 'w').write(KEY)
    open('CNAME', 'w').write('baltajmn.dev\n')
    open('.nojekyll', 'w').write('')
    print('built', len(APPS), 'apps')
