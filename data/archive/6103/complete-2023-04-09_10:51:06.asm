%include "in_out.asm"

section .data
    sum dq 0
    flag db 0
    counter db 0
    isFirstDev db 0

    msgPerfect db 'Perfect',10
    lenPerfect equ $ - msgPerfect

    msgNope db 'Nope',10
    lenNope equ $ - msgNope

    msgSpace db ' '
    lenSpace equ $ - msgSpace
section .text
    global  _start

_start:
    call readNum
    xor rcx, rcx
    mov rbx, rax

complete:   
    inc rcx
    cmp rcx, rax
    je end    ;finished
    xor rdx, rdx
    push rax
    div rcx     ;cal remaining, rdx:remaining, rax:quotient
    cmp rdx,0   ;check divisibility
    pop rax
    je check 
    
    jmp complete
check :
    cmp BYTE[flag],0
    je incsum
    jne print

print:
    cmp BYTE[isFirstDev], 0
    je firstDev

    push rbx
    push rcx
    
    mov ebx, 1
    mov ecx, msgSpace
    mov edx, lenSpace
    mov eax, 4
    int 0x80

    pop rcx
    pop rbx

    mov rax,rcx
    call writeNum
    mov rax, R9

    jmp complete
firstDev:
    mov BYTE[isFirstDev], 1
    mov rax,rcx
    call writeNum

    mov rax, rbx

    jmp complete
incsum:
    add [sum], rcx
    inc BYTE[counter]
    jmp complete
end:
    cmp BYTE[flag],1
    je exit

    cmp QWORD[sum], rax 
    je perfect
    jne nope

perfect:
    mov R9, rbx

    mov ebx, 1
    mov ecx, msgPerfect
    mov edx, lenPerfect
    mov eax, 4
    int 0x80

    mov rax, R9
    mov rbx, R9

    mov rcx, 0
    mov BYTE[flag], 1

    cmp rax, 1
    je exception

    jmp complete
exception:
    call writeNum
    jmp exit
nope:
    mov R9, rbx

    mov ebx, 1
    mov ecx, msgNope
    mov edx, lenNope
    mov eax, 4
    int 0x80

    mov rax, R9
    mov rbx, R9

    mov rcx, 0
    mov BYTE[flag], 1
    cmp rax, 0
    je exit

    jmp complete
exit:
    mov     ebx,     0
    mov     eax,     1
    int     0x80


;  one is not perfect because its divisor(1) is equal to itself