
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "mem.h"


int step() {
   char inst = map[posx + posy * COLS_DEFAULT];
   switch(inst) {
      case '@':  return 1;   // terminate
      case '>':  { dirx =  1;   diry =  0;   break; }
      case '<':  { dirx = -1;   diry =  0;   break; }
      case '^':  { dirx =  0;   diry = -1;   break; }
      case 'v':  { dirx =  0;   diry =  1;   break; }
      case '_':  {
         if (stack_ptr < 1) return 2;
         dirx = (stack[stack_ptr - 1] == 0) ? 1 : -1;
         diry = 0;
         break;
      }
      case '|':   {
         if (stack_ptr < 1) return 2;
         diry = (stack[stack_ptr - 1] == 0) ? 1 : -1;
         dirx = 0;
         break;
      }
      case '.': {
         if (stack_ptr < 1) return 2;
         putchar(stack[stack_ptr - 1]);
         break;
      }
      case ':': {
         if (stack_ptr < 1) return 2;
         printf("%d", stack[stack_ptr - 1]);
         break;
      }
      case '+':  {
         if (stack_ptr < 2) return 2; 
         stack[stack_ptr - 2] = stack[stack_ptr - 1] + stack[stack_ptr - 2];
         --stack_ptr;
         break;
      }
      case '-':  {
         if (stack_ptr < 2) return 2; 
         stack[stack_ptr - 2] = stack[stack_ptr - 2] - stack[stack_ptr - 1];
         --stack_ptr;
         break;
      }
      case '*':  {
         if (stack_ptr < 2) return 2; 
         stack[stack_ptr - 2] = stack[stack_ptr - 1] * stack[stack_ptr - 2];
         --stack_ptr;
         break;
      }
      case '/':  {
         if (stack_ptr < 2) return 2; 
         stack[stack_ptr - 2] = stack[stack_ptr - 2] / stack[stack_ptr - 1];
         --stack_ptr;
         break;
      }
      case '%':  {
         if (stack_ptr < 2) return 2; 
         stack[stack_ptr - 2] = stack[stack_ptr - 2] % stack[stack_ptr - 1];
         --stack_ptr;
         break;
      }
      case '&':  {
         if (stack_ptr < 2) return 2; 
         stack[stack_ptr - 2] = stack[stack_ptr - 1] & stack[stack_ptr - 2];
         --stack_ptr;
         break;
      }
      case ',':  {
         if (stack_ptr < 2) return 2;
         char tmp = stack[stack_ptr - 2];
         stack[stack_ptr - 2] = stack[stack_ptr - 1];
         stack[stack_ptr - 1] = tmp;
         break;
      }
      case '!': {
         if (stack_ptr < 1) return 2;
         char v = stack[stack_ptr - 1];
         stack[stack_ptr - 1] = (v == 0);
         break;
      }
      case 'g': {
         if (stack_ptr < 2) return 2;
         char x = stack[stack_ptr - 2];
         if (x < 0 || x >= cols) return 2;
         char y = stack[stack_ptr - 1];
         if (y < 0 || y >= rows) return 2;
         stack[stack_ptr - 2] = map[y * cols + x];
         --stack_ptr;
         break;
      }
      case 'p': {
         if (stack_ptr < 3) return 2;
         char x = stack[stack_ptr - 3];
         if (x < 0 || x >= cols) return 2;
         char y = stack[stack_ptr - 2];
         if (y < 0 || y >= rows) return 2;
         map[y * cols + x] = stack[stack_ptr - 1];
         stack_ptr -= 3;
         break;
      }
      case '#': {
         if (stack_ptr < 1) return 2;
         stack[stack_ptr] = stack[stack_ptr - 1];
         ++stack_ptr;
         break;
      }
      case '~':   {
         if (stack_ptr < 1) return 2;
         --stack_ptr;
         break;
      }
      //case '0':  inst = 0;  // push 0
      default:   // push 0
         if (stack_ptr >= NSTACK) return 2;
         stack[stack_ptr] = 0;
         ++stack_ptr;
   }
   // move and return false
   posx = (posx + dirx + cols) % cols;
   posy = (posy + diry + rows) % rows;
   miles += inst + 1;
   if (miles > 0x313370) return 2;
   return 0;
}


int main(int argc, const char** const argv) {

   if (argc < 3) return 1;

   // max rows
   int maxRows = atoi(argv[1]);
   if (maxRows <= 0 || maxRows > ROWS_DEFAULT) return 2;

   // read flag
   const char* flagFile = argv[2];
   FILE* fd = fopen(flagFile, "r");
   if (fd == NULL) {
      printf("could not read flag\n");
      exit(2);
   }
   fscanf(fd, "%s", flag);
   fclose(fd);

   setbuf(stdout, NULL);

   printf("\n** max_rows=%d, flag_file=%s **\n", maxRows, flagFile); 

   // setup VM
   rows = ROWS_DEFAULT;
   cols = COLS_DEFAULT;
   posx = 0;
   posy = 0;
   miles = 0;
   stack_ptr = 0;

   // read map
   //      12345678901234567890123456789012345678901234567890123
   printf("\n"
          "-=-=-=-=-=-=-=-=-=-=-=-+=====+-=-=-=-=-=-=-=-=-=-=-=-\n"
          "  [...]\n"
          "  Make thee an ark of gopher wood;\n"
          "  rooms shalt thou make in the ark, \n"
          "  and shalt pitch it within and without with pitch.\n"
          "  [...]\n"
          "-=-=-=-=-=-=-=-=-=-=-=-+=====+-=-=-=-=-=-=-=-=-=-=-=-\n"
          "\n");

   printf("chart thy voyage:\n");
   memset(map, 0, rows * cols);
   for (int i = 0; i < maxRows; ++i) {
      char* buf = map + i * cols;
      fgets(buf, cols + 2, stdin);
      int len = strlen(buf);
      if (len == 0 || (len == 1 && buf[0] == '\n')) break;
      else if (buf[len - 1] == '\n') buf[len - 1] = 0;
   }

   // exec loop
   int res;
   while ((res = step()) == 0) ;

   // summary
   if (res == 1)
      printf("thou journeyed far (%d miles), hast thou found knowledge?\n", miles);
   else
      printf("thou perished\n");

   return 0;
}
