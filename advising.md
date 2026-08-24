---
layout: default
title: Advising
permalink: /advising/
---

<h1 class="visually-hidden">{{ page.title }}</h1>

<div id="advising">
  <div id="trail"></div>
  <div id="node"></div>
</div>

<style>
#advising {
  max-width: 34rem;
  margin: 3rem auto 8rem;
}

#trail {
  margin-bottom: 2.5rem;
}

.past {
  margin-bottom: 1.1rem;
  line-height: 1.4;
}

.past .q,
.past .a {
  font-size: 0.85em;
}

.past .a {
  color: var(--accent);
}

.q-current {
  font-size: 1.25em;
  line-height: 1.35;
  margin-bottom: 1.75rem;
}

/* The pivot between acts is the one sincere line in the piece. */
.q-current.beat {
  font-size: 1.5em;
  margin-bottom: 2.5rem;
}

.choices {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  align-items: flex-start;
}

.choices button {
  font-family: inherit;
  font-size: 1em;
  color: var(--ink);
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 2px;
  padding: 0.5rem 0.9rem;
  cursor: pointer;
  text-align: left;
  transition: background 0.1s ease, border-color 0.1s ease;
}

.choices button:hover {
  background: var(--sunk);
  border-color: var(--faint);
}

/* The ending is a drawing of the page you just walked through. */
.map {
  margin: 0.5rem 0 0;
}

.map svg {
  display: block;
  width: 100%;
  height: auto;
}

/* The strands are drawn by script; their colours belong to the theme, so the
   script sets a class and the values stay here with everything else. */
.map path {
  fill: none;
}

.map .strand-mine {
  stroke: var(--accent);
  fill: none;
}

.map circle.strand-mine {
  fill: var(--accent);
}

.map .strand-other {
  stroke: var(--rule);
  fill: none;
}

.map circle.strand-other {
  fill: var(--rule);
}

.verdict {
  margin-top: 1.25rem;
  font-size: 1.15em;
  line-height: 1.35;
}

/* It never branched. It was still counting. */
.tally {
  margin-top: 1.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--rule);
  font-size: 0.8em;
  line-height: 1.9;
  color: var(--faint);
}

.tally b {
  font-weight: normal;
  color: var(--ink);
}

.others {
  margin-top: 1.25rem;
  font-size: 0.8em;
  line-height: 1.7;
  color: var(--faint);
}

.others .mine {
  color: var(--soft);
}

.again {
  margin-top: 2rem;
  font-size: 0.85em;
  color: var(--faint);
  background: none;
  border: none;
  padding: 0;
  font-family: inherit;
  cursor: pointer;
  text-decoration: underline;
}
</style>

