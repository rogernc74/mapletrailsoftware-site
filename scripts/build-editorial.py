"""Rebuild the seven static marketing pages; retain existing heads and legal bodies."""
from pathlib import Path
from html import escape
import json
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
PRODUCT_DETAILS=json.loads((ROOT/'content/product-details.json').read_text())['pages']
ACADIE_CURRENT=json.loads((ROOT/'content/acadie-current.json').read_text())
NAMES={'acadie':'Acadie','momentslater':'Moments Later','habitwallet':'Habit Wallet','momentsaway':'Moments Away','ifneeded':'If Needed'}
STORES={'acadie':'https://apps.apple.com/ca/app/acadie/id6769209012','momentslater':'https://apps.apple.com/ca/app/moments-later/id6761868181','habitwallet':'https://apps.apple.com/ca/app/habit-wallet/id6786388267','momentsaway':'https://apps.apple.com/ca/app/moments-away/id6765818943'}
PLAY='https://play.google.com/store/apps/details?id=com.mapletrailsoftware.acadie'

def img(src,alt='',cls='',lazy=True):
    from PIL import Image
    w,h=Image.open(ROOT/src.lstrip('/')).size
    return f'<img src="{src}" alt="{escape(alt)}" class="{cls}" width="{w}" height="{h}" {"loading=\"lazy\"" if lazy else "fetchpriority=\"high\""} decoding="async">'

def brand():
    return '<a class="editorial-brand" href="/" aria-label="MapleTrail Software Inc. home">'+img('/images/editorial/mapletrail-lockup.png','MapleTrail Software Inc. logo','',False)+'</a>'

def header(fr=False,acadie=False,suffix=""):
    links=''.join(f'<a href="/{k}/">{v}</a>' for k,v in NAMES.items())
    language='<div class="languages" aria-label="'+('Langue' if fr else 'Language')+'"><a href="/acadie/" lang="en" '+('' if fr else 'aria-current="page"')+'>EN</a><a href="/acadie/fr-CA/" lang="fr-CA" '+('aria-current="page"' if fr else '')+'>FR</a></div>' if acadie else ''
    language=language.replace('href="/acadie/"',f'href="/acadie/{suffix}"').replace('href="/acadie/fr-CA/"',f'href="/acadie/fr-CA/{suffix}"')
    return f'<a class="skip-link" href="#main">'+('Passer au contenu' if fr else 'Skip to content')+f'</a><header class="editorial-header"><div class="wrap header-row">{brand()}<nav aria-label="'+('Navigation principale' if fr else 'Main navigation')+f'"><details class="apps-menu"><summary>Apps</summary><div class="apps-panel">{links}</div></details><a class="about-nav" href="/#about">'+('À propos' if fr else 'About')+'</a><a href="/support/">'+('Assistance' if fr else 'Support')+f'</a></nav>{language}</div></header>'

def footer(fr=False,product=None):
    privacy=f'/{product}/privacy/' if product in ['acadie','habitwallet','ifneeded'] else '/privacy/'
    if fr: privacy='/acadie/fr-CA/privacy/'
    extra=''
    if product=='acadie':
        base='/acadie/fr-CA/' if fr else '/acadie/'
        extra=f'<a href="{base}terms/">'+('Conditions' if fr else 'Terms')+f'</a><a href="{base}account-deletion/">'+('Suppression de compte' if fr else 'Account deletion')+'</a><a href="https://www.facebook.com/AcadieApp/">Facebook Acadie</a>'
    return f'<footer class="editorial-footer"><div class="wrap footer-top">{brand()}<p>'+('Des apps réfléchies.<br>Des liens personnels.' if fr else 'Thoughtful apps.<br>Personal connections.')+f'</p><nav aria-label="'+('Pied de page' if fr else 'Footer')+'"><a href="/#apps">Apps</a><a href="/support/">'+('Assistance' if fr else 'Support')+f'</a><a href="{privacy}">'+('Confidentialité' if fr else 'Privacy')+f'</a>{extra}<a href="https://www.facebook.com/mapletrailsoftware/">Facebook</a></nav></div><div class="wrap footer-base">© 2026 MapleTrail Software Inc.<a href="mailto:support@mapletrailsoftware.com">support@mapletrailsoftware.com</a></div></footer>'

