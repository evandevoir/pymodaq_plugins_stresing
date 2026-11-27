pymodaq_plugins_template
########################

.. the following must be adapted to your developed package, links to pypi, github  description...

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_template.svg
   :target: https://pypi.org/project/pymodaq_plugins_template/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_template/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/PyMoDAQ/pymodaq_plugins_template
   :alt: Publication Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_template/actions/workflows/Test.yml/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_template/actions/workflows/Test.yml


This template implements the Stresing camera FLCC3001 in pymodaq.
This branch targets **PyMoDAQ 5.3.x** (Python 3.11 to 3.14). Use the branch matching your PyMoDAQ version.

Authors
=======

* Eliott Vandevoir  (eliott.vandevoir@ens-lyon.fr)


.. if needed use this field

    Contributors
    ============

    * First Contributor
    * Other Contributors

.. if needed use this field

  Depending on the plugin type, delete/complete the fields below


Instruments
===========

Below is the list of instruments included in this plugin

Viewer1D
++++++++

* **FLCC3001**: control of FLCC3001 1D detector


Installation instructions
=========================

* PyMoDAQ’s version: 5.3.14
* Operating system’s version.
* Stresing python already contains all the files needed.
* The config.ini file in src/pymodaq_plugins_stresing/hardware must be modified according to your setup.


Development
===========

* Install your plugin in editable mode: ``pip install -e .``
* Check it, without any hardware: ``check_plugin`` (and ``pytest``)
* If you use an AI coding assistant, point it to ``AGENTS.md``: it describes the patterns to follow for instrument
  plugins, Dashboard extensions (``CustomExt``, whenever instruments are involved) and standalone apps
  (``CustomApp``, only if no instruments are needed).
