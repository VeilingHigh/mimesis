from functools import wraps

from mimesis.data import ROMANIZATION_ALPHABETS
from mimesis.exceptions import UnsupportedLocale


def romanized(locale):
    def romanized_deco(func):
        """Cyrillic letter to latin converter. Romanization of the Cyrillic
         alphabet is the process of transliterating the Cyrillic language from
         the Cyrillic script into the Latin alphabet.

        .. note:: At this moment it's work only for Russian and Ukrainian,
        but in future we can add support for all slavic languages or for all
        Cyrillic languages.

        :param func: Function.
        :return: Latinized text.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                alphabet = ROMANIZATION_ALPHABETS[locale]
            except KeyError:
                raise UnsupportedLocale(
                    'Locale {0} is not supported yet.'.format(locale),
                )
            result = func(*args, **kwargs)
            txt = ''.join([alphabet[i] for i in result if i in alphabet])
            return txt

        return wrapper

    return romanized_deco


def type_to(new_type):
    """Convert result of function to different type

    :param new_type: New type.
    :return: Converted to new_type result.
    """
    def inner(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return new_type(result)

        return wrapper

    return inner
