<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> :book: Table of Contents</h2>

<details>
    <summary><em>click to expand...</em></summary>
    <ol>
	    <li><a href="#introduction"> ➤ Introduction</a>
		    <ul>
			    <li><a href="#document-tracking-and-version-revision-history">➭ Document Tracking and version (Revision History)</a></li>
			    <li><a href="#purpose-of-document">➭ Purpose of Document</a>
					<ul>
						<li><a href="#global-definition">➧ Global Definition</a></li>
						<li><a href="#benefits-to-engineers">➧ Benefits to engineers</a></li>
						<li><a href="#benefits-to-the-team">➧ Benefits to the team</a></li>
					</ul>
			    </li>
			    <li><a href="#points-of-contact">➭ Points of Contact</a>
			    	<ul>
					<li><a href="#points-of-contact-1">➧ Points of Contact</a></li>
					<li><a href="#authors-roles-etc">➧ Authors, roles etc.</a></li>
					<li><a href="#reviewers">➧ Reviewers</a></li>
			    	</ul>
			    </li>
			    <li><a href="#project-overview">➭ Project Overview</a>
			    	<ul>
					<li><a href="#contextbackground">➧ Context/Background</a>
						<ul>
							<li><a href="#project-genesis">Project Genesis</a></li>
							<li><a href="#methodology-dmaic-framework">Methodology (DMAIC Framework)</a></li>
							<li><a href="#what-is-harfang-3d-">What is HARFANG 3D ?</a></li>
							<li><a href="#what-is-a-code-binder-used-for-">What is a code binder used for ?</a></li>
							<li><a href="#existing-solutions--similar-technologies">Existing Solutions & Similar technologies</a></li>
						</ul>
					</li>
					<li><a href="#goals-productclient-requirements">➧ Goals, Product/Client requirements</a>
						<ul>
							<li><a href="#functional-requirements">Functional Requirements</a></li>
							<li><a href="#scope">Scope</a></li>
							<li><a href="#quality-assurance-expectations">Quality Assurance Expectations</a></li>
							<li><a href="#license">License</a></li>
						</ul>
					</li>
					<li><a href="#assumptions--constraints">➧ Assumptions & Constraints</a></li>
		    		</ul>
			    </li>
			    <li><a href="#glossary">➭ Glossary</a></li>
		    </ul>
	    </li>
    <li><a href="#proposed-solution"> ➤ Proposed Solution</a>
	<ul>
		<li><a href="#dependencies--external-elements">➭ Dependencies & External Elements</a></li>
		<li><a href="#architecture-diagrams">➭ Architecture Diagrams</a>
			<ul>
				<li><a href="#main-architecture">➧ Main Architecture</a></li>
				<li><a href="#example-of-a-binding">➧ Example of a Binding</a></li>
				<li><a href="#example-of-a-test">➧ Example of a Test</a></li>
			</ul>
		</li>
		<li><a href="#technical-specifications">➭ Technical Specifications</a>
			<ul>
				<li><a href="#conversion-tables">➧ Conversion Tables</a></li>
				<li><a href="#idiomatic-writing">➧ Idiomatic Writing</a></li>
				<li><a href="#step-by-step-build">➧ Step by Step Build</a>
					<ul>
						<li><a href="#new-folder-structure">New Folder Structure</a></li>
					</ul>
				</li>
			</ul>
		</li>
		<li><a href="#risk-assessment-and-security-risksmeasures">➭ Risk assessment and security risks/measures</a>
			<ul>
				<li><a href="#risk-prevention-matrix">➧ Risk Prevention Matrix</a></li>
				<li><a href="#rollback-plan">➧ Rollback Plan</a></li>
			</ul>
		</li>
		<li><a href="#performance">➭ Performance</a></li>
		<li><a href="#pros-and-cons">➭ Pros and Cons</a></li>
		<li><a href="#alternate-designs-or-solutions">➭ Alternate designs or solutions</a></li>
	</ul>
    </li>
    <li><a href="#development--maintenance"> ➤ Development & Maintenance</a>
	<ul>
		<li><a href="#schedule-of-development">➭ Schedule of development</a>
			<ul>
				<li><a href="#planning">➧ Planning</a></li>
				<li><a href="#efforts-and-costs">➧ Efforts & Costs</a></li>
			</ul>
		</li>
		<li><a href="#success-assessment">➭ Success Assessment</a>
			<ul>
				<li><a href="#impact">➧ Impact</a></li>
				<li><a href="#metrics">➧ Metrics</a></li>
			</ul>
		</li>
		<li><a href="#cicd-pipeline">➭ CI/CD Pipeline</a></li>
	</ul>
    </li>
    <li><a href="#conclusion"> ➤ Conclusion</a>
	<ul>
		<li><a href="#future-improvements">➭ Future Improvements</a></li>
		<li><a href="#end-matter">➭ End Matter</a>
			<ul>
				<li><a href="#footnotes">➧ Footnotes</a></li>
				<li><a href="#acknowledgements">➧ Acknowledgments</a></li>
			</ul>
		</li>
	</ul>
    </li>
    </ol>
