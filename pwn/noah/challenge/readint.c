#include <stdio.h>
#include <stdlib.h>

int main() {
   char buf[5];
   fgets(buf, 5, stdin);
   int res = atoi(buf);
   //printf("%d\n", res);
   
   return res;
}
