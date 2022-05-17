#lang scheme
(define (towersOfHanoi size fromRod toRod auxRod)
  (if (= size 1) (begin
                   (display "Move disk from rod ")
                   (display fromRod)
                   (display " to rod ")
                   (display toRod)
                   (newline))
      (begin
        (towersOfHanoi (- size 1) fromRod auxRod toRod)
        (begin
          (display "Move disk from rod ")
          (display fromRod)
          (display " to rod ")
          (display toRod)
          (newline))
        (towersOfHanoi (- size 1) auxRod toRod fromRod)
       )
      )
  )
  
(display "Enter the number of blocks in Towers of Hanoi: ")
(define size (read))
(define T1 #\A)
(define T2 #\B)
(define T3 #\C)
(towersOfHanoi size T1 T3 T2)