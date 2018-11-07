#! /usr/bin/env python

import scholarly
import json
import hashlib
import fileinput
import os
import re
import sys
import gzip
import csv
import pprint
from collections import defaultdict
from argparse import ArgumentParser

P1 = {
    '_filled': False,
    'bib': {
        'abstract': """By recognizing that software development is not a mechanical task, you can create better applications.
 Today's software development projects are often based on the traditional software engineering model, which was created to develop large-scale defense projects...""",
         'author': 'P McBreen',
         'title': 'Software craftsmanship: The new imperative',
         'url': 'https://books.google.com/books?hl=en&lr=&id=C9vvHV1lIawC&oi=fnd&pg=PR13&dq=Mcbreen+software+craftsmanship&ots=pO1q4ygQhK&sig=0UcYAyqvQSTY9pZfJ9N6how-zHc'
    },
    'citedby': 130,
    'id_scholarcitedby': '9992022440740016231',
    'source': 'scholar',
    'url_scholarbib': 'https://scholar.googleusercontent.com/scholar.bib?q=info:Z1AKSHjLqooJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW89A8xOVS3_12We0OgVskryJY6om85y5&scisf=4&ct=citation&cd=0&hl=en'
    }
P2 = {
    '_filled': False,
    'bib': {
        'abstract': """Extreme Programming (XP) was conceived and developed to address the specific needs of software development
 conducted by small teams in the face of vague and changing requirements. This new lightweight methodology
 challenges many conventional tenets, including the long-held assumption that the cost of changing a piece
 of software necessarily rises dramatically over the course of time. XP recognizes that projects have to work
 to achieve this reduction in cost and exploit the savings once they have been earned...""",
         'author': 'K Beck and E Gamma',
         'eprint': 'https://scholar.google.comhttp://javacup.ir/avan/files/article/ASTA%20-%20XP%20Explained.pdf',
         'title': 'Extreme programming explained: embrace change',
         'url': 'https://books.google.com/books?hl=en&lr=&id=G8EL4H4vf7UC&oi=fnd&pg=PR13&dq=Kent+Beck+Extreme+Programming+explained&ots=jawDvnkUzk&sig=G8S9x-bSw5v-kzdtSAKhZLfwEDE'
    },
    'citedby': 11586,
    'id_scholarcitedby': '14833523990057642889',
    'source': 'scholar',
    'url_scholarbib': 'https://scholar.googleusercontent.com/scholar.bib?q=info:ieueQnpD280J:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW89prYwtVI6thcjSKliBhkdCUn4w1C6K&scisf=4&ct=citation&cd=0&hl=en'
    }
P3 = {
    '_filled': False,
    'bib': {
        'abstract': """As the application of object technology--particularly the Java programming language--has become commonplace, a
 new problem has emerged to confront the software development community. Significant numbers of poorly designed programs have been created by less...""",
         'author': 'M Fowler and K Beck and J Brant and W Opdyke and D Roberts',
         'eprint': 'https://scholar.google.comhttp://www.academia.edu/download/35991683/refactoring.pdf',
         'title': 'Refactoring: improving the design of existing code',
         'url': 'https://books.google.com/books?hl=en&lr=&id=UTgFCAAAQBAJ&oi=fnd&pg=PR7&dq=Martin+Fowler+Refactoring&ots=WhURcvXA3e&sig=va-49AO5csjbbkyN28ZBXcvOWvI'
    },
    'citedby': 7917,
    'id_scholarcitedby': '878980806807878846',
    'source': 'scholar',
    'url_scholarbib': 'https://scholar.googleusercontent.com/scholar.bib?q=info:vnwrAmPEMgwJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW89raOqVkvOcIJqsVqtOfEVTAJAt-XWn&scisf=4&ct=citation&cd=0&hl=en'
    }
