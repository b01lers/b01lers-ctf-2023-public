#include <unistd.h>
#include <stdint.h>
#include <sys/syscall.h>

#define READS 0
#define WRITES 1
#define OPENS 2
#define CLOSES 3
#define EXITS 60
#define PTRACES 101
#define KILLS 62

#define PROGG1 __asm__ __volatile__("int3; .byte 0x11;");
#define EPIGG1 __asm__ __volatile__("int3; .byte 0x12;");
#define PROGG2 __asm__ __volatile__("int3; .byte 0x21;");
#define EPIGG2 __asm__ __volatile__("int3; .byte 0x22;");
#define PROGG3 __asm__ __volatile__("int3; .byte 0x31;");
#define EPIGG3 __asm__ __volatile__("int3; .byte 0x32;");


typedef struct g{
    int gindex;
    uint8_t gdata[8][16];
    char fname[16];
} gg;

gg gl;



uint64_t scall(uint64_t n, uint64_t a1, uint64_t a2, uint64_t a3){
    int64_t ret;
    //__asm__ __volatile__("mov %0, %%rax\n; mov %1, %%rdi\n; mov %2, %%rsi\n; mov %3, %%rdx\n; syscall" : : "r" (n), "r" (a1), "r" (a2), "r" (a3) : );
    //40017c: 48 89 f8                mov    rax,rdi
    //40017f:   48 89 f7                mov    rdi,rsi
    __asm__ __volatile__("int3\n; mov %2, %%rsi\n; mov %3, %%rdx\n; syscall" : : "r" (n), "r" (a1), "r" (a2), "r" (a3) : );


    __asm__ __volatile__("mov %%rax, %0"
                     : "=&r" (ret)
                     : 
                     : );
    return ret;

}


uint64_t min(uint64_t a, uint64_t b){
    if(a<b){
        return a;
    }else{
        return b;
    }
}


void ex(uint64_t ecode){
    scall(EXITS, ecode, 0 , 0);
}

void ws(char * s){
    uint64_t n = 0;
    uint64_t l = 0;

    while(1){
        if(s[l]==0){
            break;
        }
        l+=1;
    }

    int64_t t=0;
    while(n<l){
        t = scall(WRITES, 1, (uint64_t) &(s[n]),l-n);
        if (t<=0){
            ex(2);
        }else{
            n+=t;
        }
    }
}


int ri(){
    char c;
    int64_t rvalue;
    int ret;
    rvalue = scall(READS, 0, (uint64_t) &c, 1);
    if(rvalue<=0){
        ex(5);
    }
    if(c<'0' || c>'9'){
        ex(3);
    }
    ret = c-'0';
    rvalue = scall(READS, 0, (uint64_t) &c, 1);
    if(rvalue<=0){
        ex(5);
    }
    if(c!='\n'){
        ex(4);
    }
    return ret;
}


void readn(char* content, uint64_t fd, uint64_t s){
    uint64_t i = 0;
    int64_t rvalue;
    while(i<s){
        rvalue = scall(READS, fd, (uint64_t) &(content[i]), 1);
        if(rvalue<=0){
            ex(5);
        }
        i+=1;
    }
}

void readc(char* content, uint64_t fd, char c){
    uint64_t i = 0;
    int64_t rvalue;
    while(1){
        rvalue = scall(READS, fd, (uint64_t) &(content[i]), 1);
        if(rvalue<=0){
            ex(5);
        }
        if(content[i]==c){
            return;
        }
        i+=1;
    }
}


int opens(char* fname){
    return scall(OPENS, (uint64_t) fname, 0, 0);
}

void closes(int fd){
    scall(CLOSES, fd, 0 , 0);
}

void encrypt(){
    PROGG2

    uint8_t cc;
    int i = 0;
    ws("Your data to encrypt?:\n");
    readn(gl.gdata[gl.gindex], 0, 16);
    gl.gindex++;
    int fd = opens(gl.fname);
    readn(gl.gdata[gl.gindex], fd, 16);
    closes(fd);

    ws("Your key:\n");
    for(i=0;i<16;i++){
        scall(WRITES, 1, (uint64_t) &(gl.gdata[gl.gindex][i]), 1);
    }
    ws("\nYour encrypted data:\n");
    for(i=0;i<16;i++){
        cc = gl.gdata[gl.gindex][i] ^ gl.gdata[gl.gindex-1][i];
        scall(WRITES, 1, (uint64_t) &(cc), 1);
    }

    EPIGG2
}


void decrypt(){
    PROGG3

    uint8_t buf1[16];
    uint8_t buf2[16];
    int i = 0;
    uint8_t cc;

    ws("Your data to decrypt?:\n");
    readn(buf1, 0, 16);
    ws("Your key?:\n");
    readc(buf2, 0, '\n');

    ws("Your decrypted data:\n");
    for(i=0;i<16;i++){
        cc = buf1[i] ^ buf2[i];
        scall(WRITES, 1, (uint64_t) &(cc), 1);
    }

    EPIGG3
}

//rm s; gcc -O1 -no-pie -nostdlib s.c -o s; python ./ex.py | tee in; gdb ./s



int main(){
    PROGG1

    ws("Welcome!\n");

    //int option = ri();

    //if(option==1){
    encrypt();
    //}else if(option==2){
    decrypt();

    //reversestring();


    EPIGG1
    return 0;
}


__attribute__((force_align_arg_pointer))
void _start() {
    //scall(PTRACES, 0, 0, 0);
    //scall(KILLS, 0, 23, 0);

    __asm__ __volatile__("mov $101, %%rax\n; xor %%rdi, %%rdi; xor %%rsi, %%rsi; xor %%rdx, %%rdx; syscall" : : : );
    __asm__ __volatile__("mov $39, %%rax\n; xor %%rdi, %%rdi; xor %%rsi, %%rsi; xor %%rdx, %%rdx; syscall; mov %%rax, %%rdi;  mov $62, %%rax\n; mov $19, %%rsi; xor %%rdx, %%rdx; syscall" : : : );

    char fname[] = "/dev/urandom";
    gl.gindex = 0;
    int i=0;
    while(1){
        gl.fname[i]=fname[i];
        if(fname[i]=='\x0'){
            break;
        }
        i++;
    }



    while(1){
        int ret = main();
        if (ret != 1){
            break;
        }
    }

    ex(0);


}


/*
rm s; rm in;  rm code; gcc -O1 -no-pie -nostdlib s.c -o s; python ./ex.py | tee in; objdump -M intel -D s > code; gdb ./s
rm s; rm in;  rm code; gcc -O1 -no-pie -nostdlib s.c -o s; python ./ex.py | tee in; objdump -M intel -D s > code; strace  ./s < in
rm s; rm in;  rm code; gcc -O1 -no-pie -nostdlib s.c -o s; python ./ex.py | tee in; objdump -M intel -D s > code; strip -s ./s; objdump -M intel -D s > codes; python3 ./loader.py < in | grep -a "\|ctf"
*/
