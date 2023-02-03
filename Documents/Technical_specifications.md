- ## Introduction
	- ### Document Tracking and version (Revision History)
		- |Version n°|Edits completed by|Date|Description of edit|
		  |--|--|--|--|
		  |0.1.0|Mathis KAKAL|11.01.2023|Initial Document Outline|
		  |0.2.0|Mathis KAKAL|17.01.2023|Added all introduction except Project overview and Glossary |
	- ### Purpose of Document
		- #### Global definition
			- The purpose of this Technical Specifications Document (TSD) is to present the stakeholders with the technical discussion and choices made for the implementation of a new programming language (Rust), to the already existing FABGen code binding generator, completely, accurately and unambiguously in the most concrete way possible. This information is the work of the Tech Lead during the the second and third week of the project (ideation phase), and was updated few times during the development phases. It is derived from the Functional Requirements (FRD) which state what should and shouldn't be implemented.
			- Finally, the Technical Specifications Document contributes to splitting our work with Harfang into multiple domains. Having the Technical domain separated from the Functional one, allows us to tailor, debug and develop the solution faster to tackle either business, functional or technical issues distinctively.
		- #### Benefits to engineers
			- For engineers, the TSD outlines the specific requirements and constraints for the product. It serves as a clear and detailed guide to follow as they design and develop it. The specifications can include information on materials, design criteria, performance requirements, and testing procedures, among other things.
			  Having a technical specifications document in place helps ensure that the final product meets the desired specifications and that all members of the team are working towards the same goal. As such, it should alleviate responsibility of the choices from the engineers, so they can focus solely on the implementation of the product and its quality.
		- #### Benefits to the team
			- Technical specs, because they are a thorough view of the proposed solution, also serve as documentation for the project, both  for the implementation phase and after, to communicate the projects accomplishments. 
			  Moreover, it saves the team from repeatedly explaining design and technical choices to teammates and other stakeholders.
			  A well-written specification document will allow the team to arrive at a mutual understanding regarding the technical aspects of the project and development process.
	- ### Points of contact
		- #### Points of Contact
			- | Ivan MOLNAR| Project Manager | ivan.molnar@algosup.com |
			  |--|--|--|
			  | Mathieu CHAPUT| Program Manager | mathieu.chaput@algosup.com |
			  | Franck JEANNIN| Algosup CEO & Project overseer | franck.jeannin@algosup.com |
			  | Mathis KAKAL| Tech Lead| mathis.kakal@algosup.com |
		- #### Authors, roles etc.
			- | **Deliverable**| **Author**| **E-mail address**|
			  |--|--|--|
			  | *Functional Requirements Document*| Mathieu CHAPUT (Program Manager) | mathieu.chaput@algosup.com|
			  | *Technical Requirements Document*| Mathis KAKAL (Tech Lead)| mathis.kakal@algosup.com |
			  | *Quality Assurance Document*| **Undefined**| **Undefined** |
		- #### Reviewers:  
			- This Document has been reviewed by the whole team thanks to our small numbers, allowing for accuracy in the rendition of the specifications. This excludes a designated quality assurance manager/engineer for establishing which functions and KPI's to monitor and test, task that will be performed by the whole team. The program manager will also review the Technical Requirements Document for iteration with the the Functional Requirements, the project manager to ensure compliance with the project's expectations and finally the software engineer to ensure that it is in a language that they can understand and to develop the product.
			-
	- ### Project Overview
		- ### Context/Background
			- #### Project Genesis
				- This project was initiated on Tuesday, January 3rd 2023 as a collaboration between the customer, **HARFANG**® **3D**, a french company known for developing real-time 3D visualization tools and **ALGOSUP**, the *international software development school*.
				- As stated in the Functional Requirements Document (FSD), the main goal of this project is to be able to use **HARFANG® 3D Framework** library, which is implemented in C/C++ in Rust language, through the use of their custom made code binder **FABGen** (designed as a replacement for SWIG) which already supports transpiling to CPython, Lua and Go. Therefore, the code binder can be described as an interface generator, more specifically as an Application Binary Interface generator, as it has to interface between two languages at low levels. This implies good knowledge of source and target languages, since (especially in the case of C/C++  Rust) where syntax and functioning greatly differ.
			- #### Methodology (DMAIC Framework)
				- Although the project consists mostly of identifying code implementations, writing them and passing predefined tests, we made sure to follow the DMAIC framework seen during our lessons. Tracking was vital for us, since we did not feature a dedicated quality assurance engineer/manager, and had to cross check everything we did before moving on. We did daily meetings to learn about our progress and came up with new ideas to be implemented until the end.
					- ![DMAIC.png](/images/technical/DMAIC_1675431865139_0.png)
			- #### What is HARFANG 3D ?
				- **HARFANG® 3D Framework** is a 3D Engine built in C/C++ that is sold to diverse companies in various sectors such as automotive, railway, risk prevention, design etc. .  **HARFANG® 3D Framework**, which we will call "the engine" is able to be run with other languages thanks to an ABI generator (FABGen), which will be the main focus of our work, since we need to add another language (Rust) to it.
			- #### What is a code binder used for ?
				- Here is a simplified view of how FABGen is expected to function:
					- ![simplified diagram.png](/images/technical/simplified_diagram_1674828088999_0.png)
			- #### Existing Solutions & Similar technologies
				- ##### Automatic binding generation
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
				- ##### Semi-automatic binding generation
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
					- #admon-question https://cxx.rs/
						- ![image.png](/images/technical/image_1675162623380_0.png)
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
					- CPP Macro
						- Using C++ code directly is also an option
						- You still need to do bindings for data types and such
						- `cpp!` macro enables embedding of C++ code right into the middle of the Rust code.
						- but we want for libraries that are already written..
		- ### Goals, Product/Client requirements
			- #### Functional Requirements
				- as mentioned in the *Functional Specifications*, the main objectives of our work are:
					- Provide Rust programs with access to all of C++'s functions and data structures.
					- Be easy to use and integrate into Rust programs, with a clear and simple API that is easy to learn and use.
					- Be well-tested, following Fabgen's existing templates, to ensure that it works correctly and is reliable.
					- Be released under an open-source license, allowing developers to use and modify it as needed.
					- Be as well optimized as possible not to slow down programs using the library
					- Make the Rust code as user-friendly as possible by using idiomatic language.
			- #### Scope
				- ##### In Scope :
					- Adding Rust language to fabgen
					- Trying out FABGen on harfang.py
					- Functional on Windows & Linux
					- Documenting all the program to allow for easier developement in the future
					- Passing all the tests provided by the customer
					- Test Run on the Harfang 3D Engine
					- Reverse Engineering FABGen
				- ##### Out of scope :
					- modifying FABGen core logic
					- Using 3rd party binders
					- modifying other language implementations in FABGen
			- #### Quality Assurance Expectations
				- The test coverage of FABGen was of 92%, A total of 29 tests provided by the customer, and and passing rate must be 100% to validate the implementation
			- #### License
				- GNU GPL 3.0
					- |Permissions|Limitations|Conditions|
					  |--|--|--|
					  |✅ Commercial Use|❌ Liability|☝️ License and copyright notice|
					  |✅ Modification|❌ Warranty|☝️ State changes|
					  |✅ Distribution||☝️Disclose source|
					  |✅ Patent use||☝️Same License|
					  |✅ Private use|||
		- ### Assumptions
			- that FABGen is already "perfect" and that the existing code would not be responsible of further bugs
			- the tests are representative of the foolproofness of the algorithm
			- we assume that we are on a 64bits system so size_t == long
		- ### Constraints
			- not two way binding for the moment, unlike FABGen README states.
			- No one has actual great knowledge of target language in group
	- ### Glossary
		- code binder
		- Application Binary Interface (A.B.I.)
