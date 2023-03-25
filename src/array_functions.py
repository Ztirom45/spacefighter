#a libbery for simpel thinks with pos and other arrays
add_pos = lambda array,value: [array[0]+value,array[1]+value] 
sub_pos = lambda array,value: [array[0]-value,array[1]-value] 
mult_pos = lambda array,value: [array[0]*value,array[1]*value]
div_pos = lambda array,value: [array[0]/value,array[1]/value]

sub2_pos = lambda array1,array2: [array1[0]-array2[0],array1[1]-array2[1]]
add2_pos = lambda array1,array2: [array1[0]+array2[0],array1[1]+array2[1]]

