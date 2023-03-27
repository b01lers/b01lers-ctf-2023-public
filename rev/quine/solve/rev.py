#!/usr/bin/python3
rev_string = b"^O{(u4Xz}e(tiIh.p+}Kj<&eb]0@sHecW^[.xroBCW=N3nG+r.]rGEs.UJw^y'tn_Qv(y;Ed')#@q@xI1N:wH<X1aT)NtMvNlcY0;+x[cQ4j9>Qi2#Yq&fR#os=ELTjS^/deJZ;EuY`#IQwKL)w<N<Zh,;W9X=&t0zX&E0e<_3SVaLs(pXk6z-XGHTx8T/?-^`h[K0h}`dD6kX:vEeC,mI5fR9k]{;yfO0Wg/1-Z^=WyUqN5XY1g25K1sJgKzfG."

output = []
for i in range(0, len(rev_string), 4):
    output.append(rev_string[i]-rev_string[i+1]+(rev_string[i+2]^rev_string[i+3]))

print(bytes(output))

