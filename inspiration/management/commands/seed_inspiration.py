"""Seed the inspiration app with real fitness icons, categories, and quotes.

Photo URLs use Unsplash fitness-themed images that represent each discipline
(not portraits of specific individuals, to avoid licensing concerns). The
biographies, achievements, training tips, and quotes are sourced from
publicly-available interviews, official records, and biographies.
"""
from django.core.management.base import BaseCommand

from inspiration.models import FitnessIcon, InspirationCategory, MotivationQuote


CATEGORIES = [
    {
        'name': 'Bodybuilding',
        'slug': 'bodybuilding',
        'description': 'The art and science of building a championship physique — mass, symmetry, and stage presence.',
        'icon': '🏆',
        'accent': 'emerald',
        'display_order': 1,
    },
    {
        'name': 'CrossFit',
        'slug': 'crossfit',
        'description': 'Constantly varied, high-intensity functional movement forged in the crucible of competition.',
        'icon': '🔥',
        'accent': 'rose',
        'display_order': 2,
    },
    {
        'name': 'Strength Sports',
        'slug': 'strength',
        'description': 'Powerlifting, strongman, and weightlifting — where raw strength meets perfect technique.',
        'icon': '🏋️',
        'accent': 'amber',
        'display_order': 3,
    },
    {
        'name': 'Endurance',
        'slug': 'endurance',
        'description': 'Marathoners, ultrarunners, and triathletes who redefine what the human body can sustain.',
        'icon': '🏃',
        'accent': 'sky',
        'display_order': 4,
    },
    {
        'name': 'Athletics & Gymnastics',
        'slug': 'athletics',
        'description': 'Track stars, gymnasts, and Olympic athletes who push the boundaries of speed, power, and grace.',
        'icon': '🤸',
        'accent': 'violet',
        'display_order': 5,
    },
    {
        'name': 'Mindset & Discipline',
        'slug': 'mindset',
        'description': 'Coaches, authors, and ultra-endurance performers who prove the body achieves what the mind believes.',
        'icon': '🧠',
        'accent': 'cyan',
        'display_order': 6,
    },
]


# Use generic, proven Unsplash fitness photos. The slug-based mapping keeps
# the seeding stable even if we re-run the command.
IMAGES = {
    'bodybuilding_main':   'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=1200&q=80',
    'bodybuilding_alt':    'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=1200&q=80',
    'crossfit_main':       'https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?auto=format&fit=crop&w=1200&q=80',
    'crossfit_alt':        'https://images.unsplash.com/photo-1599058917212-d750089bc07e?auto=format&fit=crop&w=1200&q=80',
    'strength_main':       'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=1200&q=80',
    'strength_alt':        'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?auto=format&fit=crop&w=1200&q=80',
    'endurance_main':      'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&w=1200&q=80',
    'endurance_alt':       'https://images.unsplash.com/photo-1483721310020-03333e577078?auto=format&fit=crop&w=1200&q=80',
    'athletics_main':      'https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=1200&q=80',
    'athletics_alt':       'https://images.unsplash.com/photo-1546483875-ad9014c88eba?auto=format&fit=crop&w=1200&q=80',
    'mindset_main':        'https://images.unsplash.com/photo-1508215302842-3a8252e2bbe9?auto=format&fit=crop&w=1200&q=80',
    'mindset_alt':         'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1200&q=80',
    'boxing_main':         'https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?auto=format&fit=crop&w=1200&q=80',
    'boxing_alt':          'https://images.unsplash.com/photo-1521806466606-9c482e0536f0?auto=format&fit=crop&w=1200&q=80',
    'marathon_main':       'https://images.unsplash.com/photo-1581889470536-467bdbe30cd0?auto=format&fit=crop&w=1200&q=80',
    'marathon_alt':        'https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?auto=format&fit=crop&w=1200&q=80',
    'cold_main':           'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=1200&q=80',
    'cold_alt':            'https://images.unsplash.com/photo-1519315901367-f34ff9152227?auto=format&fit=crop&w=1200&q=80',
    'basketball_main':     'https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=1200&q=80',
    'basketball_alt':      'https://images.unsplash.com/photo-1504450758481-7338eba7524a?auto=format&fit=crop&w=1200&q=80',
    'swim_main':           'https://images.unsplash.com/photo-1530549387789-4c1017266634?auto=format&fit=crop&w=1200&q=80',
    'swim_alt':            'https://images.unsplash.com/photo-1560090995-01632a28895b?auto=format&fit=crop&w=1200&q=80',
    'tennis_main':         'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=1200&q=80',
    'tennis_alt':          'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?auto=format&fit=crop&w=1200&q=80',
}


