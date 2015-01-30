import sys
num_of_blk = 16384
num_of_MB  = 16
blk_content = "0000000011111111222222223333333344444444555555556666666677777777"
# def gen_blk(blk_size,blk_content):
#     blk = ""
#     for x in xrange(1,blk_size):
#         blk.append(blk_content)
#     return blk
def gen_file(num_of_blk):
    file_contents = ""
    for x in xrange(1,num_of_blk):
        file_contents += blk_content
    return file_contents
file = open("testfile.txt","a")
for x in xrange(0,num_of_MB):
    file.write(gen_file(num_of_blk))
file.close()
