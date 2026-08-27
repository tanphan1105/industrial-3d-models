import re
import shutil
from pathlib import Path

file_path = Path(r'd:\WT3D_Project\landing_page_v3_master.html')
backup_path = file_path.with_suffix(file_path.suffix + '.bak')

def sub_once(content, pattern, repl, label):
    new_content, count = re.subn(pattern, repl, content, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f'Not matched: {label}')
    return new_content

def replace_once(content, old, new, label):
    count = content.count(old)
    if count != 1:
        raise ValueError(f'Expected 1 match for {label}, found {count}')
    return content.replace(old, new, 1)

content = file_path.read_text(encoding='utf-8')
backup_path.write_text(content, encoding='utf-8')
print(f'Backup created: {backup_path}')

try:
    content = sub_once(
        content,
        r'<title>.*?</title>',
        '<title>Industrial Water Treatment 3D Models | RO Skids, Filter Systems, Membrane Housings</title>',
        'title'
    )

    content = sub_once(
        content,
        r'<meta content=".*?" name="description"/>',
        '<meta content="Browse industrial water treatment 3D models for RO skids, membrane housings, filter systems, ozone generators and plant components. Built for product demos, proposals, AR presentations and technical marketing." name="description"/>',
        'meta description'
    )

    content = sub_once(
        content,
        r'<meta content=".*?" property="og:title"/>',
        '<meta content="Industrial Water Treatment 3D Models for Proposals, AR Demos & Product Sales" property="og:title"/>',
        'og:title'
    )

    content = sub_once(
        content,
        r'<meta content=".*?" property="og:description"/>',
        '<meta content="Engineering-grade 3D models of RO systems, filtration skids and industrial components to help sales teams, engineers and product marketers present equipment more clearly." property="og:description"/>',
        'og:description'
    )

    content = replace_once(
        content,
        '''<div class="hero-ey rv" style="background:rgba(52,199,89,.1);color:var(--go);box-shadow:inset 0 0 0 1px rgba(52,199,89,.2)"><span class="n-dot" style="background:var(--go);box-shadow:0 0 6px var(--go)"></span> 100% CAD-Accurate • Zero Hallucination</div>''',
        '''<div class="hero-ey rv" style="background:rgba(52,199,89,.1);color:var(--go);box-shadow:inset 0 0 0 1px rgba(52,199,89,.2)"><span class="n-dot" style="background:var(--go);box-shadow:0 0 6px var(--go)"></span> Industrial-grade • AR-ready • Real-world scale</div>''',
        'hero ey'
    )

    content = replace_once(
        content,
        '''<h1 class="rv d1">Water Treatment.<br/><span class="gr">Built in 3D.</span></h1>
<p class="rv d2">Drop-in ready 3D models of RO Systems and filtration skids. Engineered to exact P&amp;ID specs for <strong>Sales Engineers, EPC Contractors, and 3D Artists</strong> to help close six-figure projects faster.</p>''',
        '''<h1 class="rv d1">Industrial Water Treatment<br/><span class="gr">3D Models That Sell Better</span></h1>
<p class="rv d2">Show buyers exactly what they are getting. Browse engineering-grade 3D models of RO skids, membrane housings, filter systems and industrial components for proposals, product pages, AR presentations and technical demos.</p>''',
        'hero text'
    )

    content = replace_once(
        content,
        '''<div class="hero-acts rv d3">
<a class="btn-p" href="#systems">Browse Models</a>
<a class="chev" href="AR_Industrial_Ozone_Generator.usdz" onmouseout="this.style.borderColor='rgba(0,0,0,.08)'" onmouseover="this.style.borderColor='var(--ac)'" rel="ar" style="background:var(--bg);border:1px solid rgba(0,0,0,.08);padding:12px 24px;border-radius:100px;color:var(--tx);transition:border-color .2s;display:flex;align-items:center;box-shadow:0 8px 24px rgba(0,0,0,.03)">
<svg fill="none" height="18" stroke="currentColor" stroke-width="2" style="margin-right:8px;color:var(--ac)" viewbox="0 0 24 24" width="18"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" x2="12" y1="22.08" y2="12"></line></svg>
        Direct AR File
      </a>
</div>''',
        '''<div class="hero-acts rv d3">
<a class="btn-p" href="https://www.fab.com/sellers/Trong%20Tan%20Phan" target="_blank">Browse Models on Fab</a>
<a class="chev" href="https://www.cgtrader.com/designers/tanphan1105" target="_blank" style="padding:12px 24px;display:inline-flex;align-items:center;">View on CGTrader</a>
</div>''',
        'hero actions'
    )

    content = replace_once(
        content,
        '''<div class="stats">
<div class="stat rv"><div class="stat-n"><span class="cu" data-t="27">0</span><em>+</em></div><div class="stat-l">3D Models</div></div>
<div class="stat rv d1"><div class="stat-n">2</div><div class="stat-l">Product Lines</div></div>
<div class="stat rv d2"><div class="stat-n">2</div><div class="stat-l">Platforms</div></div>
<div class="stat rv d3"><div class="stat-n">OBJ<em>+</em></div><div class="stat-l">FBX / GLB / 3DS</div></div>
</div>''',
        '''<div class="stats">
<div class="stat rv"><div class="stat-n"><span class="cu" data-t="27">0</span><em>+</em></div><div class="stat-l">Models Available</div></div>
<div class="stat rv d1"><div class="stat-n">2</div><div class="stat-l">Sales Platforms</div></div>
<div class="stat rv d2"><div class="stat-n">AR</div><div class="stat-l">Ready Assets</div></div>
<div class="stat rv d3"><div class="stat-n">OBJ<em>+</em></div><div class="stat-l">FBX / GLB / 3DS</div></div>
</div>''',
        'stats'
    )

    content = replace_once(
        content,
        '''<div class="sh-l" style="color:var(--ac)">The Conversion Gap</div>
<h2 style="font-size:clamp(24px,3.5vw,40px);font-weight:800;letter-spacing:-.03em;line-height:1.1;margin-bottom:20px">Procurement managers don't read P&amp;IDs. They approve what they can see.</h2>
<p style="font-size:15px;color:var(--tx-s);line-height:1.7;margin-bottom:32px">Your RO membrane layout, antiscalant dosing skid, and TDS sensor placement are intuitive to you. To a decision-maker reviewing a capital expenditure, a 2D drawing is noise.</p>
<div style="display:flex;gap:40px">
<div><div style="font-size:36px;font-weight:800;color:var(--ac)">3×</div><div style="font-size:12px;color:var(--tx-t);margin-top:4px">Faster project<br/>approval rate</div></div>
<div><div style="font-size:36px;font-weight:800">100%</div><div style="font-size:12px;color:var(--tx-t);margin-top:4px">Real-world scale<br/>engineering precision</div></div>
<div><div style="font-size:36px;font-weight:800;color:var(--tx-s)">0</div><div style="font-size:12px;color:var(--tx-t);margin-top:4px">Questions from<br/>non-technical buyers</div></div>
</div>
</div>
<div class="pq rv d1">
<blockquote>"We dropped the RO 30 m³/h model into our proposal deck. The client pointed at the membrane housing and said — 'So this is where the pressure drops?' We closed the project in one meeting."</blockquote>
<cite>Sales Engineer · Water Treatment, Southeast Asia</cite>''',
        '''<div class="sh-l" style="color:var(--ac)">Why 3D Sells Faster</div>
<h2 style="font-size:clamp(24px,3.5vw,40px);font-weight:800;letter-spacing:-.03em;line-height:1.1;margin-bottom:20px">Technical drawings explain the system. 3D models help buyers say yes.</h2>
<p style="font-size:15px;color:var(--tx-s);line-height:1.7;margin-bottom:32px">When clients, procurement teams or non-technical stakeholders cannot picture the equipment, decisions slow down. Clear 3D models make RO skids, vessels and filtration layouts easier to understand in proposals, product demos and AR presentations.</p>
<div style="display:flex;gap:40px">
<div><div style="font-size:36px;font-weight:800;color:var(--ac)">27+</div><div style="font-size:12px;color:var(--tx-t);margin-top:4px">Industrial models<br/>ready to browse</div></div>
<div><div style="font-size:36px;font-weight:800">100%</div><div style="font-size:12px;color:var(--tx-t);margin-top:4px">Real-world scale<br/>for clear presentations</div></div>
<div><div style="font-size:36px;font-weight:800;color:var(--tx-s)">AR</div><div style="font-size:12px;color:var(--tx-t);margin-top:4px">Ready assets for<br/>interactive demos</div></div>
</div>
</div>
<div class="pq rv d1">
<blockquote>"Used by sales teams, engineers and 3D artists to present industrial equipment more clearly in client meetings, proposal decks, product pages and AR demos."</blockquote>
<cite>Industrial Visualization Use Cases</cite>''',
        'conversion section'
    )

    content = replace_once(
        content,
        '''<div class="sh-l">Category 01 · System Packages &amp; Skids</div>
<h2>Water Treatment <span class="gr">Skids</span></h2>
<p>Full-scale RO, filtration and chemical dosing skids — modeled to exact P&amp;ID dimensions with every pipe, valve and instrument.</p>''',
        '''<div class="sh-l">Category 01 · Complete Systems &amp; Skids</div>
<h2>System-Level <span class="gr">3D Models</span></h2>
<p>Browse full RO, filtration and dosing skids built for proposals, client presentations, web showcases and AR demonstrations.</p>''',
        'systems heading'
    )

    content = replace_once(
        content,
        '''<div class="sh-l" style="color:var(--ac)">Category 02 · Single Equipment &amp; Components</div>
<h2>Components &amp; <span class="gr">Equipment</span></h2>
<p>Ozone generators, pumps, membrane housings, valves, flow meters, control panels — modeled individually for maximum reuse across projects.</p>''',
        '''<div class="sh-l" style="color:var(--ac)">Category 02 · Components &amp; Equipment</div>
<h2>Reusable <span class="gr">Industrial Assets</span></h2>
<p>Membrane housings, valves, tanks, filter housings and related equipment modeled as standalone assets for product renders, training scenes and technical visualization.</p>''',
        'equipment heading'
    )

    content = replace_once(
        content,
        '''<div style="font-family:var(--fm);font-size:11px;color:#86868b;text-transform:uppercase;letter-spacing:.1em;margin-bottom:16px">B2B SALES ENGINEERING · OBJ FBX GLB USDZ</div>
<h2>Stop losing bids.<br/>Show them the <span class="gr">Reality.</span></h2>
<p>Procurement managers don't read P&amp;IDs. Give them a 100% CAD-accurate 3D model they can explore in AR. Close your next six-figure project faster.</p>
<div class="mega-acts">
<a class="btn-p" href="https://www.fab.com/sellers/Trong%20Tan%20Phan" target="_blank">Browse 22+ Industrial Models</a>
<a class="btn-s" href="https://www.cgtrader.com/designers/tanphan1105" target="_blank">View on CGTrader</a>
</div>
<div class="mega-stats rv d1">
<div class="m-stat"><div class="m-stat-n">20+</div><div class="m-stat-l">Industrial Models</div></div>
<div class="m-stat"><div class="m-stat-n">100%</div><div class="m-stat-l">Real-world Scale</div></div>
<div class="m-stat"><div class="m-stat-n">PBR</div><div class="m-stat-l">Physical Textures</div></div>
</div>''',
        '''<div style="font-family:var(--fm);font-size:11px;color:#86868b;text-transform:uppercase;letter-spacing:.1em;margin-bottom:16px">Industrial 3D Assets · Fab · CGTrader · AR Ready</div>
<h2>Help Buyers Understand<br/>the <span class="gr">Equipment Faster</span></h2>
<p>Use ready-made industrial 3D models to make proposals clearer, product demos stronger and technical presentations easier to follow.</p>
<div class="mega-acts">
<a class="btn-p" href="https://www.fab.com/sellers/Trong%20Tan%20Phan" target="_blank">Browse All Models on Fab</a>
<a class="btn-s" href="https://www.cgtrader.com/designers/tanphan1105" target="_blank">See More on CGTrader</a>
</div>
<div class="mega-stats rv d1">
<div class="m-stat"><div class="m-stat-n">27+</div><div class="m-stat-l">Industrial Models</div></div>
<div class="m-stat"><div class="m-stat-n">100%</div><div class="m-stat-l">Real-world Scale</div></div>
<div class="m-stat"><div class="m-stat-n">AR</div><div class="m-stat-l">Ready Selection</div></div>
</div>''',
        'mega cta'
    )

    content = replace_once(
        content,
        '''<div class="faq">
<div class="fi rv d1"><div class="fq">Do the models include PBR textures?</div><div class="fa"><p>Yes. Every model ships with full PBR texture sets — Base Color, Roughness, Metallic, and Normal maps — optimized for Blender Cycles, 3ds Max V-Ray, and Unreal Engine 5.</p></div></div>
<div class="fi rv d2"><div class="fq">Are models built to real-world scale?</div><div class="fa"><p>Yes. All models are exported in real-world units (meters). Pipe diameters, flange dimensions and vessel sizes match industrial catalogue specifications.</p></div></div>
<div class="fi rv d2"><div class="fq">Can I request a custom model for my specific project?</div><div class="fa"><p>Absolutely. I build custom 3D models from your 2D CAD drawings or P&amp;ID schematics. A typical RO skid (up to 50 m³/h) takes 2–4 business days. Contact me via Zalo or email for a detailed quote.</p></div></div>
<div class="fi rv d3"><div class="fq">What software is supported?</div><div class="fa"><p>OBJ and FBX formats are compatible with Blender, 3ds Max, Maya, Cinema 4D, SketchUp and Unreal Engine 5. GLB files work natively in web-based 3D viewers and AR applications.</p></div></div>
<div class="fi rv d3"><div class="fq">Can I use these for VR/AR training?</div><div class="fa"><p>Yes. The models are optimized with clean topology and game-ready polycounts (&lt; 250k for full skids). They run at 60+ FPS in Unity and Unreal Engine, making them perfect for virtual reality operator training or Apple Vision Pro presentations.</p></div></div>
<div class="fi rv d3"><div class="fq">What about Commercial Licensing and Copyrights?</div><div class="fa"><p>All purchases include a standard royalty-free license. You can use the models in commercial presentations, video renders, and real-time apps. Reselling the raw 3D files or claiming them as your own is strictly prohibited.</p></div></div>
<div class="fi rv d3"><div class="fq">Are the 3D models rigged or animated?</div><div class="fa"><p>Currently, the skids are static geometry (not rigged). However, all moving parts like pump shafts, valve handles, and switches are separated by logical meshes so you can easily assign pivots and animate them yourself.</p></div></div>
</div>''',
        '''<div class="faq">
<div class="fi rv d1"><div class="fq">What file formats are included?</div><div class="fa"><p>Most models are available in widely used formats such as OBJ, FBX and GLB, making them suitable for 3D software, web viewers and AR workflows.</p></div></div>
<div class="fi rv d2"><div class="fq">Are the models built to real-world scale?</div><div class="fa"><p>Yes. The models are prepared at real-world scale so they are easier to use in technical presentations, product visualization and spatial review.</p></div></div>
<div class="fi rv d2"><div class="fq">Can I use these models for commercial presentations or product marketing?</div><div class="fa"><p>Yes. These assets are suitable for commercial use cases such as proposal decks, marketing visuals, website presentations and product demonstrations, subject to each platform license.</p></div></div>
<div class="fi rv d3"><div class="fq">Do you offer custom models based on CAD or P&amp;ID drawings?</div><div class="fa"><p>Yes. If you need a specific RO skid, vessel or industrial component that is not listed in the store, you can request a custom 3D model based on your drawings or references.</p></div></div>
<div class="fi rv d3"><div class="fq">Which models are suitable for AR or web viewing?</div><div class="fa"><p>AR-ready and GLB-based assets are the best fit for interactive product demos, client presentations and browser-based 3D viewing.</p></div></div>
<div class="fi rv d3"><div class="fq">Who are these models for?</div><div class="fa"><p>They are built for sales engineers, equipment suppliers, 3D artists, technical marketers and teams that need to present industrial water treatment equipment clearly.</p></div></div>
</div>''',
        'faq'
    )

    content = replace_once(
        content,
        '''<h2 style="font-size:clamp(24px,3.5vw,40px);font-weight:800;letter-spacing:-.03em;line-height:1.1;margin-bottom:16px">Need a custom model?</h2>
<p style="font-size:15px;color:var(--tx-s);line-height:1.7;margin-bottom:32px">I design engineering-accurate 3D models from your specifications — any capacity, any configuration, any format. Response within 24 hours.</p>''',
        '''<h2 style="font-size:clamp(24px,3.5vw,40px);font-weight:800;letter-spacing:-.03em;line-height:1.1;margin-bottom:16px">Need a specific industrial model?</h2>
<p style="font-size:15px;color:var(--tx-s);line-height:1.7;margin-bottom:32px">If you cannot find the exact RO skid, vessel or component in the store, request a custom 3D model based on your drawing, specification or reference image.</p>''',
        'contact heading'
    )

    content = replace_once(
        content,
        '''<div style="font-family:var(--fm);font-size:10px;color:var(--tx-t);letter-spacing:.14em;text-transform:uppercase;margin-bottom:12px">Custom Design Service</div>
<p style="color:var(--tx-s);font-size:14px;line-height:1.7;margin-bottom:24px">RO 50 m³/h, SWRO desalination, UF membrane skid, chemical dosing, wastewater treatment — any configuration you need.</p>
<a class="btn-p" href="mailto:trongtan.p@icloud.com" style="display:inline-flex">Send Request</a>''',
        '''<div style="font-family:var(--fm);font-size:10px;color:var(--tx-t);letter-spacing:.14em;text-transform:uppercase;margin-bottom:12px">Custom Model Service</div>
<p style="color:var(--tx-s);font-size:14px;line-height:1.7;margin-bottom:24px">RO systems, filtration skids, membrane housings, tanks, dosing units and other industrial water treatment equipment available on request.</p>
<a class="btn-p" href="mailto:trongtan.p@icloud.com" style="display:inline-flex">Request Custom Model</a>''',
        'contact card'
    )

    content = replace_once(
        content,
        '''<p style="color:var(--tx-s);font-size:13px;line-height:1.6;max-width:260px">Engineering-accurate 3D models of water treatment systems for B2B sales and engineering teams worldwide.</p>''',
        '''<p style="color:var(--tx-s);font-size:13px;line-height:1.6;max-width:260px">Industrial water treatment 3D models for proposals, product demos, AR presentations and technical marketing.</p>''',
        'footer intro'
    )

    file_path.write_text(content, encoding='utf-8')
    print('SEO copy applied successfully.')

except Exception as e:
    print(f'Update failed: {e}')
    shutil.copy2(backup_path, file_path)
    print('Rollback complete.')