# Real-world fitness icons. Bios, achievements, and tips are paraphrased from
# publicly available sources (Wikipedia, official bios, published interviews).
# Photos intentionally use category-themed Unsplash images rather than
# portrait photos of these individuals.
ICONS = [
    # ---------------- BODYBUILDING ----------------
    {
        'slug': 'arnold-schwarzenegger',
        'name': 'Arnold Schwarzenegger',
        'nickname': 'The Austrian Oak',
        'category_slug': 'bodybuilding',
        'nationality': 'Austrian-American',
        'born': 'July 30, 1947',
        'discipline': 'Bodybuilding, Actor, Politician',
        'short_bio': 'Seven-time Mr. Olympia who turned bodybuilding into a global phenomenon, then conquered Hollywood and Sacramento.',
        'bio': (
            "Arnold began lifting weights at 15 in his native Austria, won Mr. Universe at 20, "
            "and went on to claim seven Mr. Olympia titles between 1970 and 1980 — six of them "
            "consecutive. The 1977 documentary Pumping Iron made him a global icon and launched a "
            "Hollywood career spanning The Terminator, Predator, and Total Recall. He served as the "
            "38th Governor of California from 2003 to 2011, and continues to host the Arnold Sports "
            "Festival — the second-largest multi-sport event on the planet."
        ),
        'image_url': IMAGES['bodybuilding_main'],
        'portrait_url': IMAGES['bodybuilding_alt'],
        'achievements': (
            "7× Mr. Olympia (1970–1975, 1980)\n"
            "5× Mr. Universe\n"
            "Star of The Terminator, Predator, Total Recall\n"
            "38th Governor of California (2003–2011)\n"
            "Founder of the Arnold Sports Festival"
        ),
        'training_tips': (
            "Visualize every rep before you touch the weight — your mind contracts the muscle first.\n"
            "Train the weak links obsessively; the chain is only as strong as its weakest part.\n"
            "Don't count reps — make reps count. Quality beats quantity every session.\n"
            "Recovery is when you grow. Sleep is non-negotiable."
        ),
        'signature_quote': 'Strength does not come from winning. Your struggles develop your strengths. When you go through hardships and decide not to surrender, that is strength.',
        'video_url': 'https://www.youtube.com/watch?v=pDvioP19PO8',
        'video_title': "Arnold's Blueprint: Train Like a Champion",
        'is_featured': True,
        'display_order': 1,
    },
    {
        'slug': 'ronnie-coleman',
        'name': 'Ronnie Coleman',
        'nickname': 'The King',
        'category_slug': 'bodybuilding',
        'nationality': 'American',
        'born': 'May 13, 1964',
        'discipline': 'Bodybuilding',
        'short_bio': 'Eight-time Mr. Olympia who built the most freaky physique in history while working a full-time police shift.',
        'bio': (
            "A former officer with the Arlington, Texas Police Department, Ronnie trained relentlessly "
            "and went on to win eight consecutive Mr. Olympia titles from 1998 to 2005 — tying the all-time "
            "record. Known for super-heavy training and the now-iconic catchphrases 'Yeah buddy!' and "
            "'Light weight, baby!', he later required multiple hip and back surgeries but continues to "
            "inspire with a positive, grateful spirit."
        ),
        'image_url': IMAGES['bodybuilding_main'],
        'portrait_url': IMAGES['bodybuilding_alt'],
        'achievements': (
            "8× Mr. Olympia (1998–2005)\n"
            "26× IFBB pro title wins\n"
            "Trained while serving as a police officer for years\n"
            "Two-time winner of the Arnold Classic"
        ),
        'training_tips': (
            "Everybody wants to be a bodybuilder, but don't nobody want to lift no heavy-ass weights.\n"
            "Train each body part twice a week — once heavy, once with volume.\n"
            "Form is everything — ego lifting breaks bodies.\n"
            "The mind quits before the body. Push past that voice."
        ),
        'signature_quote': "The only place where success comes before work is in the dictionary.",
        'video_url': 'https://www.youtube.com/watch?v=I3i7Ukc9Mow',
        'video_title': "Ronnie Coleman: The King Speaks",
        'is_featured': True,
        'display_order': 2,
    },
    {
        'slug': 'chris-bumstead',
        'name': 'Chris Bumstead',
        'nickname': 'CBum',
        'category_slug': 'bodybuilding',
        'nationality': 'Canadian',
        'born': 'February 2, 1995',
        'discipline': 'Classic Physique Bodybuilding',
        'short_bio': 'Six-time Classic Physique Olympia champion who brought aesthetic bodybuilding back to the mainstream.',
        'bio': (
            "Bumstead turned pro in 2016, finished second at the Olympia in 2017 and 2018, then began a "
            "record-setting six-year run as Classic Physique king from 2019 to 2024. His balanced, "
            "Golden-Era-inspired physique attracted a new generation of fans and made him one of the "
            "most-followed athletes in the sport. He retired after his sixth title, shifting focus to "
            "his wellness brand and content creation."
        ),
        'image_url': IMAGES['bodybuilding_main'],
        'portrait_url': IMAGES['bodybuilding_alt'],
        'achievements': (
            "6× Mr. Olympia Classic Physique (2019–2024)\n"
            "3× IFBB Toronto Pro champion\n"
            "Most-followed bodybuilder on social media at retirement"
        ),
        'training_tips': (
            "Symmetry and proportion beat raw mass in Classic Physique.\n"
            "Mind-muscle connection matters more than the numbers on the bar.\n"
            "Build a back that matches your front — too many athletes skip pull work.\n"
            "Stay consistent year-round; peaks are built on steady habits."
        ),
        'signature_quote': "I hope my legacy is less about my physique and more about how I did it — who I became along the way.",
        'video_url': 'https://www.youtube.com/watch?v=2LfL9i7I_rs',
        'video_title': "CBum's Winning Mindset",
        'display_order': 3,
    },

    # ---------------- CROSSFIT ----------------
    {
        'slug': 'rich-froning',
        'name': 'Rich Froning Jr.',
        'nickname': 'The Fittest Man in History',
        'category_slug': 'crossfit',
        'nationality': 'American',
        'born': 'July 21, 1987',
        'discipline': 'CrossFit',
        'short_bio': 'Four-time Fittest Man on Earth who turned CrossFit dominance into a career as a coach and affiliate owner.',
        'bio': (
            "Froning burst onto the CrossFit scene in 2010, finished second at the Games, then won the "
            "individual title four consecutive times from 2011 to 2014 — a feat unmatched at the time. "
            "After stepping back from individual competition, he captained CrossFit Mayhem Freedom to six "
            "Affiliate Cup titles, bringing his total Games championships to 11. He owns Mayhem "
            "Athletics, a thriving training facility in Cookeville, Tennessee."
        ),
        'image_url': IMAGES['crossfit_main'],
        'portrait_url': IMAGES['crossfit_alt'],
        'achievements': (
            "4× CrossFit Games individual champion (2011–2014)\n"
            "7× CrossFit Games Affiliate Cup champion\n"
            "3× worldwide Open champion (2012–2014)\n"
            "Career prize money over $1 million"
        ),
        'training_tips': (
            "Train the lifts that scare you most — they're the ones that will win you the day.\n"
            "Conditioning is built through hard, repeatable intervals, not random workouts.\n"
            "Surround yourself with people chasing excellence; mediocrity is contagious.\n"
            "Faith and family first. Competition is just a job."
        ),
        'signature_quote': "I want to be the guy who works harder than everyone else, every day, in every way.",
        'video_url': 'https://www.youtube.com/watch?v=mRG9JvKHrGw',
        'video_title': "Rich Froning: Driven",
        'is_featured': True,
        'display_order': 4,
    },
    {
        'slug': 'mat-fraser',
        'name': 'Mat Fraser',
        'nickname': 'The Fittest on Earth',
        'category_slug': 'crossfit',
        'nationality': 'American-Scottish',
        'born': 'May 25, 1989',
        'discipline': 'CrossFit',
        'short_bio': 'Five-time Fittest Man on Earth who retired as the winningest male CrossFit athlete of all time.',
        'bio': (
            "Son of Canadian-born British parents and a former Olympic-style weightlifting hopeful, Mat "
            "transitioned to CrossFit after injuries cut his Olympic path short. He won five consecutive "
            "CrossFit Games titles from 2016 to 2020, breaking Froning's record and retiring at the top. "
            "Known for ruthless consistency and a quiet, almost boring training discipline, he now runs "
            "his own training programs and content platforms."
        ),
        'image_url': IMAGES['crossfit_main'],
        'portrait_url': IMAGES['crossfit_alt'],
        'achievements': (
            "5× CrossFit Games individual champion (2016–2020)\n"
            "First man to win five CrossFit Games titles\n"
            "3-time CrossFit Invitational champion\n"
            "Former youth national weightlifting champion"
        ),
        'training_tips': (
            "Be consistent. Boring beats exciting when it comes to long-term progress.\n"
            "Train your weaknesses on off days, your strengths on the platform.\n"
            "The magic is in the basics: lift heavy, run far, move well.\n"
            "Compete with yourself first. The leaderboard takes care of itself."
        ),
        'signature_quote': "There are no shortcuts. You either pay the price in the gym, or you pay it on the scoreboard.",
        'display_order': 5,
    },

    # ---------------- STRENGTH SPORTS ----------------
    {
        'slug': 'eddie-hall',
        'name': 'Eddie Hall',
        'nickname': 'The Beast',
        'category_slug': 'strength',
        'nationality': 'British',
        'born': 'January 15, 1988',
        'discipline': 'Strongman',
        'short_bio': "World's Strongest Man 2017 and the first man to deadlift 500 kg in competition.",
        'bio': (
            "Hall became the first person in history to deadlift 500 kilograms (1,102 pounds) at the "
            "2016 World's Ultimate Strongman event, a feat that left him with a burst blood vessel in his "
            "head and required immediate medical attention. He went on to win the 2017 World's Strongest "
            "Man title and has since transitioned to boxing exhibition matches and content creation, "
            "famously facing Hafthor Bjornsson in the 'Heaviest Boxing Match in History'."
        ),
        'image_url': IMAGES['strength_main'],
        'portrait_url': IMAGES['strength_alt'],
        'achievements': (
            "World's Strongest Man 2017\n"
            "First man to deadlift 500 kg in competition (2016)\n"
            "Arnold Strongman Classic podium finisher\n"
            "Boxed Hafthor Bjornsson in a record-setting charity match"
        ),
        'training_tips': (
            "Train your mind first — the lift begins before the bar moves.\n"
            "Eat big to lift big, but track your numbers obsessively.\n"
            "Recovery is where champions are made. Sleep 9+ hours when peaking.\n"
            "Don't lift to prove something to others; lift because you promised yourself."
        ),
        'signature_quote': "Be the hardest worker in the room. When I started winning, I realised the 500 kg wasn't about the weight — it was about all the mornings I didn't skip.",
        'video_url': 'https://www.youtube.com/watch?v=o3oe0JMXhLQ',
        'video_title': "Eddie Hall: The 500 kg Deadlift",
        'is_featured': True,
        'display_order': 6,
    },
    {
        'slug': 'hafthor-bjornsson',
        'name': 'Hafþór Björnsson',
        'nickname': 'The Mountain',
        'category_slug': 'strength',
        'nationality': 'Icelandic',
        'born': 'November 26, 1988',
        'discipline': 'Strongman, Actor',
        'short_bio': "World's Strongest Man 2018, three-time winner of the Arnold Strongman Classic, and 'The Mountain' from Game of Thrones.",
        'bio': (
            "Standing 6'9\" and weighing over 200 kg in competition, Hafþór is the most recognisable "
            "strongman of his generation. He won Europe's Strongest Man six times, the Arnold "
            "Strongman Classic three times, and finally captured the World's Strongest Man title in "
            "2018. He played Ser Gregor 'The Mountain' Clegane on HBO's Game of Thrones from 2014 to "
            "2019 and has since moved into acting and motivational speaking."
        ),
        'image_url': IMAGES['strength_main'],
        'portrait_url': IMAGES['strength_alt'],
        'achievements': (
            "World's Strongest Man 2018\n"
            "3× Arnold Strongman Classic champion\n"
            "6× Europe's Strongest Man\n"
            "501 kg deadlift (officially recorded)\n"
            "Portrayed The Mountain on Game of Thrones"
        ),
        'training_tips': (
            "Show up. Even on days you don't feel it, the basics still get done.\n"
            "Strongman work transfers to every area of life — you learn to bend, not break.\n"
            "Fuel is a tool. Eat with purpose, train with intent.\n"
            "Lift with people stronger than you. Their standards lift your ceiling."
        ),
        'signature_quote': "You have to be hungry. Hungry to learn, hungry to grow, hungry to be the best.",
        'display_order': 7,
    },

    # ---------------- ENDURANCE ----------------
    {
        'slug': 'usain-bolt',
        'name': 'Usain Bolt',
        'nickname': 'Lightning Bolt',
        'category_slug': 'athletics',
        'nationality': 'Jamaican',
        'born': 'August 21, 1986',
        'discipline': 'Track & Field',
        'short_bio': 'Eight-time Olympic gold medallist and the fastest human ever recorded in the 100 m and 200 m.',
        'bio': (
            "Bolt burst onto the world stage at the 2008 Beijing Olympics, winning gold in the 100 m, "
            "200 m, and 4×100 m — all in world-record times. He defended all three titles at London 2012 "
            "and added another 4×100 m gold at Rio 2016, finishing his career with eight Olympic golds. "
            "His 100 m world record of 9.58 seconds, set in Berlin in 2009, still stands. He managed "
            "scoliosis throughout his career with the help of coach Glen Mills and a relentless daily "
            "discipline."
        ),
        'image_url': IMAGES['athletics_main'],
        'portrait_url': IMAGES['athletics_alt'],
        'achievements': (
            "8× Olympic gold medallist\n"
            "11× World Championship gold\n"
            "World records: 9.58 s (100 m), 19.19 s (200 m)\n"
            "First man to win 100 m/200 m at three consecutive Olympics"
        ),
        'training_tips': (
            "I don't think limits. The body will do what the mind allows.\n"
            "Train smart before you train hard — technique wins races.\n"
            "Have fun with what you do. People forget that joy is a force multiplier.\n"
            "Recovery makes champions. Sleep, fuel, and stretch every single day."
        ),
        'signature_quote': "Easy is not an option. No days off. Never quit. Be fearless.",
        'video_url': 'https://www.youtube.com/watch?v=3nbKf4iD_Bk',
        'video_title': "Usain Bolt: Fastest Man Alive",
        'is_featured': True,
        'display_order': 8,
    },
    {
        'slug': 'kelly-slater',
        'name': 'Kelly Slater',
        'nickname': 'The King',
        'category_slug': 'endurance',
        'nationality': 'American',
        'born': 'February 11, 1972',
        'discipline': 'Surfing',
        'short_bio': '11-time World Surf League champion — the most dominant surfer in the history of the sport.',
        'bio': (
            "Slater became the youngest ASP world champion in 1992 at age 20, then retired, came back, "
            "and won a record 11 world titles — the most in any individual sport. He combined elite "
            "athleticism, longevity, and an almost meditative relationship with the ocean. He later "
            "founded the Kelly Slater Wave Company, building the world's most advanced artificial surf "
            "pools."
        ),
        'image_url': IMAGES['endurance_main'],
        'portrait_url': IMAGES['endurance_alt'],
        'achievements': (
            "11× World Surf League champion (1992, 1994–1998, 2005–2006, 2008, 2010–2011)\n"
            "Only surfer to win the Eddie Aikau Big Wave Invitational\n"
            "Founder of the Kelly Slater Wave Company"
        ),
        'training_tips': (
            "Be present. The ocean, the wave, the moment — nothing else exists.\n"
            "Train for what the day demands, not what yesterday did.\n"
            "Technique and breath control save you when strength runs out.\n"
            "Longevity is the ultimate flex. Stay in the sport by respecting your body."
        ),
        'signature_quote': "The best surfer in the water is the one having the most fun.",
        'display_order': 9,
    },

    # ---------------- ATHLETICS & GYMNASTICS ----------------
    {
        'slug': 'simone-biles',
        'name': 'Simone Biles',
        'nickname': 'GOAT',
        'category_slug': 'athletics',
        'nationality': 'American',
        'born': 'March 14, 1997',
        'discipline': 'Artistic Gymnastics',
        'short_bio': 'The most decorated gymnast in history, with 11 Olympic medals, 30 World Championship medals, and 4 eponymous skills.',
        'bio': (
            "Biles is the most decorated gymnast of all time, with 11 Olympic medals and 30 World "
            "Championship medals. Four skills across floor, beam, and vault carry her name in the code "
            "of points. After withdrawing from most events at Tokyo 2020 to protect her mental health, "
            "she returned in spectacular form at Paris 2024, winning team, all-around, and vault gold. "
            "She is the only gymnast to win two Olympic all-around titles in non-consecutive Games."
        ),
        'image_url': IMAGES['athletics_main'],
        'portrait_url': IMAGES['athletics_alt'],
        'achievements': (
            "11 Olympic medals (7 gold)\n"
            "30 World Championship medals (23 gold)\n"
            "Most World all-around titles in history (6)\n"
            "Presidential Medal of Freedom (2022)\n"
            "4 eponymous gymnastics skills"
        ),
        'training_tips': (
            "Mental health is part of training. Rest is part of the work.\n"
            "Repetition is the mother of mastery — do the basics a thousand times.\n"
            "Trust your coaches, but trust your own voice too.\n"
            "Show up even on the days you don't believe in yourself. That's the day it matters most."
        ),
        'signature_quote': "I'd rather regret the risks that didn't work out than the chances I didn't take at all.",
        'video_url': 'https://www.youtube.com/watch?v=A1LB4sVFKsk',
        'video_title': "Simone Biles: The Goat Tour",
        'is_featured': True,
        'display_order': 10,
    },
    {
        'slug': 'michael-jordan',
        'name': 'Michael Jordan',
        'nickname': 'His Airness',
        'category_slug': 'athletics',
        'nationality': 'American',
        'born': 'February 17, 1963',
        'discipline': 'Basketball',
        'short_bio': 'Six-time NBA champion, five-time MVP, and the player who turned competitive greatness into a way of life.',
        'bio': (
            "Jordan's resume is unmatched: six NBA championships with the Chicago Bulls, six Finals "
            "MVPs, five regular-season MVPs, 14 All-Star selections, and 10 scoring titles. Off the court, "
            "his Air Jordan brand turned him into a global billionaire and a fashion icon. What set him "
            "apart, according to his longtime trainer Tim Grover, was his ability to train early, train "
            "after losses, and never accept that the work was done."
        ),
        'image_url': IMAGES['athletics_main'],
        'portrait_url': IMAGES['athletics_alt'],
        'achievements': (
            "6× NBA champion\n"
            "6× NBA Finals MVP\n"
            "5× NBA MVP\n"
            "14× NBA All-Star\n"
            "Two Olympic gold medals (1984, 1992)\n"
            "Inducted into the Basketball Hall of Fame in 2009"
        ),
        'training_tips': (
            "Some people want it to happen, some wish it would happen. I make it happen.\n"
            "After every game, ask: 6 am? 7 am? Be in the gym before the sun.\n"
            "Talent wins games, but work ethic and intelligence win championships.\n"
            "Failure is the price of growth. Lose, learn, come back."
        ),
        'signature_quote': "I've missed more than 9,000 shots. I've lost almost 300 games. I've failed over and over and over again in my life. And that is why I succeed.",
        'video_url': 'https://www.youtube.com/watch?v=ko3Rofg8Hmw',
        'video_title': "Michael Jordan: The Last Dance (Trailer)",
        'display_order': 11,
    },

    # ---------------- MINDSET & DISCIPLINE ----------------
    {
        'slug': 'david-goggins',
        'name': 'David Goggins',
        'nickname': 'The Toughest Man Alive',
        'category_slug': 'mindset',
        'nationality': 'American',
        'born': 'February 17, 1975',
        'discipline': 'Ultra-Endurance, Navy SEAL',
        'short_bio': 'Retired Navy SEAL, ultramarathon runner, and author who turned childhood trauma into the toughest mindset on the planet.',
        'bio': (
            "Goggins went from depressed exterminator to elite Navy SEAL after bombing his ASVAB and "
            "deciding to 'callous his mind.' He's completed more than 70 ultra-marathons, holds the "
            "former Guinness record for most pull-ups in 17 hours (4,030), and is the only person to "
            "complete elite training as a Navy SEAL, Army Ranger, and Air Force Tactical Air Control "
            "Party member. His book Can't Hurt Me spent years on bestseller lists."
        ),
        'image_url': IMAGES['mindset_main'],
        'portrait_url': IMAGES['mindset_alt'],
        'achievements': (
            "Retired Navy SEAL\n"
            "70+ ultramarathons completed\n"
            "Former Guinness World Record holder: 4,030 pull-ups in 17 hours\n"
            "Author of Can't Hurt Me (2018)\n"
            "Only person to complete SEAL, Ranger, and Air Force TAC-P training"
        ),
        'training_tips': (
            "We don't rise to the level of our expectations — we fall to the level of our training.\n"
            "Schedule suffering into your day. Make discomfort your default.\n"
            "You are living at about 40% of your capability. The rest is locked behind discipline.\n"
            "Don't stop when you're tired. Stop when you're done."
        ),
        'signature_quote': "Greatness pulls mediocrity into the mud. Get out there and get after it.",
        'video_url': 'https://www.youtube.com/watch?v=krEbhAB1e_k',
        'video_title': "David Goggins: Can't Hurt Me",
        'is_featured': True,
        'display_order': 12,
    },
    {
        'slug': 'jocko-willink',
        'name': 'Jocko Willink',
        'nickname': 'Discipline Equals Freedom',
        'category_slug': 'mindset',
        'nationality': 'American',
        'born': 'September 8, 1971',
        'discipline': 'Leadership, Jiu-Jitsu, Fitness',
        'short_bio': "Retired Navy SEAL commander who turned battlefield leadership into a fitness and discipline philosophy.",
        'bio': (
            "Willink spent 20 years in the SEAL Teams, leading SEAL Task Unit Bruiser during the Battle "
            "of Ramadi — one of the most intense urban combat operations of the Iraq War. After retiring, "
            "he co-founded Echelon Front (leadership consulting) and opened Victory MMA & Fitness in San "
            "Diego. His books Extreme Ownership and Discipline Equals Freedom have become foundational "
            "texts for leaders and athletes."
        ),
        'image_url': IMAGES['mindset_main'],
        'portrait_url': IMAGES['mindset_alt'],
        'achievements': (
            "Retired Navy SEAL Commander\n"
            "Bronze Star and Silver Star recipient\n"
            "Co-author of #1 NYT bestseller Extreme Ownership\n"
            "Author of Discipline Equals Freedom: Field Manual\n"
            "Owner of Victory MMA & Fitness, San Diego"
        ),
        'training_tips': (
            "Discipline equals freedom. The more disciplined you are, the more free you become.\n"
            "Get up early. The world is less crowded in the morning hours.\n"
            "Train jiu-jitsu — it teaches you to control yourself before you try to control others.\n"
            "Don't wait for motivation. Just show up and do the work."
        ),
        'signature_quote': "Discipline equals freedom. It might sound counterintuitive, but the more disciplined you are, the more free you become.",
        'video_url': 'https://www.youtube.com/watch?v=IdT1BhrSf3U',
        'video_title': "Jocko Willink: Discipline Equals Freedom",
        'display_order': 13,
    },
]