</details>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


# Introduction
- ## Document Tracking and version (Revision History)
- |Version n°|Edits completed by|Date|Description of edit|
	|--|--|--|--|
	|0.1.0|Mathis KAKAL|11.01.2023|Initial Document Outline|
	|0.2.0|Mathis KAKAL|17.01.2023|Added all introduction except Project overview and Glossary |
	|0.3.0|Mathis KAKAL; Ivan MOLNAR|07.02.2023|Finish Introduction, Development and Conclusion|
	|0.4.0|Mathis KAKAL|13.02.2023|Added Technical Specifications|
	|0.5.0|Mathis KAKAL|14.02.2023|Added Architecture Diagrams; updated Glossary; Minor changes|
- ## Purpose of Document
- ### Global definition
	- The purpose of this Technical Specifications Document (TSD) is to present the stakeholders with the technical discussion and choices made for the implementation of a new programming language (Rust), to the already existing FABGen code binding generator, completely, accurately and unambiguously in the most concrete way possible. This information is the work of the Tech Lead during the the second and third week of the project (ideation phase), and was updated few times during the development phases. It is derived from the Functional Requirements (FRD) which state what should and shouldn't be implemented.
	- Finally, the Technical Specifications Document contributes to splitting our work with Harfang into multiple domains. Having the Technical domain separated from the Functional one, allows us to tailor, debug and develop the solution faster to tackle either business, functional or technical issues distinctively.
- ### Benefits to engineers
	- For engineers, the TSD outlines the specific requirements and constraints for the product. It serves as a clear and detailed guide to follow as they design and develop it. The specifications can include information on materials, design criteria, performance requirements, and testing procedures, among other things.
	- Having a technical specifications document in place helps ensure that the final product meets the desired specifications and that all members of the team are working towards the same goal. As such, it should alleviate responsibility of the choices from the engineers, so they can focus solely on the implementation of the product and its quality.
- ### Benefits to the team
	- Technical specs, because they are a thorough view of the proposed solution, also serve as documentation for the project, both  for the implementation phase and after, to communicate the projects accomplishments.
	- Moreover, it saves the team from repeatedly explaining design and technical choices to teammates and other stakeholders.
		A well-written specification document will allow the team to arrive at a mutual understanding regarding the technical aspects of the project and development process.
- ## Points of contact
- ### Points of Contact
	- | Ivan MOLNAR| Project Manager | ivan.molnar@algosup.com |
		|--|--|--|
		| Mathieu CHAPUT| Program Manager | mathieu.chaput@algosup.com |
		| Franck JEANNIN| Algosup CEO & Project overseer | franck.jeannin@algosup.com |
		| Mathis KAKAL| Tech Lead| mathis.kakal@algosup.com |
- ### Authors, roles etc.
	- | **Deliverable**| **Author**| **E-mail address**|
		|--|--|--|
		| *Functional Requirements Document*| Mathieu CHAPUT (Program Manager) | mathieu.chaput@algosup.com|
		| *Technical Requirements Document*| Mathis KAKAL (Tech Lead)| mathis.kakal@algosup.com |
		| *Quality Assurance Document*| **Undefined**| **Undefined** |
- ### Reviewers  
	- This Document has been reviewed by the whole team thanks to our small numbers, allowing for accuracy in the rendition of the specifications. This excludes a designated quality assurance manager/engineer for establishing which functions and KPI's to monitor and test, task that will be performed by the whole team. The program manager will also review the Technical Requirements Document for iteration with the the Functional Requirements, the project manager to ensure compliance with the project's expectations and finally the software engineer to ensure that it is in a language that they can understand and to develop the product.
