#lang scheme
(define (checkMono arr size currIndex)
  (if (= currIndex size) (display "its monotonously increasing")
      (if (> (vector-ref arr currIndex) (vector-ref arr (- currIndex 1)))
          (checkMono arr size (+ currIndex 1))
          (display "its not monotously increasing")
          )
      )
  )

(checkMono '#(1 1 3) 3 1)