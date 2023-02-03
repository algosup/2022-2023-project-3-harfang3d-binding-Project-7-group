exclude-from-graph-view:: true

- ## Introduction
  background-color:: pink
	- ### Document Tracking and version (Revision History)
	  background-color:: purple
		- |Version n°|Edits completed by|Date|Description of edit|
		  |--|--|--|--|
		  |0.1.0|Mathis KAKAL|11.01.2023|Initial Document Outline|
		  |0.2.0|Mathis KAKAL|17.01.2023|Added all introduction except Project overview and Glossary |
	- ### Purpose of Document
	  background-color:: yellow
		- #### Global definition
		  background-color:: yellow
			- #admon-success The purpose of this Technical Specifications Document (TSD) is to present the stakeholders with the technical discussion and choices made for the implementation of a new programming language (Rust), to the already existing FABGen code binding generator, completely, accurately and unambiguously in the most concrete way possible. This information is the work of the Tech Lead during the the second and third week of the project (ideation phase), and was updated few times during the development phases. It is derived from the Functional Requirements (FRD) which state what should and shouldn't be implemented.
			- #admon-success Finally, the Technical Specifications Document contributes to splitting our work with Harfang into multiple domains. Having the Technical domain separated from the Functional one, allows us to tailor, debug and develop the solution faster to tackle either business, functional or technical issues distinctively.
		- #### Benefits to engineers
		  background-color:: yellow
			- #admon-success For engineers, the TSD outlines the specific requirements and constraints for the product. It serves as a clear and detailed guide to follow as they design and develop it. The specifications can include information on materials, design criteria, performance requirements, and testing procedures, among other things.
			  Having a technical specifications document in place helps ensure that the final product meets the desired specifications and that all members of the team are working towards the same goal. As such, it should alleviate responsibility of the choices from the engineers, so they can focus solely on the implementation of the product and its quality.
		- #### Benefits to the team
		  background-color:: yellow
			- #admon-success Technical specs, because they are a thorough view of the proposed solution, also serve as documentation for the project, both  for the implementation phase and after, to communicate the projects accomplishments. 
			  Moreover, it saves the team from repeatedly explaining design and technical choices to teammates and other stakeholders.
			  A well-written specification document will allow the team to arrive at a mutual understanding regarding the technical aspects of the project and development process.
	- ### Points of contact
	  background-color:: purple
		- #### Points of Contact
		  background-color:: yellow
			- | Ivan MOLNAR| Project Manager | ivan.molnar@algosup.com |
			  |--|--|--|
			  | Mathieu CHAPUT| Program Manager | mathieu.chaput@algosup.com |
			  | Franck JEANNIN| Algosup CEO & Project overseer | franck.jeannin@algosup.com |
			  | Mathis KAKAL| Tech Lead| mathis.kakal@algosup.com |
		- Authors, roles etc.
		  background-color:: red
			- | **Deliverable**| **Author**| **E-mail address**|
			  |--|--|--|
			  | *Functional Requirements Document *| Mathieu CHAPUT (Program Manager) | mathieu.chaput@algosup.com|
			  | *Technical Requirements Document*| Mathis KAKAL (Tech Lead)| mathis.kakal@algosup.com |
			  | *Quality Assurance Document*| **Undefined**| **Undefined** |
		- Reviewers:  
		  background-color:: red
			- #admon-tips Franck ?
			- #admon-info This Document has been reviewed by the whole team thanks to our small numbers, allowing for great accuracy in the rendition of the specifications. This includes the designated quality assurance manager/engineer for establishing which functions and KPI's to monitor and test, the program manager for iteration on the the Functional Requirements Document, the project manager to ensure compliance with the project's expectations and finally the software engineer to ensure that it is in a language that they can understand.
			-
	- ### Project Overview
	  background-color:: pink
		- ### Context/Background
		  background-color:: pink
			- #### Project Genesis
			  background-color:: yellow
				- #admon-success This project was initiated on Tuesday, January 3rd 2023 as a collaboration between the customer, **HARFANG**® **3D**, a french company known for developing real-time 3D visualization tools and **ALGOSUP**, the *international software development school*.
				- #admon-success As stated in the Functional Requirements Document (FSD), the main goal of this project is to be able to use **HARFANG® 3D Framework** library, which is implemented in C/C++ in Rust language, through the use of their custom made code binder **FABGen** (designed as a replacement for SWIG) which already supports transpiling to CPython, Lua and Go. Therefore, the code binder can be described as an interface generator, more specifically as an Application Binary Interface generator, as it has to interface between two languages at low levels. This implies good knowledge of source and target languages, since (especially in the case of C/C++  Rust) where syntax and functioning greatly differ.
			- #### Harfang
			  background-color:: purple
				- #admon-info **HARFANG® 3D Framework** is a 3D Engine built in C/C++ that is sold to diverse companies in various sectors such as automotive, railway, risk prevention, design etc. .  **HARFANG® 3D Framework**, which we will call "the engine" is able to be run with other languages thanks to an ABI generator (FABGen), which will be the main focus of our work, since we need to add another language (Rust) to it.
				- #admon-info Therefore
			- #### What is a code binder used for ?
			  background-color:: gray
				- #admon-info Here is a simplified view of how FABGen is expected to function:
					- ![simplified diagram.png](../assets/simplified_diagram_1674828088999_0.png)
				- #admon-info as shown in the diagram above, FABGen takes in the
			- #### Existing Solutions
			  background-color:: pink
				- #admon-question It is important to note that FABGen was created by Harfang as a replacement for SWIG, a very-well known binding generator targeting a lot of target languages.
				- #admon-question What is SWIG?
				  * Swig is a tool for simplifying the task of interfacing different languages to C and C++ programs.
				  * In a nutshell, SWIG is a compiler that takes C++ declarations and creates the wrappers needed to access those declarations from other languages including  Perl, Python, Java etc.
				  * It usually doesn't require any modification of the existing code and can be used to build a usable interface in a relatively short time.
				  * It has many known applications that supersede simple interface developments and is used in many large open source and commercial projects
					- #admon-info Swig had many issues such as:
					  * Very old and complex codebase
					  * SWIG interface files were a language on their own
					  * Everything was done through a single Object struct which hides the real types of variables, making it difficult to debug or extend the functionalities.
					  * Uneven feature support between languages
				- ##### Automatic binding generation
				  background-color:: purple
					- #admon-tips AI generated stuff
					- #admon-info https://github.com/rust-lang/rust-bindgen
						- Parses header files and generates a rust code out of it
						- will try to convert what it can, skipping constructs it can not handle.
						- Problems include, templates, inline functions, exceptions, automatically calling copy/move constructors, cross-language inheritance.
						- Needs manual configuration to block types that don't work or mark them as "opaque"
					- #admon-info https://github.com/eqrion/cbindgen
						- Parses rust code and exposes types and functionsmarked as repr("C").
						- Typically works reliably as the programmer has already put in the hard work by making functions and types.
						- These are just the most commonly used ones, more tools available.
				- ##### Semi-automatic binding generation
				  background-color:: purple
					- #admon-info https://cxx.rs/
						- ![image.png](../assets/image_1675162623380_0.png)
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
						-
				- ##### No binding generation
					- #admon-info CPP Macro
						- Use C++ code directly!
						- You still need to do bindings for data types and such
						- `cpp!` macro enables embedding of C++ code right into the middle of the Rust code.
						- but we want for libraries that are already written..
			- #### Methodology (DMAIC Framework)
			  background-color:: gray
				- #admon-tips Diagram with team ?
		- ### Goals, Product/Client requirements
			- #### Functional Requirements
				- #admon-tips User stories ?
			- #### Scope
				- ##### In Scope :
					- #admon-info Adding Rust language to fabgen
				- ##### Out of scope :
					- #admon-info modifying FABGen
			- #### Test coverage expectations
				- #admon-tips Analyze their github actions and deduce their expectations
				- #admon-tips validate them with the client
			- #### License
				- #admon-tips Say what is allowed and not allowed with it
			- Any other requirements I can find
				- ....
		- ### Assumptions
			- #admon-info that FABGen is already "perfect" and that their code  would not be responsible of further bugs
			- #admon-info the tests are representative of the foolproofness of the algorithm
			- #admon-info we assume that we are on a 64bits system so size_t == long
		- ### Constraints
			- #admon-tips not two way binding for the moment, unlike FABGen README states.
			- #admon-info No one has actual great knowledge of target language in group
	- ### Glossary
	  background-color:: purple
		- #admon-info transpiling
		- #admon-info code binder
		- #admon-info Application Binary Interface (A.B.I.)
