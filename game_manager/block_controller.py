#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import random

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0

    # GetNextMove is main function.
    # input
    #    GameStatus : this data include all field status, 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : this data include next shape position and the other,
    #               if return None, do nothing to nextMove.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        # print GameStatus
        print("=================================================>")
        pprint.pprint(GameStatus, width = 61, compact = True)

        # search best nextMove -->
        # random sample
        nextMove["strategy"]["direction"] = random.randint(0,4)
        nextMove["strategy"]["x"] = random.randint(0,9)
        nextMove["strategy"]["y_operation"] = 1
        nextMove["strategy"]["y_moveblocknum"] = random.randint(1,8)
        # search best nextMove <--

        # return nextMove
        print("===", datetime.now() - t1)
        print(nextMove)
        return nextMove


class Block_ForeverController(object):
    ''' Implements https://tetris.wiki/Playing_forever '''

    def __init__(self):
        self.count = 0

    # GetNextMove is main function.
    # input
    #    GameStatus : this data include all field status,
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : this data include next shape position and the other,
    #               if return None, do nothing to nextMove.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        # print GameStatus
        print("=================================================>")
        pprint.pprint(GameStatus, width = 61, compact = True)

        # get data from GameStatus
        # current shape info
        block_dir = GameStatus['block_info']['currentDirection']
        block_shape = GameStatus['block_info']['currentShape']['index']
        block_x = GameStatus['block_info']['currentX']
        block_y = GameStatus['block_info']['currentY']
        board = GameStatus['field_info']['backboard']
        # default board definition
        board_w = GameStatus['field_info']['width']
        board_h = GameStatus['field_info']['height']

        shapeI = 1
        shapeL = 2
        shapeJ = 3
        shapeT = 4
        shapeO = 5
        shapeS = 6
        shapeZ = 7
        # order = (
        #     0             1             2             3             4             5             6
        #     Shape.shapeL, Shape.shapeJ, Shape.shapeT, Shape.shapeO, Shape.shapeS, Shape.shapeZ, Shape.shapeI, 6
        #     Shape.shapeL, Shape.shapeJ, Shape.shapeO, Shape.shapeS, Shape.shapeZ, Shape.shapeT, Shape.shapeI, 13

        #     Shape.shapeL, Shape.shapeJ, Shape.shapeT, Shape.shapeO, Shape.shapeS, Shape.shapeZ, Shape.shapeI, 20
        #     Shape.shapeL, Shape.shapeJ, Shape.shapeO, Shape.shapeS, Shape.shapeZ, Shape.shapeT, Shape.shapeI, 27
        # )

        # search best nextMove -->
        id_in_bag = (self.count % 140) % 7
        bag = (self.count % 140) // 7
        if bag < 12:
            # S, T, Z loop
            # T
            if self.count % 28 == 2:
                assert block_shape == shapeT
                next_dir, next_x = 3, 1
            elif self.count % 28 == 12:
                assert block_shape == shapeT
                next_dir, next_x = 2, 3
            elif self.count % 28 == 16:
                assert block_shape == shapeT
                next_dir, next_x = 0, 0
            elif self.count % 28 == 26:
                assert block_shape == shapeT
                next_dir, next_x = 1, 2
            # S
            elif self.count % 28 in (4, 10):
                assert block_shape == shapeS
                next_dir, next_x = 1, 2
            elif self.count % 28 in (18, 24):
                assert block_shape == shapeS
                next_dir, next_x = 1, 0
            # Z
            elif self.count % 28 in (5, 11):
                assert block_shape == shapeZ
                next_dir, next_x = 1, 0
            elif self.count % 28 in (19, 25):
                assert block_shape == shapeZ
                next_dir, next_x = 1, 2
            # L, O, J loop
            # L
            elif self.count % 7 == 0:
                assert block_shape == shapeL
                next_dir, next_x = 0, 6
            # J
            elif self.count % 7 == 1:
                assert block_shape == shapeJ
                next_dir, next_x = 0, 9
            # O
            elif self.count % 14 in (3, 9):
                assert block_shape == shapeO
                next_dir, next_x = 0, 7
            # I loop
            elif self.count % 28 in (6, 20):
                assert block_shape == shapeI
                next_dir, next_x = 0, 4
            elif self.count % 28 in (13, 27):
                assert block_shape == shapeI
                next_dir, next_x = 0, 5
            else:
                raise ValueError('bag < 12: count={}'.format(self.count))
        else:  # 12 <= bag < 20
            offset = 0
            if bag >= 16:
                # S, T, Z loop
                if self.count % 28 in (2, 12, 16, 26, 4, 10, 18, 24, 5, 11, 19, 25):
                    offset = 6
                # L, O loop
                elif self.count % 14 in (0, 7, 3, 9):
                    offset = -6
            # S, T, Z loop
            # T
            if self.count % 28 == 2:
                assert block_shape == shapeT
                next_dir, next_x = 3, 1 + offset
            elif self.count % 28 == 12:
                assert block_shape == shapeT
                next_dir, next_x = 2, 3 + offset
            elif self.count % 28 == 16:
                assert block_shape == shapeT
                next_dir, next_x = 0, 0 + offset
            elif self.count % 28 == 26:
                assert block_shape == shapeT
                next_dir, next_x = 1, 2 + offset
            # S
            elif self.count % 28 in (4, 10):
                assert block_shape == shapeS
                next_dir, next_x = 1, 2 + offset
            elif self.count % 28 in (18, 24):
                assert block_shape == shapeS
                next_dir, next_x = 1, 0 + offset
            # Z
            elif self.count % 28 in (5, 11):
                assert block_shape == shapeZ
                next_dir, next_x = 1, 0 + offset
            elif self.count % 28 in (19, 25):
                assert block_shape == shapeZ
                next_dir, next_x = 1, 2 + offset
            # L, O loop
            # L
            elif self.count % 14 == 0:
                assert block_shape == shapeL
                next_dir, next_x = 0, 8 + offset
            elif self.count % 14 == 7:
                assert block_shape == shapeL
                next_dir, next_x = 2, 9 + offset
            # O
            elif self.count % 14 in (3, 9):
                assert block_shape == shapeO
                next_dir, next_x = 0, 6 + offset
            # I, J loop
            # I
            elif self.count % 14 == 6:
                assert block_shape == shapeI
                next_dir, next_x = 0, 5
            elif self.count % 14 == 13:
                assert block_shape == shapeI
                next_dir, next_x = 0, 4
            # J
            elif self.count % 14 == 1:
                assert block_shape == shapeJ
                next_dir, next_x = 0, 5
            elif self.count % 14 == 8:
                assert block_shape == shapeJ
                next_dir, next_x = 2, 4
            else:
               raise ValueError('bag>=12: {}'.format(self.count))

        nextMove['strategy']['direction'] = next_dir
        nextMove['strategy']['x'] = next_x
        nextMove['strategy']['y_operation'] = 1
        nextMove['strategy']['y_moveblocknum'] = 21
        # search best nextMove <--

        # return nextMove
        print("===", datetime.now() - t1)
        print(nextMove)
        self.count += 1
        return nextMove


BLOCK_CONTROLLER = Block_ForeverController()
