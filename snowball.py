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
import contextlib
from collections import defaultdict
from argparse import ArgumentParser


P1 = {
    '_filled': False,
    'bib': {
         'author': 'P Taylor',
         'title': 'Vernacularism in Software Design Practice: does craftsmanship have a place in software engineering?',
    },
    'id_scholarcitedby': '11957781116725793580'
}

P2 = {
    '_filled': False,
    'bib': {
         'author': 'M Paasivaara, C Lassenius',
         'title': 'Communities of practice in a large distributed agile software development organization–Case Ericsson',
    },
    'id_scholarcitedby': '17290640592074044656'
}

P3 = {
    '_filled': False,
    'bib': {
         'author': 'Rodriguez, Mikkonen, Kuvaja, Oivo, Garbajosa',
         'title': 'Building lean thinking in a telecom software developement organization: strengths and challenges',
    },
    'id_scholarcitedby': '8937478263825285117'
}

P4 = {
    '_filled': False,
    'bib': {
         'author': 'Lingel, Regan',
         'title': """"it's in your spinal cord, it's in your fingertips": practices of tools and craft in building software""",
    },
    'id_scholarcitedby': '14258254205316660031'
}

P5 = {
    '_filled': False,
    'bib': {
         'author': 'I Jacobson, E Seidewitz',
         'title': """A new software engineering"""
    },
    'id_scholarcitedby': '11364895964135352608'
}

P6 = {
    '_filled': False,
    'bib': {
         'author': 'Lucena, Tizzei',
         'title': """Applying software craftsmanship practices to a scrum project: an experience report"""
    },
    'id_scholarcitedby': '12556728404775473251'
}

P7 = {
    '_filled': False,
    'bib': {
         'author': 'Coplien',
         'title': """Borland software craftsmanship: A new look at process, quality and productivity"""
    },
    'id_scholarcitedby': '14714561442407932239'
}

P8 = {
    '_filled': False,
    'bib': {
        'author': 'Pyritz',
        'title': """Craftsmanship versus engineering: Computer programming - An art or a science?"""
    },
    'id_scholarcitedby': '6423741856014791786'
}
P9 = {
    '_filled': False,
    'bib': {
        'author': 'Parsons, Susnjak, Mathrani',
        'title': """Design from detail: Analyzing data from a global day of coderetreat"""
    },
    'id_scholarcitedby': '15407616062721785800'
}
P10 = {
    '_filled': False,
    'bib': {
        'author': 'Lindell',
        'title': """Crafting interaction: The epistemology of modern programming"""
    },
    'id_scholarcitedby': '1692253220231960690'
}
P11 = {
    '_filled': False,
    'bib': {
        'author': 'Thomas',
        'title': """Professional Developers Practice their Kata to Stay Sharp."""
    },
    'id_scholarcitedby': '5221862126554876987'
}


PAPERS = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11]

Q0 = ''
Q1 = '"software+craftsmanship"+OR+"software+craft"'
Q2 = '"agile+testing"+OR+"developer+testing"'
Q3 = '"refactoring"'
Q4 = '"clean+code"'
Q5 = '"continuous+integration"+OR+"continous+integration"'
Q6 = '"code+kata"+OR+"coding+kata"+OR+"coding+dojo"'
Q7 = '"automated+regression+testing"+OR+"automated+acceptance+test-driven+development"'
Q8 = '"test-driven+development"+OR+"behaviour-driven+development"+OR+"behavior-driven+development"'


@contextlib.contextmanager
def smart_open(filename=None, *args, **kwargs):
    if filename and filename != '-':
        fh = open(filename, *args, **kwargs)
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


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
        with smart_open(filename, mode='wt', encoding='utf-8', newline='') as f:
            out = csv.writer(f, delimiter=';')
            for key in val:
                pub = defaultdict(lambda: None, self.get_item(key))
                bib = defaultdict(lambda: None, pub['bib'])
                out.writerow([key, bib['author'], bib['title'], bib['url'], self.replace_newline(bib['abstract'])])

    def replace_newline(self, line):
        if line:
            return re.sub('[\r\n]', ' ', line)
        return ''

    def progress(self, char, **kwargs):
        if self.progressbar:
            print(char, **kwargs)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-#", "--progress", dest="progress", default=False, action="store_true", help="Enable progress bar")
    parser.add_argument("-i", "--id", dest="id", help="Print cached info for given id")
    parser.add_argument("-l", "--limit", dest="limit", default=100, help="Limit to the specified number of pages")
    parser.add_argument("-o", "--out", dest="out", default="/tmp/out.csv", help="Output file to write result to")
    parser.add_argument("-O", "--stdout", dest="stdout", default=False, action="store_true", help="Write result on stdout instead of file")
    parser.add_argument("-p", "--paper", dest="paper", help="Show references for given paper, either number, or a GScholar reference id")
    parser.add_argument("-q", "--query", dest="query", help="Search given query")
    parser.add_argument("-s", "--start", dest="start", default=0, help="Start fetching result at this item")
    parser.add_argument("-t", "--time", dest="time", default=15, help="Min time between page fetches")
    parser.add_argument("-T", "--random-time", dest="randtime", default=5, help="Varying time between page fetches")

    args = parser.parse_args()

    scholarly.MIN_TIME = int(args.time)
    scholarly.FUZZY_TIME = int(args.randtime)

    scholar = ScholarInfo(args.progress)

    if args.stdout:
        args.out = None

    if args.id:
        val = [scholar.get_item(args.id)]
        pprint.pprint(val)
    elif args.paper:
        if re.match("[1-9][0-9]*$", args.paper) and int(args.paper) <= len(PAPERS):
            paperid = PAPERS[int(args.paper)-1]['id_scholarcitedby']
        else:
            paperid = args.paper
        val = scholar.search_all_citations(paperid, start=args.start, limit=args.limit)
        scholar.write_csv(args.out)
    elif args.query:
        val = scholar.search_query(args.query, start=args.start, limit=args.limit)
        scholar.write_csv(args.out)
    else:
        val = scholar.search_all_citations(scholar.citation_index(P8), start=args.start, limit=args.limit)
        scholar.write_csv(args.out)

    scholar.fini()
