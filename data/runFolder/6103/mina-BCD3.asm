%include "in_out.asm"

section .text
    global  _start

readBinary:
    xor rbx, rbx
    whileDigit:
        call getc
        cmp rax, '0'
        je ifchar
    
        cmp rax, '1'
        je ifchar

        jmp endWhile

        ifchar:
            sub rax, '0'
            shl rbx, 1
            add rbx, rax
            jmp     whileDigit

    endWhile:
        mov rax, rbx
        ret

convert256xTo100x:
    xor rcx, rcx
    shr rax, 2
    add rcx, rax

    shr rax, 1
    add rcx,rax

    shr rax, 3
    add rcx, rax
    
    mov rax, rcx
    ret 
convert16yTo10y:
    xor rcx, rcx
    shr rax, 1
    add rcx, rax

    shr rax, 2
    add rcx,rax

    mov rax, rcx
    ret 

print:
    skipzeros:
        cmp r12, 64
        je exit
        inc r12
        shl rax, 1
        jnc skipzeros
    
    call print1
    whileNotComplete:
        cmp r12, 64
        je exit

        inc r12
        shl rax, 1

        jnc print0
        jc print1
    ret
print1:
    push rax
    mov rax, 1
    call writeNum
    pop rax
    jmp whileNotComplete
print0:
    push rax
    mov rax, 0
    call writeNum
    pop rax
    jmp whileNotComplete
_start:
    mov r10, 10
    call readBinary
    xor rbx, rbx
    
    push rax

    and rax, 0xf00 ;rax = 256x
    call convert256xTo100x ;rax
    add rbx, rax 
    
    mov rax,[rsp]
    and rax, 0x0f0 
    call convert16yTo10y
    add rbx, rax

    mov rax, [rsp]
    and rax, 0x00f
    add rbx, rax

    mov rax, rbx
    xor r12, r12

    ; call writeNum
    ; call newLine

    call print
exit:
    mov     ebx,     0
    mov     eax,     1
    int     0x80
