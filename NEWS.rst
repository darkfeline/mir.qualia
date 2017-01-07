Release notes
=============

This project uses `semantic versioning <http://semver.org/>`_.

1.0.1
-----

Changed
^^^^^^^

- Moved to Python 3.6

1.0.0 (2016-11-13)
------------------

Changed
^^^^^^^

- mir.qualia is now formally specified by ``Qualifier`` tests.

0.6.0 (2016-09-24)
------------------

Changed
^^^^^^^

- BEGIN and END no longer require whitespace between them and the preceding
  comment characters.

0.5.0 (2016-09-13)
------------------

Fixed
^^^^^

- Indentation wasn't implemented correctly.

0.4.0 (2016-09-13)
------------------

Changed
^^^^^^^

- Qualified blocks now preserve indentation.

0.3.0 (2016-09-12)
------------------

Fixed
^^^^^

- Unclosed qualified blocks get removed.
- Whitespace is stripped when uncommenting.

Changed
^^^^^^^

- ``IteratorQueue`` and ``CommentPrefix`` are now private, as they are
  implementation details.

0.2.0 (2016-09-12)
------------------

Fixed
^^^^^

- Documentation related cleanup.

0.1.0 (2016-09-11)
------------------

Initial release.
