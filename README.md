
# Fairy_Stockfish Xiangqi Tool
This is a tool for ianfab's Fairy-Stockfish, which help you input your moves in chinese traditional format in `xboard` mode.
Currently, it only supports red side.

# Usage:
run xiangqi.py and type your moves in chinese traditional format.

# Examples
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

ex:
* 炮二平五 : c2=5
* 馬八進七 : h8+7
* 前車退二 : r+-2

Fairy-Stockfish's move will present in traditional chinese notation, too.
