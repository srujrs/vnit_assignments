#lang scheme
(define (getBinary size arr currSize)
  (if (= currSize size)
      (begin
        (display arr)
        (newline)
        )
      (begin
        (vector-set! arr currSize 0)
        (getBinary size arr (+ currSize 1))
        (vector-set! arr currSize 1)
        (getBinary size arr (+ currSize 1))
        )
      )
  )
      
(display "Enter the size of binary numbers u want: ")
(define size (read))
(define arr (make-vector size))
(getBinary size arr 0)