flag = b'bctf{i_f0Rg0r_1dt_h4$_cpl_$3tt1nGs_9f33526563340a912e83}'
redacted_flag = b'bctf{REDACTED_REDACTED_REDACTED_REDACTED_REDACTED_REDAC}'

def unredact(in_file, out_file):
    assert(len(flag) == len(redacted_flag))

    with open(in_file, 'rb') as input, open(out_file, 'wb') as output:
        data = input.read()
        data = data.replace(redacted_flag, flag)
        output.write(data)
        
unredact('disk_redacted.img', 'disk_final.img')
unredact('kernel_redacted', 'kernel_final')
