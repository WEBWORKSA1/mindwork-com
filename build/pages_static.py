# Stand-alone pages: daily workout, dashboard, lead plan, teams, support, contests, careers, about, contact, legal, 404.

def head(h1, lede):
    return '<div class="page-head"><h1>%s</h1><p>%s</p></div>' % (h1, lede)


def daily(c):
    return head('Today’s five-minute workout', 'Three tests chosen for today, the same for every visitor. Do them in any order. Finishing all three extends your streak.') + '''
<ul class="tiles" id="daily-picks"></ul>
<p id="daily-status" class="note focus" style="margin-top:16px" role="status"></p>
<section class="section"><div class="two">
<div class="panel"><h2>Your week</h2><ul class="streak" id="streak-dots" aria-label="Workouts completed in the last seven days"></ul><p class="muted" style="margin:12px 0 0">Longest streak: <b id="streak-best">0</b> days</p></div>
<div class="panel"><h2>Why a daily set</h2><p>Short, regular measurements tell you more than occasional long ones. Reaction time and attention scores move with sleep, stress and time of day, and a week of results shows your pattern.</p><p class="muted" style="margin:0">The workout is a gauge and a warm-up. It will not raise your intelligence; the <a href="{R}guides/does-brain-training-work.html">brain-training guide</a> explains what the evidence does and does not show.</p></div>
</div></section>''' + c['ad']('mid') + '<section class="section"><h2>All nine tests</h2><ul class="tiles">' + c['tiles'] + '</ul></section>'


def dashboard(c):
    return head('My scores', 'Your results, streak and focus time. Everything on this page is stored in this browser only; nothing is sent to a server.') + '''
<div class="three">
<div class="panel ink"><h3>MindWork.com score</h3><b class="bignum" id="comp-score">–</b><p class="muted" id="comp-note" style="margin:6px 0 0"></p></div>
<div class="panel"><h3>Workout streak</h3><b class="bignum" id="dash-streak">0</b><p class="muted" style="margin:6px 0 0">days in a row. Longest: <span id="dash-streak-best">0</span>. <a href="{R}daily.html">Open today’s workout</a></p></div>
<div class="panel"><h3>Focus time</h3><p id="focus-total" style="font-weight:700"></p><p class="muted" style="margin:0">Counted by the <a href="{R}focus/focus-timer.html">focus timer</a>.</p></div>
</div>
<section class="section"><h2>Tests</h2><div class="table-scroll"><table><thead><tr><th>Test</th><th class="num">Best</th><th class="num">Last</th><th class="num">Attempts</th><th>0 to 100 scale</th></tr></thead><tbody id="score-rows"></tbody></table></div>
<p class="muted">The scale maps each result between a fixed low and high anchor so different tests can share one bar. It is for tracking yourself and is not a percentile.</p></section>
<section class="section"><h2>Focus sessions, last seven days</h2><div class="table-scroll"><table><thead><tr><th>Day</th><th class="num">Sessions</th><th class="num">Focus time</th></tr></thead><tbody id="focus-rows"></tbody></table></div></section>
<section class="section"><h2>Your data</h2><p>Download a copy of everything this site has stored in your browser, or delete it.</p><div class="btn-row"><button class="btn ghost" type="button" id="export-btn">Download my data</button><button class="btn ghost" type="button" id="reset-btn">Delete my data</button></div></section>'''


PLAN = [
 ('Day 1', 'Measure your baseline', 'Take the <a href="{R}train/reaction-time.html">reaction time</a>, <a href="{R}train/stroop-test.html">Stroop</a> and <a href="{R}train/number-memory.html">number memory</a> tests at a time you can repeat next week. Write down the hour. You are measuring your starting point, not competing.'),
 ('Day 2', 'Protect one block', 'Tonight, choose one task for tomorrow and its first physical action. Block 60 minutes for it in the <a href="{R}focus/time-block-planner.html">time-block planner</a>, as early in the day as your calendar allows.'),
 ('Day 3', 'Close the exits', 'For today’s block: email and chat fully closed, phone in another room. Run two 25-minute sessions on the <a href="{R}focus/focus-timer.html">focus timer</a>. Note how many times you reached for something.'),
 ('Day 4', 'Batch your messages', 'Check email and chat at three fixed times only, for example 10:00, 13:00 and 16:00. At the end of the day, write down what went wrong because of it. Usually nothing did.'),
 ('Day 5', 'Sort the list', 'Put every open task into the <a href="{R}focus/eisenhower-matrix.html">Eisenhower matrix</a>. Do one item from the top-left box, put dates on the top-right box, and drop or hand off two things from the bottom row.'),
 ('Day 6', 'Recover properly', 'Take a ten-minute walk between blocks instead of opening a feed. Do three minutes of long-exhale breathing on the <a href="{R}focus/breathing-pacer.html">breathing pacer</a> before your hardest task. Stop caffeine by early afternoon and dim the lights an hour before bed.'),
 ('Day 7', 'Measure again and plan the week', 'Retake the three tests at the same hour as Day 1 and compare on your <a href="{R}dashboard.html">dashboard</a>. Then block next week’s focus sessions before the week fills up. Keep the two changes that helped most.'),
]