def buttons(key,fr=False):
    if key=='ifneeded':return '<a class="button" href="/ifneeded/support/">Get in touch</a><a class="text-link" href="#features">Explore If Needed</a>'
    s=f'<a class="button" href="{STORES[key]}">'+('App Store' if key=='acadie' else 'Download on the App Store')+'</a>'
    if key=='acadie':s+=f'<a class="button secondary" href="{PLAY}">Google Play</a>'
    return s

DATA={
'acadie':dict(title='Discover the people<br>and places of Acadie.',tag='Acadie',sub='Bilingual stories, family names, and living heritage.',desc='Follow the stories that connect us. Explore communities, culture, and the roots that make Acadie your own.',photo='coast',screen='home-app-2026.jpg',platform='Available now · iPhone, iPad & Android · English & French',rows=[('Stories','Stories that connect generations.','Watch and read cinematic stories with narration, subtitles, cultural context, and sources. Follow the people and decisions that shaped Acadian life.','stories-app-2026.jpg'),('Family names','Every name has a story.','Explore Acadian surnames and the places and stories that connect generations. Save the names that matter to you and follow your own roots.','names-app-2026.jpg'),('Places','A living culture. A personal journey.','Discover communities, events, heritage trails, food traditions, voices, and cultural places. Keep your discoveries close with saved places and the Acadian Passport.','explore-app-2026.jpg')],closing='Begin your own journey through Acadie.'),
'momentslater':dict(title='Keep the<br>little moments.',tag='Moments Later',sub='Capture now. Reflect later.',desc='A gentle space for your photos, voice notes, and thoughts — so more of life’s little moments can stay with you.',photo='memories',screen='capture.webp',platform='Available now · iPhone, iPad, Mac & Apple Watch',rows=[('01 · Capture','Capture a moment.','Save a photo, a place, a thought, or something someone said. Capture on iPhone or speak a quick entry on Apple Watch, whenever life gives you something worth remembering.','capture.webp'),('02 · Revisit','Revisit your memories.','Find your moments in a timeline, then turn them into journal entries. Keep the time, place, and context of the day close to the memories.','timeline.webp'),('03 · Reflect','Make room to reflect.','Look back, notice the details, and build a journal from the everyday. Moments Later is also available on Mac, with Premium shared across your supported devices.','mac-today.webp')],closing='The little moments add up to a life.'),
'habitwallet':dict(title='Small habits.<br>Rewards you choose.',tag='Habit Wallet',sub='Turn everyday progress into something to look forward to.',desc='Complete the habits that matter, collect points in one wallet, and save for rewards you actually want.',photo='essentials',screen='wallet.webp',platform='Available now on the App Store · Built for iPhone',rows=[('01 · Your routine','Build your routine.','Add the habits that matter to you. Choose manual check-ins, timed habits, or Apple Health progress, and make them part of your day.','earn.webp'),('02 · Your progress','Collect points.','Earn points as you complete habits. Track your streaks, quests, and progress, and keep one balance for every goal.','progress.webp'),('03 · Your rewards','Choose your rewards.','Set rewards you find motivating, from a small treat to a bigger goal. Redeem the points you have earned when you are ready.','rewards.webp')],closing='Make your habits more rewarding.'),
'momentsaway':dict(title='Remember where<br>life takes you.',tag='Moments Away',sub='Your places. Your stories.',desc='Keep your places, visits, and travel memories together. Plan the next adventure and remember the details of the last.',photo='coast',screen='map.jpg',platform='Available now · iPhone · Free with optional one-time Premium',rows=[('01 · Save','Save a place.','Keep meaningful places with notes, photos, videos, and a map location. Save countries, provinces or states, cities, and landmarks — from favourite cafés to mountain trails.','places.jpg'),('02 · Remember','Remember a visit.','Capture the details that made it special: who was there, when you visited, and what you want to remember. Plan where to go next with the Travel Checklist.','trip-stories.jpg'),('03 · Revisit','Revisit the journey.','See the bigger picture of where you have been. Look back with Year in Travel, create Trip Stories, and bring your travel record to your Home Screen with Widget Studio.','year-in-travel.jpg')],closing='Remember more of what matters.'),
'ifneeded':dict(title='Make the important<br>details easier to find.',tag='If Needed',sub='Practical information for someone you trust.',desc='Bring the everyday essentials together in a calm, organized place, so someone trusted can find what they need if they ever have to step in.',photo='essentials',screen='today.jpg',platform='Private handoff planning',rows=[('01 · Organize','Organize the essentials.','Keep bills, insurance, household information, digital-life details, wishes, and trusted contacts in clearly labelled categories. Start small and build your plan over time.','my-plan.jpg'),('02 · Add context','Make the details useful.','Add helpful notes and access information, then review what needs attention. Keep the practical context close to the item it belongs to.','add-item.jpg'),('03 · Prepare','Plan for a helping hand.','Create readable handoff PDFs and trusted-person packets when you decide you are ready. You choose what to include and when to share.','settings.jpg')],closing='A calmer way to keep important information organized.')}

