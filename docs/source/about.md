# Loom

Submission for langjam#0001

I have been exploring literate programming and animation, the past few months so the langjam topic came as a surprise! While the initial goal was to build something like docco, I realised I could do an animation inside comments using a dsl. This is a prototype of an animated approach to literate programming first invented by Don Knuth. The code rendering time is long with terminalizer which I had not anticipated. There is an option that will strip code and store comment sequences inside a sqlite for fun and its used to explore a new metric of code quality - lines of comment / lines of code.

first-class comments (interpretation): treat comment sequences as a value that can be freely passed, stored, serialized ... like python dictionaries + pickle or integers. A comment sequence is something separated by 0-width indentation of  codeblocks for now.

Examples include - hello-world and fibonacci

```{todo}
Explore if this is feasible for larger pre-existing codebases.
Add support for C style comments.
```

Limitations - some edge cases need to be explored.

# Is this a quine ?

# Instructions

```sh
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python loom.py test.py
```

Utilities for animation,

```sh
brew install cowsay
npm install -g terminalizer 
```

```sh
python source/loom.py --generate-docs fibonacci build1 # builds the db and docco like docs with sphinx
python source/loom.py --comment-stats # previous step is needed to create the database
python source/loom.py --generate-terminal-show fibonacci build2 3
python source/loom.py --clean-source < hello-world/test.py
```

# License Support

Unless stated otherwise, all source code in this document and the documentation itself is under the [Creative Commons Attribution Non Commercial No Derivatives](https://creativecommons.org/licenses/by-nc-nd/4.0) license.

<script src="https://gumroad.com/js/gumroad.js"></script>
<a class="gumroad-button" href="https://gumroad.com/l/pkoQc">Support Loom on Gumroad</a>

# About

I'm xyzzy! I'm a web developer into music and #creativeprogramming. I'm a solopreneur. Checkout my [apps](https://xyzzyapps.link) where I explore "procedural" literate programming to build practical apps. I have written a literate programming tool with the help of [cog preprocessor](https://nedbatchelder.com/code/cog/) called wheel. I am exploring 3d animation with blender and using python as a replacement for cpp in [raptor](https://xyzzyapps.link) these days ^_^