def start(c):
    f = c['form']('lead-form', 'Focus reset sign-up', 'Unlocked. All seven days are open below.',
        '<div class="row">' + c['field']('First name', 'name', extra='autocomplete="given-name" maxlength="60"') + c['field']('Email', 'email', 'email', extra='autocomplete="email" maxlength="120"') + '</div>'
        + c['select']('What gets in your way most?', 'obstacle', ['Getting started', 'Interruptions from other people', 'My own phone and feeds', 'Too many tasks', 'Low energy', 'Meetings']),
        'Unlock the 7-day plan', 'Unlock the plan in my browser and email me occasional MindWork.com updates. I can unsubscribe at any time. <a href="{R}privacy.html">Privacy policy</a>.', unlock=True)
    day = lambda d: '<div class="panel" style="margin-bottom:12px"><h3>%s: %s</h3><p style="margin:0">%s</p></div>' % d
    return head('The free 7-day focus reset', 'One small change a day for a week, using the free tools on this site. About ten minutes a day. Day 1 is open below; sign up to unlock the rest in your browser.') + '''
<div class="lead" style="margin-bottom:26px"><div><h2>What you get</h2><ul><li>A seven-day plan with one clear action a day</li><li>A before-and-after measurement of your own reaction time, attention and memory span</li><li>A printable version to keep on your desk</li><li>Occasional email when a new tool or guide is published</li></ul><p style="margin-top:14px">It is free, and it stays free. The site is paid for by advertising and supporters.</p></div><div>''' + f + '''</div></div>
<h2>The plan</h2>''' + day(PLAN[0]) + '<div class="locked" id="plan-lock"><p class="gate-msg">Sign up above to unlock days 2 to 7</p><div class="gate">' + ''.join(day(d) for d in PLAN[1:]) + '''</div></div>
<div class="btn-row no-print" style="margin-top:14px"><button class="btn ghost" type="button" id="print-plan" hidden onclick="window.print()">Print the plan</button></div>
<section class="section"><h2>Questions</h2><div class="two"><div><h3>Do I have to sign up?</h3><p>No. Day 1 is open, and every tool the plan uses is free without an account. Signing up unlocks the full seven days on this page and adds you to the update list.</p><h3>What will you email me?</h3><p>Occasional notes about new tools and guides. Your address is not sold or shared, and every email will tell you how to stop them.</p></div>
<div><h3>Will a week change anything?</h3><p>A week is long enough to find out which one or two changes help you most. It is not long enough to build a habit; that takes keeping those two changes going.</p><h3>Is this a medical or therapy programme?</h3><p>No. It is a set of work habits. If you are struggling with attention, sleep or mood in a way that affects your life, talk to a doctor.</p></div></div></section>'''