- ## Proposed Solution
	- ### Dependencies & External Elements
	- ### Architecture Diagram:
		- Example of a binding
		- Example of a test
		- The whole thing
			- ![image.png](/images/technical/image_1675436220671_0.png)
	- ### Technical Specifications
		- #### Define Languages:
			- ##### Idiomatic C/C++ Code
			- |Mutable Access|Multi-threaded|C++|Rust|
			  |--|--|--|--|
			  |No|No|`std::shared_ptr<const T>`|`std::rc::Rc<T>`|
			  |Yes|No|`std::shared_ptr<T>`|`std::rc::Rc<std::cell::RefCell<T>>`|
			  |No|Yes|`std::shared_ptr<const T>`|`std::sync::Arc<T>`|
			  |Yes|Yes|`std::shared_ptr<T>` + some other sync*|`std::sync::Arc<std::sync::Mutex<T>>`|

			- | C/C++ | Rust | Notes |  |  |
			  |:---:|:---:|:---:|---|---|
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
			- 
			- ##### Idiomatic Rust Code
				-  https://github.com/rust-lang/rfcs/blob/master/text/0430-finalizing-naming-conventions.md
				- Have to use rust unsafe
				  https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html
				-  One thing though that gets *very* complicated about using SWIG is ownership semantics. With anything more complicated than passing scalar values, it is very easy to introduce a memory leak or double-free if you don't get the flags right. I wonder if Rust types naturally allow a much better inference of ownership semantics across the language boundary?
				-  neither has C++ (compiler defined)
				-  Languages have different concepts of inheritance, lifetimes, templates
				-  Data types do not match up. Even if they contain the "same" data, fields, names/sequences/types will be different
				-  Even if datatypes would match up: different requirements on the representation of contained data. E.G. utf-8 encoded strings in rust vs bytes in unknown encoding in C++
				-  The least common denominator between the two is the C foreign function interface.
				-  C FFI is the backbone all of those are built upon.
				-  Rust has a different Macro system than C++
		- *List all the other stuff like the files tests etc*
	- ### Risk assessment and security risks/measures
		- ![image.png](/images/technical/image_1673536919062_0.png)
		- Error Handling
		- Security
		- Privacy
		- Not fully understanding the languages 
		  training people is preventive action
		- you have risks regarding Technology, security, HR, human capabilities, availability of resources, what if the technology is unstable, risks linked to stakeholders (availability, engagement)
	- ### Performance
		- Compile time (?)
	- ### Rollback plan (?) => to go in risk assessment
		- Detailed and specific liabilities
		- Plan to reduce liabilities
		- Plan describing how to prevent other components, services, and systems from being affected
	- ### Pros and Cons
	- ### Alternate designs or solutions
		- Pros and cons for each alternative
		- A summary statement for each alternative solution
		- Ways in which options were inferior to the probable solution
		- Migration plan to next best option if the proposed solution fails
- ## Development & Maintenance
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
- ## Conclusion
	- #### Future improvements
		- Adding reverse binding functionality
			- Flapigen: https://github.com/Dushistov/flapigen-rs
		- Adding automatic interface file generator
			- like the rust crate Rifgen : https://crates.io/crates/rifgen
		- Also see :
			- https://github.com/samscott89/swiggen
		- cbindgen : Rust -> C or C++11 headers