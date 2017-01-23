
import wikipedia
import re

subjects = ['New York', 'Seattle', 'Chicago', 'Tampa, Florida', 'Atlanta', 'California',
             'Pacific Ocean', 'Atlantic Ocean', 'Earth', 'climate', 'weather',
             'Chemistry', 'Chemical compound', 'molecule', 'scientific method',
             'computer network', 'logical programming', 'semantics',
             'physics', 'Particle accelerator', 'social media', 'Journalism',
             "newspaper", "programming language", "software performance testing", 'federal perkins loan',
            'the arts', "social history", "astronomy", "energy", 'robot', "communication", "information",
            "medicine", 'health']




corpus = ""

for subject in subjects:
    page = wikipedia.page(subject)
    corpus += page.content


corpus = re.sub(r'=+ .+ =+', '', corpus)
corpus = re.sub(r'\n\n+', '\n\n', corpus)

#corpus = re.sub('  +', ' ', corpus)
#corpus = re.sub('^\s', '--------', corpus, re.MULTILINE)

with open("corp_out.txt", "w", encoding="utf8") as fp:
    fp.write(corpus)