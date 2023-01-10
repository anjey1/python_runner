# screen_width = 800
# screen_height = 400


level_map = [
    # 0 #1 #2 #3... * 64
    '                            ',  # 0 * 64
    '                            ',  # 1 * 64
    ' XX    XXX              XX  ',  # 2 * 64
    ' XX P                       ',  # 3 * 64
    ' XXXX          XX        XX ',
    ' XXXX        XX             ',
    ' XX    X  XXXX    XX  XX    ',
    '       X  XXXX    XX  XXX   ',
    '    XXXX  XXXXXX  XX  XXXX  ',
    'XXXXXXXX  XXXXXX  XX  XXXX  '
]

tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size  # 10 * 64 = 640
