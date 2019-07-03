

.sub main



$P8 = new "ResizablePMCArray"
$P8[1] = 2
$P8[2] = 5
$P8[3] = 1
$P8[4] = 0
$P8[5] = 7


$P9 = new "Integer"
$P9 = 5
bubble($P8, $P9)

$P4 = $P8[1]
say $P4

$P4 = $P8[2]
say $P4

$P4 = $P8[3]
say $P4

$P4 = $P8[4]
say $P4

$P4 = $P8[5]
say $P4

.end
.sub bubble
.param pmc input
.param pmc len


$P0 = new "Integer"
$P0 = 0
while_loop_7:
if $P0 != 0 goto end_while_loop_7

$P0 = 1
loop_init_6:
.local pmc x
x = box 1

loop_test_6:
if x < len goto loop_body_6
goto loop_end_6

loop_body_6:


$P1 = new "Integer"
$P1 = x + 1

$P2 = new "Integer"
$P2 = input[x]

$P3 = new "Integer"
$P3 = input[$P1]
if $P2 <= $P3 goto end_if_5

$P0 = 0

$P4 = new "Integer"
$P4 = $P2
input[x] = $P3
input[$P1] = $P4
end_if_5:


inc x
goto loop_test_6
loop_end_6:

goto while_loop_7
end_while_loop_7:

.end