<script>
(function () {

  /* Shape of the thing: every beat is a setup and a punchline. The setup
     picks which punchline you get; the punchline always goes where the
     setup was going anyway. So the two buttons genuinely change what you
     read, and never once change where you land. Two nodes in the whole
     page branch on the answer: `fork` and `track`.

     By convention index 0 is the dignified answer and index 1 is the
     admission. `flat: true` marks the pairs where that isn't on offer,
     and those are left out of the count at the end. */

  var TREE = {

    /* ======================= ACT 0 ======================= */

    start: {
      q: "You were good at math in high school.",
      a: ["I was", "I was told I was"],
      to: ["start_a", "start_b"]
    },
    start_a: {
      q: "You were the best mathematician in a building that contained no mathematicians. That is a real thing to have been, and it is also a local maximum.",
      a: ["It still counts", "I have since seen the graph"],
      to: ["klass", "klass"]
    },
    start_b: {
      q: "By a teacher who had not done mathematics since 1994 and who was being kind.",
      a: ["She meant it", "She was right to be kind"],
      to: ["klass", "klass"]
    },

    klass: {
      q: "Then came the first class where being fast stopped working.",
      a: ["I adjusted", "I'm still adjusting"],
      to: ["klass_a", "klass_b"]
    },
    klass_a: {
      q: "You adjusted by spending nine hours on a problem whose solution is one line. The line is: consider the obvious map.",
      a: ["I found it", "I found it in the back of the book"],
      to: ["fork", "fork"]
    },
    klass_b: {
      q: "The average on that midterm was thirty-one out of a hundred. Nobody in the room found this alarming, which was the alarming part.",
      a: ["It was a hard exam", "It was working as designed"],
      to: ["fork", "fork"]
    },

    fork: {
      q: "You have to pick one.",
      a: ["Pure", "Applied"],
      to: ["p_why", "a_why"],
      flat: true
    },

    /* ===================== THE PURE ROAD ===================== */

    p_why: {
      q: "Say why. Out loud, at a party, to someone who asked.",
      a: ["It's beautiful", "It's the hardest thing there is"],
      to: ["p_why_a", "p_why_b"]
    },
    p_why_a: {
      q: "You said “beautiful” to a person who had asked what you do for a living.",
      a: ["They understood", "They said “like, numbers?”"],
      to: ["p_trivial", "p_trivial"]
    },
    p_why_b: {
      q: "Then it was never the mathematics. It was the ranking.",
      a: ["It's the math", "Keep going"],
      to: ["p_trivial", "p_trivial"]
    },

    p_trivial: {
      q: "Your professor writes a line on the board and says it is trivial.",
      a: ["It was trivial", "He then stopped"],
      to: ["p_trivial_a", "p_trivial_b"]
    },
    p_trivial_a: {
      q: "It was. You were the only person in the room who didn't see it, along with everyone else in the room.",
      a: ["I saw it", "We compared notes afterward"],
      to: ["p_eleven", "p_eleven"]
    },
    p_trivial_b: {
      q: "He stared at it. He left the room. He came back twenty minutes later and said: yes, it's trivial.",
      a: ["That's a great teacher", "That's the entire field"],
      to: ["p_eleven", "p_eleven"]
    },

    p_eleven: {
      q: "You spent October proving that the real numbers have no gaps.",
      a: ["It needed proving", "I assumed it at eleven"],
      to: ["p_eleven_a", "p_eleven_b"]
    },
    p_eleven_a: {
      q: "It did. And everything you assumed at eleven turned out to be true, which is a hard result to describe to anyone as news.",
      a: ["It's still worth proving", "Try saying it at dinner"],
      to: ["p_exists", "p_exists"]
    },
    p_eleven_b: {
      q: "You assumed it at eleven and you were right. The degree is four years of finding out why you were allowed to be.",
      a: ["That's the degree", "That's the whole degree"],
      to: ["p_exists", "p_exists"]
    },

    p_exists: {
      q: "You proved a solution exists. An engineer asks you where it is.",
      a: ["It exists", "That isn't the question"],
      to: ["p_exists_a", "p_exists_b"]
    },
    p_exists_a: {
      q: "He needs the number by Thursday. You have handed him a guarantee that the number has a location.",
      a: ["That's more than he had", "That's nothing"],
      to: ["p_arith", "p_arith"]
    },
    p_exists_b: {
      q: "So you show him the function that is continuous everywhere and differentiable nowhere. He says nothing he has ever had to model was that rude.",
      a: ["He's been lucky", "He's been right"],
      to: ["p_arith", "p_arith"]
    },

    p_arith: {
      q: "Someone at the table asks you to split the check.",
      a: ["I can split a check", "I passed the phone"],
      to: ["p_arith_a", "p_arith_b"]
    },
    p_arith_a: {
      q: "You can. It took eleven seconds and the whole table waited, and nobody was unkind about it, which was worse.",
      a: ["Eleven seconds is fine", "They were very kind"],
      to: ["p_lineage", "p_lineage"]
    },
    p_arith_b: {
      q: "You could compute an integral at seventeen. You traded that for knowing what one is, and the man who took the phone sells insurance.",
      a: ["It was a good trade", "He was faster"],
      to: ["p_lineage", "p_lineage"]
    },

    p_lineage: {
      q: "You have started to sound like the department.",
      a: ["I sound like myself", "How would I know"],
      to: ["p_lineage_a", "p_lineage_b"]
    },
    p_lineage_a: {
      q: "You looked up your advisor's advisor. Nine generations back there is a German with a Wikipedia page, and you have mentioned this at two parties.",
      a: ["It's a real lineage", "It is load-bearing"],
      to: ["p_machine", "p_machine"]
    },
    p_lineage_b: {
      q: "You have opinions about chalk. The department imports it from Japan by the case and there is a drawer with a key.",
      a: ["The chalk is genuinely better", "I have a key"],
      to: ["p_machine", "p_machine"]
    },

    p_machine: {
      q: "Overnight, a proof assistant closed a problem from your seminar.",
      a: ["That isn't understanding", "How long is it"],
      to: ["p_machine_a", "p_machine_b"]
    },
    p_machine_a: {
      q: "Four hundred thousand lines. It is correct, no person will ever read it, and correctness was supposed to be the entire point.",
      a: ["Understanding was the point", "Then say which one it was"],
      to: ["p_money", "p_money"]
    },
    p_machine_b: {
      q: "Long enough that checking it is also a machine's job now. You have automated the part you said at the party you were in it for.",
      a: ["I'm not in it for that", "I did say it at a party"],
      to: ["p_money", "p_money"]
    },

    p_money: {
      q: "Who paid for your summer?",
      a: ["A fellowship", "I'd have to look it up"],
      to: ["p_money_a", "p_money_b"]
    },
    p_money_a: {
      q: "The NSA. Number theory has one enormous customer and it is not the Institute.",
      a: ["It's still pure", "It's still pure"],
      to: ["truce", "truce"],
      flat: true
    },
    p_money_b: {
      q: "The largest employer of mathematicians in the country is not a university. It has been buying number theory since before you were born and it has never once been coy about why.",
      a: ["It's still pure mathematics", "I stopped looking things up"],
      to: ["truce", "truce"]
    },

    /* ==================== THE APPLIED ROAD ==================== */

    a_why: {
      q: "Say why. Out loud, at a party, to someone who asked.",
      a: ["It's useful", "I want a job"],
      to: ["a_why_a", "a_why_b"]
    },
    a_why_a: {
      q: "Name one person it has been useful to. A name.",
      a: ["I'd rather not", "Skip"],
      to: ["a_insult", "a_insult"]
    },
    a_why_b: {
      q: "The honest answer. The pure kids want to be paid too. They want it in a currency you cannot spend.",
      a: ["Fine", "That's generous to them"],
      to: ["a_insult", "a_insult"]
    },

    a_insult: {
      q: "A pure math student asks what you're working on.",
      a: ["Tell them", "Say “modeling”"],
      to: ["a_insult_a", "a_insult_b"]
    },
    a_insult_a: {
      q: "“Oh,” they said. “So it's numerical.” You had been thinking about it for three days.",
      a: ["It is numerical", "That isn't the insult they think it is"],
      to: ["a_prior", "a_prior"]
    },
    a_insult_b: {
      q: "“Modeling” is the word you use to prevent a second question. They asked a second question.",
      a: ["It usually works", "It has never once worked"],
      to: ["a_prior", "a_prior"]
    },

    a_prior: {
      q: "Your advisor recognizes your main result.",
      a: ["It's new", "It's new to me"],
      to: ["a_prior_a", "a_prior_b"]
    },
    a_prior_a: {
      q: "A Russian did it in 1912, in more generality, without a computer, in eleven pages.",
      a: ["Mine is constructive", "Mine has a plot"],
      to: ["a_stack", "a_stack"]
    },
    a_prior_b: {
      q: "Underneath, it is Ax = b wearing a hat. Everything down here is Ax = b wearing a hat.",
      a: ["The hat is the contribution", "I am describing my thesis"],
      to: ["a_stack", "a_stack"]
    },

    a_stack: {
      q: "Everything you know how to do, you do inside one program.",
      a: ["It's a good program", "It's a license"],
      to: ["a_stack_a", "a_stack_b"]
    },
    a_stack_a: {
      q: "It is a good program. The university renews it every August, and in the August it doesn't, your entire field becomes a collection of PDFs.",
      a: ["We would port it", "It would take a decade"],
      to: ["a_assume", "a_assume"]
    },
    a_stack_b: {
      q: "You queued the big run on Friday. It died at hour eleven on a misspelled filename and you found out on Monday.",
      a: ["I fixed it in a minute", "It cost a weekend and took a minute"],
      to: ["a_assume", "a_assume"]
    },

    a_assume: {
      q: "Line one of your paper. Assume f is smooth.",
      a: ["It is", "It's fine"],
      to: ["a_assume_a", "a_assume_b"]
    },
    a_assume_a: {
      q: "You didn't check. Nobody checked. An entire field is standing on a sentence that opens with the word assume.",
      a: ["It's always held", "It's always held so far"],
      to: ["a_exact", "a_exact"]
    },
    a_assume_b: {
      q: "It's fine the way the validation was fine. You validated against another simulation, which was validated against a third.",
      a: ["That's how it's done", "That is exactly how it's done"],
      to: ["a_exact", "a_exact"]
    },

    a_exact: {
      q: "You told them the solution was exact.",
      a: ["To six decimals", "Exact enough"],
      to: ["a_exact_a", "a_exact_b"]
    },
    a_exact_a: {
      q: "You have never once touched a real number. You work in a finite set of rationals that lies about being the continuum.",
      a: ["So does everyone", "The pure kids don't"],
      to: ["a_beaten", "a_beaten"]
    },
    a_exact_b: {
      q: "It became exact enough after you halved the timestep. You never did find out why it had been exploding.",
      a: ["It stopped exploding", "That was the finding"],
      to: ["a_beaten", "a_beaten"]
    },

    a_beaten: {
      q: "A first-year with a GPU beat your model by nine percent.",
      a: ["His model explains nothing", "It's within noise"],
      to: ["a_beaten_a", "a_beaten_b"]
    },
    a_beaten_a: {
      q: "Neither does yours. Yours has forty parameters. Von Neumann could fit an elephant with four and wiggle its trunk with five.",
      a: ["They're physical", "Thirty-five of them are physical"],
      to: ["a_money", "a_money"]
    },
    a_beaten_b: {
      q: "You checked. You changed the random seed and your own conclusion moved further than nine percent.",
      a: ["That's within noise too", "I did not change the seed again"],
      to: ["a_money", "a_money"]
    },

    a_money: {
      q: "Who paid for your summer?",
      a: ["A lab", "A subcontractor of a lab"],
      to: ["a_money_a", "a_money_b"]
    },
    a_money_a: {
      q: "Turbulence over a curved surface. The surface is a wing, and the wing is attached to something.",
      a: ["It's still just fluid", "It's still just fluid"],
      to: ["truce", "truce"],
      flat: true
    },
    a_money_b: {
      q: "The grant is titled Efficient Transport in Compressible Media. Every word in that title is doing a job.",
      a: ["It's an accurate title", "I helped write the title"],
      to: ["truce", "truce"]
    },

    /* ============ WHAT BOTH ROADS TURN OUT TO SHARE ============ */

    truce: {
      q: "A physicist tells you that rigor is a stylistic preference.",
      a: ["Let me speak", "Hold my coat"],
      to: ["truce_a", "truce_b"]
    },
    truce_a: {
      q: "He divides by a quantity he has not shown to be nonzero. He gets the right answer. He has always gotten the right answer.",
      a: ["That's luck", "That's worse than luck"],
      to: ["money1", "money1"]
    },
    truce_b: {
      q: "He refers to everything either of you does as “the notation.” For one moment you and the other kind of mathematician wanted precisely the same thing.",
      a: ["We did", "It passed"],
      to: ["money1", "money1"]
    },

    money1: {
      q: "Then look at where either of you gets paid. There are three questions.",
      a: ["Name them", "I can name them"],
      to: ["money1_a", "money1_b"]
    },
    money1_a: {
      q: "How do I read their mail. How do I hit a thing far away. How do I make a thing fly.",
      a: ["Cryptography, ballistics, aerodynamics", "That is not all of mathematics"],
      to: ["money2", "money2"]
    },
    money1_b: {
      q: "“Computer” was a job title before it was a machine, and the job was ballistics tables.",
      a: ["That was the forties", "That was the funding"],
      to: ["money2", "money2"]
    },

    money2: {
      q: "That is all of the funded mathematics. The rest is a hobby a university has agreed to house.",
      a: ["There's medicine", "There's a fourth question"],
      to: ["money2_a", "money2_b"]
    },
    money2_a: {
      q: "Medicine is hitting a small thing precisely. You have found the second question wearing a lab coat.",
      a: ["That's cynical", "That's the language in the grant"],
      to: ["money3", "money3"]
    },
    money2_b: {
      q: "There is. It is the only one with no government in it, it is younger than your parents, and it pays better than the other three combined.",
      a: ["How do I know first", "How do I know half a second before anyone else"],
      to: ["money3", "money3"]
    },

    money3: {
      q: "Your department tells one story about all of this, and tells it the same way every time.",
      a: ["The geometer", "I know the story"],
      to: ["money3_a", "money3_b"]
    },
    money3_a: {
      q: "A geometer with a theorem named after him, let go from the codebreaking shop over a letter about Vietnam, who then built the most profitable fund in history and staffed it with cryptographers and astronomers.",
      a: ["That's one man", "That's every question at once"],
      to: ["money4", "money4"]
    },
    money3_b: {
      q: "It gets told as proof that pure mathematics pays. It is a man who did the first question, then the fourth question, and the theorem is the part he did in between.",
      a: ["It's still a happy ending", "For him"],
      to: ["money4", "money4"]
    },

    money4: {
      q: "They have gentler names now. Reading their mail is privacy. Hitting a thing far away is autonomy. Making a thing fly is logistics. Knowing first is liquidity.",
      a: ["That's just what they're called", "That's what they're called now"],
      to: ["money5", "money5"]
    },
    money5: {
      q: "Pure or applied, you are downstream of somebody who wanted to know where the shell would land.",
      a: ["Not my part of it", "Especially my part of it"],
      to: ["pivot", "pivot"]
    },

    /* ---- the act break ---- */

    pivot: {
      q: "Four years pass.",
      beat: true,
      a: ["Continue"],
      to: ["track"]
    },

    /* ================ ACT II: the second real door ================ */

    track: {
      q: "Grad school or industry?",
      a: ["Grad school", "Industry"],
      to: ["@grad", "@industry"],
      flat: true
    },

    /* ---- pure, grad ---- */

    pg1: {
      q: "Five years. Possibly seven. Your advisor has three other students and a book.",
      a: ["I know", "Yes, but quietly"],
      to: ["pg1_a", "pg1_b"]
    },
    pg1_a: {
      q: "You will become the world authority on a question eleven people are qualified to evaluate. Four of them are on your committee.",
      a: ["Eleven is enough", "It isn't"],
      to: ["pg2", "pg2"]
    },
    pg1_b: {
      q: "Your advisor answers email seasonally. You have learned to phrase things so that silence is an answer.",
      a: ["That's independence", "That's what I've been calling it"],
      to: ["pg2", "pg2"]
    },
    pg2: {
      q: "Quals are in March.",
      a: ["I'll pass", "I'll pass and forget it"],
      to: ["pg2_a", "pg2_b"]
    },
    pg2_a: {
      q: "Eight months for an examination whose only function is to have been passed. Nobody will ask you about it again as long as you live.",
      a: ["It's a rite", "It's a wall built to be climbed once"],
      to: ["pg3", "pg3"]
    },
    pg2_b: {
      q: "You will forget it inside a year. So has the entire faculty, and the exam is written by people who could not sit it today.",
      a: ["They could", "Not one of them could"],
      to: ["pg3", "pg3"]
    },
    pg3: {
      q: "Your subfield posted six tenure-track jobs this year.",
      a: ["That's not nothing", "How many are real"],
      to: ["pg3_a", "pg3_b"]
    },
    pg3_a: {
      q: "Two are visiting. One is in a city you would have to look up. You are competing with the eleven people, and four of them wrote your letters.",
      a: ["I'll get one", "Someone will"],
      to: ["clock", "clock"]
    },
    pg3_b: {
      q: "Your stipend is thirty-one thousand dollars. The first-year you tutored took the fund job and cleared your stipend in eight weeks.",
      a: ["That was never the point", "I know exactly what it was"],
      to: ["clock", "clock"]
    },

    /* ---- pure, industry ---- */

    pi1: {
      q: "You're taking the job. You will start saying “technically a mathematician.”",
      a: ["I won't", "I will"],
      to: ["pi1_a", "pi1_b"]
    },
    pi1_a: {
      q: "The applied kids trained four years for this. You will be behind them, and you will call it slumming.",
      a: ["I'll catch up", "I did call it that"],
      to: ["pi2", "pi2"]
    },
    pi1_b: {
      q: "You have a profile now. Under Skills it says Mathematics, and it sits between Excel and Teamwork.",
      a: ["I'll fix the ordering", "I chose the ordering"],
      to: ["pi2", "pi2"]
    },
    pi2: {
      q: "The interview is at a whiteboard.",
      a: ["I'm good at whiteboards", "I am extremely good at whiteboards"],
      to: ["pi2_a", "pi2_b"]
    },
    pi2_a: {
      q: "You have proved Stone–Weierstrass at a whiteboard. They would like you to reverse a linked list at a whiteboard.",
      a: ["Same skill", "One of us is being tested on the wrong thing"],
      to: ["pi3", "pi3"]
    },
    pi2_b: {
      q: "The other one is at a fund. They ask you to price a coin flip. You reach for measure theory and the answer is fifty cents.",
      a: ["That was the warm-up", "I proved it was fifty cents"],
      to: ["pi3", "pi3"]
    },
    pi3: {
      q: "Both of your offers come with a rule about what you may publish.",
      a: ["That's normal", "One of them is a government"],
      to: ["pi3_a", "pi3_b"]
    },
    pi3_a: {
      q: "Cryptography is called crypto now and it is a different thing. Yours is in Maryland and it wants a form, a polygraph, and the rest of the decade.",
      a: ["I could still do the real one", "I know exactly where it is"],
      to: ["clock", "clock"]
    },
    pi3_b: {
      q: "One is a government and one is a fund, and the fund is stricter. You will do the best mathematics of your life and describe it to your parents as finance.",
      a: ["They'll understand finance", "That is why I'll say finance"],
      to: ["clock", "clock"]
    },

    /* ---- applied, grad ---- */

    ag1: {
      q: "You're going back for the rigor you skipped.",
      a: ["Yes", "That isn't why"],
      to: ["ag1_a", "ag1_b"]
    },
    ag1_a: {
      q: "You'll spend a year on the analysis you avoided and learn that it was never the analysis stopping you.",
      a: ["Then what was", "I know what it was"],
      to: ["ag2", "ag2"]
    },
    ag1_b: {
      q: "It's the title. It has been the title since sophomore year, and there is no shame in that, which is not the same as there being a reason.",
      a: ["There's a reason", "There's a title"],
      to: ["ag2", "ag2"]
    },
    ag2: {
      q: "Your funding line has a number on it.",
      a: ["It's basic research", "Whose number is it"],
      to: ["ag2_a", "ag2_b"]
    },
    ag2_a: {
      q: "Basic research is what they call it during the years they are giving it to you.",
      a: ["It's still basic", "It's basic for now"],
      to: ["ag3", "ag3"]
    },
    ag2_b: {
      q: "Your preprints go to the sponsor before they go anywhere else. They have thirty days each time and they have never once asked for a change.",
      a: ["Then it's a formality", "Thirty days, every time"],
      to: ["ag3", "ag3"]
    },
    ag3: {
      q: "You are teaching two sections of calculus.",
      a: ["I like teaching", "Two hundred people"],
      to: ["ag3_a", "ag3_b"]
    },
    ag3_a: {
      q: "Two hundred people who resent the requirement, correctly, and one who will change majors because of you, and you will never find out which one.",
      a: ["That's worth it", "That's the whole deal"],
      to: ["clock", "clock"]
    },
    ag3_b: {
      q: "It's twenty hours a week. It is not twenty hours a week in your funding letter.",
      a: ["It's part of the training", "It's the part that isn't"],
      to: ["clock", "clock"]
    },

    /* ---- applied, industry ---- */

    ai1: {
      q: "You got the job. It's SQL.",
      a: ["It isn't only SQL", "It's SQL"],
      to: ["ai1_a", "ai1_b"]
    },
    ai1_a: {
      q: "You picked applied so the mathematics would come with you into the world. The world had its own plans and they involved a spreadsheet.",
      a: ["It's temporary", "It isn't"],
      to: ["ai2", "ai2"]
    },
    ai1_b: {
      q: "There is real mathematics at this company. It is three floors up and they hire it out of the PhD programs.",
      a: ["I'll move up", "I know who they hire"],
      to: ["ai2", "ai2"]
    },
    ai2: {
      q: "Your manager has a math degree.",
      a: ["Then he'll understand", "Does he use it"],
      to: ["ai2_a", "ai2_b"]
    },
    ai2_a: {
      q: "He does not use it. He is measurably happier than you are, and he raises it rarely and kindly.",
      a: ["Good for him", "That's the part I mind"],
      to: ["ai3", "ai3"]
    },
    ai2_b: {
      q: "Once a quarter, to tell a vice president that a difference is not significant. The vice president thanks him and proceeds.",
      a: ["That's still using it", "That's the whole job"],
      to: ["ai3", "ai3"]
    },
    ai3: {
      q: "There was another offer and you have not stopped doing arithmetic about it.",
      a: ["Defense", "The fund"],
      to: ["ai3_a", "ai3_b"]
    },
    ai3_a: {
      q: "Genuinely hard, genuinely the second question, and they will let you publish some of it in nine years.",
      a: ["How do I hit a thing far away", "They have a gentler name for it now"],
      to: ["clock", "clock"]
    },
    ai3_b: {
      q: "Four times the money to separate signal from noise in data that is almost entirely noise. Your title would be Researcher. There is no paper.",
      a: ["Researcher is accurate", "There is no paper"],
      to: ["clock", "clock"]
    },

    /* ---- the last thing everyone shares ---- */

    clock: {
      q: "Either way you are counting toward a number now. Six to tenure, four to vested. Both are a clock you cannot leave early without agreeing, out loud, that you failed.",
      a: ["That isn't what leaving means", "It's what it means here"],
      to: ["last", "last"]
    },

    last: {
      q: "Last question. Which one is it?",
      a: [
        "I'm afraid I'm not smart enough",
        "I'm afraid I already found out"
      ],
      to: ["@end", "@end"]
    }
  };

  // Four endings. Only the sentence changes; the drawing is the same drawing.
  var VERDICTS = {
    "pure/grad": "You will spend six years explaining to your family what you do.",
    "pure/industry": "You will tell people you used to do math.",
    "applied/grad": "You will finally be rigorous, about something you no longer want.",
    "applied/industry": "You will build a dashboard that a vice president will not open."
  };

  var ORDER = ["pure/grad", "pure/industry", "applied/grad", "applied/industry"];

  var TOTAL_SCREENS = Object.keys(TREE).length;

  var trailEl = document.getElementById("trail");
  var nodeEl = document.getElementById("node");

  var history, tribe, track, decisions, graded, flattered;

  function reset() {
    history = [];
    tribe = "pure";
    track = "grad";
    decisions = 0;  // every node that offered two buttons
    graded = 0;     // ...of which these offered dignity or honesty
    flattered = 0;  // ...and these are the ones where you took the dignity
  }

  // How many times you have sat through this. Some browsers decline to say.
  function bumpRuns() {
    try {
      var n = (parseInt(localStorage.getItem("advising-runs"), 10) || 0) + 1;
      localStorage.setItem("advising-runs", String(n));
      return n;
    } catch (e) {
      return 1;
    }
  }

  // Most recent answer is the most legible; freshman year is a ghost.
  function fade(distance) {
    return Math.max(0.1, 0.5 * Math.pow(0.68, distance - 1));
  }

  function drawTrail() {
    trailEl.innerHTML = "";
    history.forEach(function (step, i) {
      var div = document.createElement("div");
      div.className = "past";
      div.style.opacity = fade(history.length - i);
      div.innerHTML = '<div class="q"></div><div class="a"></div>';
      div.querySelector(".q").textContent = step.q;
      div.querySelector(".a").textContent = "› " + step.a;
      trailEl.appendChild(div);
    });
  }

  // Act II reads your major back to you. It does not ask about it again.
  function resolve(target) {
    if (target === "@grad") {
      track = "grad";
      return tribe === "pure" ? "pg1" : "ag1";
    }
    if (target === "@industry") {
      track = "industry";
      return tribe === "pure" ? "pi1" : "ai1";
    }
    return target;
  }

  function choose(id, node, i) {
    history.push({ q: node.q, a: node.a[i] });

    if (node.a.length > 1) {
      decisions++;
      if (!node.flat) {
        graded++;
        if (i === 0) flattered++;
      }
    }

    if (id === "fork") tribe = i === 0 ? "pure" : "applied";
    render(resolve(node.to[i]));
  }

  function render(id) {
    drawTrail();

    if (id === "@end") {
      renderEnd();
      return;
    }

    var node = TREE[id];
    nodeEl.innerHTML = '<div class="q-current"></div><div class="choices"></div>';

    var q = nodeEl.querySelector(".q-current");
    q.textContent = node.q;
    if (node.beat) q.classList.add("beat");

    var choices = nodeEl.querySelector(".choices");
    node.a.forEach(function (label, i) {
      var b = document.createElement("button");
      b.textContent = label;
      b.addEventListener("click", function () {
        choose(id, node, i);
      });
      choices.appendChild(b);
    });

    nodeEl.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  /* ---- the drawing ----
     Two strands leave the fork and never actually merge; they only run
     alongside each other through the shared middle, then separate again
     on something you decided twenty screens earlier. Yours is in blue. */

  // Smooth a run of points into one path: straight on the verticals,
  // S-curved wherever the strand steps sideways.
  function pathOf(pts) {
    var d = "M" + pts[0][0] + "," + pts[0][1];
    for (var i = 1; i < pts.length; i++) {
      var p = pts[i - 1], c = pts[i], m = (p[1] + c[1]) / 2;
      d += "C" + p[0] + "," + m + " " + c[0] + "," + m + " " + c[0] + "," + c[1];
    }
    return d;
  }

  var LANES = {
    "pure/grad":       [150, 62],
    "pure/industry":   [150, 146],
    "applied/grad":    [250, 254],
    "applied/industry":[250, 338]
  };

  function strandFor(key) {
    var lane = LANES[key];
    return [
      [200, 14],   // start
      [200, 44],   // act 0
      [lane[0], 82],  // the fork
      [lane[0], 140], // your road
      [lane[0] < 200 ? 188 : 212, 172], // the truce, alongside but not merged
      [lane[0] < 200 ? 188 : 212, 202], // the pivot
      [lane[1], 244]  // the door, and the ending
    ];
  }

  function drawMap(mine) {
    var svgns = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(svgns, "svg");
    svg.setAttribute("viewBox", "0 0 400 258");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label",
      "The whole page: two roads that run alongside each other and end in four sentences.");

    // Your strand shares most of its length with the others, so it goes on
    // last -- otherwise the road you didn't take paints over the one you did.
    var back = ORDER.filter(function (k) { return k !== mine; }).concat([mine]);

    back.forEach(function (key) {
      var p = document.createElementNS(svgns, "path");
      p.setAttribute("d", pathOf(strandFor(key)));
      p.setAttribute("fill", "none");
      p.setAttribute("class", key === mine ? "strand-mine" : "strand-other");
      p.setAttribute("stroke-width", key === mine ? "1.6" : "1");
      svg.appendChild(p);
    });

    back.forEach(function (key) {
      var dot = document.createElementNS(svgns, "circle");
      dot.setAttribute("cx", LANES[key][1]);
      dot.setAttribute("cy", 244);
      dot.setAttribute("r", key === mine ? 4 : 2.5);
      dot.setAttribute("class", key === mine ? "strand-mine" : "strand-other");
      svg.appendChild(dot);
    });

    var wrap = document.createElement("div");
    wrap.className = "map";
    wrap.appendChild(svg);
    return wrap;
  }

  function renderEnd() {
    var runs = bumpRuns();
    var mine = tribe + "/" + track;
    var seen = history.length;

    nodeEl.innerHTML = "";
    nodeEl.appendChild(drawMap(mine));

    var verdict = document.createElement("div");
    verdict.className = "verdict";
    verdict.textContent = VERDICTS[mine];
    nodeEl.appendChild(verdict);

    var tally = document.createElement("div");
    tally.className = "tally";
    tally.innerHTML =
      "<div><b>" + decisions + "</b> decisions. <b>2</b> of them changed where you ended up.</div>" +
      "<div>You saw <b>" + seen + "</b> of the <b>" + TOTAL_SCREENS +
      "</b> screens here. The rest were the answer you didn't give.</div>" +
      "<div>You took the flattering one <b>" + flattered + "</b> of " + graded + " times.</div>";
    nodeEl.appendChild(tally);

    // Second time through, it stops pretending to be large.
    if (runs > 1) {
      var others = document.createElement("div");
      others.className = "others";
      others.innerHTML =
        "<div>Run " + runs + ". All four endings:</div>" +
        ORDER.map(function (key) {
          var lead = key === mine ? "› " : "  ";
          var cls = key === mine ? ' class="mine"' : "";
          return "<div" + cls + ">" + lead + VERDICTS[key] + "</div>";
        }).join("");
      nodeEl.appendChild(others);
    }

    var again = document.createElement("button");
    again.className = "again";
    again.textContent = runs > 1 ? "Start over anyway" : "Start over";
    again.addEventListener("click", function () {
      reset();
      render("start");
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    nodeEl.appendChild(again);

    nodeEl.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  reset();
  render("start");
})();
</script>