def teams(c):
    f = c['form']('teams-form', 'Teams and sponsorship inquiry', 'Sent. We reply by email, usually within a few working days.',
        '<div class="row">' + c['field']('Your name', 'name', extra='autocomplete="name" maxlength="80"') + c['field']('Work email', 'email', 'email', extra='autocomplete="email" maxlength="120"') + '</div>'
        '<div class="row">' + c['field']('Organisation', 'organisation', extra='maxlength="100"') + c['select']('Team size', 'team_size', ['1 to 10', '11 to 50', '51 to 250', '251 to 1,000', 'More than 1,000']) + '</div>'
        + c['select']('What are you interested in?', 'interest', ['A focus workshop for my team', 'Sponsoring a tool, guide or the monthly challenge', 'Advertising on the site', 'Licensing the tests or tools', 'A content or research partnership', 'Something else'])
        + '<label>What would you like to achieve?<textarea name="message" maxlength="2000" required></textarea></label>', 'Send my inquiry')
    return head('For teams, sponsors and partners', 'Bring the focus tools to your team, put your name beside a tool people use every day, or build something with us.') + '''
<div class="three" style="margin-bottom:26px">
<div class="panel"><h3>Focus workshop</h3><p>A 60-minute remote session for your team built on the deep work protocol: measure, protect one block, cut switching. Includes the 7-day plan as a team challenge.</p></div>
<div class="panel"><h3>Sponsorship</h3><p>Sponsor a single tool, a guide or the monthly challenge. Sponsors are named on the page they support and are always labelled as sponsors.</p></div>
<div class="panel"><h3>Licensing and partnerships</h3><p>Use the tests or planners inside your own intranet, course or product, or work with us on content and research.</p></div>
</div>
<div class="two"><div><h2>Tell us what you need</h2>''' + f + '''</div>
<div><h2>How it works</h2><ol class="steps"><li>Send the form. It goes straight to the person who runs the site.</li><li>We reply by email with questions, options and a price where one applies.</li><li>Nothing is booked or charged until you confirm in writing.</li></ol>
<p class="note">Looking to buy or lease the website or the domain name itself? Use the <a href="https://web.works/contact" target="_blank" rel="noopener">business contact page</a>.</p>
<h3>Editorial independence</h3><p class="muted">Sponsors and advertisers do not review or change what the guides say. Sponsored placements are labelled. See <a href="{R}editorial.html">how we write</a>.</p></div></div>'''


def support(c):
    amounts = ''.join('<label><input type="radio" name="amount" value="%s"%s><span>$%s</span></label>' % (a, ' checked' if a == '15' else '', a) for a in ('5', '15', '50', '150'))
    f = c['form']('support-form', 'Support pledge', 'Thank you. We will email you secure payment details for your pledge.',
        '<div><b>Choose an amount (US dollars)</b><div class="amounts" style="margin-top:8px">' + amounts + '</div></div>'
        '<div class="row"><label>Or another amount<input type="number" name="amount_other" id="amount-other" min="1" max="100000" step="1" placeholder="Any amount"></label>' + c['select']('How often?', 'frequency', ['One time', 'Every month']) + '</div>'
        '<div class="row">' + c['field']('Your name', 'name', extra='autocomplete="name" maxlength="80"') + c['field']('Email', 'email', 'email', extra='autocomplete="email" maxlength="120"') + '</div>'
        + c['select']('Put it toward', 'purpose', ['Wherever it is needed most', 'Keeping the site running', 'Paying writers, designers and developers', 'Contests and prizes', 'Outreach and promotion'])
        + '<label>A note, if you like<textarea name="message" maxlength="1000" style="min-height:70px"></textarea></label>', 'Send my pledge',
        'I understand this is a pledge, not a payment. Email me payment details. <a href="{R}privacy.html">Privacy policy</a>.')
    return head('Support MindWork.com', 'Every test, tool and guide here is free. Advertising covers part of the cost; supporters cover the rest and decide how fast new things get built.') + '''
<div class="two"><div><h2>Make a pledge</h2><div id="pay-now" class="btn-row" hidden style="margin-bottom:16px"></div>''' + f + '''
<p class="muted" style="margin-top:12px">Support is a voluntary gift to an independent website. It is not a charitable donation and is not tax-deductible. No goods or services are owed in return.</p></div>
<div><h2>Where support goes</h2><p>Our target split for every dollar received:</p>
<ul class="alloc"><li><span>Running the site</span><i style="width:30%"></i><b>30%</b></li><li><span>Contributors</span><i style="width:30%"></i><b>30%</b></li><li><span>Contests and prizes</span><i style="width:20%"></i><b>20%</b></li><li><span>Outreach</span><i style="width:20%"></i><b>20%</b></li></ul>
<dl class="kv" style="margin-top:18px"><dt>Running the site</dt><dd>Domain, tooling, testing on real devices, accessibility fixes.</dd><dt>Contributors</dt><dd>Paying the writers, designers and developers listed on the <a href="{R}careers.html">work with us</a> page.</dd><dt>Contests and prizes</dt><dd>Prize funds for the <a href="{R}contests.html">monthly challenge</a>.</dd><dt>Outreach</dt><dd>Promotion and marketing so more people find the free tools.</dd></dl>
<h3 style="margin-top:22px">Other ways to help</h3><ul><li>Share a test result or a guide with a colleague.</li><li><a href="{R}teams.html">Sponsor a tool</a> through your organisation.</li><li>Report a bug or an error on the <a href="{R}contact.html">contact page</a>.</li></ul></div></div>'''