P4 = {
    '_filled': False,
    'bib': {
        'author': 'L Crispin and J Gregory',
        'title': 'Agile testing: A practical guide for testers and agile teams'
    },
 'citedby': 282,
 'id_scholarcitedby': '4780550892992702017',
 'source': 'scholar',
 'url_scholarbib': 'https://scholar.googleusercontent.com/scholar.bib?q=info:QaaBb7XtV0IJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW89sUDLK9ggPG6NgSoBkQh1zoTd7Nc4e&scisf=4&ct=citation&cd=0&hl=en'
}
P5 = {
    '_filled': False,
    'bib': {
        'author': 'RC Martin',
        'eprint': 'https://scholar.google.comhttps://www.redshifter.org/book/413654649/download-clean-code-a-handbook-of-agile-software-craftsmanship.pdf',
        'title': 'Clean code: a handbook of agile software craftsmanship'
    },
    'citedby': 817,
    'id_scholarcitedby': '6031327959174725948',
    'source': 'scholar',
    'url_scholarbib': 'https://scholar.googleusercontent.com/scholar.bib?q=info:PMF90tKUs1MJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW89s3z_AhD-ymPnT1kHvHPC33Cs7MRu6&scisf=4&ct=citation&cd=0&hl=en'
}
P8 =  {
    '_filled': False,
    'bib': {
        'abstract': """We conducted a quasi-experiment to compare the characteristics of experts' and novices' test-driven 
development processes. Our novices were 11 computers science students who participated in an Extreme Programming lab course,
the expert group consisted of seven professionals who had industrial experience in test-driven development. 
The novices as well as two of the experts worked in a laboratory environment whereas the remaining five experts worked in their office.
The experts complied more to the rules of test-driven development and\xa0…""",
         'author': 'MM Müller and A Höfer\xa0- Empirical Software Engineering and 2007',
         'eprint': 'https://scholar.google.comhttps://link.springer.com/content/pdf/10.1007/s10664-007-9048-2.pdf',
         'title': 'The effect of experience on the test-driven development process',
         'url': 'https://link.springer.com/article/10.1007/s10664-007-9048-2'
    },
    'citedby': 52,
    'id_scholarcitedby': '14565201090169922408',
    'source': 'scholar',
    'url_scholarbib': 'https://scholar.googleusercontent.com/scholar.bib?q=info:aOO1xTj9IcoJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9A-wciC2rzLCTXixUWJXKgyJlSDbTrw&scisf=4&ct=citation&cd=0&hl=en'
}
P9 = {
    '_filled': False,
    'bib': {
         'abstract': """Background: Test-Driven Development (TDD) is claimed to have positive effects on external code quality and
programmers' productivity. The main driver for these possible improvements is the tests enforced by the test-first nature of TDD 
as previously investigated in a controlled experiment (ie the original study). Aim: Our goal is to examine the nature of the relationship
between tests and external code quality as well as programmers' productivity in order to verify/refute the results of the original study. Method: We conducted a\xa0…""",
         'author': 'D Fucci and B Turhan\xa0- Empirical Software Engineering and 2014',
         'eprint': 'https://scholar.google.comhttps://link.springer.com/article/10.1007/s10664-013-9259-7',
         'title': 'On the role of tests in test-driven development: a differentiated and partial replication',
         'url': 'https://link.springer.com/article/10.1007/s10664-013-9259-7'
    },
    'citedby': 23,
    'id_scholarcitedby': '1516483469463706449',
    'source': 'scholar',
    'url_scholarbib': 'https://scholar.googleusercontent.com/scholar.bib?q=info:UdsiSa6hCxUJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9BBmxuvjDTkQoMO41csxFicAnFE2Xqt&scisf=4&ct=citation&cd=0&hl=en'
}
P10 = { 
    '_filled': False,
    'bib': {
        'abstract': """The technical debt metaphor is gaining significant traction in the software development community as a way
to understand and communicate about issues of intrinsic quality, value, and cost. This is a report on a second workshop on managing 
technical debt, which took place as part of the 33rd International Conference on Software Engineering (ICSE 2011). The goal of this second 
workshop was to discuss the management of technical debt: to assess current practice in industry and to further refine a research agenda for software\xa0…""",
         'author': 'I Ozkaya and P Kruchten and RL Nord and N Brown\xa0- ACM SIGSOFT Software\xa0… and 2011',
         'eprint': 'https://scholar.google.comhttp://www.dtic.mil/dtic/tr/fulltext/u2/1015406.pdf',
         'title': 'Managing technical debt in software development: report on the 2nd international workshop on managing technical debt, held at ICSE 2011',
         'url': 'https://dl.acm.org/citation.cfm?id=2020979'
    },
    'citedby': 19,
    'id_scholarcitedby': '6986788749151307637',
    'source': 'scholar',
    'url_scholarbib': 'https://scholar.googleusercontent.com/scholar.bib?q=info:dQfciVkP9mAJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9BCnoacYAro6RcsiHTfYuVARgCUTOCW&scisf=4&ct=citation&cd=0&hl=en'
}

Q1 = '"software+craftsmanship"+OR+"software+craft"'
Q2 = '"agile+testing"+OR+"developer+testing"'
Q3 = '"refactoring"'
Q4 = '"clean+code"'
Q5 = '"continuous+integration"+OR+"continous+integration"'
Q6 = '"code+kata"+OR+"coding+kata"+OR+"coding+dojo"'
Q7 = '"automated+regression+testing"+OR+"automated+acceptance+test-driven+development"'
Q8 = '"test-driven+development"+OR+"behaviour-driven+development"+OR+"behavior-driven+development"'

