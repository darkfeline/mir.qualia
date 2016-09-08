import collections
import re

_START_STATE = 'normal'
_DONE_STATE = 'done'
_BEGIN_PATTERN = re.compile(r'^(?P<prefix>\S+) BEGIN (?P<quality>\S+)')
_END_PATTERN = re.compile(r'^(?P<prefix>\S+) END (?P<quality>\S+)')

_StateResult = collections.namedtuple(
    '_StateResult', 'lines state')

_DONE_RESULT = _StateResult((), _DONE_STATE)


class Qualifier:

    def __init__(self, quality):
        self.quality = quality

    def __call__(self, lines):
        state_handlers = self._STATE_HANDLERS
        state = _START_STATE
        while True:
            if state in state_handlers:
                yielded_lines, state = state_handlers[state](self, lines)
                yield from yielded_lines
            else:
                break

    def _handle_normal_state(self, lines):
        try:
            line = next(lines)
        except StopIteration:
            return _DONE_RESULT
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


class Activator:

    def __init__(self, comment_prefix):
        self.comment_prefix = comment_prefix

    def __repr__(self):
        return '{cls}({this.comment_prefix!r})}'.format(
            cls=type(self).__qualname__, this=self)

    @property
    def comment_prefix(self):
        return self._comment_prefix

    @comment_prefix.setter
    def comment_prefix(self, comment_prefix):
        self._comment_prefix = comment_prefix
        self._prefix_pattern = re.compile(r'^{}\s*'.format(comment_prefix))

    def is_active(self, lines):
        pattern = self._prefix_pattern
        return not all(pattern.search(line) for line in lines)

    def activate(self, lines):
        pattern = self._prefix_pattern
        while not self.is_active(lines):
           lines = [pattern.sub('', line) for line in lines]
        return lines

    def deactivate(self, lines):
        if self.is_active(lines):
            prefix = self.comment_prefix
            lines = [prefix + line for line in lines]
        return lines