def contests(c):
    f = c['form']('contest-form', 'Monthly challenge entry', 'Entry received. Winners are contacted by email after the round closes.',
        '<input type="hidden" name="test" id="c-test-field">'
        '<div class="row">' + c['field']('Name to show in the hall of fame', 'display_name', extra='maxlength="40"') + c['field']('Email', 'email', 'email', extra='autocomplete="email" maxlength="120"') + '</div>'
        '<div class="row">' + c['field']('Your best score this month', 'score', extra='id="c-score" maxlength="30"') + c['field']('Result code', 'result_code', extra='id="c-code" maxlength="40"') + '</div>'
        + c['field']('Country', 'country', extra='autocomplete="country-name" maxlength="60"'), 'Enter the challenge',
        'I am 18 or older, I have read the rules below, and I agree to be contacted about this entry. <a href="{R}privacy.html">Privacy policy</a>.')
    return head('The monthly challenge', 'One featured test each month. Play it as often as you like, then enter your best result. Free to enter.') + '''
<div class="two"><div class="panel ink"><h2 id="c-month">This month</h2><dl class="kv"><dt>Featured test</dt><dd id="c-test">–</dd><dt>How it is ranked</dt><dd id="c-rule">–</dd><dt>Entries close</dt><dd id="c-close">–</dd><dt>Prize</dt><dd id="c-prize">–</dd></dl><div class="btn-row" style="margin-top:16px"><a class="btn" id="c-link" href="{R}train/index.html">Play the featured test</a></div></div>
<div><h2>How to enter</h2><ol class="steps"><li>Play the featured test. Your result panel shows a result code.</li><li>Copy the score and the code from your best run this month.</li><li>Send the entry form. One entry per person per round; a later entry replaces an earlier one.</li></ol></div></div>
<section class="section"><div class="two"><div><h2>Enter this round</h2>''' + f + '''</div>
<div><h2>Hall of fame</h2><p class="note">The first round is open now. Ranked results will be listed here after it closes.</p>
<h2 style="margin-top:22px">Rules</h2><ul style="font-size:.94rem"><li>Free to enter. No purchase or payment improves your chances.</li><li>Open to people aged 18 or older, where such contests are lawful. Void where prohibited.</li><li>One entry per person per round. Scores must be your own, made on this site during the round, without automation.</li><li>Entries are ranked by score. Ties go to the earlier entry. We may ask for a screen recording before confirming a result, and may refuse entries we cannot verify.</li><li>A prize applies to a round only if it is posted on this page before the round opens. Rounds without a posted prize are for ranking only.</li><li>Winners are contacted by email and have 14 days to reply. Winners are responsible for any taxes.</li><li>By entering you agree that we may publish your display name, country and score.</li><li>The challenge is run by MindWork.com. It is not sponsored, endorsed or administered by Google, YouTube or any advertiser.</li></ul></div></div></section>'''


def careers(c):
    f = c['form']('careers-form', 'Contributor application', 'Application received. We reply by email when a matching project opens.',
        '<div class="row">' + c['field']('Your name', 'name', extra='autocomplete="name" maxlength="80"') + c['field']('Email', 'email', 'email', extra='autocomplete="email" maxlength="120"') + '</div>'
        + c['select']('Role', 'role', ['Cognitive science writer', 'Puzzle and test designer', 'Front-end developer', 'Illustrator or motion designer', 'Community and contests coordinator', 'Partnerships and sponsorship', 'Something else'])
        + c['field']('Link to your work', 'portfolio', 'url', req=False, extra='placeholder="https://" maxlength="200"')
        + '<label>What would you build or write first?<textarea name="message" maxlength="2000" required></textarea></label>', 'Send my application')
    roles = [('Cognitive science writer', 'Write and update guides. You read the primary studies, cite them, and say plainly when the evidence is weak.'), ('Puzzle and test designer', 'Design new browser tests grounded in research tasks, with scoring that is fair on any device.'), ('Front-end developer', 'Build tools in plain HTML, CSS and JavaScript that load fast and work with a keyboard and a screen reader.'), ('Illustrator or motion designer', 'Explain how a model or a memory process works in one clear picture.'), ('Community and contests coordinator', 'Run the monthly challenge, verify entries and keep the hall of fame honest.'), ('Partnerships and sponsorship', 'Find sponsors whose products fit the audience, and keep the labelling clear.')]
    return head('Work with us', 'MindWork.com is built by a small, remote group of contributors. Work is project-based and paid per project, funded by sponsors and supporters.') + '<div class="two"><div><h2>Roles we take applications for</h2><dl class="kv" style="grid-template-columns:1fr">' + ''.join('<dt style="color:var(--ink);font-weight:800;margin-top:10px">%s</dt><dd style="font-weight:400">%s</dd>' % r for r in roles) + '''</dl>
<p class="note" style="margin-top:18px">Projects open as funding allows, so there may be a wait between applying and hearing about a project. We keep applications on file for twelve months.</p></div><div><h2>Apply</h2>''' + f + '</div></div>'


