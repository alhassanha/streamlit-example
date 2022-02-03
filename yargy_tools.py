from yargy import (
    Parser,
    or_, rule
)
from yargy.pipelines import morph_pipeline
from yargy import and_, not_
from yargy.predicates import (
    eq, in_, dictionary,
    type, gram
)
from yargy.tokenizer import MorphTokenizer
from yargy import interpretation as interp
from yargy.interpretation import fact, attribute

grams_dict = {
    'NEUT': gram('neut'),
    'ADJF': gram('ADJF'),
    'NOUN': gram('NOUN'),
    'VERB': gram('VERB'),
    'PNCT': gram('PNCT'),
    'PRTF': gram('PRTF'),
    'CONJ': gram('CONJ'),
    'PREP': gram('PREP'),
}

grams_dict_1 = {
    'средний род':          gram('neut'),
    'прилагательное':       gram('ADJF'),
    'существительное':      gram('NOUN'),
    'глагол':               gram('VERB'),
    'пунктуация':           gram('PNCT'),
    'причастие':            gram('PRTF'),
    'союз':                 gram('CONJ'),
    'предлог':              gram('PREP'),
}

def make_morph_pipeline(terms: str):
    terms_list = terms.split(',')
    return morph_pipeline(terms_list)


def make_grams_production(grams: list, repeatable, optional, is_or):
    if len(grams) == 1:
        production = grams_dict_1[grams[0]]
    elif is_or:
        production = or_(*[grams_dict_1[gram] for gram in grams])
    else:
        production = and_(*[grams_dict_1[gram] for gram in grams])
    if repeatable:
        production = production.repeatable()
    if optional:
        production = production.optional()
    return production


def slice_text(text, spans):
    chunks = []
    last_idx = 0
    for span in spans:
        outer_chunk = text[last_idx:span.start]
        if outer_chunk:
            chunks.append(outer_chunk)
        chunks.append((text[span.start:span.stop], ''))
        last_idx = span.stop
    outer_chunk = text[last_idx:len(text)]
    if outer_chunk:
        chunks.append(outer_chunk)
    return chunks

def get_parser():
    METHOD = morph_pipeline([
        'метод',
        'способ',
        'технология',
        'система',
        'изобретение',
    ])

    NEUT = gram('neut')
    ADJF = gram('ADJF')
    NOUN = gram('NOUN')
    VERB = gram('VERB')
    PUNCT = gram('PNCT')
    PRTF = gram('PRTF')
    CONJ = gram('CONJ')
    PREP = gram('PREP')

    TECHNOLOGY = rule(
        METHOD,
        ADJF.repeatable().optional(),
        and_(NOUN, NEUT).repeatable(),
        or_(ADJF, NOUN, PRTF, CONJ, PREP).repeatable(),
    )

    return Parser(TECHNOLOGY)