class ScholarInfo:
    def __init__(self, progress=False):
        home = os.path.expanduser("~")
        self.publications_cache_file = home + "/.publications_scholar.json.gz"
        self.publications = self.__init_cache(self.publications_cache_file)
        self.progressbar = progress

    def __init_cache(self, filename):
        if os.path.isfile(filename):
            with gzip.open(filename, mode="rt", encoding='utf-8') as f:
                d = json.load(f)
        else:
            d = {}
        return d

    def fini(self):
        with gzip.open(self.publications_cache_file, mode='wt', encoding='utf-8') as f:
            json.dump(self.publications, f, ensure_ascii=False)

    def citation_index(self, P):
        return P['id_scholarcitedby']

    def search_query(self, Q, **kwargs):
        search_set = scholarly.search_pubs_custom_url('/scholar?hl=en&scipsc=1&q={0}&btnG='.format(Q))
        return self.retrieve_keys_for_search(search_set, kwargs['limit'])

    def search_by_paper(self, P, Q, **kwargs):
        search_set = scholarly.search_pubs_custom_url('/scholar?hl=en&cites={0}&scipsc=1&q={1}&btnG='.format(self.citation_index(P), Q))
        return self.retrieve_keys_for_search(search_set, kwargs['limit'])

    def search_all_citations(self, paper, **kwargs):
        search_set = scholarly.search_pubs_custom_url('/scholar?hl=en&cites={0}&start={1}'.format(paper, kwargs['start']))
        return self.retrieve_keys_for_search(search_set, kwargs['limit'])

    def retrieve_keys_for_search(self, search_set, limit):
        retval = list()
        i=0
        for p in search_set:
            # p.fill()
            data = p.__dict__
            if 'id_scholarcitedby' in data:
                paperid = data['id_scholarcitedby']
            else:
                url_to_fetch = data['url_scholarbib']
                try:
                    bibtex_entry = scholarly._get_page(url_to_fetch)
                    paperid = "MD5:" + hashlib.md5(bibtex_entry.encode('utf-8')).hexdigest()
                    data['fetchedbibtex'] = bibtex_entry
                except scholarly.CaptchaError:
                    paperid = url_to_fetch
            self.publications[paperid] = data
            retval.append(paperid)
            i += 1
            if i % 10 == 0:
                self.progress("#", end='', flush=True)
                if i / 10 >= int(limit):
                    break
        self.progress("", flush=True)
        return retval

    def get_item(self, key):
        return self.publications[key]

    def write_csv(self, filename):
        with open(filename, mode='wt', encoding='utf-8', newline='') as f:
            out = csv.writer(f, delimiter=';')
            for key in val:
                pub = defaultdict(lambda: None, self.get_item(key))
                bib = defaultdict(lambda: None, pub['bib'])
                out.writerow([key, bib['author'], bib['title'], bib['url']])

    def progress(self, char, **kwargs):
        if self.progressbar:
            print(char, **kwargs)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-#", "--progress", dest="progress", default=False, action="store_true", help="Enable progress bar")
    parser.add_argument("-i", "--id", dest="id", help="Print cached info for given id")
    parser.add_argument("-l", "--limit", dest="limit", default=100, help="Limit to the specified number of pages")
    parser.add_argument("-o", "--out", dest="out", default="/tmp/out.csv", help="Output file to write result to")
    parser.add_argument("-p", "--paper", dest="paper", help="Show references for given paper")
    parser.add_argument("-q", "--query", dest="query", help="Search given query")
    parser.add_argument("-s", "--start", dest="start", default=0, help="Start fetching result at this item")
    parser.add_argument("-t", "--time", dest="time", default=15, help="Min time between page fetches")
    parser.add_argument("-T", "--random-time", dest="randtime", default=5, help="Varying time between page fetches")

    args = parser.parse_args()

    scholarly.MIN_TIME = args.time
    scholarly.FUZZY_TIME = args.randtime

    scholar = ScholarInfo(args.progress)

    if args.id:
        val = [scholar.get_item(args.id)]
        pprint.pprint(val)
    elif args.paper:
        val = scholar.search_all_citations(args.paper, start=args.start, limit=args.limit)
        scholar.write_csv(args.out)
    elif args.query:
        val = scholar.search_query(Q1, start=args.start, limit=args.limit)
        scholar.write_csv(args.out)
    else:
        val = scholar.search_all_citations(scholar.citation_index(P8), start=args.start, limit=args.limit)
        scholar.write_csv(args.out)

    scholar.fini()
