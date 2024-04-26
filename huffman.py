

def encode(input_P, D):
    input_P_symbol = []
    output_P = []    # 每个码元的概率
    output_P_runtime = []
    output_P_symbol = []    # 记录各个码元由什么组成
    output_P_symbol_runtime = []
    encode_output_P = []    # 编码结果
    encode_output_P_len = []    # 编码结果长度

    for in_p,i in zip(input_P, range(len(input_P))):
        output_P.append(in_p)
        input_P_symbol.append(str(i+1))
        output_P_symbol.append(str(i+1))
        encode_output_P.append("")
        encode_output_P_len.append(0)
    
    # 霍夫曼编码求最佳二元码
    output_P_runtime = output_P.copy()
    output_P_symbol_runtime = output_P_symbol.copy()
    
    ## 从大到小排序
    while len(output_P_symbol_runtime) > 1:
    
        ## 从大到小排序
        output_P_runtime, output_P_symbol_runtime = sort_in_P(output_P_runtime, output_P_symbol_runtime)
        # make_log(str("概率：" + str(output_P_runtime) + "\n对应码元：" + str([ ("$P_{"+symbol+"}$") for symbol in output_P_symbol_runtime]).replace("+","")))
    
        ## 清空处理区域
        min_runtime = []
        min_symbol_runtime = []
    
        ## 取出最小的D数
        end_flag = 0
        for d in range(D):
            if 0 == len(output_P_runtime):
                end_flag = 1
                break
            min_runtime.append(output_P_runtime.pop())
            min_symbol_runtime.append(output_P_symbol_runtime.pop())
    
        ## 对对应的编码进行修改
        for d, min_s_r in zip(range(D), min_symbol_runtime):
            min_process(min_s_r, str(d), output_P_symbol, encode_output_P, encode_output_P_len)
    
        ## 生成新的数
        new = sum(min_runtime)
        new_symbol = ""
        for min_symbol in min_symbol_runtime:
            new_symbol += str(min_symbol + "+")
        new_symbol = new_symbol[0:-1]    # 去掉最后一个+
    
        ## 添加到列表中
        output_P_runtime.append(new)
        output_P_symbol_runtime.append(new_symbol)
    
        if 1 == end_flag:
            break
    
    return output_P, output_P_symbol, encode_output_P, encode_output_P_len

def sort_in_P(P, P_symbol):
    for i in range(len(P)):
        for j in range(i+1, len(P)):
            if P[i] < P[j]:
                P[i], P[j] = P[j], P[i]
                P_symbol[i], P_symbol[j] = P_symbol[j], P_symbol[i]
            elif P[i] == P[j]:
                if len(P_symbol[i]) < len(P_symbol[j]):
                    P_symbol[i], P_symbol[j] = P_symbol[j], P_symbol[i]

    return P, P_symbol

def min_process(min_symbol_runtime, add_char, output_P_symbol, encode_output_P, encode_output_P_len):
    once_flag = 0

    while ("+" in min_symbol_runtime) or (0 == once_flag):
        right = min_symbol_runtime.split("+")[-1]
        encode_output_P[output_P_symbol.index(right)] = add_char + encode_output_P[output_P_symbol.index(right)]
        encode_output_P_len[output_P_symbol.index(right)] += 1
        min_symbol_runtime = min_symbol_runtime[0:-len(right)-1]

        if ("+" not in min_symbol_runtime) and ("" != min_symbol_runtime):
            right = min_symbol_runtime
            encode_output_P[output_P_symbol.index(right)] = add_char + encode_output_P[output_P_symbol.index(right)]
            encode_output_P_len[output_P_symbol.index(right)] += 1
            min_symbol_runtime = min_symbol_runtime[0:-len(right)-1]

        once_flag = 1

def compress(path_src, path_dst):

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

    output, output_symbol, encode_output, encode_output_len = encode(P_src_symbol, 2)    # 2元编码
    
    # 判断是否唯一可译码
    flag = 0
    for i in range(len(encode_output)):
        for j in range(i+1, len(encode_output)):
            if encode_output[j][0:len(encode_output[i])] == encode_output[i]:
                return

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