def about(c):
    return head('About MindWork.com', 'A free mental gym and thinking toolkit for people who think for a living.') + '''
<div class="layout"><article class="prose">
<h2 style="margin-top:0">What this site is</h2><p>Mind work is the kind of work most of us now do: reading, deciding, writing, designing, analysing, explaining. It depends on attention and memory far more than on time at a desk, and almost nobody is taught how to look after either.</p>
<p>MindWork.com collects the useful parts in one place. There are tests that show how sharp you are today, tools that make focused work easier to start, mental models for decisions and problems, and guides that explain the research in plain language.</p>
<h2>What we promise</h2><ul><li><b>Free and open.</b> No account, no paywall, no download.</li><li><b>Private by design.</b> Your scores and plans stay in your browser.</li><li><b>Honest about evidence.</b> We list sources, and we say when a popular claim does not hold up. We do not claim that our tests raise intelligence or treat any condition.</li><li><b>Clear about money.</b> The site is funded by advertising, sponsors and voluntary support. Sponsored content is labelled.</li></ul>
<h2>How it is built</h2><p>The site is static HTML, CSS and JavaScript, generated from plain content files and hosted on GitHub Pages. A scheduled job refreshes the research radar and video shelf every day. The source lives in a public repository.</p>
<h2>Who runs it</h2><p>MindWork.com is an independent website operated from its own domain. It is not affiliated with any company or product with a similar name; see the <a href="{R}trademark.html">trademark and copyright page</a>.</p>
<h2>Get in touch</h2><p>For questions and corrections use the <a href="{R}contact.html">contact page</a>. For teams, sponsorship and advertising see <a href="{R}teams.html">teams and sponsors</a>.</p>
</article><aside><div class="panel ink"><h3>Start here</h3><p class="muted">Three tests, five minutes.</p><a class="btn small" href="{R}daily.html">Open today’s workout</a></div><div class="panel"><h3>Support the site</h3><p class="muted">Keep the tools free and fund new ones.</p><a class="btn small ghost" href="{R}support.html">Make a pledge</a></div></aside></div>'''


def contact(c):
    f = c['form']('contact-form', 'Contact form', 'Sent. We reply by email.',
        '<div class="row">' + c['field']('Your name', 'name', extra='autocomplete="name" maxlength="80"') + c['field']('Email', 'email', 'email', extra='autocomplete="email" maxlength="120"') + '</div>'
        + c['select']('What is it about?', 'topic', ['A question about a test or tool', 'A correction to a guide', 'A bug or accessibility problem', 'Privacy or my data', 'Copyright or trademark', 'Something else'])
        + '<label>Your message<textarea name="message" maxlength="3000" required></textarea></label>', 'Send my message')
    return head('Contact', 'Questions, corrections, bugs and privacy requests. Messages go to the person who runs the site.') + '<div class="two"><div>' + f + '''</div>
<div><div class="panel ink" style="margin-bottom:16px"><h3>Business inquiries</h3><p>Interested in this website, the domain name, sponsorship, advertising or a partnership?</p><a class="btn small" href="https://web.works/contact" target="_blank" rel="noopener">Open the business contact page</a></div>
<div class="panel"><h3>Before you write</h3><ul style="margin:0"><li>Scores are stored in your browser. We cannot see or restore them.</li><li>For team workshops and sponsorship, the <a href="{R}teams.html">teams form</a> asks the right questions.</li><li>To apply as a contributor, use <a href="{R}careers.html">work with us</a>.</li></ul></div></div></div>'''


