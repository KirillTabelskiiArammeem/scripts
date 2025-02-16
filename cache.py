# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# decorator makes wrappers that have the same API as their wrapped function;
# this is important for the odoo.api.guess() that relies on signatures
from collections import defaultdict
from decorator import decorator
# from inspect import formatannotation, getargspec # import removed for compatibility with python3.11
import logging

from . import pycompat

unsafe_eval = eval

_logger = logging.getLogger(__name__)


# formatargspec and getargspec was removed from python3.11
# that function bellow is a copy from python3.10

import re
import types
import warnings
from inspect import getfullargspec
from collections import namedtuple

ArgSpec = namedtuple('ArgSpec', 'args varargs keywords defaults')

def formatannotation(annotation, base_module=None):
    if getattr(annotation, '__module__', None) == 'typing':
        def repl(match):
            text = match.group()
            return text.removeprefix('typing.')
        return re.sub(r'[\w\.]+', repl, repr(annotation))
    if isinstance(annotation, types.GenericAlias):
        return str(annotation)
    if isinstance(annotation, type):
        if annotation.__module__ in ('builtins', base_module):
            return annotation.__qualname__
        return annotation.__module__+'.'+annotation.__qualname__
    return repr(annotation)


def formatargspec(args, varargs=None, varkw=None, defaults=None,
                  kwonlyargs=(), kwonlydefaults={}, annotations={},
                  formatarg=str,
                  formatvarargs=lambda name: '*' + name,
                  formatvarkw=lambda name: '**' + name,
                  formatvalue=lambda value: '=' + repr(value),
                  formatreturns=lambda text: ' -> ' + text,
                  formatannotation=formatannotation):
    """Format an argument spec from the values returned by getfullargspec.

    The first seven arguments are (args, varargs, varkw, defaults,
    kwonlyargs, kwonlydefaults, annotations).  The other five arguments
    are the corresponding optional formatting functions that are called to
    turn names and values into strings.  The last argument is an optional
    function to format the sequence of arguments.

    Deprecated since Python 3.5: use the `signature` function and `Signature`
    objects.
    """

    from warnings import warn

    warn("`formatargspec` is deprecated since Python 3.5. Use `signature` and "
         "the `Signature` object directly",
         DeprecationWarning,
         stacklevel=2)

    def formatargandannotation(arg):
        result = formatarg(arg)
        if arg in annotations:
            result += ': ' + formatannotation(annotations[arg])
        return result
    specs = []
    if defaults:
        firstdefault = len(args) - len(defaults)
    for i, arg in enumerate(args):
        spec = formatargandannotation(arg)
        if defaults and i >= firstdefault:
            spec = spec + formatvalue(defaults[i - firstdefault])
        specs.append(spec)
    if varargs is not None:
        specs.append(formatvarargs(formatargandannotation(varargs)))
    else:
        if kwonlyargs:
            specs.append('*')
    if kwonlyargs:
        for kwonlyarg in kwonlyargs:
            spec = formatargandannotation(kwonlyarg)
            if kwonlydefaults and kwonlyarg in kwonlydefaults:
                spec += formatvalue(kwonlydefaults[kwonlyarg])
            specs.append(spec)
    if varkw is not None:
        specs.append(formatvarkw(formatargandannotation(varkw)))
    result = '(' + ', '.join(specs) + ')'
    if 'return' in annotations:
        result += formatreturns(formatannotation(annotations['return']))
    return result