FRENCH=dict(title='Découvrez les gens<br>et les lieux de l’Acadie.',tag='Acadie',sub='Récits bilingues, noms de famille et patrimoine vivant.',desc='Suivez les récits qui nous relient. Explorez les communautés, la culture et les racines qui font de l’Acadie une histoire personnelle.',photo='coast',screen='home-app-2026.jpg',platform='Disponible · iPhone, iPad et Android · Français et anglais',rows=[('Récits','Des récits qui relient les générations.','Regardez et lisez des récits cinématographiques avec narration, sous-titres, contexte culturel et sources. Découvrez les gens et les décisions qui ont façonné la vie acadienne.','stories-app-2026.jpg'),('Noms de famille','Chaque nom porte une histoire.','Explorez les noms de famille acadiens et les lieux et récits qui relient les générations. Enregistrez les noms qui comptent pour vous et suivez vos racines.','names-app-2026.jpg'),('Lieux','Une culture vivante. Un parcours personnel.','Découvrez les communautés, événements, parcours patrimoniaux, traditions culinaires et lieux culturels. Gardez vos découvertes grâce aux lieux enregistrés et au Passeport acadien.','explore-app-2026.jpg')],closing='Commencez votre propre parcours en Acadie.')

def screen_path(key,name,fr=False):return f'/images/{key}/'+('fr-CA/' if fr and key=='acadie' else '')+name

def details(key,fr):
    if key=='acadie':
        return '<section class="wrap product-notes" id="interviews"><div><p class="eyebrow">'+('Pour aller plus loin' if fr else 'Behind the app')+'</p><h2>'+('Les histoires continuent.' if fr else 'The stories continue.')+'</h2><p>'+('Explorez les récits bilingues, la culture et les racines personnelles avec Acadie et l’option Acadie+.' if fr else 'Explore bilingual stories, culture, and personal roots with Acadie and optional Acadie+.')+'</p></div><div><h3>'+('Acadie dans les médias' if fr else 'Acadie in the news')+'</h3><a class="text-link" href="https://ici.radio-canada.ca/ohdio/premiere/emissions/le-reveil-nouvelle-ecosse-et-t-n/segments/rattrapage/2502170/revue-culturelle">Radio-Canada · Le Réveil</a><br><a class="text-link" href="https://lecourrier.com/francophonie/2026/10/09/application-acadie-patrimoine-et-histoire-a-lere-2-0/">Le Courrier · 9 octobre 2026</a><p class="small">'+('Entrevues avec Roger Cormier, en français.' if fr else 'Interviews with Roger Cormier, in French.')+'</p></div></section>'
    values={
    'momentslater':('More room for your memories.','Capture in seconds on iPhone or Apple Watch. Reflect on iPhone, iPad, or Mac. Premium is available now and shared across supported devices through your App Store account.','Keep the context close.','Explore richer day context, journal reflection, Memory Gallery achievements, and optional Strava activity context. Choose the features that fit the way you remember.','/privacy/'),
    'habitwallet':('Progress that fits your life.','Use manual, timed, and Apple Health habits. Insights and history help you review your routines, while points and rewards give your progress a purpose.','A little more with Premium.','Start with the core habit-and-reward loop. Explore the app’s optional Premium features as your routines grow.','/habitwallet/privacy/'),
    'momentsaway':('Your essential travel record stays free.','Places, visits, memories, Travel Checklist, World Progress, backup, and export remain free. Optional iCloud sync keeps your record across your Apple devices.','One-time Premium.','Add full Year in Travel reports, shareable Trip Stories, customizable widgets, themes, Collector Insights, and milestones with an optional one-time purchase.','/privacy/#moments-away'),
    'ifneeded':('Designed around local-first planning.','If Needed can work without a MapleTrail account. Private iCloud sync is optional. Device authentication and your choice of export help keep you in control.','A plan that can grow with you.','The starter plan supports up to eight items. The one-time Lifetime Unlock option includes unlimited items, PDF export, trusted-person packets, and private iCloud sync. Contact MapleTrail for current availability.','/ifneeded/privacy/')}
    a,b,c,d,link=values[key]
    return f'<section class="wrap product-notes" id="premium"><div><p class="eyebrow">Thoughtfully made</p><h2>{a}</h2><p>{b}</p><a class="text-link" href="{link}">Read the privacy policy</a></div><div><h3>{c}</h3><p>{d}</p></div></section>'


