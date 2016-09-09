import itertools
import re

_START_STATE = 'normal'
_DONE_STATE = 'done'
_BEGIN_PATTERN = re.compile(r'^(?P<prefix>\S+) BEGIN (?P<quality>\S+)')
_END_PATTERN = re.compile(r'^(?P<prefix>\S+) END (?P<quality>\S+)')


class Qualifier:

    def __init__(self, qualities, initial_state=_START_STATE):
        self.qualities = qualities
        self.state = initial_state

    def __call__(self, lines):
        state_handlers = self._STATE_HANDLERS
        while self.state in state_handlers:
            yielded_lines = state_handlers[self.state](self, lines)
            yield from yielded_lines

    def _handle_normal_state(self, lines):
        try:
            line = next(lines)
        except StopIteration:
            self.state = _DONE_STATE
            return ()
        else:
            match = _BEGIN_PATTERN.search(line)
            if match is None:
                return _StateResult((line,), 'normal')
            else:
                ...

    def _handle_in_block_state(self, lines):
        ...

    _STATE_HANDLERS = {
        'normal': _handle_normal_state,
        'in_block': _handle_in_block_state,
    }


class IteratorMonad:

    """Iterator monad.

    >>> list(IteratorMonad(range(2)).bind([1, 0]).bind(range(2)))
    [0, 1, 1, 0, 0, 1]

    Since Python isn't a pure functional language, this isn't a real monad.
    Iterator state is shared between bound instances.

    """

    def __init__(self, iterable=()):
        self.iterator = iter(iterable)

    def __iter__(self):
        return self.iterator

    def bind(self, iterable):
        """Bind iterable to monad."""
        return IteratorMonad(itertools.chain(self.iterator, iterable))


class CommentPrefix:

    """Comments and uncomments lines, given a prefix.

    >>> prefix = CommentPrefix('#')
    >>> prefix.uncomment(['#export EDITOR=vi'])
    ['export EDITOR=vi']
    >>> prefix.comment(['export EDITOR=vi'])
    ['#export EDITOR=vi']
    >>> prefix.is_commented(['export EdITOR=vi'])
    False

    Do not modify the comment_prefix attribute on an instance.

    """

    def __init__(self, comment_prefix):
        self.comment_prefix = comment_prefix
        self._prefix_pattern = re.compile(r'^{}\s*'.format(comment_prefix))

    def __repr__(self):
        return '{cls}({this.comment_prefix!r})}'.format(
            cls=type(self).__qualname__, this=self)

    def is_commented(self, lines):
        """Return True if all lines are commented."""
        pattern = self._prefix_pattern
        return all(pattern.search(line) for line in lines)

    def uncomment(self, lines):
        """Uncomment lines."""
        pattern = self._prefix_pattern
        while self.is_commented(lines):
           lines = [pattern.sub('', line) for line in lines]
        return lines

    def comment(self, lines):
        """Comment lines."""
        if not self.is_commented(lines):
            prefix = self.comment_prefix
            lines = [prefix + line for line in lines]
        return lines
