## declaração de glifos
os glifos devem ser declarados num arquivo json com o padrão esperado. isso envolve colocar os dados de todos os paths num array dentro desse json  
isso é feito abrindo o svg como texto e obtendo o valor de string do elemento \<d\> de cada path. cada path novo deve ser um item separado no array
  
## transformação de glifos
no inkscape, o que deve ser transformado SEMPRE é o path do glifo em si, e não o seu grupo  
isso evita ter que usar transforms diferentes pra cada glifo e os mantêm normalizados  
  
depois de qualquer alteração na transformação do path, deve se aplicar ela  
isso é feito com ctrl + shift + m > apply