def recovered_sections(key,fr=False,founder_only=False):
    page=key+('/fr-CA' if fr else '')
    output=[]
    for section in PRODUCT_DETAILS[page]:
        founder=section['heading']=='Built from a real regret.'
        if founder!=founder_only:continue
        # Features retain the main screenshot anchor; Premium owns its original anchor.
        anchor='why' if founder else 'app-features' if section['id']=='features' else section['id']
        classes='founder-story' if founder else 'product-detail'
        parts=[f'<section class="wrap {classes}" id="{anchor}">']
        if section['eyebrow']:parts.append(f'<p class="eyebrow">{escape(section["eyebrow"])}</p>')
        parts.append(f'<h2>{escape(section["heading"])}</h2>')
        in_list=False
        for unit in section['units']:
            kind=unit['kind'];text=escape(unit['text'])
            if kind=='li':
                if not in_list:parts.append('<ul>');in_list=True
                parts.append(f'<li>{text}</li>');continue
            if in_list:parts.append('</ul>');in_list=False
            if kind=='link':parts.append(f'<p><a class="text-link" href="{escape(unit["href"],quote=True)}">{text}</a></p>')
            elif kind=='strong':parts.append(f'<p><strong>{text}</strong></p>')
            else:parts.append(f'<{kind}>{text}</{kind}>')
        if in_list:parts.append('</ul>')
        parts.append('</section>');output.append(''.join(parts))
    return ''.join(output)


def current_acadie(fr=False):
    data=ACADIE_CURRENT['fr' if fr else 'en']
    labels=['Jeux','Communauté','Créateurs'] if fr else ['Games','Community','Creators']
    parts=[f'<section class="wrap current-acadie" id="living-acadie"><p class="eyebrow">{escape(data["eyebrow"])}</p><h2>{escape(data["title"])}</h2><p class="current-intro">{escape(data["intro"])}</p><nav class="current-nav" aria-label="{escape(data["nav_label"])}">']
    for card,label in zip(data['cards'],labels):parts.append(f'<a href="#{card["id"]}">{label}</a>')
    parts.append('</nav><div class="current-grid">')
    for card in data['cards']:
        src=screen_path('acadie',card['image'],fr)
        parts.append(f'<article id="{card["id"]}"><h3>{escape(card["title"])}</h3><figure><a href="{src}" target="_blank" rel="noopener" aria-label="{escape(card["alt"])}">{img(src,card["alt"])}</a></figure><p>{escape(card["copy"])}</p><p class="current-note">{escape(card["note"])}</p></article>')
    parts.append(f'</div><div class="current-extras"><div id="web-radio"><h3>{escape(data["radio_title"])}</h3><p>{escape(data["radio_copy"])}</p></div><div><h3>{escape(data["plus_title"])}</h3><p>{escape(data["plus_copy"])}</p></div></div><p class="current-note">{escape(data["screenshot_note"])}</p></section>')
    return ''.join(parts)

