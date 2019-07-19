
.. VNEMGAS documentation master file, created by
   sphinx-quickstart on Wed Jul 17 17:22:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _index:

####################################
Welcome to VNEMGAS's documentation!
####################################

The main purpose of VNEMGAS development  is serviced for visualization of `NEGMAS <https://github.com/yasserfarouk/negmas>`_ and for data analyser of NEGMAS.

**************************************************
Basic framework and relative technology of VNEMGAS
**************************************************

| **About web framework:** NEGMAS is written with Python. So the first choice is a framework that is also written with Python.
  Django and FLASK are both modern framework.
  Contrast the Django, FLASK is a micro web framework.
  it does not require particular tools or libraries.
  For visualization of NEGMAS,FLASK is a better and enough tool.

| **About charts:** PYECHARTS(python package) to realize the transformation of data to charts.
  ECHARTS(javascript) render and interact charts in site.
  Many libraries can be selected for realization of render of charts,
  such as charts.js, d3.js, Highcharts and so on.
  But advantages of ECHARTS is the powerful Graph chart and can connect
  with PYECHARTS effective. That means Developer don not care about so
  much javascript code, just finally use it to render.
  Use python to define the data and attributes of charts.

| **About specific chart, Graph:** NETWORKX(python package) is a useful module that has kinds of function
  and class that used for definition of Graph. such as nodes, links and
  the timing information. The corresponding information in NEGMAS
  are factories, contracts and the timing information of
  contracts(step information). don not need
  to define the data structure information of Graph.

***********************************
How To Use (Quick Start)
***********************************

For User
===================================

| Introduction: User care about which information of NEGMAS that
  can see in VNEMGAS. So either use pip or
  download the source file to get the module vnegmas.
  And then create a simple python file,
  import this module, call the run function of vnegmas
  module. Below is relative command and code.

- Use pip to download

.. code-block:: bash

    pip install vnegmas

- latest source code download

.. code-block:: bash

    git clone https://github.com/YueNing/vnegmas.git
    pip install -r requirements.txt

- download the stable compressed release package at the release page of `GITHUB release <https://github.com/YueNing/vnegmas/releases>`_

Run VNEMGAS
------------------------------------

| create a python file and write the following code,
  all code here `quickstart <https://github.com/YueNing/vnegmas/tree/master/test/quickstart.py>`_

.. code-block:: python

    from vnegmas import VNegmas
    vnegmas = VNegmas(name="VNegmas")
    vnegmas.run()

For Data Analyser
=====================================

| Introduction: Data Analyser need to analyse data that received from NEGMAS,
  so in this section, introduce the process
  that how to receive data from NEGMAS, the structure of data,
  how to send the data that be processed to vnegmas,
  the structure of data that after processed and some specific
  interface. Finally, data analyser can simply and quickly get
  the data that be needed, and send the data to vnegmas.

| When you want to know the details of the dataflow of vnegmas, this page is useful. :ref:`dataflow`
  Otherwise, you can skip this page. Look below.

| Below is relative command and code(example).

- Receive data from NEGMAS

.. code-block:: python

    import vnegmas
    from vnegmas import NegmasDataBridge, DataVNegmasBridge
    n_d_b = NegmasDataBridge()
    data  = n_d_b.get_data(type="breach")

- Send data to VNEMGAS and Add specific chart into VNEMGAS

.. code-block:: python

    d_b_b = DataVNegmasBridge()

    def get_sum(data):
        sum = 0
        for index, value in enumerate(data):
            sum = sum + value
            yield index, sum

    def process_average(data):
        sum = get_sum(data)
        average = []
        for _ in range(len(data)):
            index, value = next(sum)
            average.append(value / (index+1))
        return average

    """ processFunc function is some function that is
    predefined or defined by data analyser that
    used for process the data that received from NEGMAS.
    here is a example that use process_average() to get the
    average of breach after every simulation step """

    d_b_b.register(data=data, name="breach_average"
                    chart_type='Bar', processFunc=process)

- Run the VNEMGAS

.. code-block:: python

    vnegmas.run()


:ref:`api`

For Developer of VNEMGAS
=====================================

| Introduction: More participants can make the system more perfect. So in this section will
  explain the whole system and try to make development in the future
  more easier and available. vnegmas of this version contains
  mainly Below parts:

- Monitor
- NegmasDataBridge
- DataVNegmasBridge
- EventEngine(send data to Analyse module)
- Analyse and Process(verify the Data, pick up Data)
- Data-Pyecharts
- Communication between backend and frontend
- Website Design and Interface

| reduce the small parts, mainly three parts are monitor negmas,
  data analyse middle layer and view layout.

The description of every module, please go to this page :ref:`develop`

.. toctree::
   :maxdepth: 2

   use
   dataflow
   develop
   api


Indices and tables
==================

* :ref:`index`
* :ref:`develop`
* :ref:`search`
