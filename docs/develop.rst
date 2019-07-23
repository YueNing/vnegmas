.. _develop:

###########################
Development Tutorial
###########################

****************************
Monitor
****************************

| This module is the entrance from NEGMAS to VNEGMAS.
  monitor module of VNEGMAS contains three parts.

- Online Serial

| Base on this mode, that means we decide to use **serial** in NEGMAS, use world call back function of NEGMAS to send the data.
  the description of this mode is here `serial NEGMAS <https://negmas.readthedocs.io/en/stable/api/negmas.apps.scml.anac2019_tournament.html?highlight=serial#anac2019-tournament>`_

- Online File

| In this mode, use a monitor function watch_fs,
  call it from vnegmas.backend.api.configs. base on class NegmasMonitorFile,
  can detect the file system changed.

- Online Memory

| In this mode, combine the api between NEGMAS and VNEGMAS,
  can at the same time get multiple world data. (Developing)


******************************
Negmas Data Bridge
******************************

| Use this module to receive data from NEGMAS.
  Data type can receive from NEGMAS use Negmas Data Bridge.

    - negotiation
        * save_negotiations
    - contract
        * save_signed_contracts
        * save_cancelled_contracts
    - breach
        * save_resolved_breaches
        * save_unresolved_breaches

******************************
Data VNegmas Bridge
******************************

| Use this module to send data to VNEGMAS.
  Data type can be sended to VNEGMAS use Data VNegmas Bridge.

    - specific List
    - specific Dict

| Chart type can be used in VNEGMAS, also use Data VNegmas
  Bridge to tell the VNEGMAS.

    - Bar
    - Line
    - Graph
    - 3D Bar

******************************
Event Engine
******************************

| The main idea of this module is a simple framework used for sending data to the module of Analyse. decouple the data and Analyse.
  later can simply add new Event(new type data) and send to module Analyse.

******************************
Analyse and Process
******************************

| The data that received from event publisher may not be the data that can be combined with Pyecharts.
  So use this module to deal with data. Prepare for
  the next module Data Pyecharts.

******************************
Data Pyecharts
******************************

| Use Pyecharts to define the type of charts.

******************************************
Communication between backend and frontend
******************************************

| Use Flask

**************************************
Website Design and Interface
**************************************

| ECharts, Bootstrap, JQuery, Html, CSS