- ## Project Overview
- ### Context/Background
	- ### Project Genesis
	- This project was initiated on Tuesday, January 3rd 2023 as a collaboration between the customer, **HARFANG**® **3D**, a french company known for developing real-time 3D visualization tools and **ALGOSUP**, the *international software development school*.
	- As stated in the Functional Requirements Document (FSD), the main goal of this project is to be able to use **HARFANG® 3D Framework** library, which is implemented in C/C++ in Rust language, through the use of their custom made code binder **FABGen** (designed as a replacement for SWIG) which already supports transpiling to CPython, Lua and Go. Therefore, the code binder can be described as an interface generator, more specifically as an Application Binary Interface generator, as it has to interface between two languages at low levels. This implies good knowledge of source and target languages, since (especially in the case of C/C++  Rust) where syntax and functioning greatly differ.
	- ### Methodology (DMAIC Framework)
	- Although the project consists mostly of identifying code implementations, writing them and passing predefined tests, we made sure to follow the DMAIC framework seen during our lessons. Tracking was vital for us, since we did not feature a dedicated quality assurance engineer/manager, and had to cross check everything we did before moving on. We did daily meetings to learn about our progress and came up with new ideas to be implemented until the end.
	![DMAIC.png](/Documents/images/technical/DMAIC_1675431865139_0.png)
	- ### What is HARFANG 3D ?
	- **HARFANG® 3D Framework** is a 3D Engine built in C/C++ that is sold to diverse companies in various sectors such as automotive, railway, risk prevention, design etc. .  **HARFANG® 3D Framework**, which we will call "the engine" is able to be run with other languages thanks to an ABI generator (FABGen), which will be the main focus of our work, since we need to add another language (Rust) to it.
	- ### What is a code binder used for ?
	> *Here is a simplified view of how FABGen is expected to function:*

	![simplified diagram.png](/Documents/images/technical/simplified_diagram_1674828088999_0.png)
	- ### Existing Solutions & Similar technologies
		- ### Automatic binding generation
			- rust-bindgen
				- https://github.com/rust-lang/rust-bindgen
				- Parses header files and generates a rust code out of it
				- will try to convert what it can, skipping constructs it can not handle.
				- Problems include, templates, inline functions, exceptions, automatically calling copy/move constructors, cross-language inheritance.
				- Needs manual configuration to block types that don't work or mark them as "opaque"
			- cbindgen
				- https://github.com/eqrion/cbindgen
				- Parses rust code and exposes types and functionsmarked as repr("C").
				- Typically works reliably as the programmer has already put in the hard work by making functions and types.
				- These are just the most commonly used ones, more tools available.
		- #### Semi-automatic binding generation
			- It is important to note that FABGen was created by Harfang as a replacement for SWIG, a very-well known binding generator targeting a lot of target languages. 
				What is SWIG? 
				* Swig is a tool for simplifying the task of interfacing different languages to C and C++ programs.
				* In a nutshell, SWIG is a compiler that takes C++ declarations and creates the wrappers needed to access those declarations from other languages including  Perl, Python, Java etc.
				* It usually doesn't require any modification of the existing code and can be used to build a usable interface in a relatively short time.
				* It has many known applications that supersede simple interface developments and is used in many large open source and commercial projects
				- Swig had many issues such as:
					* Very old and complex codebase
					* SWIG interface files were a language on their own
					* Everything was done through a single Object struct which hides the real types of variables, making it difficult to debug or extend the functionalities.
					* Uneven feature support between languages
			- https://cxx.rs/
				![image.png](/Documents/images/technical/image_1675162623380_0.png)
				- Requires custom code/data to generate bindings for C++ and Rust. A CFFI interface is hidden between the two bindings.
				- Its Aim is to describe interface and generate safe and fast bindings from and to C++ code.
				- **Safe** in the rust sense: Rust compiler enforces its invariants.
				- The C++ isn't safe in this sense: The rust compiler can not reason about the C++ code. The code generated by cxx is safe.
				- **Fast**: Zero copy, no transformations going between languages => custom types like CxxString in rust and rust::String in c++
				- Interface definition in Rust. (macro for the win! )
				- Shared data structures go straight into the FFI module. CXX maps data types.
				- Structs and functions/methods exposed from Rust. Must be parent scope!
				- structs and functions/methods exposed from C++. Add unsafe/lifetimes here, which will be ignored in C++ but leads to better bindings. CXX will assert that signature match!
				- How does this work?
					- Code is generated from this definition that implements C FFI + nicer facade in front of that:
					- Rust side: Macro based, so during rust build
					- C++: As aprt of build.rs/via command line tool. Needs build system integration!
		- #### No binding generation
			- CPP Macro
				- Using C++ code directly is also an option
				- You still need to do bindings for data types and such
				- `cpp!` macro enables embedding of C++ code right into the middle of the Rust code.
				- but we want for libraries that are already written..
