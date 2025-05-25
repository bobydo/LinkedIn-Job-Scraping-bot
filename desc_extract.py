import re
import spacy

class JobDescriptionExtractor:
    def __init__(self):
        # Load spaCy English model
        self.nlp = spacy.load("en_core_web_sm")
        self.patterns = [
            r"\d+[-+]?\s*years? experience",
            r"proficiency in [\w, ]+",
            r"degree in [\w, ]+",
            r"experience with [\w, ]+",
            r"strong [\w ]+ knowledge",
            r"expertise in [\w, ]+",
            r"ability to [\w, ]+",
            r"comfortable [\w, ]+",
            r"prior experience [\w, ]+",
            r"good understanding of [\w, ]+"
        ]

    def extract_requirements(self, text):
        doc = self.nlp(text)
        requirements = []
        for sent in doc.sents:
            for pat in self.patterns:
                if re.search(pat, sent.text, re.IGNORECASE):
                    requirements.append(sent.text.strip())
        return requirements
