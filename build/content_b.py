# Content for the Think pillar (mental models) and the Learn pillar (guides).

CATS = [('decide','Decide'),('solve','Solve'),('prioritise','Prioritise'),('learn','Learn'),('systems','See systems'),('communicate','Communicate')]

def M(slug, name, cat, line, what, steps, example, trap, related, origin):
    return dict(slug=slug, name=name, cat=cat, line=line, what=what, steps=steps, example=example, trap=trap, related=related, origin=origin)

MODELS = [
 M('second-order-thinking','Second-order thinking','decide','Ask “and then what?” before you act.',
   'First-order thinking stops at the immediate result of a decision. Second-order thinking follows the chain one or two steps further, to the reactions and side effects that the first result sets off.',
   ['Write the decision and its obvious first result.','Ask “and then what?” and write what that result causes, for customers, colleagues and competitors.','Repeat once more. Mark any consequence that reverses the first benefit.','Decide with the whole chain in view, not the first link.'],
   'A team cuts support response targets from four hours to one. First order: happier customers. Second order: agents rush, answers get worse, tickets reopen. Third order: volume rises and the one-hour target fails anyway.',
   'Chains can be extended forever. Stop at the second or third step, where you can still estimate likelihoods.',
   ['inversion','feedback-loops','pre-mortem'], 'The phrase was popularised by the investor Howard Marks in The Most Important Thing (2011).'),
 M('inversion','Inversion','decide','Work out what would guarantee failure, then avoid it.',
   'Instead of asking how to succeed, ask how to fail. Problems that are vague when approached forwards often become concrete when turned around, because failure usually has fewer and clearer causes than success.',
   ['State the goal.','List everything that would reliably ruin it.','Rank those causes by how likely you are to commit them.','Build the plan around not doing the top three.'],
   'Goal: a product launch that goes well. Inverted: what makes launches go badly? No owner for support, untested payment flow, announcement before the site can take load. Each becomes a checklist item.',
   'Avoiding failure is not the same as a strategy. Use inversion to stress-test a plan, then return to the forward question.',
   ['pre-mortem','second-order-thinking','five-whys'], 'The mathematician Carl Jacobi advised “invert, always invert”; Charlie Munger made it a staple of business thinking.'),
 M('two-way-doors','Reversible and irreversible decisions','decide','Move fast on choices you can undo; slow down on those you cannot.',
   'Decisions differ in how costly they are to reverse. A two-way door can be walked back through at low cost; a one-way door cannot. Treating every decision as a one-way door makes organisations slow, and treating none as one makes them reckless.',
   ['Ask what undoing this decision would cost in money, time and trust.','If the cost is low, decide now with the information you have and set a review date.','If the cost is high, slow down: gather evidence, widen the options, get dissent.','Look for ways to turn a one-way door into a two-way one, such as a pilot.'],
   'Changing a pricing page for two weeks is reversible. Signing a five-year office lease is not. The first deserves an afternoon; the second deserves a month.',
   'People under-estimate reversal costs that are social, such as a public announcement or a promise to a team.',
   ['expected-value','pre-mortem','regret-minimisation'], 'Jeff Bezos described “Type 1” and “Type 2” decisions in Amazon’s 2015 letter to shareholders.'),
 M('expected-value','Expected value','decide','Weigh each outcome by its probability, then add them up.',
   'Expected value is the average result you would get if you could make the same bet many times: each possible outcome multiplied by its probability, summed. It lets you compare options that mix likely small results with unlikely large ones.',
   ['List the possible outcomes of each option.','Estimate a probability and a value for each outcome.','Multiply and add to get each option’s expected value.','Check the worst case separately. A positive expected value does not help if one outcome ends the game.'],
   'Proposal A wins 80,000 with 50% probability. Proposal B wins 300,000 with 15%. A is worth 40,000 in expectation and B 45,000, but B fails 85% of the time, which matters if you need a win this quarter.',
   'The inputs are guesses. Run the sum with pessimistic and optimistic probabilities and see whether the ranking survives.',
   ['two-way-doors','opportunity-cost','compounding'], 'The idea dates to the 1654 letters between Blaise Pascal and Pierre de Fermat on dividing the stakes of an unfinished game.'),
 M('regret-minimisation','Regret minimisation','decide','Choose what your older self would be least sorry about.',
   'For large personal decisions, project yourself decades ahead and ask which choice you would regret more. The exercise strips out short-term discomfort, which dominates in the moment and barely registers in memory.',
   ['Picture yourself at 80, looking back.','Ask which you would regret more: having tried this and failed, or never having tried.','Write the answer and the reason in one sentence.','Check it against your obligations to other people before acting.'],
   'An engineer weighing a move into management pictures both paths at 80. She would not regret trying and returning to engineering; she would regret never finding out.',
   'It favours action over caution by design. For decisions with irreversible downsides, pair it with a sober look at the worst case.',
   ['two-way-doors','opportunity-cost','circle-of-competence'], 'Jeff Bezos has described using this framing when he left a finance job to start Amazon.'),
 M('pre-mortem','Pre-mortem','decide','Imagine the project has failed, then explain why.',
   'Before work begins, the team assumes the project has already failed and writes down the most plausible reasons. Because the failure is treated as certain, people voice doubts they would otherwise keep quiet.',
   ['Brief the team on the plan.','Say: “It is a year from now and this failed badly. Take five minutes and write why.”','Go round the table, one reason each, until the lists are empty.','Pick the top risks and change the plan to address them.'],
   'A migration team runs a pre-mortem and three people independently write “no rollback path if data validation fails on the night”. The plan gains a rehearsed rollback.',
   'A pre-mortem that produces a list and no plan changes is theatre. Assign an owner to each top risk before the meeting ends.',
   ['inversion','second-order-thinking','five-whys'], 'Described by the psychologist Gary Klein in Harvard Business Review in 2007. It builds on research showing that imagining an outcome as already certain helps people generate more reasons for it.'),
 M('first-principles','First-principles thinking','solve','Break the problem down to what is certainly true and build up from there.',
   'Most reasoning works by analogy: we do what was done before, with small changes. First-principles reasoning sets the analogy aside, identifies the facts and constraints that cannot be argued with, and reasons upward from those.',
   ['Write the assumption everyone accepts.','Ask what is known to be true underneath it, and how you know.','Separate real constraints (physics, law, arithmetic) from conventions.','Rebuild a solution using only the real constraints.'],
   '“A weekly status meeting is required.” What is actually required is that six people know what changed and what is blocked. A shared written update meets that need in ten minutes.',
   'It is slow and tiring. Save it for problems where the conventional answer is clearly failing or the stakes justify the effort.',
   ['five-whys','occams-razor','map-and-territory'], 'The approach goes back to Aristotle, who described first principles as the first basis from which a thing is known.'),
 M('five-whys','Five whys','solve','Ask “why?” repeatedly until you reach a cause you can fix.',
   'Problems usually present as symptoms. Asking why the symptom occurred, then why that cause occurred, and so on, walks back along the chain to a root cause, typically a missing process and not a careless person.',
   ['State the problem as a specific event.','Ask why it happened and write the answer.','Ask why again of that answer. Continue until the answer is a process you can change.','Fix that process, and check that the fix would have prevented the original event.'],
   'The report went out with wrong figures. Why? The export was stale. Why? The refresh job failed. Why? A password expired. Why? Nobody owns service passwords. Fix: assign an owner and an expiry alert.',
   'Real incidents have several causes. If the chain branches, follow each branch instead of forcing one story.',
   ['first-principles','inversion','bottleneck'], 'Developed by Sakichi Toyoda and used throughout the Toyota Production System, as described by Taiichi Ohno.'),
 M('occams-razor','Occam’s razor','solve','Prefer the explanation that needs the fewest assumptions.',
   'When several explanations fit the facts, start with the one that requires the fewest new assumptions. It is not guaranteed to be right, but it is the cheapest to test and the most likely to survive.',
   ['List the candidate explanations.','Count the assumptions each one needs that you have not verified.','Test the one with the fewest first.','Move to a more complex explanation only when the simple one fails.'],
   'Sign-ups dropped on Tuesday. One story involves a competitor campaign, a search algorithm change and seasonality. Another says the sign-up form broke on mobile. Check the form first.',
   'Simple does not mean familiar or comfortable. Count assumptions honestly, including the ones you like.',
   ['first-principles','hanlons-razor','map-and-territory'], 'Named after the fourteenth-century friar and philosopher William of Ockham.'),
 M('issue-tree','Issue trees','solve','Split a big question into parts that do not overlap and leave nothing out.',
   'An issue tree breaks a question into sub-questions, and those into smaller ones, until each branch can be answered with data. Good branches are mutually exclusive and collectively exhaustive, so nothing is counted twice or missed.',
   ['Write the question at the top.','Split it into two to four parts that together cover it completely.','Split each part again until every branch is something you can check.','Work the branches in order of likely impact.'],
   '“Why is profit down?” splits into revenue and cost. Revenue splits into price and volume; volume into new and returning customers. The data shows returning customers fell: the search narrows to retention.',
   'A tidy tree can hide a wrong first split. Try a second way of cutting the problem before committing.',
   ['pyramid-principle','five-whys','pareto-principle'], 'The technique and the test for good branches were developed at McKinsey; the test was named by Barbara Minto.'),
 M('pareto-principle','The Pareto principle','prioritise','A few causes usually produce most of the effect.',
   'In many systems outcomes are unevenly distributed: a small share of inputs accounts for a large share of results. The 80/20 split is a rule of thumb, not a law, but the unevenness is real often enough to check for.',
   ['Pick an outcome you care about, such as revenue, bugs or complaints.','List the sources and measure each one’s contribution.','Sort from largest to smallest and find the small group that explains most of the total.','Put effort there first.'],
   'A support team tags a month of tickets. Three of forty issue types account for 61% of volume. Fixing those three does more than chipping at all forty.',
   'The remaining 20% of results may still matter, for example safety issues or your largest customer’s edge case.',
   ['bottleneck','eisenhower-matrix','opportunity-cost'], 'Vilfredo Pareto observed in 1896 that about 80% of Italian land was owned by 20% of the population. Joseph Juran generalised the pattern to management.'),
 M('eisenhower-matrix','The Eisenhower matrix','prioritise','Sort by urgent and important; they are not the same thing.',
   'Urgent tasks demand attention now. Important tasks serve your goals. Crossing the two gives four boxes with four different instructions: do, schedule, hand off and drop.',
   ['List your open tasks.','Mark each as important or not, by your own goals.','Mark each as urgent or not, by a real deadline.','Do the urgent and important ones, schedule the important ones, and shrink the rest.'],
   'Preparing next quarter’s plan is important and not urgent, so it keeps losing to email, which is urgent and not important. Scheduling two blocks for the plan fixes the imbalance.',
   'Everything can be argued into the top-left box. Limit it to what truly cannot wait until tomorrow.',
   ['pareto-principle','parkinsons-law','opportunity-cost'], 'Based on a remark Dwight D. Eisenhower quoted in a 1954 speech, and turned into a matrix by Stephen Covey.'),
 M('opportunity-cost','Opportunity cost','prioritise','The real cost of a choice is the best alternative you gave up.',
   'Every hour and every unit of budget can only be used once. The cost of using it on one thing is the value of the best other thing it could have bought, whether or not money changes hands.',
   ['Before committing, name the best alternative use of the same time or money.','Estimate what that alternative would return.','Compare the two directly.','Say yes only if the new commitment beats the alternative, not merely if it has some value.'],
   'A senior developer spends a week on an internal dashboard. The dashboard is useful. The alternative was a week on a checkout bug that loses sales daily. The dashboard cost that fix.',
   'Do not count imaginary alternatives. Compare with what you would realistically have done instead.',
   ['expected-value','pareto-principle','eisenhower-matrix'], 'The term was coined by the Austrian economist Friedrich von Wieser.'),
 M('parkinsons-law','Parkinson’s law','prioritise','Work expands to fill the time available for it.',
   'Give a task a week and it tends to take a week; give it two days and it often takes two. Deadlines shape scope and effort, so loose deadlines invite polishing, deferral and second-guessing.',
   ['Estimate how long the task would take with full focus.','Set the deadline at that length, not at the next convenient date.','Define “done” before starting.','Stop when done is reached, even if time remains.'],
   'A slide deck “for Friday” absorbs four afternoons. The next one is given a ninety-minute block and a rule of ten slides. It is finished in the block and is shorter and clearer.',
   'Deadlines that are too tight produce errors and burnout. Tighten gradually and watch quality.',
   ['eisenhower-matrix','bottleneck','deliberate-practice'], 'From a 1955 essay in The Economist by the historian C. Northcote Parkinson.'),
 M('feynman-technique','The Feynman technique','learn','If you cannot explain it simply, you do not understand it yet.',
   'Explaining an idea in plain words, as if to someone new to the subject, exposes the gaps that familiarity hides. The gaps tell you exactly what to go back and study.',
   ['Write the concept at the top of a page.','Explain it in plain language, without jargon, as if teaching a beginner.','Mark every point where you got stuck or reached for a technical term.','Go back to the source for those points, then simplify the explanation again.'],
   'An analyst preparing to present a regression model writes a one-page explanation for the sales team. She cannot explain why one variable was dropped, rereads the method, and finds an error.',
   'A smooth explanation can still be wrong. Test it on a real person or against worked examples.',
   ['spaced-repetition','deliberate-practice','pyramid-principle'], 'Named after the physicist Richard Feynman, known for explaining difficult ideas in plain terms.'),
 M('spaced-repetition','Spaced repetition','learn','Review just before you would forget, at growing intervals.',
   'Memory fades quickly after learning and more slowly after each successful recall. Reviewing material at widening intervals, by testing yourself, produces durable memory in far less total time than cramming.',
   ['Turn what you need to remember into questions.','Test yourself the next day.','Each time you answer correctly, roughly double the gap before the next test.','When you fail one, bring it back to a short interval.'],
   'A new manager learning forty colleagues’ names and roles reviews a list on day 1, 2, 4, 8 and 16. Five short sessions replace a month of awkward guessing.',
   'It builds recall, not understanding. Learn the idea properly first, then space the review.',
   ['feynman-technique','deliberate-practice','compounding'], 'Hermann Ebbinghaus measured the forgetting curve in 1885; Sebastian Leitner’s card-box system made spacing practical in 1972.'),
 M('deliberate-practice','Deliberate practice','learn','Practise the part you cannot yet do, with feedback, at full attention.',
   'Experience alone does not produce expertise. Improvement comes from practice aimed at a specific weakness, at the edge of current ability, with immediate feedback and full concentration.',
   ['Pick one narrow sub-skill that limits you.','Design a short drill that isolates it.','Get feedback on every attempt from a coach, a recording or a measurable result.','Stop when concentration fades, usually within an hour.'],
   'A consultant who rambles in presentations records the first two minutes of each talk, counts filler words, and repeats the opening until the count halves.',
   'Hours of comfortable repetition feel like practice and produce little. If it is not effortful, it is probably not deliberate.',
   ['feynman-technique','spaced-repetition','circle-of-competence'], 'From the research of K. Anders Ericsson and colleagues, published in 1993.'),
 M('circle-of-competence','Circle of competence','learn','Know where your knowledge ends, and act accordingly.',
   'Everyone has areas where their judgement is reliable and areas where it only feels reliable. The size of the circle matters less than knowing where its edge is.',
   ['List the areas where you have years of feedback on your own decisions.','List the areas where you have opinions but no track record.','Inside the circle, trust your judgement and move quickly.','Outside it, slow down, ask an expert, or pass.'],
   'A product leader with ten years in consumer apps is asked to judge a hardware supplier. She recognises she is outside her circle and brings in someone who has run a supply chain.',
   'Confidence is not evidence of competence. Use track record, not feeling, to draw the edge.',
   ['map-and-territory','deliberate-practice','steelmanning'], 'Warren Buffett described the idea in his 1996 letter to Berkshire Hathaway shareholders.'),
 M('feedback-loops','Feedback loops','systems','Outputs circle back and change the system that produced them.',
   'In a reinforcing loop, a change feeds on itself and accelerates. In a balancing loop, a change triggers a response that pushes back toward a set point. Most stubborn problems are loops, not straight lines.',
   ['Draw the chain of cause and effect for the problem.','Look for where the last effect influences the first cause.','Label the loop reinforcing or balancing.','Intervene on the loop itself: weaken a harmful one or strengthen a helpful one.'],
   'Overtime causes fatigue, fatigue causes errors, errors cause rework, rework causes overtime. Adding more overtime strengthens the loop. Cutting rework at its source breaks it.',
   'Delays hide loops. A fix can look like it failed when its effect simply has not arrived yet.',
   ['second-order-thinking','bottleneck','compounding'], 'A core idea of systems thinking, set out clearly in Donella Meadows’s Thinking in Systems (2008).'),
 M('bottleneck','Bottlenecks','systems','A system moves only as fast as its slowest step.',
   'Every process has one constraint that limits total output. Improving any other step adds nothing; improving the constraint improves everything, until a new constraint appears.',
   ['Map the steps from request to delivery.','Find where work piles up or waits longest.','Make sure that step is never idle and never does work others could do.','Add capacity there only after the first two fixes, then look for the next constraint.'],
   'Developers finish features in three days, and features wait nine days for review by one architect. Hiring developers lengthens the queue. Sharing review among three seniors doubles throughput.',
   'The bottleneck moves. Re-check after every improvement instead of assuming it is where it used to be.',
   ['pareto-principle','feedback-loops','five-whys'], 'Formalised as the theory of constraints by Eliyahu Goldratt in The Goal (1984).'),
 M('map-and-territory','The map is not the territory','systems','Every model leaves things out. Check it against reality.',
   'Plans, dashboards, org charts and forecasts are maps: simplified pictures built for a purpose. They are useful because they simplify, and dangerous when their simplifications are forgotten.',
   ['Name the map you are relying on.','Ask what it leaves out and when it was last updated.','Go and look at the territory: talk to a customer, watch the process, read the raw data.','Update the map, or stop using it for this decision.'],
   'A dashboard shows customer satisfaction at 4.6 out of 5. Reading the comments reveals that only customers who complete an order are surveyed. The unhappy ones never reach the survey.',
   'Distrusting every model leaves you with no way to decide. The aim is to know a map’s limits, not to throw it away.',
   ['first-principles','circle-of-competence','occams-razor'], 'The phrase is Alfred Korzybski’s, from 1931. The statistician George Box made a similar point: all models are wrong, but some are useful.'),
 M('compounding','Compounding','systems','Small gains that build on themselves become large, slowly and then quickly.',
   'When each period’s gain is added to the base for the next period, growth is exponential. The early results are unimpressive and the late results are dramatic, which is why people abandon compounding processes too soon.',
   ['Identify what in your work builds on itself: knowledge, relationships, reusable tools, reputation.','Invest a small, regular amount in it.','Protect the streak; interruptions cost more than they appear to.','Judge progress over years, not weeks.'],
   'A team that spends 10% of each sprint on shared tooling ships slightly less this month. Two years later their releases take hours instead of days.',
   'Costs compound too. Technical debt, skipped maintenance and small discourtesies grow on the same curve.',
   ['feedback-loops','spaced-repetition','expected-value'], 'The arithmetic of compound interest has been understood for centuries; the insight is applying it beyond money.'),
 M('pyramid-principle','The pyramid principle','communicate','Lead with the answer, then give the reasons, then the evidence.',
   'Busy readers want the conclusion first. Put your main point at the top, support it with three or so grouped arguments, and place the data beneath each argument. A reader can stop at any level and still have the message.',
   ['Write your answer in one sentence.','List the three or four reasons it is true.','Under each reason, put the evidence.','Open with the answer in every email, document and slide title.'],
   'Instead of four paragraphs of background, the email begins: “I recommend we delay the launch two weeks. Three reasons: payment testing is incomplete, support is not trained, and a competitor ships Tuesday.”',
   'If you do not know your answer yet, the structure will show it. That is a signal to keep thinking, not to add background.',
   ['issue-tree','feynman-technique','steelmanning'], 'Developed by Barbara Minto at McKinsey and set out in her book The Pyramid Principle.'),
 M('steelmanning','Steelmanning','communicate','Argue against the strongest version of the other view, not the weakest.',
   'A straw man is a weak version of an opponent’s argument, set up to be knocked down. A steel man is the opposite: you restate their position so well that they would agree with your summary, and only then respond.',
   ['Restate the other position in your own words.','Ask its holder whether you have it right, and adjust until they say yes.','Name what you agree with and what you learned from it.','Only then state your disagreement.'],
   'Before opposing a move to a four-day week, a manager writes the best case for it, including the retention data. Half of her objections disappear, and the remaining one becomes a precise question about client coverage.',
   'Do not invent a stronger argument than the person actually holds and then credit them with it. Check your summary with them.',
   ['hanlons-razor','circle-of-competence','pyramid-principle'], 'The four steps follow rules proposed by the game theorist Anatol Rapoport, as summarised by the philosopher Daniel Dennett.'),
 M('hanlons-razor','Hanlon’s razor','communicate','Do not assume bad intent when a mistake or a busy day explains it.',
   'Most slights at work are caused by oversight, overload or missing context, not hostility. Assuming malice first makes you respond in ways that damage the relationship and are usually wrong.',
   ['Notice the story you are telling about the other person’s motive.','List two or three ordinary explanations: they did not see it, misread it, or are swamped.','Ask a neutral question before reacting.','Escalate only if the pattern repeats after you have raised it.'],
   'A colleague leaves you off a meeting invite. Before concluding you are being sidelined, you ask. The invite was copied from last quarter’s list, before you joined the project.',
   'It is a starting assumption, not a rule. Repeated harm after clear feedback is a pattern and should be treated as one.',
   ['steelmanning','occams-razor','map-and-territory'], 'Attributed to Robert J. Hanlon, in a 1980 collection of Murphy’s-law sayings.'),
]

