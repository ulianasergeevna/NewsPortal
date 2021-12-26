from django import template
import random


register = template.Library()

STOP_LIST = [
    'пончик',
    'ватрушка',
]

SYMBOLS = ['*', '!', '#']

@register.filter(name='censor')
def censor(text: str):
    for word in text.split(' '):
        if word.lower() in STOP_LIST:
             return (random.choice(SYMBOLS)
 * len(word)).join('')