# Create your own Python package
## Step 0 - Prerequisites

- Install any version of python

## Step 1 - Create some useful files

Python files can be separated into two groups: modules, which are imported by other files, and scripts, which are ran by the python interpreter and serve as an entry point. At any point, a file (even if it is a script) can become a module by importing it

    import my_module
    import my_script

At this point, the entirety of that script/file is ran and its outputs can be access by from the script you're running, and to showcase this, we will create two files: a.py

    foo = 6

and `b.py`
    import a
    print (a.foo)

If we run `a.py`, nothing outputs because only a variable was written to memory. However, if we run `b.py`, we can use the information from `a.py`. There are a few things to note here:

- when we ran `a.py`, it was considered a script
- when we ran `b.py`, it was considered a script, but we imported `a.py`, making it a module in this scenario

Technically, every file is a module because even the script you're running is considered the main module. If we put `print(__name__)` into each of our files and run each of our files, we can see how this works.

With this terminology out of the way, let's now make some useful python files we can eventually turn into packages. For this package, we will create a series of objects that build up to make 3-D geometry, each of which will be in separate files for organization purposes. We will start with vertices:

    class Vertex():
        def __init__(self,x,y,z):
            self.position = [x,y,z]
        
        def distance(self, other):
            sum = 0
            for i,j in zip(self.position,other.position):
                sum += (i+j)**2
            return sum**(1/2)

and edges, which are made up of two vertices:

    import vertex

    class Edge():
        def __init__(self,v1,v2):
            self.vertices = [v1,v2]

        def get_length(self):
            return self.vertices[0].distance(self.vertices[1])

        def bisect(self):
            new_position = [
                (self.vertices[0].position[i]+self.vertices[1].position[i])/2
                for i in range(3)
            ]
            return vertex.Vertex(*new_position)

Each of these are in separate files `vertex.py` and `edge.py`, respectively. Let us put them to the test by creating a line in space and bisecting it in a script called `line.py`

    import vertex
    import edge

    v1 = vertex.Vertex(*[0,0,0])
    v2 = vertex.Vertex(*[1,1,1])
    e1 = edge.Edge(*[v1,v2])

    print(e1.bisect().position)

making sure all the files are in the same folder our command line is in, we can run

    py line.py

## Step 2 - My first package

Let's now create a more organized set of files by organizing them into a package. You have likely seen many packages in your time using Python; some of the most popular are `numpy` or `pandas`. When you import these packages, it looks much the same as when you import a module:

    import numpy
    # vs
    import vertex

The difference between these is that numpy is a collection of modules or even more packages

    import numpy.linalg

It is actually very simple to create our own package; all we have to do is place our modules into a folder called `geometry` with an `__init__.py` file. Now, when we run our `line.py` file, we get an error because the location of our modules have changed and are now withing a package.

We have to change our import statements to

    import geometry.vertex
    import geometry.edge

and to simplify the variables in our file, we can use an alias

    import geometry.vertex as vertex
    import geometry.edge as edge

Congratulations! You've made your first package. If you were the only one to ever use this package, you could stop here and have the organizational benefits of modules and packages, but if you want your code, and specifically your `geometry` package to be used by others, we still have a few more steps to complete.

## Step 3 - Examples, Tests, and their Directories

Usually when someone publishes their code, the reusable parts come from the packages rather than what you originally developed the package to achieve. What I mean by this is that the `line.py` file is too specific and won't be useful to another user, but our `geometry` definitions and classes might be. Instead, our `line.py` file is more useful as an example of how the `geometry` package might be used. Similar to examples, we might want to create additional scripts that test the functionality of the package and leave that code acessible to the person who downloads the package so they can test it themselves. Example and test files are helpful in scientific computing packages/libraries, so if we want to publish our package, we should include them too. Let's quickly create a test file, `test.py`, so that we can have both.

    import geometry.vertex as vertex
    import geometry.edge as edge

    v1 = vertex.Vertex(*[0,0,0])
    v2 = vertex.Vertex(*[1,1,1])
    e1 = edge.Edge(*[v1,v2])

    assert(abs(e1.get_length()-3**(1/2))<1e-5)

Now, we can run the test from our main project directory, and it should pass! However, as we make more tests and examples, they will clutter up the project directory, and we will want to make separate directories for them.

This causes an issue when we run a test or example now because python can't find the package. This has to do with default search locations, which you can modify them manually, but the approach we will take puts our package in one of those default location and puts us one step closer to sharing our package with others. Here is how you would modify your test and examples otherwise

    import sys
    sys.path.append(".")

note when using relative paths, the path starts from where the interpreter is launched


## Step 4 - building your package

To put our `geometry` package in a place python expects to find it, we will want to build and install it. Python isn't a compiled language so it seems weird to talk about building it, but the language actually relies on compiled languages quite often (e.g. numpy uses BLAS). To take out the complications of building the compiled parts of these packages, Python inventied the wheel file, which is essentially everything already compiled and ready to be installed. If you ever install a package, youll probably see something about a wheel.

    pip install numpy
    Collecting numpy
    Using cached numpy-2.0.2-cp39-cp39-win_amd64.whl (15.9 MB)
    Installing collected packages: numpy
    WARNING: The scripts f2py.exe and numpy-config.exe are installed in 'C:\Users\Jacob Pavelka\AppData\Roaming\Python\Python39\Scripts' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    Successfully installed numpy-2.0.2
    WARNING: You are using pip version 22.0.4; however, version 24.3.1 is available.
    You should consider upgrading via the 'C:\Program Files\Python39\python.exe -m pip install --upgrade pip' command.

Of course, if you dont have any components that need to be compiled, you have other options available too, but python will always use a wheel file first if it is available.

Before we can build our package, we will first need to give a little extra information to python. The basic file needed is a `pyproject.toml` (toms obvious markup language) or a `setup.py` (older method), which will contain build information and meta data. `toml` is broken up into categories using brackets `[category 1]`, and in each category, settings can be specified.

    [project]
    name = "example_package_YOUR_USERNAME_HERE"
    version = "0.0.1"


### scr layout vs flat layout

#### src layout
    src/
        package/
    tests/
    docs/

pros
- can fully test the installed version, eliminating issues that can be missed in development

cons

- cannot be easily used from the command line when developing

#### flat layout
    
    package/
    tests/
    docs/
pros
- 

## Step 5 - Extra reading

If you want to see a good standard for laying out scientific computing projects, check out [pyOpenSci](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html)

    myPackageRepoName
    ├── CHANGELOG.md               ┐
    ├── CODE_OF_CONDUCT.md         │
    ├── CONTRIBUTING.md            │
    ├── docs                       │ Package documentation
    │   └── index.md
    │   └── ...                    │
    ├── LICENSE                    │
    ├── README.md                  ┘
    ├── pyproject.toml             ] Package metadata and build configuration
    ├── src                        ┐
    │   └── myPackage              │
    │       ├── __init__.py        │ Package source code
    │       ├── moduleA.py         │
    │       └── moduleB.py         ┘
    └── tests                      ┐
    └── ...                        ┘ Package tests