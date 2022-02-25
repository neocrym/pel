# Pel is the most elegant build system
## Introduction

Pel is an easy-to-use build system/task runner written in Python. It is designed to be more advanced than task runners like [Make](https://www.gnu.org/software/make/) or [Invoke](https://www.pyinvoke.org/), but much simpler than complex build systems like [CMake](https://cmake.org/) or [Bazel](https://bazel.build/).

## Installation

### Installation from pip

```
pip3 install --user pel
```

It is safe to install Pel as a global Python package. **Installing Pel will never modify any other Python packages on your computer.**

## Development status

Pel is still in the early stages of development. It is not currently ready for production use.

## Features

### Cross-platform support

Pel is written in pure Python, and is intended to work on any operating system supported by Python, such as:
* Linux
* Windows
* macOS
* FreeBSD

## Why we made Pel

Most build systems are either **too simple** or **too complex**.

 * A **simple** build system, like [Make](https://www.gnu.org/software/make/) or [Invoke](https://www.pyinvoke.org/) makes it easy to run arbitrary shell commands, but makes it hard to add non-trivial dependency management and build caching
 * A **complex** build system, like [CMake](https://cmake.org/) or [Bazel](https://bazel.build/), offers sophisticated dependency management and build caching, but only for predefined types of build targets. These build systems are excellent choices for building a large C++ monorepo, but can be unwieldy to integrate with arbitrary commands and obscure build tools.

Pel is designed to be the happy medium between simple and complex.