- ## Goals, Product/Client requirements
- ### Functional Requirements
	- As mentioned in the *Functional Specifications*, the main objectives of our work are:
		- Provide Rust programs with access to all of C++'s functions and data structures.
		- Be easy to use and integrate into Rust programs, with a clear and simple API that is easy to learn and use.
		- Be well-tested, following Fabgen's existing templates, to ensure that it works correctly and is reliable.
		- Be released under an open-source license, allowing developers to use and modify it as needed.
		- Be as well optimized as possible not to slow down programs using the library
		- Make the Rust code as user-friendly as possible by using idiomatic language.
- ### Scope
	- |<p align="center" padding-top="15px"><img src="/Documents/images/technical/inScope.png" height="150px"></p>|<p align="center"><img src="/Documents/images/technical/outOfScope.png" height="150px"></p>|
		|--|--|
		|<p align="center"><strong>In Scope</strong></p>|<p align="center"><strong>Out of Scope</strong></p>|
		|Reverse Engineering FABGen|Modifying FABGen core logic|
		|Adding Rust language to fabgen|Using 3rd party binders|
		|Trying out FABGen on harfang.py|Modifying other language implementations in FABGen|
		|Functional on Windows & Linux|Cannot run on Mac M1|
		|Documenting the program to allow for easier developement in the future|Security => Out of scope|
		|Passing all the tests provided by the customer|Privacy => Out of scope|
		|Test Run on the Harfang 3D Engine||
- ### Quality Assurance Expectations
	- The test coverage of FABGen was of 92%, A total of 29 tests provided by the customer, and and passing rate must be 100% to validate the implementation. The same should be true for the delivered product
- ### License
	- GNU GPL 3.0
		- |Permissions|Limitations|Conditions|
			|--|--|--|
			|✅ Commercial Use|❌ Liability|☝️ License and copyright notice|
			|✅ Modification|❌ Warranty|☝️ State changes|
			|✅ Distribution||☝️Disclose source|
			|✅ Patent use||☝️Same License|
			|✅ Private use|||
- ## Assumptions & Constraints
	- |<p align="center" padding-top="15px"><img src="/Documents/images/technical/assumptions.png" height="130px"></p> |<p align="center"><img src="/Documents/images/technical/constraints.png" height="150px"></p>|
		|--|--|
		|<p align="center"><strong>Assumptions</strong></p>|<p align="center"><strong>Constraints</strong></p>|
		|We assume that FABGen is already "perfect" and that the existing code would not be responsible of further bugs|Not a two way binding for the moment, unlike FABGen README states.|
		|The tests are representative of the foolproofness of the algorithm|No one has actual great knowledge of target language in group|
		|We assume that we are on a 64bits system so size_t == long||
		|We assume that Rust is compatible with FABGen||