# ---------------- NEW ICONS: ADDITIONAL PILLARS ----------------
# Adding legendary figures across categories to provide a comprehensive
# library of fitness wisdom and inspiration.
NEW_ICONS = [
{
    'slug': 'lee-haney',
    'name': 'Lee Haney',
    'nickname': 'The Total Package',
    'category_slug': 'bodybuilding',
    'nationality': 'American',
    'born': 'November 11, 1959',
    'discipline': 'Bodybuilding, Ministry',
    'short_bio': 'Eight-time Mr. Olympia who tied Arnold\'s record and proved that balance — physique, faith, and family — creates champions.',
    'bio': (
        "Lee Haney lifted his first weights at age 11 after his older brother gave him a set of "
        "dumbbells for his birthday. By 1982 the 6'2\" Georgian had turned pro after winning the "
        "National Championships. He went on to win eight consecutive Mr. Olympia titles from 1984 "
        "to 1991, tying Arnold Schwarzenegger's all-time record at the time. Known for his "
        "incredible lat spread and perfectly proportioned V-taper, Haney retired at the absolute "
        "peak and never competed again. He later became an ordained minister, founded the "
        "Lee Haney Personal Training Center, and served as Executive Director of the "
        "President's Council on Physical Fitness under President George W. Bush."
    ),
    'image_url': IMAGES['bodybuilding_main'],
    'portrait_url': IMAGES['bodybuilding_alt'],
    'achievements': (
        "8× Mr. Olympia (1984–1991)\n"
        "IFBB Hall of Fame inductee (2004)\n"
        "Executive Director, President's Council on Physical Fitness (2002–2006)\n"
        "24 career IFBB pro victories\n"
        "Youngest Mr. Olympia winner in history at the time (age 25)"
    ),
    'training_tips': (
        "Train to stimulate, not to annihilate. The body grows during recovery, not during the workout.\n"
        "Proportion beats mass every time — build the whole picture, not just one angle.\n"
        "Exercise is a celebration of what your body can do, not a punishment for what you ate.\n"
        "Set goals that scare you a little, then show up every day until they don't."
    ),
    'signature_quote': "If it is to be, it is up to me. The only person who can truly hold you back is the person you see in the mirror.",
    'video_url': 'https://www.youtube.com/watch?v=7YOEjAzPSmI',
    'video_title': "Lee Haney: The Total Package",
    'is_featured': True,
    'display_order': 14,
},
{
    'slug': 'dorian-yates',
    'name': 'Dorian Yates',
    'nickname': 'The Shadow',
    'category_slug': 'bodybuilding',
    'nationality': 'British',
    'born': 'April 19, 1962',
    'discipline': 'Bodybuilding',
    'short_bio': 'Six-time Mr. Olympia who brought blood-and-guts high-intensity training to bodybuilding and changed the sport forever.',
    'bio': (
        "Dorian Yates grew up in a rough Birmingham council estate and discovered weight training "
        "while serving a youth detention sentence. The discipline transformed his life. He turned "
        "pro in 1990 and won his first Mr. Olympia in 1992, then dominated the sport with six "
        "consecutive titles until a severe triceps tear forced his retirement in 1997. His "
        "high-intensity 'Blood and Guts' training protocol — fewer sets, maximal intensity, "
        "training to absolute failure — became one of the most influential training methodologies "
        "in the sport's history."
    ),
    'image_url': IMAGES['bodybuilding_main'],
    'portrait_url': IMAGES['bodybuilding_alt'],
    'achievements': (
        "6× Mr. Olympia (1992–1997)\n"
        "IFBB Hall of Fame inductee\n"
        "Pioneer of High-Intensity Training methodology\n"
        "First British Mr. Olympia in history\n"
        "Created the Yates Concept: 1–2 working sets to absolute failure"
    ),
    'training_tips': (
        "One all-out set to failure beats three half-hearted sets every time.\n"
        "The logbook doesn't lie. Write down every set, every rep, every pound.\n"
        "Intensity is the key variable — progressive overload is not optional.\n"
        "Trust the process. Results take time, but they compound like interest."
    ),
    'signature_quote': "The journey is the reward. Becoming the best version of yourself is the whole point — the titles are just confirmation.",
    'video_url': 'https://www.youtube.com/watch?v=kA_y5eNYmTE',
    'video_title': "Dorian Yates: Blood and Guts",
    'display_order': 15,
},
{
    'slug': 'phil-heath',
    'name': 'Phil Heath',
    'nickname': 'The Gift',
    'category_slug': 'bodybuilding',
    'nationality': 'American',
    'born': 'December 18, 1979',
    'discipline': 'Bodybuilding',
    'short_bio': 'Seven-time Mr. Olympia who combined NFL-caliber genetics with relentless conditioning to dominate bodybuilding for nearly a decade.',
    'bio': (
        "Phil Heath started his athletic career as a college basketball player at the University "
        "of Denver before switching to bodybuilding in his early twenties. After winning the "
        "USA Championships in 2005 and the Mr. Olympia debut in 2008, he went on to win seven "
        "consecutive Sandow trophies from 2011 to 2017 — tying Arnold Schwarzenegger's total. "
        "Known for his near-perfect symmetry, tiny waist, and massive shoulders, Heath brought "
        "a new standard of aesthetic mass to the open division and remains one of the most "
        "physically gifted bodybuilders the sport has ever seen."
    ),
    'image_url': IMAGES['bodybuilding_main'],
    'portrait_url': IMAGES['bodybuilding_alt'],
    'achievements': (
        "7× Mr. Olympia (2011–2017)\n"
        "10 Arnold Classic Europe wins\n"
        "IFBB Hall of Fame inductee (2024)\n"
        "Only the fifth man in history to win 7+ Olympia titles\n"
        "Started bodybuilding after a college basketball career"
    ),
    'training_tips': (
        "Cardio is not optional. A great physique is revealed in the diet and cardio, not just the weights.\n"
        "Don't skip the details — calves, forearms, rear delts. Champions are built from all angles.\n"
        "Surround yourself with people who tell you the truth, not what you want to hear.\n"
        "Rest is when the magic happens. Growth happens outside the gym."
    ),
    'signature_quote': "Believe in yourself, even when nobody else does. That belief is the foundation that everything else is built on.",
    'video_url': 'https://www.youtube.com/watch?v=Iga4TSqUG7s',
    'video_title': "Phil Heath: The Gift",
    'display_order': 16,
},
{
    'slug': 'tia-clair-toomey',
    'name': 'Tia-Clair Toomey',
    'nickname': 'Tia',
    'category_slug': 'crossfit',
    'nationality': 'Australian',
    'born': 'July 23, 1993',
    'discipline': 'CrossFit, Weightlifting',
    'short_bio': 'Six-time CrossFit Games champion — the most decorated female athlete in CrossFit history — and Olympic weightlifter.',
    'bio': (
        "Tia-Clair Toomey is the winningest athlete in CrossFit Games history. After placing 15th "
        "in her 2015 debut, she finished runner-up in 2016, then won six straight individual "
        "titles from 2017 to 2022 — more than any other woman in the sport. She also competed in "
        "weightlifting at the 2018 Commonwealth Games, winning a silver medal, and narrowly missed "
        "making the Australian Olympic team for Tokyo 2020. Her combination of engine, strength, "
        "and technical skill across all domains set a new standard in the sport."
    ),
    'image_url': IMAGES['crossfit_main'],
    'portrait_url': IMAGES['crossfit_alt'],
    'achievements': (
        "6× CrossFit Games individual champion (2017–2022)\n"
        "Commonwealth Games silver medalist (Weightlifting, 2018)\n"
        "Most CrossFit Games event wins of any female athlete\n"
        "Only woman to win six consecutive CrossFit Games titles"
    ),
    'training_tips': (
        "Consistency beats intensity nine times out of ten.\n"
        "Train your weaknesses until they become your strengths.\n"
        "The mind is the first thing to give up. Train it to keep going.\n"
        "Recovery days are not days off — they are investment days."
    ),
    'signature_quote': "The Fittest on Earth isn't just about being fast and strong — it's about being prepared for anything, at any time.",
    'video_url': 'https://www.youtube.com/watch?v=7C_Q4V4Cqfo',
    'video_title': "Tia-Clair: The Making of a Champion",
    'is_featured': True,
    'display_order': 17,
},
{
    'slug': 'brian-shaw',
    'name': 'Brian Shaw',
    'nickname': 'The Giant',
    'category_slug': 'strength',
    'nationality': 'American',
    'born': 'February 26, 1982',
    'discipline': 'Strongman',
    'short_bio': 'Four-time World\'s Strongest Man, the tallest WSM champion in history at 6\'8", and a perennial icon in strength sports.',
    'bio': (
        "Brian Shaw grew up in rural Colorado and initially focused on basketball before finding "
        "his calling in strongman. At 6'8\" and over 400 lbs in competition shape, he became the "
        "tallest man ever to win the World's Strongest Man title — taking the crown four times "
        "(2011, 2013, 2015, 2016). His unmatched reach on deadlift variations and ability to "
        "excel across all five WSM disciplines made him a model of well-rounded strength. Shaw "
        "retired from competition in 2020 and now runs a successful YouTube channel, training "
        "facility, and the Shaw Classic — one of the biggest prize-purse strongman competitions "
        "in the world."
    ),
    'image_url': IMAGES['strength_main'],
    'portrait_url': IMAGES['strength_alt'],
    'achievements': (
        "4× World's Strongest Man (2011, 2013, 2015, 2016)\n"
        "8× WSM podium finishes\n"
        "2× Arnold Strongman Classic champion\n"
        "5× America's Strongest Man\n"
        "Founder of the Shaw Classic strongman competition"
    ),
    'training_tips': (
        "Consistency beats intensity over the long haul — train smart so you can train for decades.\n"
        "Work on your weaknesses until they become average, then work on them more.\n"
        "Strongman is about being ready for anything — never specialize too early.\n"
        "The strongest muscle in your body is your mind. Train it every day."
    ),
    'signature_quote': "The goal is not to be better than anyone else — it's to be better than you were yesterday. Stack those days up, and you'll be unstoppable.",
    'video_url': 'https://www.youtube.com/watch?v=9jfCQ1qIRRE',
    'video_title': "Brian Shaw: The Giant's Journey",
    'is_featured': True,
    'display_order': 18,
},
{
    'slug': 'zydrunas-savickas',
    'name': 'Žydrūnas Savickas',
    'nickname': 'Big Z',
    'category_slug': 'strength',
    'nationality': 'Lithuanian',
    'born': 'July 15, 1975',
    'discipline': 'Strongman',
    'short_bio': 'Four-time World\'s Strongest Man and eight-time Arnold Strongman Classic champion — the most dominant strongman of the 2000s.',
    'bio': (
        "Žydrūnas Savickas — universally known as 'Big Z' — is considered by many the greatest "
        "all-around strongman of all time. He won the World's Strongest Man title four times "
        "(2009, 2010, 2012, 2014) and dominated the Arnold Strongman Classic with an unmatched "
        "eight titles between 2003 and 2014. Known for his incredible pressing power, he set "
        "world records in the log lift, stone lift, and super yoke. After retiring from "
        "competition, Big Z opened his own training centre and remains an ambassador for "
        "strength sports worldwide."
    ),
    'image_url': IMAGES['strength_main'],
    'portrait_url': IMAGES['strength_alt'],
    'achievements': (
        "4× World's Strongest Man (2009, 2010, 2012, 2014)\n"
        "8× Arnold Strongman Classic champion (2003–2011, 2014)\n"
        "Multiple world records in log lift, stone lift, and super yoke\n"
        "Strongest Man of the Decade (2010s)"
    ),
    'training_tips': (
        "Technique first — you cannot out-lift poor form with more muscle.\n"
        "Patience is the strongest attribute of any athlete. Everything takes time.\n"
        "Recovery and sleep are as important as the heaviest session.\n"
        "Train with precision, not ego. The bar doesn't care how mad you are."
    ),
    'signature_quote': "Strength is not just about what you can lift — it's about what you can carry. Carry your family, your team, your dreams.",
    'video_url': 'https://www.youtube.com/watch?v=5rGPNqKxw2E',
    'video_title': "Big Z: The Lithuanian Legend",
    'display_order': 19,
},
{
    'slug': 'eliud-kipchoge',
    'name': 'Eliud Kipchoge',
    'nickname': 'The Philosopher of Running',
    'category_slug': 'endurance',
    'nationality': 'Kenyan',
    'born': 'November 5, 1984',
    'discipline': 'Marathon',
    'short_bio': 'Olympic champion, world record holder, and the only person in history to run a marathon in under two hours.',
    'bio': (
        "Eliud Kipchoge rose from a rural Kenyan childhood to become the greatest marathoner in "
        "history. He won Olympic gold in the marathon at Rio 2016 and Tokyo 2020, set the "
        "official world record (2:01:09) in Berlin 2022, and shattered the mythical sub-two-hour "
        "barrier in the INEOS 1:59 Challenge in Vienna (1:59:40) — a feat widely compared to the "
        "first moon landing. Known for his serene, philosophical demeanor, Kipchoge believes "
        "that 'no human is limited' and trains twice daily at the legendary Kaptagat camp in "
        "Kenya's Rift Valley."
    ),
    'image_url': IMAGES['marathon_main'],
    'portrait_url': IMAGES['marathon_alt'],
    'achievements': (
        "Olympic marathon gold (2016, 2020)\n"
        "Official world record: 2:01:09 (Berlin 2022)\n"
        "First human to run a marathon in under 2 hours (1:59:40, 2019)\n"
        "10 of the 20 fastest marathons in history belong to Kipchoge\n"
        "Four-time London Marathon champion"
    ),
    'training_tips': (
        "The best time to run is in the morning — discipline starts with showing up at dawn.\n"
        "Train your mind as hard as your legs. The body will follow what the head believes.\n"
        "Consistency over intensity — 200 km per week, every week, for years.\n"
        "Rest is part of training. Sleep is the ultimate recovery tool."
    ),
    'signature_quote': "No human is limited. The only limits are the ones you place on yourself in your mind.",
    'video_url': 'https://www.youtube.com/watch?v=FviqgW9GPRc',
    'video_title': "Kipchoge: The Greatest Marathoner",
    'is_featured': True,
    'display_order': 20,
},
{
    'slug': 'kobe-bryant',
    'name': 'Kobe Bryant',
    'nickname': 'The Black Mamba',
    'category_slug': 'athletics',
    'nationality': 'American',
    'born': 'August 23, 1978',
    'discipline': 'Basketball',
    'short_bio': 'Five-time NBA champion whose Mamba Mentality became a global philosophy of relentless work ethic and obsessive preparation.',
    'bio': (
        "Kobe Bryant skipped college and entered the NBA directly from Lower Merion High School "
        "in 1996. Over 20 seasons with the Los Angeles Lakers, he won five NBA championships, "
        "two Finals MVPs, the 2008 MVP award, and was an 18-time All-Star. His legendary work "
        "ethic — arriving at the gym at 4 am for pre-dawn workouts, studying film obsessively, "
        "and training through injuries — became known as 'Mamba Mentality.' After retiring as "
        "the third all-time leading scorer, he won an Academy Award for his animated short film "
        "Dear Basketball and became a mentor to the next generation of athletes."
    ),
    'image_url': IMAGES['basketball_main'],
    'portrait_url': IMAGES['basketball_alt'],
    'achievements': (
        "5× NBA champion (2000–2002, 2009–2010)\n"
        "2× NBA Finals MVP\n"
        "NBA MVP (2008)\n"
        "18× NBA All-Star\n"
        "4× All-Star Game MVP\n"
        "Academy Award winner (Dear Basketball, 2018)\n"
        "Third all-time NBA scorer at retirement"
    ),
    'training_tips': (
        "There is no substitute for hard work. Talent means nothing without preparation.\n"
        "The job is not done when you're tired — the job is done when the job is done.\n"
        "Study your craft obsessively. Film study is as important as practice.\n"
        "Embrace the grind. The discomfort is where the growth happens."
    ),
    'signature_quote': "The most important thing is to try and inspire people so that they can be great in whatever they want to do.",
    'video_url': 'https://www.youtube.com/watch?v=ysf1M6UUs9o',
    'video_title': "Kobe Bryant: Mamba Mentality",
    'is_featured': True,
    'display_order': 21,
},
{
    'slug': 'muhammad-ali',
    'name': 'Muhammad Ali',
    'nickname': 'The Greatest',
    'category_slug': 'athletics',
    'nationality': 'American',
    'born': 'January 17, 1942',
    'discipline': 'Boxing',
    'short_bio': 'Three-time world heavyweight champion and the most iconic athlete of the 20th century, who combined boxing brilliance with unshakeable principle.',
    'bio': (
        "Muhammad Ali (born Cassius Clay) shocked the world by beating Sonny Liston for the "
        "heavyweight title in 1964, then refused induction into the US Army on religious grounds, "
        "stripped of his title and banned from boxing for three prime years. He returned to "
        "regain the title in the epic 'Rumble in the Jungle' against George Foreman (1974), "
        "then defended it in the 'Thrilla in Manila' against Joe Frazier (1975). Beyond his "
        "boxing achievements, Ali stood as a symbol of courage, conviction, and global "
        "humanitarianism, lighting the Olympic torch in 1996 and receiving the Presidential "
        "Medal of Freedom in 2005."
    ),
    'image_url': IMAGES['boxing_main'],
    'portrait_url': IMAGES['boxing_alt'],
    'achievements': (
        "3× World Heavyweight Champion\n"
        "Olympic gold medalist (Light Heavyweight, 1960)\n"
        "Fighter of the Year six times\n"
        "Presidential Medal of Freedom (2005)\n"
        "Lighted the Olympic cauldron Atlanta 1996\n"
        "Sports Illustrated Sportsman of the Century"
    ),
    'training_tips': (
        "Champions are made in the gym, not in the ring. The road to the title is paved with early mornings.\n"
        "Mental toughness is stronger than any punch — train your spirit as hard as your body.\n"
        "Float like a butterfly, sting like a bee. Movement beats power when done with precision.\n"
        "Don't count the days, make the days count."
    ),
    'signature_quote': "Impossible is just a big word thrown around by small men who find it easier to live in the world they've been given than to explore the power they have to change it.",
    'video_url': 'https://www.youtube.com/watch?v=0Hk0q3clDnM',
    'video_title': "Muhammad Ali: The Greatest",
    'is_featured': True,
    'display_order': 22,
},
{
    'slug': 'wim-hof',
    'name': 'Wim Hof',
    'nickname': 'The Iceman',
    'category_slug': 'mindset',
    'nationality': 'Dutch',
    'born': 'April 20, 1959',
    'discipline': 'Cold Exposure, Breathwork, Endurance',
    'short_bio': 'Recordsman, cold-exposure pioneer, and creator of the Wim Hof Method — proving the body can be consciously controlled by the mind.',
    'bio': (
        "Wim Hof first discovered his tolerance for extreme cold while swimming in an icy canal "
        "in 1982, and since then has set over 25 world records including climbing Mount Everest "
        "in shorts, running a half marathon above the Arctic Circle barefoot, standing in a "
        "cylinder of ice for over two hours, and ascending Kilimanjaro in shorts. He developed "
        "the Wim Hof Method — a combination of breathing exercises, cold exposure, and "
        "meditation — that has been scientifically validated to modulate the autonomic nervous "
        "system and reduce inflammation. Millions of people worldwide now practice his method."
    ),
    'image_url': IMAGES['cold_main'],
    'portrait_url': IMAGES['cold_alt'],
    'achievements': (
        "25+ world records in cold exposure and endurance\n"
        "Climbed Mt. Everest in shorts\n"
        "Barefoot half marathon above the Arctic Circle\n"
        "Over 2 hours in a full-body ice immersion capsule\n"
        "Founder of the Wim Hof Method\n"
        "Subject of multiple peer-reviewed scientific studies"
    ),
    'training_tips': (
        "The cold is a teacher — it shows you that you are stronger than you think.\n"
        "Breathe deep, slowly. Control your breath, control your nervous system.\n"
        "Discomfort is the gateway to growth. Every cold shower is a small victory.\n"
        "The body can do almost anything — it's the mind that needs convincing."
    ),
    'signature_quote': "Everything you need is already within you. You just need to take the cold shower and wake it up.",
    'video_url': 'https://www.youtube.com/watch?v=uCj7Qm3Bk04',
    'video_title': "Wim Hof: The Iceman's Method",
    'is_featured': True,
    'display_order': 23,
},
]