def getargspec(func):
    """Get the names and default values of a function's parameters.

    A tuple of four things is returned: (args, varargs, keywords, defaults).
    'args' is a list of the argument names, including keyword-only argument names.
    'varargs' and 'keywords' are the names of the * and ** parameters or None.
    'defaults' is an n-tuple of the default values of the last n parameters.

    This function is deprecated, as it does not support annotations or
    keyword-only parameters and will raise ValueError if either is present
    on the supplied callable.

    For a more structured introspection API, use inspect.signature() instead.

    Alternatively, use getfullargspec() for an API with a similar namedtuple
    based interface, but full support for annotations and keyword-only
    parameters.

    Deprecated since Python 3.5, use `inspect.getfullargspec()`.
    """
    warnings.warn("inspect.getargspec() is deprecated since Python 3.0, "
                  "use inspect.signature() or inspect.getfullargspec()",
                  DeprecationWarning, stacklevel=2)
    args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = \
        getfullargspec(func)
    if kwonlyargs or ann:
        raise ValueError("Function has keyword-only parameters or annotations"
                         ", use inspect.signature() API which can support them")
    return ArgSpec(args, varargs, varkw, defaults)



class ormcache_counter(object):
    """ Statistic counters for cache entries. """
    __slots__ = ['hit', 'miss', 'err']

    def __init__(self):
        self.hit = 0
        self.miss = 0
        self.err = 0

    @property
    def ratio(self):
        return 100.0 * self.hit / (self.hit + self.miss or 1)

# statistic counters dictionary, maps (dbname, modelname, method) to counter
STAT = defaultdict(ormcache_counter)


