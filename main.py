import os
import math
# import cv2 as cv
import huffman as hf

def make_log(log, print_sw, str):
    log.write(str + '\n')
    if print_sw: 
        print(str)

def process(path_src, path_dst, path_log):

    log = open(path_log, "w+", encoding="UTF-8")

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

    make_log(log, 0, "【编码报告】")
    
    # 计算平均码长、平均信息熵、编码效率
    average_len = 0
    H_U = 0
    for p, lenght in zip(output, encode_output_len):
        average_len += p*lenght
        H_U += (- (p*math.log2(p)) )
    
    make_log(log, 0, "平均码长：" + str(average_len))
    make_log(log, 0, "平均信息熵：" + str(H_U))
    make_log(log, 0, "编码效率：" + str( (H_U / average_len) * 100 ) + "%")
    
    # 判断是否唯一可译码
    flag = 0
    for i in range(len(encode_output)):
        for j in range(i+1, len(encode_output)):
            if encode_output[j][0:len(encode_output[i])] == encode_output[i]:
                make_log(log, 0, "非唯一可译码")
                flag = 1
                break
    
    if 0 == flag:
        make_log(log, 0, "唯一可译码：是")
    else:
        make_log(log, 0, "唯一可译码：否")
    
    # 计算编码的方差
    sigma_I = 0
    for p in output:
        sigma_I += p*(((-math.log2(p)) - H_U) * ((-math.log2(p)) - H_U) )
    
    make_log(log, 0, "方差：" + str(sigma_I))
    
    # 输出
    output = [round(r, 3) for r in output]
    
    make_log(log, 0, '|次数|概率|码元|霍夫曼编码|码长|')
    make_log(log, 0, '|:-:|:-:|:-:|:-:|:-:|')
    for times_sym, p, symbol, encode_r, encode_r_len in zip(hashmap_src, output, [("$P_{" + symbol + "}$") for symbol in output_symbol], encode_output, encode_output_len):
        make_log(log, 0, "|" + str(times_sym) + "|" + str(p) + "|" + str(symbol) + "|" + str(encode_r) + "|" + str(encode_r_len) + "|")

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

            cache_dst += encode_output[readByte]    # 写入编码

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
                
                cache_dst = ""    # 清空缓冲区
        
            else:
                continue    # 凑不够
                
    
    src.close()
    dst.close()

if __name__ == "__main__":
    
    path_src = "src"
    path_dst = "dst"
    path_log = "log"

    root_log = open(path_log + "\\main.md", "w+", encoding="UTF-8")

    for root, dirs, files in os.walk(path_src):
        for file in files:
            if ".bmp" in file:
                path_tarSrc = os.path.join(root, file)
                path_tarDst = os.path.join(root, file + ".hf").replace(path_src, path_dst)
                path_tarLog = os.path.join(root, file + ".md").replace(path_src, path_log)

                process(path_tarSrc, path_tarDst, path_tarLog)

                tarSrc_size = os.path.getsize(path_tarSrc)
                tarDst_size = os.path.getsize(path_tarDst)
                
                if 0 == tarDst_size:
                    make_log(root_log, 1, f"[ERROR] 图片 {path_tarSrc} 压缩后大小为 0 ")
                else: 
                    compress_rate = (tarDst_size / tarSrc_size)
                    make_log(root_log, 1, f"[INFO] 图片 {path_tarSrc} 压缩比为：{compress_rate} ({tarSrc_size} B => {tarDst_size} B)")
