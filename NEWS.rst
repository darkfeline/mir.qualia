Release notes
=============

This project uses `semantic versioning <http://semver.org/>`_.

1.0.0
-----

Changed
^^^^^^^

- mir.qualia is now formally specified by ``Qualifier`` tests.

0.6.0
-----

Changed
^^^^^^^

- BEGIN and END no longer require whitespace between them and the preceding
  comment characters.

0.5.0
-----

Fixed
^^^^^

- Indentation wasn't implemented correctly.

0.4.0
-----

Changed
^^^^^^^

- Qualified blocks now preserve indentation.

0.3.0
-----

Fixed
^^^^^

- Unclosed qualified blocks get removed.
- Whitespace is stripped when uncommenting.

Changed
^^^^^^^

- ``IteratorQueue`` and ``CommentPrefix`` are now private, as they are
  implementation details.

0.2.0
-----

Initial release.
