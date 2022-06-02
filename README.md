
# Fairy-Stockfish Xiangqi Tool
This is a tool for ianfab's Fairy-Stockfish, which help you input your moves in chinese traditional format in `xboard` mode.
Currently, it only supports red side.

# Usage:
run xiangqi.py and type your moves in chinese traditional format.

piece|notation
---|---
將 King | k
士 adviser | a
象 elephant | e
車 rook | r
馬 horse | h
炮 cannon | c
兵 pawn | p

movement | notation
---|---
進 advance | +
退 back | -
平  horizontal move | =

## other command
* *d* show board
* *e* show evaluation of current position
* *s* show history moves


# Examples

* 炮二平五 : c2=5
* 馬八進七 : h8+7
* 前車退二 : r+-2

 *e* : +0.13
 
 *s* :
炮2平5
馬2進3
馬2進3
馬8進7
車1平2
車9平8
車2進6
炮8平9



Fairy-Stockfish's move will present in traditional chinese notation, too.
see [this page](https://xqinenglish.com/index.php/en/basics-of-xiangqi/1058-a-detailed-introduction-to-the-notation-system-in-xiangqi-chinese-chess) for more details 
