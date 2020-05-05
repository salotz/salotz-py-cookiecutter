.. created by sphinx-quickstart
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

{{cookiecutter.project_name}} : {{cookiecutter.project_description}}
====================================================

.. optional logo here
   .. image:: /_static/logo.svg
      :width: 450 pt
      :align: center
      :target: https://{{owner_nickname}}.github.io/{{cookiecutter.project_name}}/

Getting Started
---------------

.. toctree::
   :maxdepth: 1

   source/introduction
   source/installation
   source/quick_start

Software Documentation
----------------------

.. toctree::
   :maxdepth: 1
      
   _source/tutorials/index
   _source/users_guide
   _source/howtos
   _source/troubleshooting
   _source/reference              
   _source/glossary
   API Overview <_source/api>
   Full API <_api/modules>
              

Project & Developer Information
-------------------------------

.. toctree::
   :maxdepth: 1
              
   _source/general_info
   _source/news
   _source/changelog
   _source/dev_guide


Metrics, Reports, & Dashboards
------------------------------

`Performance Regressions <regressions/index.html>`_

`Code Quality <quality/index.html>`_

`Test Coverage <coverage/index.html>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
