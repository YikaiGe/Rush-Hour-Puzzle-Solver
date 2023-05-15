(define (domain rush-hour)

  (:requirements :typing)

  (:types vehicle cell )

  (:predicates 
            (empty ?c - cell)
            (vehicleSizeThree ?v - vehicle ?c1 - cell ?c2 - cell ?c3 - cell)
            (vehicleSizeTwo ?v - vehicle ?c1 - cell ?c2 - cell)
            (horizontalRight ?c1 - cell ?c2 - cell)   
            (horizontalLeft ?c1 - cell ?c2 - cell)
            (verticalAbove ?c1 - cell ?c2 - cell)
            (verticalBelow ?c1 - cell ?c2 - cell)
            (horizontalDirection ?v - vehicle) 
            (verticalDirection ?v - vehicle)          
            (solved ?v - vehicle ?c1 ?c2 - cell)
  )


  (:action move-right-three-sized-vehicle
           :parameters (?v - vehicle ?c1 ?c2 ?c3 ?c4 - cell )
           :precondition (and (vehicleSizeThree ?v ?c1 ?c2 ?c3) (empty ?c4) (horizontalRight ?c3 ?c4) (horizontalDirection ?v))
           :effect (and (vehicleSizeThree ?v ?c2 ?c3 ?c4)
                        (not(vehicleSizeThree ?v ?c1 ?c2 ?c3))
                        (not (empty ?c2))
                        (not (empty ?c3))
                        (not (empty ?c4))
                        (horizontalDirection ?v)
                        (empty ?c1)))
                        

  (:action move-left-three-sized-vehicle
           :parameters (?v - vehicle ?c1 ?c2 ?c3 ?c4 - cell )
           :precondition (and (vehicleSizeThree ?v ?c1 ?c2 ?c3) (empty ?c4) (horizontalLeft ?c1 ?c4) (horizontalDirection ?v))
           :effect (and (vehicleSizeThree ?v ?c4 ?c1 ?c2)
                        (not(vehicleSizeThree ?v ?c1 ?c2 ?c3))
                        (not (empty ?c4))
                        (not (empty ?c1))
                        (not (empty ?c3))
                        (horizontalDirection ?v)
                        (empty ?c3)))

  (:action move-up-three-sized-vehicle
           :parameters (?v - vehicle ?c1 ?c2 ?c3 ?c4 - cell)
           :precondition (and (vehicleSizeThree ?v ?c1 ?c2 ?c3) (empty ?c4) (verticalAbove ?c1 ?c4) (verticalDirection ?v))
           :effect (and (vehicleSizeThree ?v ?c4 ?c1 ?c2)
                        (not(vehicleSizeThree ?v ?c1 ?c2 ?c3 ))
                        (not (empty ?c4))
                        (not (empty ?c1))
                        (not (empty ?c2))
                        (verticalDirection ?v)
                        (empty ?c3)))

  (:action move-down-three-sized-vehicle
           :parameters (?v - vehicle ?c1 ?c2 ?c3 ?c4 - cell)
           :precondition (and (vehicleSizeThree ?v ?c1 ?c2 ?c3) (empty ?c4) (verticalBelow ?c3 ?c4) (verticalDirection ?v))
           :effect (and (vehicleSizeThree ?v ?c2 ?c3 ?c4)
                        (not(vehicleSizeThree ?v ?c1 ?c2 ?c3))
                        (not (empty ?c2))
                        (not (empty ?c3))
                        (not (empty ?c4))
                        (verticalDirection ?v)
                        (empty ?c1)))
  
   (:action move-right-two-sized-vehicle
           :parameters (?v - vehicle ?c1 ?c2 ?c3 - cell)
           :precondition (and (vehicleSizeTwo ?v ?c1 ?c2) (empty ?c3) (horizontalRight ?c2 ?c3) (horizontalDirection ?v))
           :effect (and (vehicleSizeTwo ?v ?c2 ?c3)
                        (not(vehicleSizeTwo ?v ?c1 ?c2))
                        (not (empty ?c3))
                        (not (empty ?c2))
                        (empty ?c1)
                        (horizontalDirection ?v)))

  (:action move-left-two-sized-vehicle
           :parameters (?v - vehicle ?c1 ?c2 ?c3 - cell)
           :precondition (and (vehicleSizeTwo ?v ?c1 ?c2) (empty ?c3) (horizontalLeft ?c1 ?c3) (horizontalDirection ?v))
           :effect (and (vehicleSizeTwo ?v ?c3 ?c1)
                        (not(vehicleSizeTwo ?v ?c1 ?c2))
                        (not (empty ?c3))
                        (not (empty ?c1))
                        (empty ?c2)
                        (horizontalDirection ?v)))

  (:action move-up-two-sized-vehicle
           :parameters (?v - vehicle ?c1 ?c2 ?c3 - cell)
           :precondition (and (vehicleSizeTwo ?v ?c1 ?c2) (empty ?c3) (verticalAbove ?c1 ?c3) (verticalDirection ?v))
           :effect (and (vehicleSizeTwo ?v ?c3 ?c1)
                        (not(vehicleSizeTwo ?v ?c1 ?c2))
                        (not (empty ?c3))
                        (not (empty ?c1))
                        (empty ?c2)
                        (verticalDirection ?v)))

  (:action move-down-two-sized-vehicle
           :parameters (?v - vehicle ?c1 ?c2 ?c3 - cell)
           :precondition (and (vehicleSizeTwo ?v ?c1 ?c2) (empty ?c3) (verticalBelow ?c2 ?c3) (verticalDirection ?v))
           :effect (and (vehicleSizeTwo ?v ?c2 ?c3)
                        (not(vehicleSizeTwo ?v ?c1 ?c2))
                        (not (empty ?c2))
                        (not (empty ?c3))
                        (empty ?c1)
                        (verticalDirection ?v)))
                        
  (:action get-out
           :parameters (?v - vehicle ?c1 ?c2 - cell)
           :precondition (and (vehicleSizeTwo X ?c1 ?c2))
           :effect (and (not(vehicleSizeTwo X ?c1 ?c2))
                        (solved X ?c1 ?c2)))
  

)