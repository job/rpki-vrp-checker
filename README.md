[![Requirements Status](https://requires.io/github/job/rpki-vrp-checker/requirements.svg?branch=master)](https://requires.io/github/job/rpki-vrp-checker/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/job/rpki-vrp-checker/badge.svg?branch=master)](https://coveralls.io/github/job/rpki-vrp-checker?branch=master)

RPKI VRP Checker
================

The `rpki-vrp-checker` utility takes a set of VRPs (in JSON format)
and applies a number of tests to the VRP set to assess whether
the set conforms to the Network Operator's expectations.

Features
--------

* Canary checking (assert whether expected ROAs are part of the VRP set)
* ...

Usage
-----

```
$ pip3 install rpki-vrp-checker
$ rpki-vrp-checker -i data/to-be-considered-vrp-set.json -b /tmp/not_yet_implemented -c data/canaries.yaml
ERROR: WRONG AT RIR LEVEL?
--------------------------

The following RPKI VRPs have been registered at the RIR level,
but were not added as canaries:

Entry #1:
  Prefix       : 204.2.255.0/25 (MaxLength: 25)
  Origin AS    : 20940
  Trust Anchor : ARIN

Entry #2:
  Prefix       : 2001:67c:208c::/48 (MaxLength: 48)
  Origin AS    : 15562
  Trust Anchor : RIPE

ERROR: MISSING VIPAR RPKI CANARY REGISTRATIONS?
-----------------------------------------------

The following canaries are not visible in RPKI data at the RIR level:

Entry #1:
  Prefix       : 2001:67c:208c::/48 (MaxLength: 48)
  Origin AS    : 15562
  Trust Anchor : ARIN

$
```

Purpose
-------

There are various types of human error, operational failures, or attack
scenarios related to RPKI pipeline operations imaginable. This utility is
intended to be a verification tool between an internal ROA administration and
the RPKI data as published on the Internet.

Comparing "ROAs that are expected to exist" with Validated ROA Payloads as
observed from RPKI data can help in cases such as:

* Resource holder has ARIN IP prefixes, and ARIN CA has [encoding issues](https://www.arin.net/announcements/20200813/)
* Compromise of RIR systems (sudden appareance of ROAs covering an operator's resources under the wrong Trust Anchor)
* Fat fingering during ROA creation process (too many or too little ROAs were actually created compared to the internal administration)