def G(slug, title, desc, minutes, body, sources):
    return dict(slug=slug, title=title, desc=desc, minutes=minutes, body=body, sources=sources)

GUIDES = [
 G('deep-work-protocol','Deep work: a protocol you can run this week','A five-step routine for getting two hours of real concentration into an ordinary working day.',6,
 '''<p>Cal Newport defines deep work as professional activity performed in a state of distraction-free concentration that pushes your abilities to their limit. The definition matters less than the observation behind it: the work that creates most of your value needs long, unbroken attention, and the ordinary working day is built to prevent it.</p>
<p>You do not need a cabin or a sabbatical. You need a small, repeatable routine. This one takes about ten minutes to set up each day.</p>
<h2>Step 1. Decide the session the day before</h2>
<p>At the end of each day, write down one task for tomorrow’s deep session and the first physical action it starts with. “Draft section 2 of the proposal: open the outline and write the problem statement” beats “work on proposal”. Deciding in advance removes the choice at the moment you are most tempted to check email instead.</p>
<h2>Step 2. Put it on the calendar, early</h2>
<p>Block 90 to 120 minutes at the time your energy is highest, which for most people is the first half of the morning. Treat the block as a meeting with someone you would not cancel on. The <a href="../focus/time-block-planner.html">time-block planner</a> will lay out the rest of the day around it.</p>
<h2>Step 3. Remove the exits</h2>
<p>Close email and chat completely; do not just minimise them. Put your phone in another room or in a bag. Sophie Leroy’s research on attention residue shows why this matters: after switching away from a task, part of your attention stays behind with it. A glance at a message is a switch, and it costs you several minutes of full capacity.</p>
<h2>Step 4. Work in two or three timed sessions</h2>
<p>Use the <a href="../focus/focus-timer.html">focus timer</a> at 50 minutes with a 10-minute break, or 25 and 5 if 50 feels long at first. In the break, stand up and look at something far away. Do not open a feed; a feed is another task and leaves its own residue.</p>
<h2>Step 5. Close the session on paper</h2>
<p>When the block ends, write two lines: what you finished and the next action. This gives your mind permission to let go, and it makes tomorrow’s Step 1 trivial.</p>
<h2>How much is enough?</h2>
<p>Less than you think. In the study of violinists that launched the research on deliberate practice, Anders Ericsson and colleagues found that the best students practised about three and a half hours a day, in sessions of no more than about 90 minutes. Newport suggests that around four hours a day is the ceiling for most knowledge workers, and that beginners should expect one. Two solid hours, five days a week, is ten hours of your best thinking. Most people get close to none.</p>
<h2>When it fails</h2>
<ul><li><b>You get interrupted.</b> Say when you will be available: “I am in the middle of something; can I come to you at 11?” Most requests survive a 45-minute delay.</li>
<li><b>You cannot start.</b> Shrink the first action until it is trivially small, and run a <a href="../train/schulte-table.html">two-minute attention warm-up</a> first.</li>
<li><b>Your day is all meetings.</b> Protect one block a week and defend it. Then use the track record of what that block produced to ask for a second.</li></ul>''',
 ['Newport, C. (2016). Deep Work: Rules for Focused Success in a Distracted World.','Leroy, S. (2009). Why is it so hard to do my work? The challenge of attention residue when switching between work tasks. Organizational Behavior and Human Decision Processes.','Ericsson, K. A., Krampe, R. T., &amp; Tesch-Römer, C. (1993). The role of deliberate practice in the acquisition of expert performance. Psychological Review.']),

 G('how-memory-works','How memory works, and how to make things stick','The three stages of memory in plain terms, and the four study techniques with the strongest evidence behind them.',7,
 '''<p>Memory is not one thing and it is not a recording. It is a set of processes: taking information in, holding it briefly, storing some of it, and rebuilding it later. Each stage fails in its own way, and each has a known fix.</p>
<h2>Three stages</h2>
<p><b>Working memory</b> is the small workspace where you hold what you are thinking about right now. George Miller’s famous estimate was about seven items; later work by Nelson Cowan puts it nearer four chunks. It lasts seconds unless you rehearse. The <a href="../train/number-memory.html">number memory test</a> measures it directly.</p>
<p><b>Encoding</b> moves information into long-term storage. What gets stored depends on how deeply you process it. Craik and Lockhart showed that thinking about what something means leaves a stronger trace than noticing how it looks or sounds.</p>
<p><b>Retrieval</b> is the act of pulling a memory back, and it is reconstructive: you rebuild the memory each time from stored fragments. That is why confident memories can be wrong, and also why the act of recalling changes what is stored.</p>
<h2>Why you forget</h2>
<p>Hermann Ebbinghaus tested himself on lists of nonsense syllables in the 1880s and plotted how fast they faded. His forgetting curve drops steeply in the first day and then levels off. Most forgetting is not decay of a stored record; it is failure to encode deeply in the first place, or failure to find the route back.</p>
<h2>Four techniques that work</h2>
<p>In 2013 John Dunlosky and colleagues reviewed ten common study techniques. Two were rated high in usefulness. Two popular ones, highlighting and rereading, were rated low.</p>
<ol><li><b>Test yourself.</b> Close the book and write down what you remember. Roediger and Karpicke found that students who practised recall remembered far more a week later than students who reread, even though the rereaders felt more confident.</li>
<li><b>Space it out.</b> Review after a day, then a few days, then a week. A meta-analysis by Cepeda and colleagues covering hundreds of experiments found spaced study consistently beat massed study. See <a href="../models/spaced-repetition.html">spaced repetition</a>.</li>
<li><b>Explain it.</b> Putting an idea into your own plain words forces deep processing and exposes gaps. That is the <a href="../models/feynman-technique.html">Feynman technique</a>.</li>
<li><b>Use places and pictures.</b> The method of loci, placing vivid images along a familiar route, is the technique memory champions use. In a 2017 study by Martin Dresler’s group, ordinary volunteers who trained with it for six weeks more than doubled the number of words they could recall from a list.</li></ol>
<h2>A five-minute routine</h2>
<p>After a meeting, a chapter or a course module: close the source, write everything you can recall for two minutes, check what you missed, and put three questions in your calendar for tomorrow, next week and next month. That is retrieval, feedback and spacing in one habit.</p>
<h2>What does not help much</h2>
<p>Rereading and highlighting feel productive because the material becomes familiar. Familiarity is not recall. If you can only recognise an idea when you see it, you have not learned it yet. Sleep, on the other hand, helps a great deal; see <a href="sleep-exercise-and-thinking.html">the basics guide</a>.</p>''',
 ['Miller, G. A. (1956). The magical number seven, plus or minus two. Psychological Review.','Craik, F. I. M., &amp; Lockhart, R. S. (1972). Levels of processing: a framework for memory research. Journal of Verbal Learning and Verbal Behavior.','Roediger, H. L., &amp; Karpicke, J. D. (2006). Test-enhanced learning. Psychological Science.','Cepeda, N. J., et al. (2006). Distributed practice in verbal recall tasks: a review and quantitative synthesis. Psychological Bulletin.','Dunlosky, J., et al. (2013). Improving students’ learning with effective learning techniques. Psychological Science in the Public Interest.','Dresler, M., et al. (2017). Mnemonic training reshapes brain networks to support superior memory. Neuron.']),

 G('does-brain-training-work','Does brain training work? What the evidence says','An honest reading of the research on brain games: what improves, what does not carry over, and what is worth your time.',7,
 '''<p>This site offers cognitive tests, so you deserve a straight answer to the obvious question. The short version: practising a mental task makes you better at that task. Whether it makes you better at anything else is where the evidence gets thin.</p>
<h2>Near transfer and far transfer</h2>
<p>Researchers separate two kinds of benefit. Near transfer means improving on the trained task and tasks that closely resemble it. Far transfer means improving at different things: your job, your memory for names, your general reasoning. Near transfer is easy to produce. Far transfer is what the marketing promises.</p>
<h2>The main studies</h2>
<p>In 2010 Adrian Owen and colleagues ran a six-week online trial with 11,430 participants for the BBC. People improved on every task they trained, and showed no meaningful gain on untrained tests, even closely related ones.</p>
<p>In 2014 a group of about 70 scientists signed a statement, organised by the Stanford Center on Longevity, objecting to claims that brain games prevent cognitive decline. A second group of more than 100 scientists replied that the statement went too far. In 2016 Daniel Simons and six colleagues reviewed the studies cited by brain-training companies and concluded that there was extensive evidence of improvement on trained tasks, less for similar tasks, and little for everyday performance.</p>
<p>The same year, the makers of one of the best-known brain-training apps agreed to pay 2 million dollars to settle US Federal Trade Commission charges that their advertising about work, school and age-related decline was not backed by evidence.</p>
<h2>The strongest case in favour</h2>
<p>The ACTIVE trial followed about 2,800 older adults for ten years after short courses of memory, reasoning or speed-of-processing training. Trained groups kept an edge on the trained ability, and a later analysis linked speed training with a lower risk of dementia. It is one trial with a specific kind of training, and researchers still argue about how to read it, but it is the reason the question is not closed.</p>
<h2>What this means for you</h2>
<ul><li><b>Use tests as a gauge.</b> Your reaction time and Stroop score move with sleep, stress and fatigue. Tracking them tells you something about your state today. That is how we suggest you use the <a href="../train/index.html">tests here</a>.</li>
<li><b>Train skills you want for their own sake.</b> Faster mental arithmetic is useful in itself. So is a memory technique. Neither needs to “raise your IQ” to be worth ten minutes.</li>
<li><b>Do not expect a game to replace the basics.</b> The best-supported ways to protect thinking are unglamorous: aerobic exercise, sleep, and learning demanding new skills. In the Synapse Project, older adults who spent three months learning digital photography or quilting improved their memory, while a group doing easy, familiar activities did not.</li></ul>
<h2>Our position</h2>
<p>The tests on this site are free measurements and short drills. They are not a treatment, and they will not make you smarter in general. Used for five minutes a day they are a decent warm-up and an honest mirror, and that is all we claim for them.</p>''',
 ['Owen, A. M., et al. (2010). Putting brain training to the test. Nature.','Simons, D. J., et al. (2016). Do “brain-training” programs work? Psychological Science in the Public Interest.','Federal Trade Commission (2016). Lumosity to pay $2 million to settle FTC deceptive advertising charges. Press release, 5 January 2016.','Rebok, G. W., et al. (2014). Ten-year effects of the ACTIVE cognitive training trial. Journal of the American Geriatrics Society.','Edwards, J. D., et al. (2017). Speed of processing training results in lower risk of dementia. Alzheimer’s &amp; Dementia: Translational Research &amp; Clinical Interventions.','Park, D. C., et al. (2014). The impact of sustained engagement on cognitive function in older adults: the Synapse Project. Psychological Science.']),

 G('attention-residue','Attention residue: why switching tasks costs more than you think','What happens in your head when you jump between tasks, how much it costs, and four ways to cut the bill.',5,
 '''<p>You are writing a report. A message arrives; you answer it in forty seconds and return to the report. It feels free. It is not. For the next several minutes part of your mind is still on the message, and your work on the report is slower and worse.</p>
<h2>The research</h2>
<p>Sophie Leroy named this effect attention residue in a 2009 paper. In her experiments, people who moved to a second task before finishing the first performed worse on the second, because thoughts about the unfinished task kept intruding. The effect was strongest when the first task was left incomplete and without a deadline.</p>
<p>Laboratory work on task switching explains the mechanism. Rubinstein, Meyer and Evans showed in 2001 that every switch has two costs: changing goals (“I am doing this now, not that”) and loading the rules for the new task. Each cost is a fraction of a second, but they multiply across a day of switching, and they grow as tasks get more complex.</p>
<p>In real offices the numbers are larger. Gloria Mark’s field studies of information workers found that people switched activities every few minutes, and that after a real interruption it took more than twenty minutes on average to return to the original task. In a 2008 experiment her team found that interrupted people actually worked faster to compensate, and paid for it with more stress, frustration and effort.</p>
<h2>Four ways to cut the cost</h2>
<ol><li><b>Finish or park.</b> Before switching, either reach a natural stopping point or write one line: where you are and what comes next. Leroy’s later work found that a short “ready-to-resume” note reduces residue.</li>
<li><b>Batch the small stuff.</b> Check email and chat at set times, three or four a day, instead of continuously. Each batch is one switch instead of thirty.</li>
<li><b>Make interruptions expensive.</b> Close the apps, silence notifications, and put the phone out of reach during focus blocks. The <a href="../focus/focus-timer.html">focus timer</a> gives the block an edge.</li>
<li><b>Single-task meetings.</b> A meeting attended while answering messages costs the meeting and the messages. Decline it or attend it.</li></ol>
<h2>Measure it yourself</h2>
<p>Run the <a href="../train/stroop-test.html">Stroop test</a> after an hour of uninterrupted work, and again after an hour of constant switching. Interference scores usually rise when attention is fragmented. One pair of runs proves little, but a week of them will show you your own pattern.</p>
<h2>The exception</h2>
<p>Some jobs are interruptions: support, operations, management of a busy team. If that is yours, the aim is not zero switching. Protect one block for the work that needs depth, and accept the rest as the job.</p>''',
 ['Leroy, S. (2009). Why is it so hard to do my work? The challenge of attention residue when switching between work tasks. Organizational Behavior and Human Decision Processes.','Rubinstein, J. S., Meyer, D. E., &amp; Evans, J. E. (2001). Executive control of cognitive processes in task switching. Journal of Experimental Psychology: Human Perception and Performance.','Mark, G., Gonzalez, V. M., &amp; Harris, J. (2005). No task left behind? Examining the nature of fragmented work. Proceedings of CHI 2005.','Mark, G., Gudith, D., &amp; Klocke, U. (2008). The cost of interrupted work: more speed and stress. Proceedings of CHI 2008.']),

 G('better-decisions','Better decisions under pressure: a working checklist','Six questions to ask before any decision that matters, with the research behind each one.',6,
 '''<p>Most bad decisions at work are not caused by missing intelligence. They are caused by skipped steps: nobody asked what else could be done, what would prove the plan wrong, or what it would cost to reverse. A short checklist catches most of them. Atul Gawande’s work on surgical checklists made the general point: experts fail on the simple steps, under pressure, and a list on paper prevents it.</p>
<h2>The six questions</h2>
<ol><li><b>Can this be undone?</b> Reversible decisions deserve speed; irreversible ones deserve care. Most are more reversible than they feel. See <a href="../models/two-way-doors.html">two-way doors</a>.</li>
<li><b>What are the other options?</b> “Should we do X?” is half a question. Force a third option onto the table, including doing nothing. The <a href="../focus/decision-matrix.html">decision matrix</a> makes the comparison explicit.</li>
<li><b>What usually happens?</b> Before trusting your forecast for this project, ask how similar projects turned out. Daniel Kahneman calls this the outside view, and it is the best single correction for the planning fallacy.</li>
<li><b>What would change my mind?</b> Name the evidence that would make you drop the plan, then go and look for it. This is the working cure for confirmation bias.</li>
<li><b>How does this fail?</b> Run a <a href="../models/pre-mortem.html">pre-mortem</a>: assume it failed and write why. Gary Klein introduced the method because people speak more freely about a failure that is treated as already certain.</li>
<li><b>What happens after it works?</b> Follow the consequences one step further. See <a href="../models/second-order-thinking.html">second-order thinking</a>.</li></ol>
<h2>Does it matter when you decide?</h2>
<p>You may have read that judges grant parole less often as they get hungry. That finding, from a 2011 study by Danziger and colleagues, is real, but other researchers have argued that the order in which cases were scheduled explains much of the pattern. The broader theory behind it, that willpower is a fuel that runs down, also failed a large multi-laboratory replication in 2016.</p>
<p>So the strong claim is shaky. The modest version is safe: tired, rushed, hungry people rely more on defaults and first impressions. Put the decisions that matter in the part of the day when you are fresh, and do not make them at the end of a six-hour meeting.</p>
<h2>Keep a decision journal</h2>
<p>For each significant decision, write four lines: what you decided, what you expected to happen, why, and how confident you were. Review the entries every quarter. Without the record, hindsight rewrites your memory of what you believed, and you learn nothing. With it, you find out which kinds of decisions you are reliably good and bad at.</p>
<h2>Groups</h2>
<p>In meetings, have people write their view before anyone speaks, and let the most senior person speak last. Both steps cut anchoring and deference, and they cost two minutes.</p>''',
 ['Kahneman, D. (2011). Thinking, Fast and Slow.','Klein, G. (2007). Performing a project premortem. Harvard Business Review.','Gawande, A. (2009). The Checklist Manifesto.','Danziger, S., Levav, J., &amp; Avnaim-Pesso, L. (2011). Extraneous factors in judicial decisions. PNAS.','Weinshall-Margel, K., &amp; Shapard, J. (2011). Overlooked factors in the analysis of parole decisions. PNAS.','Hagger, M. S., et al. (2016). A multilab preregistered replication of the ego-depletion effect. Perspectives on Psychological Science.']),

 G('pomodoro-technique','The Pomodoro Technique: rules, variations and when not to use it','The original six steps, the two rules people skip, what the research says about timed breaks, and when a timer gets in the way.',5,
 '''<p>Francesco Cirillo invented the Pomodoro Technique as a university student in the late 1980s. Struggling to concentrate, he challenged himself to study for ten minutes using a tomato-shaped kitchen timer (pomodoro is Italian for tomato). The method that grew from it is now the most widely used focus routine in the world.</p>
<h2>The six steps</h2>
<ol><li>Choose one task.</li><li>Set a timer for 25 minutes.</li><li>Work on the task until the timer rings.</li><li>Mark one session done.</li><li>Take a five-minute break.</li><li>After four sessions, take a longer break of 15 to 30 minutes.</li></ol>
<p>The <a href="../focus/focus-timer.html">focus timer</a> on this site runs the whole cycle and counts sessions against your tasks.</p>
<h2>Two rules people skip</h2>
<p><b>A session is indivisible.</b> If you abandon it, it does not count. This is what gives the timer its force: stopping at minute 18 to check a message throws away the 18 minutes.</p>
<p><b>Interruptions are handled, not obeyed.</b> For an internal urge (“I should look that up”), write it on a list and carry on. For a person, Cirillo’s sequence is inform, negotiate, schedule, call back: tell them you are in the middle of something, agree a time, and return to them when the session ends.</p>
<h2>Does it work?</h2>
<p>The technique itself has been studied less than its popularity suggests, but its two ingredients have support. Ariga and Lleras found in 2011 that brief breaks during a long attention task prevented the usual decline in performance. In a 2023 study of students, Biwer and colleagues compared fixed, Pomodoro-style breaks with breaks taken whenever students felt like it. The fixed-break groups reported better concentration and motivation and less fatigue, and they finished similar work in less time.</p>
<h2>Variations worth trying</h2>
<ul><li><b>50 and 10</b> for programming, writing and analysis, where 25 minutes ends just as you get going.</li>
<li><b>15 and 3</b> for tasks you dread. The aim is only to start.</li>
<li><b>Count, do not clock.</b> Plan the day in sessions (“this report is four”) and compare your estimate with the result. Within two weeks your estimates get noticeably better.</li></ul>
<h2>When not to use it</h2>
<ul><li>When you are already absorbed and the work is flowing. A timer that breaks a good run is doing harm; let the session continue and take a longer break afterwards.</li>
<li>For meetings, calls and collaborative work, which run on other people’s clocks.</li>
<li>For open-ended creative thinking, where a walk often does more than a countdown.</li></ul>
<p>Not sure it is the right method for you? The <a href="../quizzes/productivity-method.html">productivity method quiz</a> compares it with five others.</p>''',
 ['Cirillo, F. (2006). The Pomodoro Technique.','Ariga, A., &amp; Lleras, A. (2011). Brief and rare mental “breaks” keep you focused: deactivation and reactivation of task goals preempt vigilance decrements. Cognition.','Biwer, F., et al. (2023). Understanding effort regulation: comparing “Pomodoro” breaks and self-regulated breaks. British Journal of Educational Psychology.']),

 G('sleep-exercise-and-thinking','Sleep, exercise and thinking: the basics that beat every hack','What the research says about the two habits with the largest effect on how well you think, in practical terms.',6,
 '''<p>No timer, app or technique on this site will do as much for your thinking as sleeping enough and moving regularly. The research on both is large and unusually consistent. This guide is general information for healthy adults, not medical advice; talk to a doctor about persistent sleep problems or before starting a new exercise programme if you have a health condition.</p>
<h2>Sleep: what the loss costs</h2>
<p>In a 2003 study led by Hans Van Dongen, volunteers were limited to six hours in bed a night for two weeks. Their attention lapses rose steadily, reaching the level of people who had been kept awake for a full night or more. The striking part was that they did not feel it: their own sleepiness ratings levelled off after a few days while their performance kept falling.</p>
<p>Being awake too long has a similar effect. Williamson and Feyer found that after 17 to 19 hours without sleep, performance on some tasks matched that of people with a blood alcohol level of 0.05%.</p>
<h2>Sleep: what it does for memory</h2>
<p>Sleep is when the brain stabilises what it learned during the day. Diekelmann and Born’s 2010 review describes how memories are replayed and strengthened during deep sleep. Practically: studying and then sleeping beats staying up to study more.</p>
<h2>Sleep: what to do</h2>
<ul><li>Aim for at least seven hours. That is the adult recommendation from the American Academy of Sleep Medicine and the Sleep Research Society.</li>
<li>Keep a regular wake time, weekends included. It anchors everything else.</li>
<li>Get daylight early in the day and dim the lights in the last hour before bed.</li>
<li>Stop caffeine by early afternoon; it stays in your system for hours.</li></ul>
<h2>Exercise: the evidence</h2>
<p>A single session helps a little, straight away. A 2012 meta-analysis by Chang and colleagues found a small, reliable improvement in thinking during and shortly after a bout of exercise.</p>
<p>Regular training does more. In a year-long trial by Kirk Erickson’s group, older adults who walked briskly three days a week increased the volume of the hippocampus, a region central to memory, by about 2%, while it shrank in a stretching-only control group. Memory performance improved along with it.</p>
<h2>Exercise: what to do</h2>
<ul><li>Follow the World Health Organization guideline of at least 150 minutes a week of moderate aerobic activity, such as brisk walking.</li>
<li>Use a ten-minute walk as a break between focus blocks. It works better than a feed.</li>
<li>Put a walk before the hardest thinking of the day when you can.</li></ul>
<h2>Check it on yourself</h2>
<p>Take the <a href="../train/reaction-time.html">reaction time test</a> at the same hour after a short night and after a full one. The difference is often 20 to 40 milliseconds, enough to see on the <a href="../dashboard.html">dashboard</a>. Your own numbers are more persuasive than any study.</p>''',
 ['Van Dongen, H. P. A., et al. (2003). The cumulative cost of additional wakefulness. Sleep.','Williamson, A. M., &amp; Feyer, A.-M. (2000). Moderate sleep deprivation produces impairments in cognitive and motor performance equivalent to legally prescribed levels of alcohol intoxication. Occupational and Environmental Medicine.','Diekelmann, S., &amp; Born, J. (2010). The memory function of sleep. Nature Reviews Neuroscience.','Watson, N. F., et al. (2015). Recommended amount of sleep for a healthy adult. Sleep.','Chang, Y. K., et al. (2012). The effects of acute exercise on cognitive performance: a meta-analysis. Brain Research.','Erickson, K. I., et al. (2011). Exercise training increases size of hippocampus and improves memory. PNAS.','World Health Organization (2020). WHO guidelines on physical activity and sedentary behaviour.']),

 G('build-a-thinking-toolkit','Build a thinking toolkit: how to use mental models at work','Why a handful of well-chosen models beats a long list, and a four-week plan for making five of them automatic.',6,
 '''<p>A mental model is a compact idea about how something works, small enough to carry and general enough to reuse. “Work expands to fill the time available” is one. “A system moves as fast as its slowest step” is another. Each one lets you see a pattern faster than you could reason it out from scratch.</p>
<h2>Why you need more than one</h2>
<p>Abraham Maslow wrote in 1966 that if the only tool you have is a hammer, it is tempting to treat everything as a nail. A single model, however good, gets applied where it does not fit. Charlie Munger’s answer, in a 1994 talk to business students, was a “latticework” of models drawn from several disciplines, so that problems can be looked at from more than one side.</p>
<p>The opposite mistake is more common now: collecting a hundred models and using none. A model only helps if it comes to mind at the moment of decision.</p>
<h2>Start with five</h2>
<p>Pick one from each area where your work most often goes wrong. A reasonable starting set:</p>
<ul><li>For choosing: <a href="../models/two-way-doors.html">reversible and irreversible decisions</a></li>
<li>For risk: <a href="../models/pre-mortem.html">the pre-mortem</a></li>
<li>For priorities: <a href="../models/pareto-principle.html">the Pareto principle</a></li>
<li>For process problems: <a href="../models/bottleneck.html">bottlenecks</a></li>
<li>For communication: <a href="../models/pyramid-principle.html">the pyramid principle</a></li></ul>
<h2>Attach each model to a trigger</h2>
<p>Models fire when they are tied to situations. Write an if-then line for each: “If I am about to commit more than a week of someone’s time, then I ask whether it is a one-way door.” “If I am writing an update, then the first sentence is the conclusion.” Psychologists call these implementation intentions, and they are one of the more reliable ways to turn an intention into a habit.</p>
<h2>A four-week plan</h2>
<ol><li><b>Week 1.</b> Read the five model pages. Write your five if-then lines on one card and keep it where you work.</li>
<li><b>Week 2.</b> Use each model once on a real decision, however small. Note in two lines what it changed.</li>
<li><b>Week 3.</b> Explain one model to a colleague using an example from your own team. If you cannot, reread it.</li>
<li><b>Week 4.</b> Review your notes. Keep the models that changed a decision, replace the ones that did not, and add one new model.</li></ol>
<h2>Remember what a model is</h2>
<p>Alfred Korzybski’s phrase “the map is not the territory” applies to every model here, including that one. A model is a simplification that is useful for a purpose. When it stops fitting the facts in front of you, the facts win.</p>
<p>The full <a href="../models/index.html">model library</a> is sorted by the kind of problem each one helps with, and every page has the steps, a workplace example and the usual way it gets misused.</p>''',
 ['Munger, C. T. (1994). A lesson on elementary, worldly wisdom as it relates to investment management and business. Talk at USC Marshall School of Business.','Maslow, A. H. (1966). The Psychology of Science.','Gollwitzer, P. M. (1999). Implementation intentions: strong effects of simple plans. American Psychologist.','Korzybski, A. (1933). Science and Sanity.']),
]
