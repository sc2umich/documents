# Create your own Python package
## Step 0 - Prerequisites

- Install any version of python

## Step 1 - Create some useful files

Python files can be separated into two groups: modules, which are imported by other files, and scripts, which are ran by the python interpreter and serve as an entry point. At any point, a file (even if it is a script) can become a module by importing it

    import my_module
    import my_script

Modules are usefule because they allow us to better organize and compartmentalize our code. At this point, the entirety of that script/file is ran and its outputs can be access by from the script you're running, and to showcase this, we will create two files: a.py

    foo = 6

and `b.py`

    import a
    foo = 20
    print(foo)
    print (a.foo)

If we run `a.py`, nothing outputs because only a variable was written to memory. However, if we run `b.py`, we can use the information from `a.py`. There are a few things to note here:

- when we ran `a.py`, it was considered a script
- when we ran `b.py`, it was considered a script, but we imported `a.py`, making it a module in this scenario
- we have two variables named foo, but since we used a module, they have separate name spaces (`foo` and `a.foo`) and dont overwrite each other

Technically, every file is a module because even the script you're running is considered the main module. If we put `print(__name__)` into each of our files, we can see how this works.

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

Each of these are in separate files `vertex.py` and `edge.py`, respectively. Let us get some use out of these files by creating a line in space and bisecting it in a script called `line.py`

    import vertex
    import edge

    v1 = vertex.Vertex(*[0,0,0])
    v2 = vertex.Vertex(*[1,1,1])
    e1 = edge.Edge(*[v1,v2])

    print(e1.bisect().position)

making sure all the files are in the same folder our command line is in, we can run

    py line.py

## Step 2 - My first package

Let's now create a more organized set of files by organizing them into a package. Packages are important because they separate the core functionality from use-cases; they separate scripts from modules so that everything you might want to import is in one place. You have likely seen many packages in your time using Python; some of the most popular are `numpy` or `pandas`. When you import these packages, it looks much the same as when you import a module:

    import numpy
    # vs
    import vertex

The difference between these is that numpy is a collection of modules or even more packages:

    import numpy.linalg

It is actually very simple to create our own package; all we have to do is place our modules into a folder called `geometry_uniqname` with an `__init__.py` file. Now, when we run our `line.py` file, we get an error because the location of our modules have changed and are now withing a package.

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

To put our `geometry` package in a place python expects to find it, we will want to build and install it. Python isn't a compiled language so it seems weird to talk about building it, but the language actually relies on compiled languages quite often (e.g. numpy uses BLAS). To take out the complications of building the compiled parts of these packages (see the CMAKE tutorial), Python inventied the wheel file, which is essentially everything already compiled and ready to be installed. If you ever install a package, youll probably see something about a wheel.

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

Before we can build our package, we will first need to give a little extra information to python. The basic file needed is a `pyproject.toml` (toms obvious, minimal language) or a `setup.py` (older method), which will contain build information and meta data. `toml` is broken up into tables using brackets `[category 1]`, and in each, key/value pairs can be specified to change settings.

    [project]
    name = "example_package_YOUR_USERNAME_HERE"
    version = "0.0.1"

The important tables to define are:
 - `[build-system]`: defines which "backend" build system and build dependencies you will used to create wheels
 - `[project]`: Project metadata (e.g. author, name, versions supprted)
 - `[project.optional-dependencies]`: additional dependencies (e.g. numpy) if the user wants to take advantage of special features (e.g. fast matmul). The standard dependencies will be located in the `[project]` table.

Here is our minimum working example:

    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [project]
    name = "geometry_[uniqname]"
    version = "0.0.1"
    authors = [
    { name="your name", email="uniqname@umich.edu" },
    ]
    description = "A small example package"
    requires-python = ">= your version"
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
    license = "MIT"
    dependencies = [
        ...
    ]

Now that we have that basic information set up, python will know how to build our package, allowing it to make a wheel file and also a compressed folder of all of our source files (this is the other method of sharing code). First we need to install the build module from python. If you are on linux or macOS and didn't install from source, you might have to install pip separately (`apt install python3-pip`)

    py -m pip install build
    py -m build

We did it! Now, we just need to install it, which requires the `wheel` package if you don't already have it.

    py -m pip list
    py -m pip install whl  
    py -m pip list

Share the `wheel` and `tar.gz` with all your friends! They can install it in the same way. We can verify this works by running our previous test, and you will see that even if we delete our original source files, the test still passes!

## Step 5 - Edit mode installation

Snap, you made a mistake in your development and now you have to rebuild and reinstall the package. This can be a tedious process

    py -m build
    py -m pip install dist\geometry_jpavelka-0.0.1-py3-none-any.whl --force-reinstall

Thankfully, there is an "edit mode", which is a much easier way to use an installed package without having to rebuild it constantly. To install your package in edit mode add the `-e` flag to your pip install with the target being the directory of the package

    py -m pip install . -e

Now, we can change the source files in the installed version of the package, which ideal for developement where updates, testing, and mistakes are cyclical.

## Step 6 - uploading to a repository

Now we want to make our package easily installable for others by uploading it to a repository. The most famous python repository is the python package index or PyPI (this is where pip pulls packages from), but conda and source forge are also common. 

Additionally, you can upload it to your github page for people to download and install manually.

Here we will briefly cover how to upload it to a test version of PyPI, essentially following this [guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives), but be warned, it takes some time to set up your user account with 2FA and all.

First, make sure pip, twine, and package are up to date

    py -m pip install -U pip
    py -m pip install -U package
    py -m pip install -U twine

then simply use twine with the correct arguments to upload the package. You will have to enter your api key to successfully upload.

    py -m twine upload --repository testpypi dist/*

Now we can test out the download, but there will be a few more steps since we uploaded our package to the test directory instead of the real one.

    py -m pip install --index-url https://test.pypi.org/simple/ geometry_jpavelka


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

### scr layout vs flat layout

#### src layout
    .
    ├── README.md
    ├── noxfile.py
    ├── pyproject.toml
    ├── setup.py
    ├── src/
    │    └── awesome_package/
    │       ├── __init__.py
    │       └── module.py
    └── tools/
        ├── generate_awesomeness.py
        └── decrease_world_suck.py

pros
- can fully test the installed version, eliminating issues that can be missed in development

cons

- cannot be easily used from the command line when developing

#### flat layout
    .
    ├── README.md
    ├── noxfile.py
    ├── pyproject.toml
    ├── setup.py
    ├── awesome_package/
    │   ├── __init__.py
    │   └── module.py
    └── tools/
        ├── generate_awesomeness.py
        └── decrease_world_suck.py
pros
- can run package from command line

cons
- adds readme and other configration files on the import path

## Sources
[Python Packaging User Guide](https://packaging.python.org/en/latest/)

[pyOpenSci Packaging User Guide](https://www.pyopensci.org/python-package-guide/package-structure-code/intro.html)
