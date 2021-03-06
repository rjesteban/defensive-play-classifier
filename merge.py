zonedefs1 = {"0021500149": [364, 375, 381, 392, 404],
            "0021500197": [381, 383, 388, 393],
            "0021500270": [411, 415],
            "0021500316": [320, 322, 324, 338, 352, 377, 385, 392, 395,
                           424, 426, 431, 440, 446, 454, 462, 465],
            "0021500350": [389, 393, 409, 417, 441, 446, 450,
                           454, 466, 484, 486, 496, 520, 523, 526],
            "0021500428": [339, 394, 409, 411, 414, 428, 430,
                           441, 443, 500, 502],
            "0021500476": [278, 346],
            "0021500582": [4, 7, 20, 26, 30, 71, 79, 110, 120,
                           138, 328, 343, 346, 364, 407, 411, 510],
            }


mandefs1 = {"0021500149": [33, 90, 97, 137, 157, 188, 200, 205, 206,
                          215, 269, 279, 294, 328, 342, 382, 396, 434,
                          475, 477, 500, 540, 550, 555],
           "0021500197": [],
           "0021500270": [422, 426, 427, 477, 496, 514, 556],
           "0021500316": [22, 136, 139, 141, 169, 176, 190, 254, 257,
                          264, 381, 411, 420, 425, 443],
           "0021500350": [485],
           "0021500428": [24, 60, 65, 86, 100, 103, 130, 167, 179, 264,
                          278, 281, 305, 306, 328, 341, 499, 520],
           "0021500476": [2, 9, 16, 26, 27, 36, 51, 62, 85, 86, 107, 109,
                          124, 143, 312, 329, 377, 411, 453, 490, 505],
           "0021500582": [106, 118, 141, 153, 312, 452, 457, 503,
                          525, 541, 543, 577]
           }


mandefs2 = {"0021500149": [2, 4, 7, 15, 32, 40, 41, 52, 62, 67, 72, 82, 95, 110,
                           112, 118, 126, 135, 150, 198, 202, 208, 216, 222,
                           224, 237, 249, 285, 296, 298, 312, 314, 333, 390,
                           409, 422, 425, 428, 433, 436, 440, 445, 446, 449,
                           473, 499, 527, 555],
            "0021500197": [],
            "0021500270": [410, 428, 474, 518, 545, 547],
            "0021500316": [2, 13, 89, 90, 164, 166, 170, 173, 183, 187, 188,
                           255, 314, 343, 372, 406, 415, 430, 432, 483],
            "0021500350": [410, 493, 520],
            "0021500428": [3, 14, 29, 43, 53, 73, 81, 116, 119, 123, 133, 185,
                           197, 202, 203, 219, 221, 223, 246, 261, 268, 284,
                           298, 308, 316, 340, 346, 351, 355, 359, 367, 372,
                           373, 409, 414, 428, 436, 457, 467, 473,
                           474, 482, 488, 493],
            "0021500476": [7, 19, 46, 73, 110, 121, 132, 151, 160, 168, 178,
                           179, 214, 215, 216, 217, 259, 315, 316, 319, 328,
                           329, 344, 355, 367, 369, 380, 382, 397, 437, 438,
                           440, 441, 448, 454, 484, 486, 498, 502],
            "0021500582": [13, 29, 31, 33, 67, 109, 154, 321, 326, 329, 346,
                           347, 380, 386, 409, 417, 434, 446, 481, 535, 549]
}


merged_mans = {"0021500149": [],
               "0021500197": [],
               "0021500270": [],
               "0021500316": [],
               "0021500350": [],
               "0021500428": [],
               "0021500476": [],
               "0021500582": [],
}

for game in sorted(mandefs1.keys()):
    merged_mans[game] = sorted(set(mandefs1[game] + mandefs2[game]))

print "mandefs = {"

for game in sorted(mandefs1.keys()):
    print '"' + game + '" : ' + str(merged_mans[game])

print "}"


examples = 0
for game in sorted(mandefs1.keys()):
    examples += len(zonedefs1[game]) + len(merged_mans[game])


print "\n\n\n\nNumber of examples" + str(examples)