PRIVACY = head('Privacy policy', 'What this site stores, what it sends, and who else is involved. Last updated November 2026.') + '''<article class="prose">
<h2 style="margin-top:0">The short version</h2><p>MindWork.com has no accounts and no database. Your test scores, streaks, tasks and plans are saved in your own browser and never leave it. We receive personal information only when you send us a form.</p>
<h2>Information stored on your device</h2><p>The site uses your browser’s local storage to keep your scores, daily workout streak, timer history, tool settings, colour theme and cookie choice. You can download or delete this data from the <a href="{R}dashboard.html">dashboard</a>, or by clearing site data in your browser.</p>
<h2>Information you send us</h2><p>When you submit a form (plan sign-up, contact, teams, support pledge, contest entry or contributor application), the fields you fill in are sent by email to the site operator through FormSubmit, a third-party form relay, which processes the message in order to deliver it. We use what you send only for the purpose of that form: to reply to you, to send the updates you asked for, to run the contest, or to arrange a pledge. We do not sell or rent it. Ask us to delete it at any time through the <a href="{R}contact.html">contact page</a>.</p>
<h2>Advertising</h2><p>This site uses Google AdSense to show advertisements. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites. Google’s use of advertising cookies enables it and its partners to serve ads to you based on your visits to this site and other sites on the internet.</p>
<ul><li>You can opt out of personalised advertising in <a href="https://adssettings.google.com/" target="_blank" rel="noopener">Google Ads Settings</a>.</li><li>You can opt out of some third-party vendors’ cookies at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>.</li><li>Read <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>.</li></ul>
<p>The cookie notice on this site lets you choose non-personalised ads. In regions where the law requires it, Google may show its own consent message.</p>
<h2>Other third parties</h2><ul><li><b>YouTube.</b> Videos are embedded in privacy-enhanced mode and load only when you press play. Playing a video connects your browser to YouTube, which is operated by Google.</li><li><b>Google Fonts.</b> Typefaces are loaded from Google’s servers, which receive your IP address as part of the request.</li><li><b>GitHub Pages.</b> The site is hosted by GitHub, which may log technical data such as IP addresses for security.</li></ul>
<h2>Children</h2><p>The site is written for adults and is not directed at children under 16. We do not knowingly collect personal information from children.</p>
<h2>Your rights</h2><p>Depending on where you live, you may have the right to see, correct, delete or object to our use of your personal information. Use the <a href="{R}contact.html">contact page</a> and we will respond.</p>
<h2>Changes</h2><p>If this policy changes, the new version will be posted here with a new date.</p></article>'''

TERMS = head('Terms of use', 'The rules for using MindWork.com. Last updated November 2026.') + '''<article class="prose">
<h2 style="margin-top:0">Using the site</h2><p>You may use the tests, tools, models and guides for personal and internal business purposes, free of charge. Do not use automated means to submit forms, manipulate scores, interfere with the site or its advertising, or copy the site in bulk.</p>
<h2>No professional advice</h2><p>Everything here is general information and entertainment. It is not medical, psychological, legal, financial or other professional advice, and the tests are not diagnostic. See the <a href="{R}disclaimer.html">disclaimer</a>.</p>
<h2>Your content</h2><p>If you send us a message, suggestion or contest entry, you allow us to use it to operate the site, including publishing your contest display name, country and score.</p>
<h2>Intellectual property</h2><p>The site’s text, design and code belong to MindWork.com unless stated otherwise. You may quote short passages with a link to the source page. Third-party names, headlines and videos belong to their owners; see <a href="{R}trademark.html">trademark and copyright</a>.</p>
<h2>Advertising and links</h2><p>The site shows advertising and links to other websites. We are not responsible for the content, products or practices of advertisers or linked sites.</p>
<h2>Support pledges and contests</h2><p>Pledges are voluntary gifts and are not refundable once paid, except where the law requires. Contests are governed by the rules on the <a href="{R}contests.html">contest page</a>.</p>
<h2>Availability and liability</h2><p>The site is provided as it is, without warranties of any kind. To the extent the law allows, MindWork.com is not liable for any loss arising from your use of the site, including lost data stored in your browser.</p>
<h2>Changes</h2><p>We may update these terms. Continuing to use the site after a change means you accept the new terms.</p></article>'''