def app_main(key,fr=False):
    d=(FRENCH if fr else DATA[key]).copy()
    if key=='acadie':
        d['screen']='current-home.webp'
        d['sub']='Récits, jeux, créateurs et communauté vivante.' if fr else 'Stories, games, creators, and a living community.'
        d['desc']='Découvrez le patrimoine et les noms de famille, rencontrez les créateurs et échangez autour de la culture acadienne. Jouez sur iPhone et iPad.' if fr else 'Explore heritage and family roots, meet creators, and connect through living Acadian culture. Play daily games on iPhone and iPad.'
    photo='/images/editorial/'+d['photo']+'.webp'
    main=f'<main id="main"><div class="wrap breadcrumb"><a href="/#apps">'+('Nos apps' if fr else 'Our apps')+f'</a><span>/</span><span>{d["tag"]}</span></div><section class="product-hero"><div class="wrap product-hero-grid"><div class="product-hero-copy"><p class="product-name">{d["tag"]}</p><h1>{d["title"]}</h1><p class="subhead">{d["sub"]}</p><div class="actions">{buttons(key,fr)}</div><p class="hero-description">{d["desc"]}</p><p class="availability">{d["platform"]}</p></div><figure class="product-art">{img(photo,"", "scene",False)}{img(screen_path(key,d["screen"],fr),d["tag"]+(" — écran de l’app" if fr else " — actual app screen"),"hero-screen",False)}</figure></div></section><section id="features" class="wrap story-rows">'
    if key=='acadie':
        main=main.replace('<section id="features" class="wrap story-rows">',current_acadie(fr)+'<section id="features" class="wrap story-rows">')
        main=main.replace('<p class="hero-description">','<a class="text-link founder-link" href="#living-acadie">'+('Jeux, Communauté et créateurs' if fr else 'Games, Community, and creators')+'</a><p class="hero-description">')
    if key=='momentslater':
        marker='<section id="features" class="wrap story-rows">'
        main=main.replace(marker,recovered_sections(key,fr,True)+marker)
        main=main.replace('<p class="hero-description">','<a class="text-link founder-link" href="#why">Why I built Moments Later</a><p class="hero-description">')
    for i,(label,title,copy,screen) in enumerate(d['rows']):
        wide=' wide-screen' if screen.startswith('mac-') else ''
        main+=f'<article class="story-row"><figure class="story-visual{wide}">{img(photo,"","story-photo")}{img(screen_path(key,screen,fr),d["tag"]+" — "+title,"story-screen")}</figure><div class="story-copy"><p class="eyebrow">{label}</p><h2>{title}</h2><p>{copy}</p></div></article>'
    main+='</section>'+recovered_sections(key,fr)
    main+=f'<section class="wrap closing"><p class="eyebrow">'+('À vous de découvrir' if fr else 'Made for your everyday')+f'</p><h2>{d["closing"]}</h2><div class="actions">{buttons(key,fr)}</div></section></main>'
    return main

