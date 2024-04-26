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