DISCLAIMER = head('Disclaimer', 'What the tests, tools and guides on this site are, and what they are not.') + '''<article class="prose">
<h2 style="margin-top:0">Not medical or psychological advice</h2><p>MindWork.com provides general information and self-help tools for healthy adults. Nothing on the site is medical, psychological or psychiatric advice, diagnosis or treatment. Do not use it as a substitute for seeing a qualified professional. If you are concerned about your memory, attention, mood or sleep, talk to a doctor.</p>
<h2>The tests are not diagnostic</h2><p>The cognitive tests are simplified browser versions of research tasks. Results are affected by your device, your screen, your internet connection, the time of day and how you feel. They are not IQ tests, are not validated clinical instruments, and cannot detect or rule out any condition. The result labels and ranges are informal guides.</p>
<h2>No promised results</h2><p>We do not claim that using this site will improve intelligence, memory, job performance or health. Research on brain training is mixed, and we describe it honestly in <a href="{R}guides/does-brain-training-work.html">our guide</a>.</p>
<h2>Breathing, sound and exercise</h2><p>Stop the breathing pacer if you feel dizzy or unwell. Keep the noise mixer at a comfortable volume. Check with a doctor before changing your exercise or sleep routine if you have a health condition.</p>
<h2>Accuracy</h2><p>We work to keep the guides accurate and list our sources, but research changes and mistakes happen. Tell us through the <a href="{R}contact.html">contact page</a> and we will correct them.</p>
<h2>Advertising and affiliations</h2><p>The site is funded by advertising, sponsors and supporters. Advertisers do not influence our content. An advertisement is not an endorsement.</p></article>'''

TRADEMARK = head('Trademark and copyright disclosure', 'How the name of this site is used, who owns what, and how to raise a concern.') + '''<article class="prose">
<h2 style="margin-top:0">About the name</h2><p>“MindWork.com” is the internet domain name of this website, and it is used here only to identify the website at that address. The words “mind work” are used in their ordinary descriptive sense: the work a mind does.</p>
<p>This website is independent. It is <b>not affiliated with, sponsored by, endorsed by or connected to</b> any company, organisation, product, app, publication or service whose name includes “Mindwork”, “MindWork”, “Mind Work”, “Mindworks”, “MindWorks” or a similar term, anywhere in the world.</p>
<p>We are aware that trademarks containing the word MINDWORKS are registered or applied for in the United States by unrelated parties, for goods and services that include meditation training, educational software, cognitive-skills training materials and workflow software, and that an application exists for MINDWORK GROUP. Those marks belong to their respective owners. To avoid confusion, this site does not use the plural form “Mindworks” as a name, does not present “MindWork” as a brand for meditation training, courses or software products, and does not imitate any other party’s logo, trade dress or product names.</p>
<h2>No claim over third-party marks</h2><p>All product names, company names and logos mentioned on this site are the property of their respective owners and are used for identification only. In particular:</p>
<ul><li>Pomodoro Technique® and Pomodoro® are registered trademarks of Francesco Cirillo. This site is not affiliated with or endorsed by Francesco Cirillo.</li><li>Getting Things Done® and GTD® are registered trademarks of the David Allen Company.</li><li>Google, AdSense and YouTube are trademarks of Google LLC.</li><li>Names of journals, publishers, universities and apps appear only to cite or describe them.</li></ul>
<h2>Copyright in this site</h2><p>Unless stated otherwise, the text, design, graphics and code of this site are &copy; MindWork.com. The tests are original implementations of long-published research tasks; the tasks themselves are scientific methods, not our property. The mental models are described in our own words and credited to the people who developed them.</p>
<h2>Third-party content</h2><ul><li><b>Research headlines</b> on the research radar belong to their publishers. We show the headline, source name and date as a link to the original, and copy no article text.</li><li><b>Videos</b> are embedded from YouTube under its standard embedding terms and remain the property of their creators.</li><li><b>Typefaces</b> are Archivo and Source Serif 4, used under the SIL Open Font License.</li></ul>
<h2>Raising a concern</h2><p>If you believe something on this site infringes your trademark or copyright, send the details through the <a href="{R}contact.html">contact page</a> (choose “Copyright or trademark”). Tell us the page, the material and your rights in it. We review every notice and will remove or correct material where the concern is valid.</p>
<p class="note" style="font-family:var(--sans)">This page is a good-faith disclosure and is not legal advice.</p></article>'''

