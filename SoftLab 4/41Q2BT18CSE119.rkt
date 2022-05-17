#lang scheme

(define (reverse num num1)
  (cond ((= num 0) num1)
  (else (reverse (/ (- num (remainder num 10)) 10) (+ (remainder num 10) (* num1 10)))))
  )

(define (revListNums list1)
  (if (null? list1) null
      (cons (reverse (car list1) 0) (revListNums (cdr list1)))
      )
  )

(define temp (revListNums '(12 34) ))
(display temp)