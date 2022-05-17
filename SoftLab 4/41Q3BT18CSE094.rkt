#lang scheme

(define (countDigits num count)
  (if (= num 0) (display count)
      (countDigits (/ (- num (remainder num 10)) 10) (+ count 1)) 
      )
  )
 

(display "Enter your num: ")
(define num (read))
(countDigits num 0)