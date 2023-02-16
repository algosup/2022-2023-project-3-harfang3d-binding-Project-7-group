# Goals

Our main goal is to create bindings[^1] between C++[^2] and Rust[^3] programming languages.
This project is realised for the use of Harfang[^4] and is an extention to the Fabgen[^5] Python library.

For this project our research will strongly focus on:

​* The client (and their specific needs)
* Understanding how bindings work
* Understanding how Fabgen works
* The specifics of C++ and Rust
* (Optional) Learning how to use Harfang3D

## Client
​
Our client is [Harfang](https://www.harfang3d.com/en_US/). They created an efficient and memory safe 3D engine. Harfang3d has been mainly created for industrial use and simulations rather then video games.

## Product

The endproduct is an extention to the [Fabgen](https://github.com/ejulien/FABGen) Python library. The purpose of this library is to create bindings between C++ and a variety of other programming languages.
At the moment, Fabgen is used to bind towards CPython, Lua and GoLang.
Our objective is to add Rust to that list.
The code for Fabgen is licensed under the "GNU General Public License v3.0" which allows us to use it and modify it for our project.


## Skills
​
The skills needed to realize this project are mostly technical. Again this is not something that we can easily research because it is more about understanding the code provided and replicating it for Rust. This is something that we can only learn by reading the code and by asking questions to our client.

Still, we need to have an understanding of the languages involved. This is why the documentation of the languages is important to us. They are good resources because the are official, up to date and explain in details the concepts we need to understand.
- [The Rust documentation](https://doc.rust-lang.org/std/index.html): This is our main resource for Rust specific information. It is our most important rust resource since it is the official documentation of the language.
- [The C++ documentation](https://en.cppreference.com/w/): This is our main resource for C++ specific information. It is our most important C++ resource since it is the official documentation of the language.
- [The Python documentation](https://docs.python.org/3/): This is our main resource for Python specific information. It is our most important Python resource since it is the official documentation of the language.

Those three languages are the ones we will be using to create the binding.
# Roadmap



# Organization / Team work

The tasks are organized using [Trello](https://trello.com/en)

The distribution of the tasks abide to the following generic structure:

![org diagram](../images/Project%20Harfang%20Roadmap.png)



# documentation saving and sharing system
​
Most of the research done during this project focuses around the minute details necessary for the implementation of the project. Such details are rarely useful beyond their immediate use and as such are not saved anywhere. In addition, since we are following already existing implementations, our most useful resource is the code that is provided and that we need to understand.

If the document in question is deemed important enough to be shared with the entierity of the group or must be saved for longterm use then it is shared in the Discord server created for the sake of communication between team members.

# Resources

As a starting point, we have access to the following documents:

- [Fabgen's Github Repository](https://github.com/ejulien/FABGen): This is where we find the base code.
- [A Github repository created for the collaboration between Harfang and ALGOSUP](https://github.com/harfang3d/algosup-binding-project): This repository contains a few information relevant to our project meant to help us in our task.
- [Harfang3D's Github repository](https://github.com/harfang3d/harfang3d): This repository helps us learn more about the final product of our client.
- [Harfang3D's documentation](https://dev.harfang3d.com/): This will help us implement an example to show that our project works in the end.