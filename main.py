import math
# import cv2 as cv
import huffman as hf

log = open("log.md", "w+")

def make_log(str):
    log.write(str + '\n')
    print(str)

if __name__ == "__main__":
    path_src = "src.bmp"
    path_dst = "src.bmp.hf"
    hashmap_src = [0 for i in range(0, 256)]

    # ==================== 码元统计 ====================
    
    # src = cv.imread(path_src)    # 原图
    with open(path_src, "rb") as src:
        while True:
            readByte = src.read(1)    # 读入 8 位

            # 检查是否已到达文件末尾
            if not readByte:
                break

            # 将字节转换为无符号整数
            readByte = ord(readByte)

            hashmap_src[readByte] += 1    # 统计一次

    sum_hashmap_src = sum(hashmap_src)
    P_src_symbol = [(hashmap_src[i] / sum_hashmap_src) for i in range(0, 256)]

    src.close()

    # ==================== 霍夫曼编码 ====================

    output, output_symbol, encode_output, encode_output_len = hf.encode(P_src_symbol, 2)    # 2元编码

    make_log("【编码报告】")

    if 1 != sum(output):
        make_log("结果出错：" + str(sum(output)))
    
    # 计算平均码长
    average_len = 0
    H_U = 0
    for p, lenght in zip(output, encode_output_len):
        average_len += p*lenght
        H_U += (- (p*math.log2(p)) )
    
    make_log("平均码长：" + str(average_len))
    make_log("编码效率：" + str(H_U / (average_len * math.log2(2)) * 100) + "%")
    
    # 判断是否唯一可译码
    flag = 0
    for i in range(len(encode_output)):
        for j in range(i+1, len(encode_output)):
            if encode_output[j][0:len(encode_output[i])] == encode_output[i]:
                make_log("非唯一可译码")
                flag = 1
                break
    
    if 0 == flag:
        make_log("唯一可译码")
    
    # 计算编码的方差
    sigma_I = 0
    for p in output:
        sigma_I += p*(((-math.log2(p)) - H_U) ** 2 )
    
    make_log("方差：" + str(sigma_I))
    
    # 输出
    # output = [round(r, 3) for r in output]
    
    make_log('|次数|概率|码元|霍夫曼编码|码长|')
    make_log('|:-:|:-:|:-:|:-:|:-:|')
    for times_sym, p, symbol, encode_r, encode_r_len in zip(hashmap_src, output, [("$P_{" + symbol + "}$") for symbol in output_symbol], encode_output, encode_output_len):
        make_log("|" + str(times_sym) + "|" + str(p) + "|" + str(symbol) + "|" + str(encode_r) + "|" + str(encode_r_len) + "|")

    # ==================== 文件写入 ====================

    with open(path_src, "rb") as src, open(path_dst, "wb") as dst:
        cache_dst = ""    # 缓冲区，凑够整个整个字节再写入

        while True:
            readByte = src.read(1)    # 读入 8 位

            # 检查是否已到达文件末尾
            if not readByte:
                break

            # 将字节转换为无符号整数
            readByte = ord(readByte)

            cache_dst += encode_output[readByte]

            if 0 == (len(cache_dst) % 8):    # 凑够了
                while "" != cache_dst:
                    byte_toWrite = 0

                    for i in range(0, 8):
                        if '1' == cache_dst[i]:
                            byte_toWrite = (byte_toWrite << 1) + 1
                        if '0' == cache_dst[i]:
                            byte_toWrite = (byte_toWrite << 1) + 0

                    dst.write(byte_toWrite.to_bytes(1, "big"))    # 写入最前面的一个字节
                    cache_dst = cache_dst[8:]    # 去掉已写入的
            else:
                cache_dst += encode_output[readByte]    # 凑不够，丢到缓冲区后面
    
    src.close()
    dst.close()