class ormcache(object):
    """ LRU cache decorator for model methods.
    The parameters are strings that represent expressions referring to the
    signature of the decorated method, and are used to compute a cache key::

        @ormcache('model_name', 'mode')
        def _compute_domain(self, model_name, mode="read"):
            ...

    For the sake of backward compatibility, the decorator supports the named
    parameter `skiparg`::

        @ormcache(skiparg=1)
        def _compute_domain(self, model_name, mode="read"):
            ...

    Methods implementing this decorator should never return a Recordset,
    because the underlying cursor will eventually be closed and raise a
    `psycopg2.OperationalError`.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.skiparg = kwargs.get('skiparg')

    def __call__(self, method):
        self.method = method
        self.determine_key()
        lookup = decorator(self.lookup, method)
        lookup.clear_cache = self.clear
        return lookup

    def determine_key(self):
        """ Determine the function that computes a cache key from arguments. """
        if self.skiparg is None:
            # build a string that represents function code and evaluate it
            args = formatargspec(*getargspec(self.method))[1:-1]
            if self.args:
                code = "lambda %s: (%s,)" % (args, ", ".join(self.args))
            else:
                code = "lambda %s: ()" % (args,)
            self.key = unsafe_eval(code)
        else:
            # backward-compatible function that uses self.skiparg
            self.key = lambda *args, **kwargs: args[self.skiparg:]

    def lru(self, model):
        counter = STAT[(model.pool.db_name, model._name, self.method)]
        return model.pool.cache, (model._name, self.method), counter

    def lookup(self, method, *args, **kwargs):
        d, key0, counter = self.lru(args[0])
        key = key0 + self.key(*args, **kwargs)
        try:
            r = d[key]
            counter.hit += 1
            return r
        except KeyError:
            counter.miss += 1
            value = d[key] = self.method(*args, **kwargs)
            return value
        except TypeError:
            counter.err += 1
            return self.method(*args, **kwargs)

    def clear(self, model, *args):
        """ Clear the registry cache """
        model.pool._clear_cache()


class ormcache_context(ormcache):
    """ This LRU cache decorator is a variant of :class:`ormcache`, with an
    extra parameter ``keys`` that defines a sequence of dictionary keys. Those
    keys are looked up in the ``context`` parameter and combined to the cache
    key made by :class:`ormcache`.
    """
    def __init__(self, *args, **kwargs):
        super(ormcache_context, self).__init__(*args, **kwargs)
        self.keys = kwargs['keys']

    def determine_key(self):
        """ Determine the function that computes a cache key from arguments. """
        assert self.skiparg is None, "ormcache_context() no longer supports skiparg"
        # build a string that represents function code and evaluate it
        spec = getargspec(self.method)
        args = formatargspec(*spec)[1:-1]
        cont_expr = "(context or {})" if 'context' in spec.args else "self._context"
        keys_expr = "tuple(%s.get(k) for k in %r)" % (cont_expr, self.keys)
        if self.args:
            code = "lambda %s: (%s, %s)" % (args, ", ".join(self.args), keys_expr)
        else:
            code = "lambda %s: (%s,)" % (args, keys_expr)
        self.key = unsafe_eval(code)


class ormcache_multi(ormcache):
    """ This LRU cache decorator is a variant of :class:`ormcache`, with an
    extra parameter ``multi`` that gives the name of a parameter. Upon call, the
    corresponding argument is iterated on, and every value leads to a cache
    entry under its own key.
    """
    def __init__(self, *args, **kwargs):
        super(ormcache_multi, self).__init__(*args, **kwargs)
        self.multi = kwargs['multi']

    def determine_key(self):
        """ Determine the function that computes a cache key from arguments. """
        assert self.skiparg is None, "ormcache_multi() no longer supports skiparg"
        assert isinstance(self.multi, pycompat.string_types), "ormcache_multi() parameter multi must be an argument name"

        super(ormcache_multi, self).determine_key()

        # key_multi computes the extra element added to the key
        spec = getargspec(self.method)
        args = formatargspec(*spec)[1:-1]
        code_multi = "lambda %s: %s" % (args, self.multi)
        self.key_multi = unsafe_eval(code_multi)

        # self.multi_pos is the position of self.multi in args
        self.multi_pos = spec.args.index(self.multi)

    def lookup(self, method, *args, **kwargs):
        d, key0, counter = self.lru(args[0])
        base_key = key0 + self.key(*args, **kwargs)
        ids = self.key_multi(*args, **kwargs)
        result = {}
        missed = []

        # first take what is available in the cache
        for i in ids:
            key = base_key + (i,)
            try:
                result[i] = d[key]
                counter.hit += 1
            except Exception:
                counter.miss += 1
                missed.append(i)

        if missed:
            # call the method for the ids that were not in the cache; note that
            # thanks to decorator(), the multi argument will be bound and passed
            # positionally in args.
            args = list(args)
            args[self.multi_pos] = missed
            result.update(method(*args, **kwargs))

            # store those new results back in the cache
            for i in missed:
                key = base_key + (i,)
                d[key] = result[i]

        return result


class dummy_cache(object):
    """ Cache decorator replacement to actually do no caching. """
    def __init__(self, *l, **kw):
        pass

    def __call__(self, fn):
        fn.clear_cache = self.clear
        return fn

    def clear(self, *l, **kw):
        pass


def log_ormcache_stats(sig=None, frame=None):
    """ Log statistics of ormcache usage by database, model, and method. """
    from odoo.modules.registry import Registry
    import threading

    me = threading.currentThread()
    me_dbname = getattr(me, 'dbname', 'n/a')

    for dbname, reg in sorted(Registry.registries.items()):
        # set logger prefix to dbname
        me.dbname = dbname
        entries = defaultdict(int)
        # beware: we use .keys() on purpose here (reg.cache is not a real dict)
        for key in reg.cache.keys():
            entries[key[:2]] += 1
        # show entries sorted by model name, method name
        for key in sorted(entries, key=lambda key: (key[0], key[1].__name__)):
            model, method = key
            stat = STAT[(dbname, model, method)]
            _logger.info(
                "%6d entries, %6d hit, %6d miss, %6d err, %4.1f%% ratio, for %s.%s",
                entries[key], stat.hit, stat.miss, stat.err, stat.ratio, model, method.__name__,
            )

    me.dbname = me_dbname


def get_cache_key_counter(bound_method, *args, **kwargs):
    """ Return the cache, key and stat counter for the given call. """
    model = bound_method.__self__
    ormcache = bound_method.clear_cache.__self__
    cache, key0, counter = ormcache.lru(model)
    key = key0 + ormcache.key(model, *args, **kwargs)
    return cache, key, counter

# For backward compatibility
cache = ormcache