def home_main():
    result='<main id="main"><section class="coastal-hero">'+img('/images/editorial/coast.webp','','coastal-photo',False)+'<div class="wrap"><div class="coastal-copy"><p class="eyebrow">Independent software, thoughtfully made</p><h1>Thoughtful apps.<br>Personal connections.</h1><p>For the moments, places,<br>and details worth keeping.</p><a class="button" href="#apps">Explore our apps</a></div></div></section>'
    result+='<section class="wrap featured-app"><div class="featured-copy"><p class="eyebrow">Featured app</p><h2>Acadie</h2><p>Discover the people, places, and stories that keep Acadian heritage alive.</p><p class="small">Community, creators & Web Radio.<br>Games on iPhone & iPad.<br>English & French · iOS & Android</p><a class="text-link" href="/acadie/">Discover Acadie</a></div><div class="featured-visual">'+img('/images/editorial/coast.webp','','featured-photo')+'<div class="featured-screens">'+img('/images/acadie/current-home.webp','Acadie home screen with stories, Web Radio, and games.','')+img('/images/acadie/explore-app-2026.jpg','Acadie Explore screen with communities and places.','')+'</div></div></section>'
    result+='<section id="apps" class="wrap app-collection"><div class="section-title"><p class="eyebrow">Our apps</p><p>A little more meaning in the everyday.</p></div><div class="app-grid">'
    photos={'momentslater':'memories','habitwallet':'essentials','momentsaway':'coast','ifneeded':'essentials'}
    summaries={'momentslater':'A simpler way to keep today’s little moments.','habitwallet':'Small steps. Rewards that matter to you.','momentsaway':'Keep your places and travel stories together.','ifneeded':'Keep the important details within reach.'}
    for key in photos:
        result+=f'<article class="app-card {key}"><a class="app-photo" href="/{key}/" tabindex="-1" aria-hidden="true">'+img('/images/editorial/'+photos[key]+'.webp','','')+f'</a><h3><a href="/{key}/">{NAMES[key]}</a></h3><p>{summaries[key]}</p><a class="text-link" href="/{key}/" aria-label="Learn more about {NAMES[key]}">Learn more</a></article>'
    result+='</div></section><section id="about" class="about-band"><div class="wrap about-grid"><p class="eyebrow">About MapleTrail</p><div><h2>Care in the details.<br>Room for real life.</h2><p>MapleTrail Software Inc. is an independent software company building apps for memory, travel, everyday routines, practical planning, and Acadian cultural discovery.</p><p>Different purposes. The same care for clear design, personal connection, and long-term usefulness.</p><a class="text-link" href="mailto:support@mapletrailsoftware.com">Get in touch</a></div></div></section></main>'
    return result

def write_page(path,main,key=None,fr=False):
    p=ROOT/path;soup=BeautifulSoup(p.read_text(),'html.parser')
    head=str(soup.head)
    desc={'acadie':('Acadie est disponible sur iOS et Android. Découvrez les récits, forums, créateurs, Acadie Web Radio, lieux et racines. Jouez sur iPhone et iPad.' if fr else 'Acadie is available on iOS and Android. Explore stories, Community, creators, Web Radio, places, and family roots. Play daily games on iPhone and iPad.'),'momentslater':'Capture now. Reflect later. Moments Later is available on iPhone, iPad, Mac, and Apple Watch, with shared Premium across supported devices.',None:'Thoughtful apps. Personal connections. Discover Acadie, Moments Later, Habit Wallet, Moments Away, and If Needed from MapleTrail Software Inc.'}.get(key)
    if desc:
        for meta in soup.head.select('meta[name="description"], meta[property="og:description"], meta[name="twitter:description"]'):meta['content']=desc
        head=str(soup.head)
    body=f'<body class="editorial {key or "home"}">{header(fr,key=="acadie")}{main}{footer(fr,key)}</body>'
    if 'editorial.css' not in head:head=head.replace('</head>','<link rel="stylesheet" href="/editorial.css">\n</head>')
    p.write_text('<!doctype html>\n<html lang="'+('fr-CA' if fr else 'en')+'">\n'+head+'\n'+body.replace('<br>','<br> ')+'\n</html>\n')

write_page('index.html',home_main())
for k in DATA:write_page(k+'/index.html',app_main(k),k)
write_page('acadie/fr-CA/index.html',app_main('acadie',True),'acadie',True)
# Legal/support copy remains verbatim; share the same shell and editorial reading style.
for p in ROOT.rglob('index.html'):
    if p.relative_to(ROOT).as_posix() in ['index.html']+[k+'/index.html' for k in DATA]+['acadie/fr-CA/index.html']:continue
    s=BeautifulSoup(p.read_text(),'html.parser');fr=s.html.get('lang','').startswith('fr');key=p.relative_to(ROOT).parts[0]
    s.body['class']=['editorial','document-page'];[x.decompose() for x in s.select('.skip-link')];s.header.replace_with(BeautifulSoup(header(fr,key=='acadie',p.parent.name+'/'),'html.parser'));s.footer.replace_with(BeautifulSoup(footer(fr,key),'html.parser'));s.main['id']='main'
    if not s.select_one('link[href="/editorial.css"]'):
        l=s.new_tag('link',rel='stylesheet',href='/editorial.css');s.head.append(l)
    p.write_text(str(s))
print('Built 7 marketing pages and shared shell on 12 support/legal pages.')
