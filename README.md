[![Build Status](https://travis-ci.org/job/rpki-vrp-checker.svg?branch=master)](https://travis-ci.org/job/rpki-vrp-checker)
[![Requirements Status](https://requires.io/github/job/rpki-vrp-checker/requirements.svg?branch=master)](https://requires.io/github/job/rpki-vrp-checker/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/job/rpki-vrp-checker/badge.svg?branch=master)](https://coveralls.io/github/job/rpki-vrp-checker?branch=master)

RPKI VRP Checker
================

The `rpki-vrp-checker` utility takes a set of VRPs (in JSON format)
and applies a number of tests to the VRP set to assess whether
the set conforms to the Network Operator's expectations.

Features
--------

* Apply SLURM filters
* Canary checking (assert whether expected ROAs are part of the VRP set)
* ...

Usage
-----

```
$ pip3 install rpki-vrp-checker
$ rpki-vrp-checker -i ./export.json -o blessed-vrp-set.json
```
