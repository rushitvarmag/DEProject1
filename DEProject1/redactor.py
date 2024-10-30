import spacy
import re
import os
import argparse
import glob
import sys

class Redactor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            print("Error: en_core_web_md model not found. Please install it using:")
            print("python -m spacy download en_core_web_md")
            exit(1)
        self.stats = {
            "names": 0,
            "dates": 0,
            "phones": 0,
            "addresses": 0,
            "concepts": 0
        }

    def redact_names(self, doc):
        redacted_text = doc.text
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                redacted_text = redacted_text.replace(ent.text, '█' * len(ent.text))
                self.stats["names"] += 1
        return self.nlp(redacted_text)

    def redact_dates(self, doc):
        redacted_text = doc.text
        for ent in doc.ents:
            if ent.label_ in ['DATE', 'TIME']:
                redacted_text = redacted_text.replace(ent.text, '█' * len(ent.text))
                self.stats["dates"] += 1
        return self.nlp(redacted_text)

    def redact_phones(self, doc):
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\d{10}'
        redacted_text = re.sub(phone_pattern, lambda m: '█' * len(m.group()), doc.text)
        self.stats["phones"] += len(re.findall(phone_pattern, doc.text))
        return self.nlp(redacted_text)

    def redact_address(self, doc):
        redacted_text = doc.text
        for ent in doc.ents:
            if ent.label_ in ['GPE', 'LOC', 'FAC']:
                redacted_text = redacted_text.replace(ent.text, '█' * len(ent.text))
                self.stats["addresses"] += 1
        return self.nlp(redacted_text)

    def redact_concepts(self, doc, concepts):
        redacted_text = doc.text
        for sent in doc.sents:
            for concept in concepts:
                if concept.lower() in sent.text.lower():
                    start = sent.text.lower().index(concept.lower())
                    end = start + len(concept)
                    redacted_text = redacted_text.replace(sent.text[start:end], '█' * len(concept))
                    self.stats["concepts"] += 1
        return self.nlp(redacted_text)

    def process_file(self, input_path, output_dir, args):
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()
            doc = self.nlp(text)

            if args.names:
                doc = self.redact_names(doc)
            if args.dates:
                doc = self.redact_dates(doc)
            if args.phones:
                doc = self.redact_phones(doc)
            if args.address:
                doc = self.redact_address(doc)
            if args.concept:
                doc = self.redact_concepts(doc, args.concept)

            output_path = os.path.join(output_dir, os.path.basename(input_path) + ".censored")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(doc.text)
        except IOError as e:
            print(f"Error processing file {input_path}: {str(e)}")

    def write_stats(self, stat_path):
        stat_text = "\n".join([f"{key}: {value}" for key, value in self.stats.items()])
        if stat_path in ['stderr', 'stdout']:
            print(stat_text, file=getattr(sys, stat_path))
        elif stat_path:
            with open(stat_path, 'w') as f:
                f.write(stat_text)

def get_arguments():
    parser = argparse.ArgumentParser(description="Redacts sensitive information from text files.")
    parser.add_argument('--input', nargs='+', help='Input files as glob pattern', required=True)
    parser.add_argument('--output', help='Directory to store censored files', required=True)
    parser.add_argument('--names', action='store_true', help='Redact names')
    parser.add_argument('--dates', action='store_true', help='Redact dates')
    parser.add_argument('--phones', action='store_true', help='Redact phone numbers')
    parser.add_argument('--address', action='store_true', help='Redact addresses')
    parser.add_argument('--concept', action='append', help='Concepts to redact')
    parser.add_argument('--stats', help='File or location for stats (stderr, stdout)')
    return parser.parse_args()

def main():
    args = get_arguments()
    os.makedirs(args.output, exist_ok=True)
    redactor = Redactor()

    for input_pattern in args.input:
        for input_path in glob.glob(input_pattern):
            redactor.process_file(input_path, args.output, args)

    if args.stats:
        redactor.write_stats(args.stats)

if __name__ == '__main__':
    main()
