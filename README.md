[![Build Status](https://travis-ci.org/solarnz/polygamy.png?branch=master)](https://travis-ci.org/solarnz/polygamy)[![Stories in Ready](http://badge.waffle.io/solarnz/polygamy.png)](http://waffle.io/solarnz/polygamy)  
polygamy
====

A tool to handle the management of multiple git repositories.

Installation
------------
`pip install git+https://github.com/solarnz/polygamy`

Configuration
-------------
`.polygamy.json`
```json
{
    "remotes": {
        "github": {
            "url": "git@github.com:",
            "branch": "master"
        }
    },
    "repos": {
        "molokai": {
            "remote": "github",
            "name": "/solarnz/molokai"
        }
    }
}
```
Usage
-----
`polygamy` in the same directory that the .polygamy.json file is in.

Licence
-------

BSD 2-Clause Licensed.


Copyright (c) 2014, Christopher Trotman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