- ## Glossary
	- **Code binder**:
		- <em>Also explained in <a href="#what-is-a-code-binder-used-for-">'What is a code binder used for'</a></em><b
	- **Application Binary Interface (A.B.I.)**:
		- An application binary interface (ABI) is a low-level interface between an operating system or a microprocessor architecture and an application program. It defines how the binary code for a program should be formatted so that it can be executed by a system. The ABI specifies various details such as data types, register usage, exception handling, system call conventions, and other implementation-specific details that are required for an application to run on a particular platform.
		- ABIs are important because they ensure compatibility between different components in a system. By adhering to a common ABI, different components can be developed and maintained independently, while still being able to work together. This helps to avoid the problems that can arise when different parts of a system are built with different assumptions about how they will interact with each other. 
	- **Makefile**:
		- In C/C++, a makefile is a text file that is used in C/C++ projects to specify how the software should be built and the dependencies between different components. The makefile is processed by the "make" utility, which is a standard tool in most Unix-like operating systems.
		- The makefile contains a series of rules that describe how the target files should be built from their dependencies. A rule in a makefile typically consists of a target, a list of dependencies, and a series of commands that should be executed to build the target. 
	- **Idiomatic (language)**:
		- Having idiomatic knowledge of a language refers to the understanding of expressions, phrases and specificities that are unique to a particular language and culture. These expressions are usually not easily translated or understood by someone who is ignorant of that said language/culture.
		- For example, in [Malbolge](https://fr.wikipedia.org/wiki/Malbolge) the following is a valid Hello World:
			- ```malbolge
				(=<`#9]~6ZY32Vx/4Rs+0No-&Jk)"Fh}|Bcy?`=*z]Kw%oG4UUS0/@-ejc(:'8dc
				```
		- While Python users would rather do it this way:
			- ```python
				print('Hello World')
				```
		- As you can see languages and cultures differ...
	- **API**:
		- An **application programming interface** (**API**) is a way for two or more computer programs to communicate with each other. It is a type of software interface, offering a service to other pieces of software. A document or standard that describes how to build or use such a connection or interface is called an *API specification*. A computer system that meets this standard is said to *implement* or *expose* an API. The term API may refer either to the specification or to the implementation.
		- In contrast to a user interface, which connects a computer to a person, an application programming interface connects computers or pieces of software to each other. It is not intended to be used directly by a person (the end user) other than a computer programmer who is incorporating it into the software. An API is often made up of different parts which act as tools or services that are available to the programmer. A program or a programmer that uses one of these parts is said to *call* that portion of the API. The calls that make up the API are also known as subroutines, methods, requests, or endpoints. An API specification *defines* these calls, meaning that it explains how to use or implement them.
		- One purpose of APIs is to hide the internal details of how a system works, exposing only those parts a programmer will find useful and keeping them consistent even if the internal details later change. An API may be custom-built for a particular pair of systems, or it may be a shared standard allowing interoperability among many systems. 
	- **Wrapper Object**:
		- A **wrapper function** is a function in a software library or a computer program whose main purpose is to call a second subroutine or a system call with little or no additional computation. Wrapper functions are used to make writing computer programs easier by abstracting away the details of a subroutine's underlying implementation.
		- Wrapper functions are a means of delegation and can be used for a number of purposes.
	- **Types**:
		- In computer science and computer programming, a data type (or simply type) is a collection or grouping of data values, usually specified by a set of possible values, a set of allowed operations on these values, and/or a representation of these values as machine types. A data type specification in a program constrains the possible values that an expression, such as a variable or a function call, might take. On literal data, it tells the compiler or interpreter how the programmer intends to use the data.
		- Most programming languages support basic data types of integer numbers (of varying sizes), floating-point numbers (which approximate real numbers), characters and Booleans.
	- **Compiler**:
		- In computing, a compiler is a computer program that translates computer code written in one programming language (the source language) into another language (the target language). The name "compiler" is primarily used for programs that translate source code from a high-level programming language to a low-level programming language (e.g. assembly language, object code, or machine code) to create an executable program. 

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

# Proposed Solution
- ## Dependencies & External Elements
- 64bit Windows or linux OS
- Python 3.2 minimum except ?
- FABGen
- Optionally: Harfang 3D
- Rustc compiler
- Cargo
- GCC and G++
- Visual Studio 2019
- ## Architecture Diagrams:
- ### Main Architecture
	![image.png](/Documents/images/technical/image_1675436220671_0.png)
	- *Main architecture diagram*:
- ### Example of a binding
- > WIP
- ### Example of a test
- > WIP
- ## Technical Specifications
- ### Conversion Tables
- > WIP
- ### Idiomatic Writing:
	- ### Idiomatic C/C++ & Rust Code
		- *Basic Features Comparison:*
			- |Mutable Access|Multi-threaded|C++|Rust|
			  |--|--|--|--|
			  |No|No|`std::shared_ptr<const T>`|`std::rc::Rc<T>`|
			  |Yes|No|`std::shared_ptr<T>`|`std::rc::Rc<std::cell::RefCell<T>>`|
			  |No|Yes|`std::shared_ptr<const T>`|`std::sync::Arc<T>`|
			  |Yes|Yes|`std::shared_ptr<T>` + some other sync*|`std::sync::Arc<std::sync::Mutex<T>>`|
		- *Most likely type associations*
			- | C/C++ | Rust | Notes |
			  |--|--|--|
			  | `char` | `i8` (or `u8`) | The signedness of a C++ char can be signed or unsigned - the assumption here is signed but it varies by target system. A Rust char is not the same as a C/C++ char since it can hold any Unicode character. [1] |
			  | `unsigned char` | `u8` |  |
			  | `signed char` | `i8` |  |
			  | `short int` | `i16` |  |
			  | `unsigned short int` | `u16` |  |
			  | `(signed) int` | `i32` or `i16` | In C/C++ this is data model dependent |
			  | `unsigned int` | `u32` or `u16` | In C/C++ this is data model dependent |
			  | `(signed) long int` | `i32` or `i64` | In C/C++ this is data model dependent |
			  | `unsigned long int` | `u32` or `u64` | In C/C++ this is data model dependent |
			  | `(signed) long long int` | `i64` |  |
			  | `unsigned long long int` | `u64` |  |
			  | `size_t` | `usize` | `usize` holds numbers as large as the address space [2] |
			  | `float` | `f32` |  |
			  | `double` | `f64` |  |
			  | `long double` | `f128` | `f128` support was present in Rust but removed due to issues for some platforms in implementing it. |
			  | `bool` | `bool` |  |
			  | `void` | `()` | The unit type (see below) |
			- [1]: Rust's `char` type, is 4 bytes wide, enough to hold any Unicode character. This is equivalent to the belated `char32_t` that appears in C++11 to rectify the abused C++98 `wchar_t` type which on operating systems such as Windows is only 2 bytes wide. When you iterate strings in Rust you may do so either by character or `u8`, i.e. a byte.
			- [2]: Rust has a specific numeric type for indexing on arrays and collections called `usize`. A `usize` is designed to be able to reference as many elements in an array as there is addressable memory. i.e. if memory is 64-bit addressable then usize is 64-bits in length. There is also a signed `isize` which is less used but also available.
	- > WIP

- ### Step by Step Build
	- ### New Folder Structure
	> Keep in mind the *italic text* represents modified files/folders, while **bold** text represents newly created files/folders
	<pre>root
	├── <em>.github/workflows</em>
	│   └── <strong>main.yml</strong>
	├── <em>examples</em>
	│   ├── <strong>harfang_libs</strong>
	│   └── <em>harfang.py</em>
	├── <em>lang</em>
	│   └── <strong>rust.py</strong>
	├── <em>lib</em>
	│   ├── <strong>rust</strong>
	│   │   ├── <strong>WrapperConverter.rs_</strong>
	│   │   ├── <strong>__init__.py</strong>
	│   │   ├── <strong>std.py</strong>
	│   │   └── <strong>stl.py</strong>
	│   ├── <em>stl.py</em>
	│   └── <em>__init__.py</em>
	├── <em>tests</em>
	│   ├── <em>arg_out.py</em>
	│   ├── <em>basic_type_exchange.py</em>
	│   ├── <em>cpp_exceptions.py</em>
	│   ├── <em>enumeration.py</em>
	│   ├── <em>extern_type.py</em>
	│   ├── <em>function_call.py</em>
	│   ├── <em>function_template_call.py</em>
	│   ├── <em>method_route_feature.py</em>
	│   ├── <em>repr.py</em>
	│   ├── <em>return_nullptr_as_none.py</em>
	│   ├── <em>shared_ptr.py</em>
	│   ├── <em>shared_ptr_default_comparison.py</em>
	│   ├── <em>std_function.py</em>
	│   ├── <em>std_future.py</em>
	│   ├── <em>std_vector.py</em>
	│   ├── <em>struct_bitfield_member_access.py</em>
	│   ├── <em>struct_default_comparison.py</em>
	│   ├── <em>struct_exchange.py</em>
	│   ├── <em>struct_inheritance.py</em>
	│   ├── <em>struct_inheritance_cast.py</em>
	│   ├── <em>struct_instantiation.py</em>
	│   ├── <em>struct_member_access.py</em>
	│   ├── <em>struct_method_call.py</em>
	│   ├── <em>struct_nesting.py</em>
	│   ├── <em>struct_operator_call.py</em>
	│   ├── <em>struct_static_const_member_access.py</em>
	│   ├── <em>template_struct_nesting.py</em>
	│   ├── <em>transform_rval.py</em>
	│   └── <em>variable_access.py</em>
	├── <strong>Dockerfile</strong>
	├── <em>bind.py</em>
	├── <em>gen.py</em>
	└── <em>tests.py</em></pre>
	


- ## Risk assessment and security risks/measures
- ### Risk Prevention Matrix
	- |<p align="center" padding-top="15px"><img src="/Documents/images/technical/risk.png" height="130px"></p>|<p align="center" padding-top="15px"><img src="/Documents/images/technical/riskPrevention.png" height="130px"></p>|
	  |--|--|
	  |<p align="center"><strong>Possible Risks</strong></p>|<p align="center"><strong>Preventive Action</strong></p>|
	  |Program Errors|Already Handled by FABGen |
	  |Security Risks|Out of Scope (considering resources)|
	  |Privacy Risks|Out of Scope (considering resources)|
	  |Lack of Time|Good task Prioritization and communication with customer to do so|
	  |Lack of Manpower|Mutual help among groups and good communication with customer and good research effort|
	  |Compatibility issues|Type conversion is not fully coverable within the constraints of the project. Solution was tested in the two target environments.|
	  |Diverging POVs between project overseer and Customer|Regular communication with both. Clearing up any confusion.|
	  |No full understanding of the source and target languages|Spent time (two weeks) researching and learning about them|
- ### Rollback Plan
	- Since our work is on a Fork from the original product, there is no need to establish a specific Rollback plan, other than mentioning that preserving the Git history of changes is necessary to enable this safeguard.
- ## Performance
- > WIP
- ## Pros and Cons
- |<p align="center" padding-top="15px"><img src="/Documents/images/technical/pros.png" height="130px"></p>|<p align="center" padding-top="15px"><img src="/Documents/images/technical/minus.png" height="130px"></p>|
  |--|--|
  |<p align="center"><strong>Pros</strong></p>|<p align="center"><strong>Cons</strong></p>|
  |More stable than if we had used bind gen in addition to FABGen.|Given the constraints, we cannot ensure complete coverage of the features.|
  |For FABgen: it is integrated in their existing workflow.|Given the constraints, we cannot ensure idiomatic Rust.|
  |It remains 🌈FABulous✨||
- ## Alternate designs or solutions
- <em>Please Refer to <a href="#existing-solutions--similar-technologies">Existing solutions</a></em>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

# Development & Maintenance
- ## Schedule of development
- ### Efforts and costs
    - ### Priority Matrix
  	- |Flexibility|Importance|
  		|--|--|
  		|F0|Most Important|
  		|F1|Important|
  		|F2|Less Important|

  	- |Task|Priority|
  		|--|--|
  		|Make it work on Mac M1|F2|
  		|Implementing Async/Future|F2|
  		|Implementing Structs|F0|
  		|Make Tests Pass|F0|
  		|Implementing Vectors|F1|
  		|Implementing Strings|F1|
  		|Implementing Bindings for enums|F1|
  		|Create Exhaustive documentation |F2|
  		|Create Documentation for the implementation|F0|
  		|Implementing all Basic types|F0|
  		|Binding Harfang.py|F1|
  		|Implement Functions|F0|
    - ### Milestones
  	- |**Milestone**|**Date**|
  		|--|--|
  		|Kickoff Meeting|By Wednesday 4th, January 2023|
  		|Understanding the Project|By Friday 6th, January 2023|
  		|First Meeting with the client|By Thursday 12th, January 2023|
  		|Finishing the functional Specifications|By Tuesday 24th, January 2023|
  		|Finishing the technical Specifications|By Tuesday 31th, January 2023|
  		|Getting a simple binding working|By Tuesday 7th, February|
  		|Passing all the tests|By Friday 10th, February 2023|
  		|Getting `harfang.py` working|By Tuesday 14th, February 2023|
  		|Oral Exam|By Friday 17th, February 2023|
  		|Closure Meeting|By Friday 17th, February 2023|
    - ### Work estimates
  	- We estimate being able to finish the project on time (approx. 7 weeks), even though lack of idiomatic knowledge on Rust will probably set us back at some point.
  	- As stated in the <a href="#risk-assessment-and-security-risksmeasures">risk prevention</a>, some of our team members will train during project time and in their personal time as well, to allow us to fully grasp the specificities of the project and the language.
- ### Planning
- We used a Trello to keep track of the tasks in a day-to-day fashion and to identify bugs and bottlenecks.
<img src="/Documents/images/technical/trello.png">
<br>
<div>We used multiple PERT graphs to force us to have a critical path, which allowed us to lay out a basic retro planning on a Gantt diagram to prioritize the work and give better estimates for the deliverables and milestones.</div>
<br>
<img src="/Documents/images/technical/gantt.png">

- ## Success Assessment
- Throughout the whole project, we have identified the passing of the tests as the main metric for our success. We can also mention overall implementation (100% is impossible) of the language as an important one as well. As we want to improve from our previous projects, we would like documentation coverage to be on watchlist as well.
- ### Impact
- Our goal is to help HARFANG port their engine to more languages and thus, customers. If we have succeeded in our mission, HARFANG should be able to deploy our solution with minimal work left from us and from them.
- We are proud to be part of a project that may impact the field of systems programming languages: indeed, this project creates new bridges between old codebases and newer ones, contributing to the advent of `Rust`.
- ### Metrics
- We use Trello, counting cards and checklists to measure the state of different topics.
	- Objects can be either in `Backlog`, `Todo`, `Doing`, `On Hold`, `Done`, `Abandoned`.
		- `Backlog` can be filled infinitely.
		- `Doing` can only feature one task per person at a given time.
		- `On Hold` should only be filled to pause something and resume later, otherwise checklists are recommended
		- There are actually multiple `Done` states
			- `Done`
			- `Proof-Read`
			- `Peer-Reviewed`
			- `Formatted`
			- `Documented`
		- An object is really considered done when it has been documented.
- Therefore, our progress rate is calculated with documentation, hence the longer time to completion.
- ## CI/CD Pipeline
- Tests are run automatically when pushed in main, via the following github actions code:
- ```yaml
	name: Global Testing
	
	on:
	pull_request:
		branches:
		- main
	jobs:
	Build_Linux:
		runs-on: ubuntu-latest
		steps:
		- uses: actions/checkout@v3
		- name: Set up Python 3.10
		uses: actions/setup-python@v3
		with:
			python-version: '3.10'
		- run: pip install pypeg2
		- run: pip install coverage
		- run: pip install PyYAML==5.1
		- run: pip install python-coveralls==2.9.1
		- run: python3 tests.py --x64 --linux --pybase "/opt/hostedtoolcache/Python/3.10.9/x64"
	```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

- # Conclusion
- ## Future improvements
- Considering we did not reach our goal of binding `harfang.py`, reaching this objective would be our first future perspective.
- After that, adding reverse binding functionality like [Flapigen](https://github.com/Dushistov/flapigen-rs) would be interesting (which seems to be FABGen's original statement)
- As of now, FABGen is a semi-automatic binding generator because the user has to manually write the application-specific bindings. It would be interesting to work on making it an automatic binding generator by automatically generating interface files like [Rifgen](https://crates.io/crates/rifgen)
- We would also like to be granted more time to write more idiomatic rust, whilst testing for security and privacy concerns for instance, as we have focused our efforts on binding `harfang.py`
- ### Acknowledgments
    - ### People
  	- |<a href="https://www.linkedin.com/in/franck-jeannin/">Franck Jeannin</a>|<a href="https://algosup.com/">Algosup</a> CEO & Project Overseer|
  	  |--|--|
  	  |<a href="https://www.linkedin.com/in/astrofra/">François Gutherz</a>|CTO & Project Lead @<a href="https://www.harfang3d.com/">Harfang</a>|
  	  |<a href="https://www.linkedin.com/in/ejulien/">Emmanuel Julien</a>|Lead Developer @<a href="https://www.harfang3d.com/">Harfang</a>|
  	  |<a href="https://www.linkedin.com/in/thomas-simonnet-39968480/">Thomas Simonnet</a>|Lead Developer @<a href="https://www.harfang3d.com/">Harfang</a>|
  	  |<a href="https://www.linkedin.com/in/jihane-billacois/">Jihane Billacois</a>|Research @E-STANCE|
  	  |<a href="https://www.linkedin.com/in/delphine-prousteau/">Delphine Prousteau</a>|Customer Satisfaction @<a href="https://www.linkedin.com/company/quanaup/">QuanauP</a>|
  	  |<a href="https://www.linkedin.com/in/caroline-cordier-dpo/">Caroline Cordier</a>|Project Management & Quality Assurance @<a href="https://www.linkedin.com/company/enablon/">Enablon</a>|
    - ### Media
  	- <a href="https://www.flaticon.com/free-icons/audit" title="audit icons">Audit icons created by Freepik - Flaticon</a>
  	- <a href="https://www.flaticon.com/free-icons/constraint" title="constraint icons">Constraint icons created by orvipixel - Flaticon</a>
  	- <a href="https://www.flaticon.com/free-icons/aim" title="aim icons">Aim icons created by Prosymbols - Flaticon</a>
  	- <a href="https://www.flaticon.com/free-icons/pet" title="pet icons">Pet icons created by Freepik - Flaticon</a>
  	- <a href="https://www.flaticon.com/free-icons/risk" title="risk icons">Risk icons created by bsd - Flaticon</a>
  	- <a href="https://www.flaticon.com/free-icons/prevention" title="prevention icons">Prevention icons created by Freepik - Flaticon</a>
  	- <a href="https://www.flaticon.com/free-icons/plus" title="plus icons">Plus icons created by Freepik - Flaticon</a>
  	- <a href="https://www.flaticon.com/free-icons/minus" title="minus icons">Minus icons created by Google - Flaticon</a>
  	- <a href="https://www.flaticon.com/free-icons/functional" title="functional icons">Functional icons created by Eucalyp - Flaticon</a>
  	- <div> Icons made by <a href="https://www.flaticon.com/authors/orvipixel" title="orvipixel"> orvipixel </a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
  	- <div> Icons made by <a href="https://www.freepik.com" title="Freepik"> Freepik </a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
  	- <div> Icons made by <a href="https://www.flaticon.com/authors/hajicon" title="HAJICON"> HAJICON </a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

<div align="right"><a href="#-book-table-of-contents"><img src="/Documents/images/technical/back.png" width="75px"></a></div>