## Proposed Solution
background-color:: pink
	- ### Dependencies & External Elements
	  background-color:: gray
	- ### Architecture Diagram:
	  background-color:: gray
		- Example of a binding
		- Example of a test
		- The whole thing
	- ### Technical Specifications
	  background-color:: pink
		- Define Languages:
			- <ins>What defines a supported language in swig?</ins>
				- Target languages are given a status of either 'Supported' or 'Experimental' depending on their maturity as broadly outlined in the [Target language introduction](https://www.swig.org/Doc4.1/SWIGDocumentation.html#Introduction_target_languages). This section provides more details on how this status is given.
				- A target language is given the 'Supported' status when
				- It is in a mature, well functioning state.
				- It has its own comprehensive chapter in the documentation. The level of documentation should be comprehensive and match the standard of the other mature modules. Python and Java are good references.
				- It passes all of the main SWIG test-suite. The main test-suite is defined by the tests in the C_TEST_CASES, CPP_TEST_CASES and MULTI_CPP_TEST_CASES lists in Examples/test-suite/common.mk. All the newer C++ standard tests need to work and are grouped together, such as CPP11_TEST_CASES for C++11. These more 'modern' C++ standards are only tested though if the compiler is detected as supporting the given standard.
				- The test-suite must also include at least twenty wide-ranging runtime tests. The most mature languages have a few hundred runtime tests. Note that porting runtime tests from another language module is a quick and easy way to achieve this.
				- It supports the vast majority of SWIG features. Some more advanced features, such as, directors, full nested class support and target language namespaces (nspace) may be unimplemented. A few support libraries may be missing, for example, a small number of STL libraries.
				- It provides strong backwards compatibility between releases. Each point release must aim to be fully backwards compatible. A point release version is the 3rd version digit, so each of the x.y.* versions should be backwards compatible. Backwards compatibility breakages can occur in a new major or minor version if absolutely necessary and if documented. A major or minor version is the first or second digit in the three digit version.
				- Fixing unintended regressions in the Supported languages will be given higher priority over experimental languages by the core SWIG developers.
				- Examples must be available and run successfully.
				- The examples and test-suite must be fully functioning on the Github Actions Continuous Integration platform.
				- #### A target language is given the 'Experimental' status when
				- It is of sub-standard quality, failing to meet the above 'Supported' status.
				- It is somewhere between the mid to mature stage of development.
				- It is in need of help to finish development. Some minimum requirements and notes about languages with the 'Experimental' status:
				- Will at least implement basic functionality - support wrapping C functions and simple C++ classes and templates.
				- Have its own documentation chapter containing a reasonable level of detail. The documentation must provide enough basic functionality for a user to get started.
				- Have fully functional examples of basic functionality (the simple and class examples).
				- The test-suite must be implemented and include a few runtime tests for both C and C++ test cases.
				- Failing tests must be put into one of the FAILING_CPP_TESTS or FAILING_C_TESTS lists in the test-suite. This will ensure the test-suite can be superficially made to pass by ignoring failing tests. The number of tests in these lists should be no greater than half of the number of tests in the full test-suite.
				- The examples and test-suite must also be fully functioning on the Github Actions Continuous Integration platform. However, experimental languages will be flagged as 'continue-on-error'. This means that pull requests and normal development commits will not break the entire Github Actions build should an experimental language fail.
				- Any new failed tests will be fixed on a 'best effort' basis by core developers with no promises made.
				- If a language module has an official maintainer, then the maintainer will be requested to focus on fixing test-suite regressions and commit to migrating the module to become a 'Supported' module.
				- If a module does not have an official maintainer, then, as maintenance will be on a 'best efforts' basis by the core maintainers, no guarantees will be provided from one release to the next and regressions may creep in.
				- Experimental target languages will have a (suppressible) warning explaining the Experimental sub-standard status and encourage users to help improve it.
				- No backwards compatibility is guaranteed as the module is effectively 'in development'. If a language module has an official maintainer, then a backwards compatibility guarantee may be provided at the maintainer's discretion and should be documented as such.
				- New target language modules can be included in SWIG and contributions are encouraged for popular languages. In order to be considered for inclusion, a language must at a minimum fit the 'Experimental' status described above.
				- Below are some practical steps that should help meet these requirements.
				- The "simple" example needs to be working to demonstrate basic C code wrappers. Port the example from another language, such as from Examples/python/simple.
				- The "class" example needs to be working to demonstrate basic C++ code wrappers. Port the example from another language, such as from Examples/python/class.
				- Modify configure.ac, Makefile.in and Examples/Makefile.in to run these examples. Please make sure that if the new language is not installed properly on a box, make -k check should still work by skipping the tests and examples for the new language module.
				- Copying an existing language module and adapting the source for it is likely to be the most efficient approach to fully developing a new module as a number of corner cases are covered in the existing implementations. The most advanced scripting languages are Python and Ruby. The most advanced compiled target languages are Java and C#.
				- Get the [test-suite](https://www.swig.org/Doc4.1/SWIGDocumentation.html#Extending_running_test_suite) running for the new language (make check-[lang]-test-suite). While the test-suite tests many corner cases, we'd expect the majority of it to work without much effort once the generated code is compiling correctly for basic functionality as most of the corner cases are covered in the SWIG core. Aim to first get one C and one C++ runtime test running in the test-suite. Adding further runtime tests should be a lot easier afterwards by porting existing runtime tests from another language module.
				- The structure and contents of the html documentation chapter can be copied and adapted from one of the other language modules.
				- Source code can be formatted correctly using the info in the [coding style guidelines](https://www.swig.org/Doc4.1/SWIGDocumentation.html#Extending_coding_style_guidelines) section.
				- When ready, post a patch on Github, join the swig-devel mailing list and email the SWIG developers with a demonstration of commitment to maintaining the language module, certainly in the short term and ideally long term. Once accepted into the official Git repository, development efforts should concentrate on getting the entire test-suite to work in order to migrate the language module to the 'Supported' status. Runtime tests should be added for existing testcases and new test cases can be added should there be an area not already covered by the existing tests.
			- #### Idiomatic C/C++ Code
			  background-color:: pink
				-
			- #### Idiomatic Rust Code
			  background-color:: pink
				- #admon-info https://github.com/rust-lang/rfcs/blob/master/text/0430-finalizing-naming-conventions.md
				- #admon-tips Have to use rust unsafe
				  https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html
				- #admon-info One thing though that gets *very* complicated about using SWIG is ownership semantics. With anything more complicated than passing scalar values, it is very easy to introduce a memory leak or double-free if you don't get the flags right. I wonder if Rust types naturally allow a much better inference of ownership semantics across the language boundary?
				- #admon-info neither has C++ (compiler defined)
				- #admon-info Languages have different concepts of inheritance, lifetimes, templates
				- #admon-info Data types do not match up. Even if they contain the "same" data, fields, names/sequences/types will be different
				- #admon-info Even if datatypes would match up: different requirements on the representation of contained data. E.G. utf-8 encoded strings in rust vs bytes in unknown encoding in C++
				- #admon-info The least common denominator between the two is the C foreign function interface.
				- #admon-info C FFI is the backbone all of those are built upon.
				- #admon-info Rust has a different Macro system than C++
		- Type conversion/compatibility tables example:
			- <ins>Integers:</ins>
				- {{renderer :tables_viqvozlrze}}
					- data nosum
						- Length
							- 8-bit
							- 16-bit
							- 32-bit
							- 64-bit
							- 128-bit
						- Signed
							- i8
							- i16
							- i32
							- i64
							- i128
						- Unsigned
							- u8
							- u16
							- u32
							- u64
							- u128
				-
		- *List all the other stuff like the files tests etc*
	- ### Test Plan & Quality Assurance
		- What are our quality goals?
		- Descriptions of how the tests will ensure that user requirements are met
		- QA
		- Integrations tests
		- Unit tests
	- ### Risk assessment and security risks/measures
		- ![image.png](../assets/image_1673536919062_0.png){:height 271, :width 640}
		- Error Handling
		- Security
		- Privacy
		- #admon-question Not fully understanding the languages 
		  training people is preventive action
		- #admon-tips you have risks regarding Technology, security, HR, human capabilities, availability of resources, what if the technology is unstable, risks linked to stakeholders (availability, engagement)
	- ### Performance
		- Compile time (?)
	- ### #admon-failure Rollback plan (?) => to go in risk assessment
		- Detailed and specific liabilities
		- Plan to reduce liabilities
		- Plan describing how to prevent other components, services, and systems from being affected
	- ### Pros and Cons
	- ### Alternate designs or solutions
		- Pros and cons for each alternative
		- A summary statement for each alternative solution
		- Ways in which options were inferior to the probable solution
		- Migration plan to next best option if the proposed solution fails
## Development & Maintenance
background-color:: gray
	- ### Schedule of development
		- define each phases
		- Efforts and costs planning
			- **a. Work estimates and timelines**
				- List of specific, measurable, and time-bound tasks
				- Resources needed to finish each task
				- Time estimates for how long each task needs to be completed
			- **b. Prioritization**
				- Categorization of tasks by urgency and impact
			- **c. Milestones**
				- Dated checkpoints when significant chunks of work will have been completed
				- Metrics to indicate the passing of the milestone
			- **d. Future work**
				- List of tasks that will be completed in the future
	- ### Success Assessment
		- #### a. Impact
			- (Security, cost, performance impact)
		- #### b. Metrics
			- Tools to capture and measure metrics
			- List of metrics to capture
	- ### Ongoing Testing
	- ### CI/CD Pipeline
## Conclusion
background-color:: gray
	- #### Future improvements
		- Adding reverse binding functionality
			- Flapigen: https://github.com/Dushistov/flapigen-rs
		- Adding automatic interface file generator
			- like the rust crate Rifgen : https://crates.io/crates/rifgen
		- Also see :
			- https://github.com/samscott89/swiggen
		- cbindgen : Rust -> C or C++11 headers