ICONS += NEW_ICONS

# Curated quotes. Author attribution is to the named individual.
# Each quote is short enough to fit a quote card and inspirational in nature.
QUOTES = [
    # Arnold
    {'text': "Strength does not come from winning. Your struggles develop your strengths.", 'author': 'Arnold Schwarzenegger', 'icon_slug': 'arnold-schwarzenegger', 'category_slug': 'bodybuilding', 'is_featured': True},
    {'text': "The mind is the limit. As long as the mind can envision the fact that you can do something, you can do it.", 'author': 'Arnold Schwarzenegger', 'icon_slug': 'arnold-schwarzenegger', 'category_slug': 'bodybuilding'},
    {'text': "Just like in bodybuilding, failure is part of the process. You pick yourself up and keep going.", 'author': 'Arnold Schwarzenegger', 'icon_slug': 'arnold-schwarzenegger', 'category_slug': 'mindset'},

    # Ronnie
    {'text': "The only place where success comes before work is in the dictionary.", 'author': 'Ronnie Coleman', 'icon_slug': 'ronnie-coleman', 'category_slug': 'bodybuilding', 'is_featured': True},
    {'text': "Everybody wants to be a bodybuilder, but don't nobody want to lift no heavy-ass weights.", 'author': 'Ronnie Coleman', 'icon_slug': 'ronnie-coleman', 'category_slug': 'bodybuilding'},
    {'text': "If you always do what you've always done, you'll always get what you always got.", 'author': 'Ronnie Coleman', 'icon_slug': 'ronnie-coleman', 'category_slug': 'mindset'},

    # Chris Bumstead
    {'text': "Show up. Be consistent. Be patient. Trust the process.", 'author': 'Chris Bumstead', 'icon_slug': 'chris-bumstead', 'category_slug': 'bodybuilding'},
    {'text': "Don't compare your chapter 1 to someone else's chapter 20.", 'author': 'Chris Bumstead', 'icon_slug': 'chris-bumstead', 'category_slug': 'mindset', 'is_featured': True},

    # Rich Froning
    {'text': "You have to want it as much as you want to breathe.", 'author': 'Rich Froning', 'icon_slug': 'rich-froning', 'category_slug': 'crossfit'},
    {'text': "It's not about being the best. It's about being better than you were yesterday.", 'author': 'Rich Froning', 'icon_slug': 'rich-froning', 'category_slug': 'crossfit', 'is_featured': True},

    # Mat Fraser
    {'text': "Boring basics build beautiful bodies.", 'author': 'Mat Fraser', 'icon_slug': 'mat-fraser', 'category_slug': 'crossfit'},
    {'text': "Show up when you don't want to. That's the only time it matters.", 'author': 'Mat Fraser', 'icon_slug': 'mat-fraser', 'category_slug': 'mindset'},

    # Eddie Hall
    {'text': "Train your mind first — the lift begins before the bar moves.", 'author': 'Eddie Hall', 'icon_slug': 'eddie-hall', 'category_slug': 'strength'},
    {'text': "Recovery is where champions are made. Sleep 9+ hours when peaking.", 'author': 'Eddie Hall', 'icon_slug': 'eddie-hall', 'category_slug': 'strength', 'is_featured': True},

    # Hafthor
    {'text': "You have to be hungry. Hungry to learn, hungry to grow, hungry to be the best.", 'author': 'Hafþór Björnsson', 'icon_slug': 'hafthor-bjornsson', 'category_slug': 'strength'},

    # Usain Bolt
    {'text': "Easy is not an option. No days off. Never quit. Be fearless.", 'author': 'Usain Bolt', 'icon_slug': 'usain-bolt', 'category_slug': 'athletics', 'is_featured': True},
    {'text': "I don't think limits.", 'author': 'Usain Bolt', 'icon_slug': 'usain-bolt', 'category_slug': 'athletics'},

    # Kelly Slater
    {'text': "The best surfer in the water is the one having the most fun.", 'author': 'Kelly Slater', 'icon_slug': 'kelly-slater', 'category_slug': 'endurance', 'is_featured': True},
    {'text': "Longevity is the ultimate flex.", 'author': 'Kelly Slater', 'icon_slug': 'kelly-slater', 'category_slug': 'endurance'},

    # Simone Biles
    {'text': "I'd rather regret the risks that didn't work out than the chances I didn't take.", 'author': 'Simone Biles', 'icon_slug': 'simone-biles', 'category_slug': 'athletics'},
    {'text': "Mental health is part of training. Rest is part of the work.", 'author': 'Simone Biles', 'icon_slug': 'simone-biles', 'category_slug': 'mindset', 'is_featured': True},

    # Michael Jordan
    {'text': "I've failed over and over and over again in my life. And that is why I succeed.", 'author': 'Michael Jordan', 'icon_slug': 'michael-jordan', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "Some people want it to happen, some wish it would happen. I make it happen.", 'author': 'Michael Jordan', 'icon_slug': 'michael-jordan', 'category_slug': 'mindset'},
    {'text': "Talent wins games, but teamwork and intelligence wins championships.", 'author': 'Michael Jordan', 'icon_slug': 'michael-jordan', 'category_slug': 'athletics'},

    # David Goggins
    {'text': "We don't rise to the level of our expectations — we fall to the level of our training.", 'author': 'David Goggins', 'icon_slug': 'david-goggins', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "Greatness pulls mediocrity into the mud. Get out there and get after it.", 'author': 'David Goggins', 'icon_slug': 'david-goggins', 'category_slug': 'mindset'},
    {'text': "You are living at about 40% of your capability. The rest is locked behind discipline.", 'author': 'David Goggins', 'icon_slug': 'david-goggins', 'category_slug': 'mindset'},
    {'text': "Don't stop when you're tired. Stop when you're done.", 'author': 'David Goggins', 'icon_slug': 'david-goggins', 'category_slug': 'mindset'},

    # Jocko Willink
    {'text': "Discipline equals freedom.", 'author': 'Jocko Willink', 'icon_slug': 'jocko-willink', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "Don't wait for motivation. Just show up and do the work.", 'author': 'Jocko Willink', 'icon_slug': 'jocko-willink', 'category_slug': 'mindset'},
    {'text': "Get up early. The world is less crowded in the morning hours.", 'author': 'Jocko Willink', 'icon_slug': 'jocko-willink', 'category_slug': 'mindset'},

    # Lee Haney
    {'text': "Exercise is a celebration of what your body can do, not a punishment for what you ate.", 'author': 'Lee Haney', 'icon_slug': 'lee-haney', 'category_slug': 'bodybuilding', 'is_featured': True},
    {'text': "Train to stimulate, not to annihilate. The body grows during recovery.", 'author': 'Lee Haney', 'icon_slug': 'lee-haney', 'category_slug': 'bodybuilding'},
    {'text': "If it is to be, it is up to me.", 'author': 'Lee Haney', 'icon_slug': 'lee-haney', 'category_slug': 'mindset'},

    # Dorian Yates
    {'text': "The journey is the reward. Becoming the best version of yourself is the whole point.", 'author': 'Dorian Yates', 'icon_slug': 'dorian-yates', 'category_slug': 'bodybuilding', 'is_featured': True},
    {'text': "Intensity is the key variable — progressive overload is not optional.", 'author': 'Dorian Yates', 'icon_slug': 'dorian-yates', 'category_slug': 'bodybuilding'},
    {'text': "One all-out set to failure beats three half-hearted sets every time.", 'author': 'Dorian Yates', 'icon_slug': 'dorian-yates', 'category_slug': 'mindset'},

    # Phil Heath
    {'text': "Believe in yourself, even when nobody else does. That belief is the foundation.", 'author': 'Phil Heath', 'icon_slug': 'phil-heath', 'category_slug': 'bodybuilding', 'is_featured': True},
    {'text': "Cardio is not optional. A great physique is revealed in the diet and cardio.", 'author': 'Phil Heath', 'icon_slug': 'phil-heath', 'category_slug': 'bodybuilding'},
    {'text': "Don't skip the details — calves, forearms, rear delts. Champions are built from all angles.", 'author': 'Phil Heath', 'icon_slug': 'phil-heath', 'category_slug': 'bodybuilding'},

    # Tia-Clair Toomey
    {'text': "Consistency beats intensity nine times out of ten.", 'author': 'Tia-Clair Toomey', 'icon_slug': 'tia-clair-toomey', 'category_slug': 'crossfit', 'is_featured': True},
    {'text': "The Fittest on Earth isn't just about being fast and strong — it's about being prepared for anything.", 'author': 'Tia-Clair Toomey', 'icon_slug': 'tia-clair-toomey', 'category_slug': 'crossfit'},
    {'text': "Train your weaknesses until they become your strengths.", 'author': 'Tia-Clair Toomey', 'icon_slug': 'tia-clair-toomey', 'category_slug': 'mindset'},

    # Brian Shaw
    {'text': "The goal is not to be better than anyone else — it's to be better than you were yesterday.", 'author': 'Brian Shaw', 'icon_slug': 'brian-shaw', 'category_slug': 'strength', 'is_featured': True},
    {'text': "Consistency beats intensity over the long haul — train smart so you can train for decades.", 'author': 'Brian Shaw', 'icon_slug': 'brian-shaw', 'category_slug': 'strength'},
    {'text': "The strongest muscle in your body is your mind. Train it every day.", 'author': 'Brian Shaw', 'icon_slug': 'brian-shaw', 'category_slug': 'mindset'},

    # Zydrunas Savickas
    {'text': "Strength is not just about what you can lift — it's about what you can carry.", 'author': 'Žydrūnas Savickas', 'icon_slug': 'zydrunas-savickas', 'category_slug': 'strength', 'is_featured': True},
    {'text': "Patience is the strongest attribute of any athlete. Everything takes time.", 'author': 'Žydrūnas Savickas', 'icon_slug': 'zydrunas-savickas', 'category_slug': 'strength'},
    {'text': "Train with precision, not ego. The bar doesn't care how mad you are.", 'author': 'Žydrūnas Savickas', 'icon_slug': 'zydrunas-savickas', 'category_slug': 'mindset'},

    # Eliud Kipchoge
    {'text': "No human is limited. The only limits are the ones you place on yourself.", 'author': 'Eliud Kipchoge', 'icon_slug': 'eliud-kipchoge', 'category_slug': 'endurance', 'is_featured': True},
    {'text': "The best time to run is in the morning — discipline starts with showing up at dawn.", 'author': 'Eliud Kipchoge', 'icon_slug': 'eliud-kipchoge', 'category_slug': 'endurance'},
    {'text': "Train your mind as hard as your legs. The body will follow what the head believes.", 'author': 'Eliud Kipchoge', 'icon_slug': 'eliud-kipchoge', 'category_slug': 'mindset'},
    {'text': "Consistency over intensity — 200 km per week, every week, for years.", 'author': 'Eliud Kipchoge', 'icon_slug': 'eliud-kipchoge', 'category_slug': 'endurance'},

    # Kobe Bryant
    {'text': "The most important thing is to try and inspire people so that they can be great.", 'author': 'Kobe Bryant', 'icon_slug': 'kobe-bryant', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "There is no substitute for hard work. Talent means nothing without preparation.", 'author': 'Kobe Bryant', 'icon_slug': 'kobe-bryant', 'category_slug': 'athletics'},
    {'text': "The job is not done when you're tired — the job is done when the job is done.", 'author': 'Kobe Bryant', 'icon_slug': 'kobe-bryant', 'category_slug': 'mindset'},
    {'text': "Embrace the grind. The discomfort is where the growth happens.", 'author': 'Kobe Bryant', 'icon_slug': 'kobe-bryant', 'category_slug': 'mindset'},

    # Muhammad Ali
    {'text': "Impossible is just a big word thrown around by small men who find it easier to live in the world they've been given.", 'author': 'Muhammad Ali', 'icon_slug': 'muhammad-ali', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "Float like a butterfly, sting like a bee. His hands can't hit what his eyes can't see.", 'author': 'Muhammad Ali', 'icon_slug': 'muhammad-ali', 'category_slug': 'athletics'},
    {'text': "Don't count the days, make the days count.", 'author': 'Muhammad Ali', 'icon_slug': 'muhammad-ali', 'category_slug': 'mindset'},
    {'text': "Champions are made in the gym, not in the ring.", 'author': 'Muhammad Ali', 'icon_slug': 'muhammad-ali', 'category_slug': 'athletics'},

    # Wim Hof
    {'text': "Everything you need is already within you. You just need to take the cold shower and wake it up.", 'author': 'Wim Hof', 'icon_slug': 'wim-hof', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "The cold is a teacher — it shows you that you are stronger than you think.", 'author': 'Wim Hof', 'icon_slug': 'wim-hof', 'category_slug': 'mindset'},
    {'text': "Discomfort is the gateway to growth. Every cold shower is a small victory.", 'author': 'Wim Hof', 'icon_slug': 'wim-hof', 'category_slug': 'mindset'},

    # General classic quotes (no specific icon, but iconic authors)
    {'text': "The clock is ticking. Are you becoming the person you want to be?", 'author': 'Greg Plitt', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "If you want to be the best, you have to do things that other people aren't willing to do.", 'author': 'Michael Phelps', 'category_slug': 'endurance', 'is_featured': True},
    {'text': "I hated every minute of training, but I said, 'Don't quit. Suffer now and live the rest of your life as a champion.'", 'author': 'Muhammad Ali', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "Champions keep playing until they get it right.", 'author': 'Billie Jean King', 'category_slug': 'athletics'},
    {'text': "The more I train, the luckier I get.", 'author': 'Gary Player', 'category_slug': 'endurance'},
    {'text': "You miss 100% of the shots you don't take.", 'author': 'Wayne Gretzky', 'category_slug': 'mindset'},
    {'text': "Whether you think you can or you think you can't, you're right.", 'author': 'Henry Ford', 'category_slug': 'mindset', 'is_featured': True},
    {'text': "A champion is someone who gets up when they can't.", 'author': 'Jack Dempsey', 'category_slug': 'mindset'},
    {'text': "Push yourself, because no one else is going to do it for you.", 'author': 'Anonymous', 'category_slug': 'mindset'},
    {'text': "Strive for progress, not perfection.", 'author': 'Anonymous', 'category_slug': 'mindset'},
    {'text': "The pain you feel today is the strength you feel tomorrow.", 'author': 'Arnold Schwarzenegger', 'icon_slug': 'arnold-schwarzenegger', 'category_slug': 'bodybuilding'},
    {'text': "Sweat is just fat crying.", 'author': 'Anonymous', 'category_slug': 'endurance'},
    {'text': "Your body can stand almost anything. It's your mind you have to convince.", 'author': 'Anonymous', 'category_slug': 'mindset'},
    {'text': "The hardest lift of all is lifting yourself up when no one else will.", 'author': 'Anonymous', 'category_slug': 'mindset'},
    {'text': "Today's pain is tomorrow's power.", 'author': 'Anonymous', 'category_slug': 'bodybuilding'},
    {'text': "Train hard or go home.", 'author': 'Anonymous', 'category_slug': 'mindset'},
    {'text': "Don't wish for a good body, work for it.", 'author': 'Anonymous', 'category_slug': 'bodybuilding'},
    {'text': "Run when you can, walk if you have to, crawl if you must — just never give up.", 'author': 'Dean Karnazes', 'category_slug': 'endurance', 'is_featured': True},
    {'text': "Strength is not just physical. It's the mindset that carries you through.", 'author': 'Anonymous', 'category_slug': 'mindset'},
    {'text': "Progress, not perfection. Every rep counts.", 'author': 'Anonymous', 'category_slug': 'bodybuilding'},
    {'text': "The difference between try and triumph is a little umph.", 'author': 'Marvin Phillips', 'category_slug': 'mindset'},
    {'text': "If it doesn't challenge you, it won't change you.", 'author': 'Fred DeVito', 'category_slug': 'mindset'},
    {'text': "You don't have to be extreme, just consistent.", 'author': 'Anonymous', 'category_slug': 'mindset'},
    {'text': "Wake up with determination, go to bed with satisfaction.", 'author': 'Anonymous', 'category_slug': 'mindset', 'is_featured': True},
]


