mir.qualia
==========

.. image:: https://circleci.com/gh/darkfeline/mir.qualia.svg?style=shield
   :target: https://circleci.com/gh/darkfeline/mir.qualia
.. image:: https://codecov.io/gh/darkfeline/mir.qualia/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/darkfeline/mir.qualia

..

   There are recognizable qualitative characters of the given, which may be
   repeated in different experiences, and are thus a sort of universals; I call
   these "qualia." But although such qualia are universals, in the sense of
   being recognized from one to another experience, they must be distinguished
   from the properties of objects. Confusion of these two is characteristic of
   many historical conceptions, as well as of current essence-theories. The
   quale is directly intuited, given, and is not the subject of any possible
   error because it is purely subjective.

   -- Clarence Irving Lewis

mir.qualia provides a Python 3 script for conditionally commenting and
uncommenting blocks in files, for example configuration files (dotfiles).  This
can be used to keep dotfiles for different machines in a single version control
repository and check out the right copy on each machine.

Installation
------------

Installing from PyPi is recommended::

  $ pip3 install mir.qualia

Basic usage
-----------

qualia is a filter script, so it is used by redirecting stdin and stdout::

  $ qualia [qualities] <infile >outfile

Here is an example of how qualia works.  Let's say you have a ``.bashrc``
containing the following::

  # BEGIN laptop
  alias home="cd /home/bob"
  # END laptop

  # BEGIN desktop
  alias home="cd /home/robert"
  # END desktop

Here is the output from qualia::

  $ qualia <infile
  # BEGIN laptop
  #alias home="cd /home/bob"
  # END laptop

  # BEGIN desktop
  #alias home="cd /home/robert"
  # END desktop

::

  $ qualia laptop <infile
  # BEGIN laptop
  alias home="cd /home/bob"
  # END laptop

  # BEGIN desktop
  #alias home="cd /home/robert"
  # END desktop

::

  $ qualia desktop <infile
  # BEGIN laptop
  #alias home="cd /home/bob"
  # END laptop

  # BEGIN desktop
  alias home="cd /home/robert"
  # END desktop

::

  $ qualia laptop desktop <infile
  # BEGIN laptop
  alias home="cd /home/bob"
  # END laptop

  # BEGIN desktop
  alias home="cd /home/robert"
  # END desktop

qualia is idempotent, so you can run it multiple times; only the last time takes effect::

  $ qualia <infile | qualia laptop | qualia desktop | qualia laptop
  # BEGIN laptop
  alias home="cd /home/bob"
  # END laptop

  # BEGIN desktop
  #alias home="cd /home/robert"
  # END desktop

Using qualia with Git filters
-----------------------------

qualia can be used with `Git filters`_ to automatically uncomment and comment
the right blocks on different computers.

_`Git filters`: https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes

Here's an example setup::

  $ cd ~
  $ git init
  $ git add .bashrc
  $ cat <<EOF >.gitattributes
  * filter=qualia
  .* filter=qualia
  EOF
  $ git add .gitattributes
  $ git commit -m 'Initial commit'

On each of your machines, clone your dotfiles repository and run::

  $ git config filter.qualia.clean qualia
  $ git config filter.qualia.smudge "qualia [qualities]"

Now, whenever you check out, commit, pull and push your dotfiles around, your
machine specific configuration will always be correctly commented and
uncommented on each machine.

Note that because Git applies its filters when files are checked out or
committed, you may need to force Git to apply the filters when you first set
this up::

  $ git checkout HEAD^
  $ git checkout master
