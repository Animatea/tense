<div id="top"></div>
Project: tense
<br>
License: Apache 2.0
<br>
About: Time Processing Tool
<br>
OS: Independent
<br>
Python: 3.9+
<br>
Typing: Typed
<br>
Topic: Utilities
<br />
    <p align="center">
    <br />
    <a href="https://animatea.github.io/tense/">Documentation</a>
    ·
    <a href="https://github.com/Animatea/tense/issues">Report Bug</a>
    ·
    <a href="https://github.com/Animatea/tense/issues">Request Feature</a>
    </p>
<div id="top"></div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#welcome">Welcome</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#with-pypi">With Pip</a></li>
        <li><a href="#with-poetry">With Poetry</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#built-in-basic">Built-in basics</a></li>
        <li><a href="#reconfiguring-existing-settings">Reconfiguring existing settings</a></li>
        <li><a href="#adding-new-settings">Adding new settings</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </li>
    <li><a href="#examples">Examples</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project
<a href="https://circleci.com/gh/Animatea/tense/tree/main"><img height="20" src="https://dl.circleci.com/status-badge/img/gh/Animatea/tense/tree/main.svg?style=svg"></a>
<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://github.com/psf/black"><img height="20" alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img height="20" alt="Supported python versions" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336">

### Welcome
> Have you ever needed to convert, for example, the string "1d1minute 2 sec" 
to the number of seconds or a datetime.timedelta object?

No? Then advise us to your friends :) And if you really need our tool - let's move on!

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Getting started
### With PyPi
```bash
$ pip3 install tense
```

### With Poetry
```bash
$ poetry add tense
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Usage
### Built-in basic

```py
import datetime
from tense import TenseParser

time_string = "1d2minutes 5 sec"

# <-- Digit parser -->
digit_parser = TenseParser(TenseParser.DIGIT)
assert digit_parser.parse(time_string) == 86525

# <-- Timedelta parser -->
delta_parser = TenseParser(TenseParser.TIMEDELTA)
delta_value = delta_parser.parse(time_string)
# <-- Assertions -->
assert isinstance(delta_value, datetime.timedelta)
assert str(delta_value) == "1 day, 0:02:05"
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

### Reconfiguring existing settings

```py
from tense import TenseParser, from_tense_file_source

config_emulation = """
[model.Tense]
multiplier = 2  # each unit of time will be multiplied by 2
# !!! Note: If the multiplier is <= 0, then the parsers will 
# not work correctly. In this case, a warning will be sent to the console.

[units.Minute]
duration = 120  # Why not?...
aliases = my_minute, my_minutes, my_min, my_mins
"""
parser = TenseParser(
    TenseParser.TIMEDELTA,
    tenses=from_tense_file_source(config_emulation),
)
delta_value = parser.parse("1 my_min 10my_mins 9  my_minutes")
assert str(delta_value) == "1:20:00"  # (each 120 * 2)
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

### Adding new settings

```py
from tense import TenseParser, from_tense_file_source

config_emulation = """
[model.Tense]  # This header is required.

[virtual]
duration = exp(year * 10)
aliases = decade, dec, decs, decades
"""

parser = TenseParser(
    TenseParser.TIMEDELTA,
    tenses=from_tense_file_source(config_emulation),
)
delta_value = parser.parse("1year 10 decades5   seconds")
assert str(delta_value) == "36865 days, 0:00:05"
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

### FAQ
But what if you need to parse a string like: "1day and 10 minutes + 5 seconds"?
Let's see:

```py
>> > from tense import TenseParser

>> > complex_string = "1day and 10 minutes + 5 seconds"

>> > parser = TenseParser(TenseParser.TIMEDELTA)
>> > parser.parse(complex_string)
'0:00:05'
```
Wait... What? 5 second? But there are days and minutes...
- It's okay, you're using flexible tense! This problem is solved in two ways:
  1) You write your own time_resolver and pass it
  2) Choose an existing one from tense.resolvers

Let's demonstrate!
I will use the second option, since the built-in time resolvers in tense are suitable for me.

```py
>> > from tense import TenseParser, resolvers

>> > complex_string = "1day and 10 minutes + 5 seconds"

>> > parser = TenseParser(TenseParser.TIMEDELTA, time_resolver=resolvers.smart_resolver)
>> > parser.parse(complex_string)
'1 day, 0:10:05'
```
Well, that's better!

**tense.application.resolvers.smart_resolver()** is also case insensitive!

```py
>> > from tense import TenseParser, resolvers

>> > complex_string = "1DAY and 10 MINUTES + 5 SECONDS"

>> > parser = TenseParser(TenseParser.TIMEDELTA, time_resolver=resolvers.smart_resolver)
>> > parser.parse(complex_string)
'1 day, 0:10:05'
```

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Examples.
If you think that this is where the possibilities of tense ends, then you are wrong! 
The possibilities of tense are too many for a README, so I suggest you move on to viewing 
the usage examples here:
<p align="center">
<br />
<a href="https://github.com/Animatea/tense/tree/main/examples">Tense Examples</a>
</p>
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

<!-- LICENSE -->
## License

Distributed under the Apache 2.0 License. See [`LICENSE`](https://github.com/Animatea/tense/blob/main/LICENSE) for more information.

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>


<!-- CONTACT -->
## Contact
<div align="left">
    <a href="https://discord.com/invite/KKUFRZCt4f"><img src="https://discordapp.com/api/guilds/744099317836677161/widget.png?style=banner4" alt="" /></a>
</div>

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>


## Acknowledgments
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Python](https://www.python.org)
* [Python Community](https://www.python.org/community/)
* [MkDocs](https://www.mkdocs.org)
* [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>