EDITORIAL = head('How we write and correct our pages', 'Our standards for evidence, sources, advertising and corrections.') + '''<article class="prose">
<h2 style="margin-top:0">Evidence first</h2><p>Guides and tool pages are built from published research. Each page lists the studies it relies on so you can check our reading of them. Where findings conflict or failed to replicate, we say so, even when a simpler story would be more appealing.</p>
<h2>How pages are produced</h2><p>Pages are drafted with the help of AI tools from published research and edited by the people who run the site. Drafting tools can make mistakes, which is one reason every page names its sources. If you find an error, tell us through the <a href="{R}contact.html">contact page</a> and we will fix it and note the correction.</p>
<h2>Claims we do not make</h2><ul><li>We do not say our tests measure intelligence or diagnose anything.</li><li>We do not say brain training makes you smarter in general.</li><li>We do not publish testimonials or user numbers we cannot verify.</li></ul>
<h2>Advertising and sponsorship</h2><p>Advertising is served by Google AdSense and is kept visually separate from tests and tools. Sponsors may fund a tool, a guide or a contest and are named as sponsors on that page. Neither advertisers nor sponsors see or change editorial content before it is published.</p>
<h2>The research radar and video shelf</h2><p>These two pages are assembled automatically once a day from public feeds, filtered by topic. Appearing there is not an endorsement. We link to the original publisher and do not copy article text.</p>
<h2>Corrections</h2><p>We correct factual errors as soon as we confirm them. Significant corrections are noted at the foot of the page.</p></article>'''

NOTFOUND = '<div class="page-head" style="padding-top:40px"><h1>That page is not here</h1><p>The link may be old, or the address may have a typo. Try one of these instead.</p></div><div class="btn-row"><a class="btn" href="{R}index.html">Go to the home page</a><a class="btn ghost" href="{R}train/index.html">Take a test</a><a class="btn ghost" href="{R}sitemap.html">See every page</a></div>'

STATIC = [
 dict(path='daily.html', title='Daily workout: three tests in five minutes', desc='A fresh set of three cognitive tests every day. Finish all three to build a streak. Free, no sign-up.', body=daily, page='daily', crumb='Daily workout', prio='0.9'),
 dict(path='dashboard.html', title='My scores', desc='Your personal bests, streak and focus time across the nine MindWork.com tests, stored privately in your browser.', body=dashboard, page='dashboard', prio='0.6'),
 dict(path='start.html', title='Free 7-day focus reset', desc='A free seven-day plan for better focus at work: one small change a day, a before-and-after measurement and a printable plan.', body=start, page='start', crumb='7-day focus reset', prio='0.9'),
 dict(path='teams.html', title='For teams, sponsors and partners', desc='Focus workshops for teams, sponsorship of tools and contests, advertising, licensing and partnerships with MindWork.com.', body=teams, crumb='Teams and sponsors', prio='0.7'),
 dict(path='support.html', title='Support MindWork.com', desc='Help keep the tests, tools and guides free. Make a pledge toward running costs, contributors, contests and outreach.', body=support, page='support', crumb='Support', prio='0.6'),
 dict(path='contests.html', title='Monthly challenge', desc='One featured cognitive test each month. Enter your best score, free, and earn a place in the hall of fame.', body=contests, page='contest', prio='0.7'),
 dict(path='careers.html', title='Work with us', desc='Project-based roles for writers, test designers, developers, illustrators and coordinators at MindWork.com.', body=careers, prio='0.5'),
 dict(path='about.html', title='About', desc='What MindWork.com is, what it promises, how it is built and how it is funded.', body=about, prio='0.5'),
 dict(path='contact.html', title='Contact', desc='Send a question, correction, bug report or privacy request to MindWork.com.', body=contact, prio='0.5'),
 dict(path='privacy.html', title='Privacy policy', desc='How MindWork.com handles data: local storage for scores, form submissions by email, Google AdSense cookies and third parties.', body=PRIVACY, prio='0.3'),
 dict(path='terms.html', title='Terms of use', desc='The terms that apply when you use MindWork.com.', body=TERMS, prio='0.3'),
 dict(path='disclaimer.html', title='Disclaimer', desc='The tests and guides on MindWork.com are for education and entertainment and are not medical or professional advice.', body=DISCLAIMER, prio='0.3'),
 dict(path='trademark.html', title='Trademark and copyright disclosure', desc='MindWork.com is an independent website named after its domain and is not affiliated with any similarly named company or trademark.', body=TRADEMARK, crumb='Trademark and copyright', prio='0.3'),
 dict(path='editorial.html', title='How we write and correct our pages', desc='Editorial standards at MindWork.com: evidence, sources, AI-assisted drafting, advertising separation and corrections.', body=EDITORIAL, crumb='How we write', prio='0.3'),
 dict(path='404.html', title='Page not found', desc='That page is not here.', body=NOTFOUND, index=False),
]
