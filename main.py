# ==================== import ====================

import os
import math
import time
import json
import huffman as hf
import matplotlib.pyplot as plt

# ==================== 类 ====================

class treeNode:
    val = -1
    left = None
    right = None

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
    def printNode(self):
        return f"{[self.left, self.val, self.right]}\n"
    
# ==================== 全局变量 ====================

root_log = open("./log/main.md", "w+", encoding="UTF-8")

# ==================== function ====================     

def make_log(log, print_sw, str):
    log.write(str + '\n')
    if print_sw: 
        print(str)

def process(path_src, path_dst, path_log):

    start_time = time.time()

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
        if p > 0:
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
                flag = 1
                break
    
    if 0 == flag:
        make_log(log, 0, "唯一可译码：是")
    else:
        make_log(log, 0, "唯一可译码：否")
    
    # 计算编码的方差
    sigma_I = 0
    for p in [out for out in output if out > 0]:
        sigma_I += p*(((-math.log2(p)) - H_U) * ((-math.log2(p)) - H_U) )
    
    make_log(log, 0, "方差：" + str(sigma_I))
    
    # 输出
    output = [round(r, 3) for r in output]
    
    make_log(log, 0, '|次数|概率|码元|霍夫曼编码|码长|')
    make_log(log, 0, '|:-:|:-:|:-:|:-:|:-:|')
    for times_sym, p, symbol, encode_r, encode_r_len in zip(hashmap_src, output, [("$P_{" + symbol + "}$") for symbol in output_symbol], encode_output, encode_output_len):
        make_log(log, 0, "|" + str(times_sym) + "|" + str(p) + "|" + str(symbol) + "|" + str(encode_r) + "|" + str(encode_r_len) + "|")

    # ==================== 文件写入 ====================

    keys = ["HF_CODE_NUM", "HF_CODE_MIN_LEN", "HF_CODE_MAX_LEN", "HF_CODE_LIST"]
    vals = [len(output_symbol), min(encode_output_len), max(encode_output_len), encode_output]
    huffman_list = dict(zip(keys, vals))
    with open(path_dst + "list", "w+", encoding="UTF-8") as hflist:
        hflist.write(json.dumps(huffman_list, indent=4, ensure_ascii=False))
    hflist.close()

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

    make_log(root_log, 1, f"[SUCCESS] 压缩用时 {time.time() - start_time} s")

def unprocess(path_src, path_dst, path_log):

    start_time = time.time()

    # ==================== 加载霍夫曼码表 ====================
    with open(path_src + "list", "rb") as hflist:
        info_header = json.load(hflist)
    hflist.close()

    # ==================== 生成霍夫曼二叉树 ====================
    rootNode_index = 0
    huffTree = [treeNode(-1)]
    
    for code, i in zip(info_header["HF_CODE_LIST"], range(0, info_header["HF_CODE_NUM"])):
        now_index = rootNode_index

        while "" != code:
            if '0' == code[0]:    # 左子节点
                if None ==  huffTree[now_index].left:
                    huffTree.append(treeNode(-1))
                    huffTree[now_index].left = len(huffTree) - 1
                
                now_index = huffTree[now_index].left
            
            elif '1' == code[0]:    # 右子节点
                if None ==  huffTree[now_index].right:
                    huffTree.append(treeNode(-1))
                    huffTree[now_index].right = len(huffTree) - 1
                
                now_index = huffTree[now_index].right
            
            code = code[1:]    # 去掉已处理的
        
        huffTree[now_index].val = i    # 叶子节点

    # ==================== 重建文件 ====================
    readBytes_num = math.ceil(info_header["HF_CODE_MAX_LEN"] / 8.0)
    flag_eof = 0
    
    with open(path_src, "rb") as src, open(path_dst, "wb") as dst:
        cache_byte_str = ""
        now_index = rootNode_index
        while True:
            for i in range(0, readBytes_num):
                origin_byte = src.read(1)
                if not origin_byte:    # 检查是否已到达文件末尾
                    flag_eof = 1
                    break

                cache_byte_str = cache_byte_str + bin(ord(origin_byte))[2:].zfill(8)    # 读入 8 位
            
            while "" != cache_byte_str:
                if -1 != huffTree[now_index].val:
                    dst.write(huffTree[now_index].val.to_bytes(1, "big"))
                    now_index = rootNode_index    # 已写入一个值，回到根节点
                    continue
                elif '0' == cache_byte_str[0]:
                    now_index = huffTree[now_index].left
                elif '1' == cache_byte_str[0]:
                    now_index = huffTree[now_index].right
                
                cache_byte_str = cache_byte_str[1:]
            
            if flag_eof:    # 文件读取完毕
                make_log(root_log, 1, f"[SUCCESS] 图片 {path_src} 重建完成 ")
                break

    src.close()
    dst.close()
    make_log(root_log, 1, f"[SUCCESS] 重建用时 {time.time() - start_time} s")

# ==================== main ====================

if __name__ == "__main__":
    
    path_src = "src"
    path_dst = "dst"
    path_log = "log"
    path_rebuild = "rebuild"

    for root, dirs, files in os.walk(path_src):
        for file in files:
            if file.endswith(".bmp"):
                path_tarSrc = os.path.join(root, file)
                path_tarDst = os.path.join(root, file + ".hf").replace(path_src, path_dst)
                path_tarLog = os.path.join(root, file + ".md").replace(path_src, path_log)
                path_tarRebuild = os.path.join(root, file).replace(path_src, path_rebuild).replace(".bmp", "_rebuild.bmp")

                process(path_tarSrc, path_tarDst, path_tarLog)

                tarSrc_size = os.path.getsize(path_tarSrc)
                tarDst_size = os.path.getsize(path_tarDst)
                tarDst_size += os.path.getsize(path_tarDst + "list")
                
                if 0 == tarDst_size:
                    make_log(root_log, 1, f"[ERROR] 图片 {path_tarSrc} 压缩后大小为 0 ")
                else: 
                    compress_rate = (tarDst_size / tarSrc_size)
                    make_log(root_log, 1, f"[INFO] 图片 {path_tarSrc} 压缩比为：{compress_rate} ({tarSrc_size} B => {tarDst_size} B)")
                
                unprocess(path_tarDst, path_tarRebuild, path_tarLog)
