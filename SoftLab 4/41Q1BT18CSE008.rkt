#lang scheme

(define (length num)
  (if (= num 0) 0 (+ 1 (length (/ (- num (remainder num 10)) 10)))))

(define (pow a b)
  (if (= b 0) 1 (* a (pow a (- b 1)))))

(define (generate n k)
  (if (= k 1) n (+ (* (generate n (- k 1)) (pow 10 (length n))) n)))

(define (sum num)
  (if (= num 0) 0 (+ (remainder num 10) (sum (/ (- num (remainder num 10)) 10)))))

(define (digitalSum num)
  (if (= (length num) 1) num (digitalSum (sum num))))

(display "Enter n: ")
(define n (read))
(display "Enter k: ")
(define k (read))
(digitalSum (generate n k))
