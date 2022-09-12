# 난독화가 안된 경우 # 비난독화를 하는 대신 해당 파일을 psParser1.txt에 저장해야 함.
def fileRead(path_origin):
    f_origin = open(path_origin, 'r')
    f_decoding = open("psParser1.txt", 'w')
    while True:
        line = f_origin.readline()
        if not line: break
        print("원본 내용 : ", line)
        f_decoding.write(line)
        f_decoding.write("\n")

    f_origin.close()
    f_decoding.close()

