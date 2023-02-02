use std::fs;


fn main(){
    // get arguments from command line
    let args: Vec<String> = std::env::args().collect();
    let mut path = ".";
    if args.len() > 1 {
        path = &args[1];
    }

    // check if the files need to be moved in an out folder to run the makefile 
    if !path.ends_with("/out") {
        
        // copy *.c and *.cpp files to ./out for the Makefile to find them
        let paths = fs::read_dir(path).unwrap();
        let mut files_to_copy = Vec::new();
        for file in paths {
            let file_name = file.as_ref().unwrap().path();
            if file_name.to_str().unwrap().ends_with(".c") || file_name.to_str().unwrap().ends_with(".cpp") || file_name.to_str().unwrap().ends_with(".h"){
                files_to_copy.push(file.unwrap().path());
            }
        }
        if !fs::read_dir("./out").is_ok() {
            fs::create_dir("./out").expect("Error while creating directory");
        }
        for file in files_to_copy {
            fs::copy(&file, format!("./out/{}", &file.file_name().unwrap().to_str().unwrap())).expect("Error while copying file");
        }
    }

    // run make command
    
    if cfg!(target_os = "windows"){
        let output = std::process::Command::new("make")
        .output()
        .expect("failed to execute process");
    } else {
        let output = std::process::Command::new("make")
        .arg("linux")
        .output()
        .expect("failed to execute process");
    }
    fs::copy("./out/build.dll", "./src/build.dll").expect("Error while copying file");
    fs::copy("./out/build.lib", "./src/build.lib").expect("Error while copying file");
    // println!("status: {}", output.status);
    // println!("stdout: {}", String::from_utf8_lossy(&output.stdout));
    // println!("stderr: {}", String::from_utf8_lossy(&output.stderr));
    // run cargo build
    // let output = std::process::Command::new("cargo")
    //     .arg("run")
    //     .output()
    //     .expect("failed to execute process");
}