"""Missing utterances in each speakers"""


from typing import List


# Missing utterances in each speaker
MISSINGS: List[List[int]] = [
    # p225
    [
        15, 31, 32, 34, 41, 42, 43, 47, 48, 50, 55, 68, 69, 74, 75, 76, 77, 78, 79, 80,
        85, 87, 88, 91, 93, 95, 96, 97, 98, 99, 100, 101, 102, 105, 106, 107, 112, 119,
        125, 129, 130, 132, 134, 137, 138, 139, 140, 146, 148, 154, 155, 160, 161, 162,
        163, 164, 167, 168, 170, 178, 180, 181, 183, 184, 185, 186, 187, 188, 189, 190,
        194, 198, 204, 205, 206, 207, 209, 213, 214, 215, 216, 217, 226, 227, 228, 229,
        230, 231, 232, 233, 234, 245, 246, 247, 249, 250, 251, 252, 255, 256, 259, 260,
        261, 262, 263, 267, 269, 270, 271, 272, 278, 283, 284, 288, 292, 304, 306, 307,
        311, 313, 321, 327, 333, 338, 339, 340, 341, 342, 343, 344, 345, 360, 361, 362, 364
    ],
    [35, 38, 81, 87, 123, 147, 170, 182, 196, 222, 250, 275, 277, 282],
    [7, 115, 182, 185, 202, 221, 224, 225, 234, 325, 346, 362, 381],
    [17, 80, 201, 273, 314],
    [49, 107, 208, 276, 291, 299, 317, 321, 327, 372, 375, 383, 385],
    [4, 11, 15, 22, 67, 82, 98, 111, 136, 187, 193, 197, 229, 256, 275, 294, 301, 320, 403, 412],
    [22, 60, 75, 77, 84, 96, 182, 187, 204, 227, 287, 306, 311, 321, 335, 356, 410, 413, 425, 455],
    [157, 222, 304],
    [10, 31, 34, 35, 36, 69, 78, 124, 145, 202, 205, 206, 207, 219, 227, 287, 293, 318, 372, 380],
    [11, 78, 206, 215],
    [1, 8, 22, 67, 82, 106, 150, 160, 171, 248, 334],
    [22, 115, 116, 152, 158, 197, 209, 261, 269, 319, 324, 336],
    [153, 205, 210, 348, 367, 457],
    [], [287, 350, 356],
    [
        15, 20, 22, 54, 60, 86, 97, 131, 156, 194, 201, 263,
        316, 318, 335, 339, 341, 348, 355, 361, 367
    ],
    [17, 124, 285, 307, 351],
    [21, 202, 289, 332],
    [52, 153, 159, 169, 255],
    [269, 317, 356],
    [15, 201, 313, 478],
    [], [1, 15, 85, 91, 151, 158, 175, 195, 215, 227, 228, 233, 242, 250, 264, 325, 333, 334, 346],
    [29, 41, 112, 122, 145, 203, 213, 256, 259, 279, 303, 307, 347, 373, 470],
    [31, 86, 229, 261, 277, 354, 358, 363, 370, 371],
    [31, 49, 70, 107, 159, 180, 192, 249, 257, 259, 261, 272, 285, 318, 377, 398],
    [
        6, 19, 22, 70, 94, 105, 137, 155, 159, 166, 172, 174, 193, 204, 210, 246, 259,
        284, 286, 295, 306, 312, 315, 321, 325, 347, 353, 362, 370, 389, 393, 395, 396, 398, 406
    ],
    [36, 89, 142, 274, 325, 328],
    [56, 291],
    [299], [], [], [], [325], [], [], [240, 290],
    [17, 22, 52, 95, 111, 175, 220, 225, 229, 239, 338, 384],
    [1, 9, 62, 261], [185, 383], [101, 241, 315, 324], [8, 23, 136, 159, 281],
    [95, 120, 178, 192, 262, 351, 390],
    [], [], [1], [1, 215, 315], [1, 172, 265, 395],
    [5, 21, 107, 202, 204, 206, 232, 245, 267, 318, 319, 401, 412],
    [1, 246, 371], [1, 227, 247, 345], [1], [1], [], [1], [1], [325, 355], [], [], [], [], [],
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 18, 19],
    [17, 31, 299, 353],
    [246], [23, 24, 136, 223, 417], [22, 64, 73, 89, 214, 252, 253],
    [], [], [353], [], [113, 178, 256, 273], [], [173], [],
    [170, 200, 271, 280, 350, 353],
    [4, 385, 409, 415], [], [184], [], [1, 333], [337, 338], [],
    # p315
    [
        2, 7, 8, 10, 11, 12, 15, 17, 21, 24, 28, 29, 32, 34, 35, 36, 37, 38, 39, 40, 43,
        44, 45, 50, 52, 53, 54, 58, 59, 60, 61, 62, 63, 64, 65, 67, 69, 74, 80, 81, 82,
        83, 84, 86, 88, 89, 90, 91, 92, 97, 98, 101, 103, 104, 106, 108, 110, 112, 113,
        116, 117, 118, 119, 120, 122, 125, 127, 130, 132, 133, 134, 135, 137, 138, 139,
        140, 143, 144, 145, 146, 147, 148, 150, 151, 152, 153, 155, 156, 157, 159, 160,
        162, 163, 165, 168, 169, 170, 172, 173, 175, 177, 180, 181, 182, 185, 186, 187,
        189, 190, 191, 192, 194, 195, 197, 198, 199, 200, 201, 202, 204, 205, 211, 215,
        218, 220, 222, 223, 224, 225, 227, 233, 234, 235, 236, 237, 238, 240, 243, 244,
        245, 246, 247, 249, 251, 252, 253, 254, 258, 259, 263, 267, 268, 269, 270, 271,
        272, 274, 275, 276, 277, 278, 279, 283, 284, 286, 287, 288, 289, 290, 291, 292,
        296, 297, 299, 300, 301, 303, 304, 313, 316, 317, 321, 322, 323, 324, 325, 326,
        329, 330, 331, 332, 333, 334, 335, 338, 339, 340, 341, 342, 348, 351, 353, 354,
        355, 356, 358, 361, 362, 363, 364, 365, 367, 369, 370, 371, 373, 374, 376, 377,
        378, 379, 381, 382, 383, 384, 385, 386, 387, 389, 394, 395, 396, 398, 399, 400,
        401, 402, 404, 407, 409, 410, 411, 412, 413, 415, 416, 417, 419, 420
    ],
    [24, 203], [], [3, 4], [], [365], [], [], [29, 214, 314], [152], [9],
    [212, 298, 341, 342, 367, 414], [106], [23], [235],
    [8, 17, 138, 156, 200, 212, 272, 305, 329, 330, 373, 380],
    [], [42], [105], [], [131], [202], [279, 340, 342, 400],
    [52, 80, 93, 139, 186, 295, 296, 307],
    [], [47, 62, 281]
]
