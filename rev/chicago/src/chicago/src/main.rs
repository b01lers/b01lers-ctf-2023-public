use std::io;
use std::process::Command;
fn main() {
    let mut buffer = String::new();
    let stdin = io::stdin(); // We get `Stdin` here.
    stdin.read_line(&mut buffer).expect("Input err");
    let numbers:Vec<char> = buffer.strip_suffix('\n').unwrap().chars().rev().collect(); 
    if numbers.len() < 10{
        panic!("Bad length");
    }

    let mut sum = 0;
    for i in 1..numbers.len(){
        //going from rightmost to leftmost digit
        let current_num:i32= numbers[i].to_digit(10).unwrap() as i32;
        if i%2 != 0{
            //every second digit must be doubled
            //sum += current_num*2;
            if current_num*2 >= 10{
                let second_digit = (current_num*2) % 10;
                let first_digit:i32 = (current_num*2) /10;
                let target = first_digit+second_digit;
                sum += target;
            }
            else{
                sum += current_num*2;
            }
        }
        else{
            sum += current_num;
        }
    }
    let check_digit = numbers[0].to_digit(10).unwrap() as i32;
    let calculated_check_digit = (10-(sum %10))%10;
    if check_digit == calculated_check_digit{
        println!("{:?}", Command::new("cat").arg("./flag.txt").output().expect("Contact admin"));

    }

}
