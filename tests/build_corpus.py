
import wikipedia
import re

subjects = ['new york', 'seattle', 'chicago', 'tampa, florida', 'atlanta', 'california', 'alaska', 'virginia', 'montana',
            'germany', 'brazil', 'argentina', 'mexico', 'canada', 'france', 'belgium', 'denmark', 'japan', 'egypt',
            'bahamas', 'africa', 'asia', 'europe', 'south america', 'desert', 'mountain', 'river', 'lake', 'ocean',
             'pacific ocean', 'atlantic ocean', 'earth', 'climate', 'weather', 'cloud',
             'chemistry', 'chemical compound', 'molecule', 'scientific method',
             'computer network', 'logical programming', 'semantics',
             'physics', 'particle accelerator', 'social media', 'journalism', 'lawyer',
             "newspaper", "programming language", "software performance testing", 'federal perkins loan',
            'the arts', "social history", "astronomy", "energy", 'robot', "communication", "information",
            "medicine", 'health', 'ethics', 'laughter', 'sports', 'casino', 'statue', 'nominative determinism',
            'fun', 'psychology', 'parrots', 'dogs', 'cats', 'animals', 'traffic', 'hotel', 'hollywood', 'random']




corpus = ""

for subject in subjects:
    try:
        page = wikipedia.page(subject)
        corpus += page.content
    except:
        print("Failed on: " + subject)

corpus = re.sub(r'=+ .+ =+', '', corpus)
#corpus = re.sub(r'\n\n+', '\n\n', corpus)
#corpus = re.sub('  +', ' ', corpus)
#corpus = re.sub('^\s', '--------', corpus, re.MULTILINE)

with open("corpus.txt", "w", encoding="utf8") as fp:
    fp.write(corpus)
