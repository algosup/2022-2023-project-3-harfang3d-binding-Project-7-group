# **Functional Specifications**

<details>
<summary>
Table of contents
</summary>

* [Introduction](#Introduction)
* [Use case](#Use-case)
* [Personas](#Personas)
    * [Anna](#Anna)
    * [John](#John)
* [Objectives](#Objectives)
* [Scope](#Scope)
* [Requirements](#Requirements)
* [Deliverables](#Deliverables)
* [License](#License)
* [Compatibility](#Compatibility)
* [Competitors](#Competitors)
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
The goal of the project is to create an access to [Harfang3D](https://github.com/harfang3d/harfang3d) in Rust. To do that we will need to create a binding between C++ and Rust using [Fabgen](https://github.com/ejulien/FABGen). Fabgen is a tool for generating bindings for C++ libraries. It was written for the Harfang 3D project to bring the C++ engine to languages such as Python, Lua and Go. This document outlines the requirements for the addition of a Rust binding to Fabgen, which will allow Rust programs to use the functionality provided by C++ libraries.

## Use case
* User wants to import a C++ library in Rust

## Personas
![Anna](./images/Persona_Anna.png)
![John](./images/Persona_John.png)


## Objectives
The main objectives of the binding are to:
* Provide Rust programs with access to all of the functions and data structures in C++.
* Be easy to use and integrate into Rust programs, with a clear and simple API that is easy to learn and use.
* Be well-tested, following the templates existing, to ensure that it works correctly and is reliable.
* Be released under an open source license, allowing developers to use and modify it as needed.
* Be as well optimized as possible not to slow down programs using the library

## Scope
The scope of the binding includes:
* All <!-- Fabgen?--> functions and data structures in C++.
* Tests for the binding, including unit and integration tests, following the existing templates of binding, to ensure that it works correctly and is reliable.
* Support for all platforms that Fabgen supports, including Windows, and Linux.
* Documentation for all functions and data structures, including descriptions of their behavior and usage examples.

<!-- ## Out of scope -->

## Requirements
The binding must meet the following requirements:
<!-- * Be implemented as a Rust crate -->
* Provide Rust programs with access to all of the functions and data structures in C++.
* Be easy to use and integrate into Rust programs, with a clear and simple API that is easy to learn and use.
* Be well-tested, with comprehensive unit and integration tests, following the existing templates of binding, to ensure that it works correctly and is reliable.
* Support all platforms that Fabgen supports, including Windows and Linux.
* Be released under an open source license, allowing developers to use and modify it as needed.
* Provide documentation for all functions and data structures, including descriptions of their behavior and usage examples.
<!-- * Be as well optimized as possible not to slow down programs using the library -->

## Risks and Assumptions
The following risks and assumptions have been made:
* Fabgen is a viable solution for generating bindings for C++ libraries.
* Fabgen will be able to generate a binding for the C++ library that is compatible with Rust.
* Fabgen will be able to generate the documentation for the binding.
* The template for the tests is complete and reliable.

## Deliverables
The final deliverables for the binding will include:
<!-- * The Rust crate, including all necessary Rust code and configuration files. -->
* The extension of Fabgen capable of building the Rust library 
* Documentation for the binding, including descriptions of all functions and data structures, usage examples, and any other necessary information.
* Tests for the binding, including unit and integration tests, following the existing templates of binding, to ensure that it works correctly and is reliable.

## Compatibility
The binding should be compatible with the latest stable version of Rust, as well as any earlier versions that are still in active use. It should also be compatible with all platforms that Fabgen supports, including Windows and Linux.

## Competitors
* [FFI (Foreign Function Interface)](https://doc.rust-lang.org/nomicon/ffi.html): Allows Rust programs to call C functions. It is a low-level library that requires the developer to write a lot of unsafe code. It is not compatible with C++ libraries.

* [rustcxx](https://github.com/google/rustcxx): is a Rust library that allows Rust programs to call C++ functions. It is a high-level library that requires the developer to write a lot of unsafe code. It is not compatible with C libraries. It also hasn't been updated since 2016.

* [rust-bindgen](https://rust-lang.github.io/rust-bindgen/): is a Rust library that generates Rust FFI bindings to C and C++ libraries.

## Documentation
The documentation for the binding will be generated automatically by Fabgen, and will include descriptions of all functions and data structures. 

## License
The binding will be released under an open source license, allowing developers to use and modify it as needed.

## Testing
The binding will be tested following the templates existing in the Fabgen project. The tests will include unit and integration tests to ensure that it works correctly and is reliable.
<!-- 
## Deployment
The binding should be distributed as a fork of the existing repository of the Harfang3D C++ API. The fork should include all necessary Rust code and configuration files, and should be kept up to date with the latest version of the C++ API. -->

## Support
Users will be able to file bug reports and feature requests on the project's issue tracker on Github. 

## Conclusion
This functional specification outlines the requirements for the addition of a Rust binding to Fabgen, which will provide Rust programs with access to the functionalities provided by Fabgen. By meeting these requirements, the Rust binding will allow Rust developers to use Harfang3D in their projects, and will provide a safe and idiomatic binding to work with C++ libraries.

## Glossary
* API: An application programming interface, which is a set of routines, protocols, and tools for building software applications.
* Binding: A set of code that allows a program to use the functionality provided by another program.
* Unit test: A test that checks the behavior of a single unit of code, such as a function or class.
* Integration test: A test that checks the behavior of multiple units of code, such as a module or program.
* Library: A collection of code that can be used by other programs.