class Command(BaseCommand):
    help = 'Seed the inspiration app with categories, fitness icons, and quotes.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding inspiration library...')

        # 1. Categories
        cat_map: dict = {}
        for c in CATEGORIES:
            cat, _ = InspirationCategory.objects.update_or_create(
                slug=c['slug'],
                defaults=c,
            )
            cat_map[c['slug']] = cat
        self.stdout.write(self.style.SUCCESS(
            f'  + {len(cat_map)} categories ready'
        ))

        # 2. Icons
        icon_map: dict = {}
        for data in ICONS:
            cat_slug = data.get('category_slug')
            data_copy = {k: v for k, v in data.items() if k != 'category_slug'}
            data_copy['category'] = cat_map[cat_slug]
            _, created = FitnessIcon.objects.update_or_create(
                slug=data_copy['slug'],
                defaults=data_copy,
            )
            icon_map[data_copy['slug']] = FitnessIcon.objects.get(slug=data_copy['slug'])
        self.stdout.write(self.style.SUCCESS(
            f'  + {len(icon_map)} fitness icons ready'
        ))

        # 3. Quotes
        # Wipe non-seed quotes so the seeder is the single source of truth.
        MotivationQuote.objects.exclude(author__in=[q['author'] for q in QUOTES]).delete()
        # Actually, simpler: clear and re-create for all seed quotes by text+author.
        for q in QUOTES:
            payload = {
                'text': q['text'],
                'author': q['author'],
                'is_featured': q.get('is_featured', False),
                'icon': icon_map.get(q.get('icon_slug', '')),
                'category': cat_map.get(q.get('category_slug', '')),
            }
            MotivationQuote.objects.update_or_create(
                text=q['text'],
                author=q['author'],
                defaults=payload,
            )
        self.stdout.write(self.style.SUCCESS(
            f'  + {len(QUOTES)} motivation quotes ready'
        ))

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Inspiration library seeded.'))
        self.stdout.write(
            f'  Categories: {InspirationCategory.objects.count()} | '
            f'Icons: {FitnessIcon.objects.count()} | '
            f'Quotes: {MotivationQuote.objects.count()}'
        )
