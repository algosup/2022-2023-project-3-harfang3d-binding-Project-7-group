# **Functional Specifications**

<details>
<summary>
Table of contents
</summary>

* [Introduction](#Introduction)
* [Objectives](#Objectives)
* [Scope](#Scope)
* [Requirement](#Requirement)
* [Deliverables](#Deliverables)
* [License](#License)
* [Compatibility](#Compatibility)
* [Documentation](#Documentation)
* [Testing](#Testing)
* [Support](#Support)
* [Conclusion](#Conclusion)
* [Glossary](#Glossary)
</details>

## Project Team

| Members         | Roles             |
| --------------- | ----------------- |
| [Ivan Molnar](https://github.com/ivan-molnar)        | Project Manager   |
| [Mathis Kakal](https://github.com/mathiskakal)       | Tech Lead         |
| [Maxime Pages](https://github.com/MaximePagesAlgoSup)| Software Engineer |
| [Matieu Chaput](https://github.com/Chaput-Mathieu)   | Program Manager   |



## Introduction
The goal of the project is to create an access to [Harfang3D](https://github.com/harfang3d/harfang3d) in rust. To do that we will need to create a binding between c++ and rust using [FABgen](https://github.com/ejulien/FABGen). FABgen is a tool for generating bindings for C++ libraries.
It is written in Python and is available on GitHub under an open source license. This document outlines the requirements for the addition of a Rust binding to FABgen, which will allow Rust programs to use the functionality provided by C++ libraries.

## Objectives
The main objectives of the binding are to:
* Provide Rust programs with access to all of the functions and data structures in C++.
* Be easy to use and integrate into Rust programs, with a clear and simple API that is easy to learn and use.
* Be well-tested, following the templates existing, to ensure that it works correctly and is reliable.
* Be released under an open source license, allowing developers to use and modify it as needed.

## Scope
The scope of the binding includes:
* All functions and data structures in C++.
* Support for all platforms that FABgen supports, including Windows, and Linux.
* Documentation for all functions and data structures, including descriptions of their behavior and usage examples.

## Requirements
The binding must meet the following requirements:
* Provide Rust programs with access to all of the functions and data structures in C++.
<!-- * Be implemented as a Rust crate -->
* Support all platforms that FABgen supports, including Windows and Linux.
* Provide documentation for all functions and data structures, including descriptions of their behavior and usage examples.
* Be easy to use and integrate into Rust programs, with a clear and simple API that is easy to learn and use.
* Be well-tested, with comprehensive unit and integration tests, following the existing templates of binding, to ensure that it works correctly and is reliable.
* Be released under an open source license, allowing developers to use and modify it as needed.

## Risks and Assumptions
The following risks and assumptions have been made:
* FABgen is a viable solution for generating bindings for C++ libraries.
* FABgen will be able to generate a binding for the C++ library that is compatible with Rust.
* FABgen will be able to generate the documentation for the binding.
* The template for the tests is complete and reliable.

## Deliverables
The final deliverables for the binding will include:
<!-- * The Rust crate, including all necessary Rust code and configuration files. -->
* Documentation for the binding, including descriptions of all functions and data structures, usage examples, and any other necessary information.
* Tests for the binding, including unit and integration tests, following the existing templates of binding, to ensure that it works correctly and is reliable.

## Compatibility
The binding should be compatible with the latest stable version of Rust, as well as any earlier versions that are still in active use.

## Documentation
The documentation for the binding will be generated automatically by FABgen, and will include descriptions of all functions and data structures.

## License
The binding will be released under an open source license, allowing developers to use and modify it as needed. 

## Testing
The binding will be tested following the templates existing in the FABgen project. The tests will include unit and integration tests to ensure that it works correctly and is reliable.
<!-- 
## Deployment
The binding should be distributed as a fork of the existing repository of the Harfang3D C++ API. The fork should include all necessary Rust code and configuration files, and should be kept up to date with the latest version of the C++ API. -->

## Support
Users will be able to file bug reports and feature requests on the project's issue tracker on Github.

## Conclusion
This functional specification outlines the requirements for the addition of a Rust binding to FABgen, which will provide Rust programs with access to the functionality provided by the FABgen Python module. By meeting these requirements, the Rust binding will allow Rust developers to use FABgen in their projects, and will provide a safe and idiomatic binding to work with C++.
<!-- ## Overview -->
<!-- ## Design Goals -->
<!-- ## Walkthrough -->

## Glossary
* API: An application programming interface, which is a set of routines, protocols, and tools for building software applications.
* Binding: A set of code that allows a program to use the functionality provided by another program.
* Unit test: A test that checks the behavior of a single unit of code, such as a function or class.
* Integration test: A test that checks the behavior of multiple units of code, such as a module or program.