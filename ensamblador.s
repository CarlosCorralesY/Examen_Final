.data

var_x1: .word 0:1
var_f2: .word 0:1
var_f3: .word 0:1

.text

label_f1:

move $fp $sp
sw $ra 0($sp)
addiu $sp $sp -4


lw $a0, 8($sp)
sw $a0, 0($sp)
addiu $sp $sp -4

li $a0,10

lw $t1 4($sp)



add $a0 $t1 $a0

addiu $sp $sp 4

lw $ra 4($sp)
addiu $sp $sp 12
lw $fp 0($sp)
jr $ra


main:

la $t0, var_x1
lw $a0, 0($t0)
sw $a0, 0($sp)
addiu $sp, $sp, -4

li $a0,15
sw $a0 0($sp)
addiu $sp $sp-4

li $a0,1

lw $t1 4($sp)



add $a0 $t1 $a0

addiu $sp $sp 4

lw $t1 4($sp)

la $t0, var_x1
sw $a0, 0($t0)

li $a0, 10
sw $a0, 0($sp)
add $sp, $sp, -4

li $a0, 5
sw $a0, 0($sp)
add $sp, $sp, 4

bgt $a0, $t1, label_true_>
label_true_>:
la $t0, var_f2
lw $a0, 0($t0)
sw $a0, 0($sp)
addiu $sp, $sp, -4

li $a0,5
sw $a0 0($sp)
addiu $sp $sp-4

li $a0,1

lw $t1 4($sp)



add $a0 $t1 $a0

addiu $sp $sp 4

lw $t1 4($sp)

la $t0, var_f2
sw $a0, 0($t0)


label_false:
la $t0, var_f3
lw $a0, 0($t0)
sw $a0, 0($sp)
addiu $sp, $sp, -4

li $a0,1
sw $a0 0($sp)
addiu $sp $sp-4

li $a0,6

lw $t1 4($sp)



add $a0 $t1 $a0

addiu $sp $sp 4

lw $t1 4($sp)

la $t0, var_f3
sw $a0, 0($t0)


b label_end

label_end:

sw $fp 0($sp)
addiu $sp $sp-4

li $a0, 5
sw $a0 0($sp)
addiu $sp $sp -4

jal label_f1


jr $ra