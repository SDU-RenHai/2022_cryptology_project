import hashlib
import random
import string

#首先定义merkle_tree的类结构
class TreeNode():
    def __init__(self, value):
        self.left = None  # 左子节点
        self.right = None  # 右子节点
        self.parent = None  # 父节点
        self.brother = None  # 兄弟节点
        self.is_root = False  # 判断是否为根节点
        self.is_left = False  # 判断是否为父节点的左子树
        self.value = value  # 叶子结点的值
        self.hash_value = hashlib.sha256(('0x00'+value).encode('utf-8')).hexdigest()  # 叶子节点的hash值

#Merkle_Tree的构造函数，输入叶子节点列表，返回根节点
def construct_tree(leave_list):
    nodes=[]
    for i in leave_list:
        nodes.append(TreeNode(i))
    while len(nodes) != 1:
        tmp=[]
        for i in range(0,len(nodes),2):
            node_left = nodes[i]
            node_left.is_left = True
            if (i+1) < len(nodes):
                node_right = nodes[i+1]
            else:
                tmp.append(nodes[i]) #对于奇数的情况，放入上一层进行计算
                break
            connect = node_left.hash_value + node_right.hash_value #级联，用于计算父节点

            #设置父节点
            parent = TreeNode(connect)
            parent.left = node_left
            parent.right = node_right
            parent.hash_value= hashlib.sha256(('0x01'+connect).encode('utf-8')).hexdigest() 
            #由于叶子节点和树节点的hash计算方式不同，此处需特别注明

            #关联左子节点和右子节点的信息
            node_left.parent = parent  # 左子节点的父节点是parent
            node_right.parent = parent  # 右子节点的父节点是parent
            node_left.brother = node_right  # 左子节点的兄弟是node_r
            node_right.brother = node_left  # 右子节点的兄弟是node_l
            node_left.is_left = True

            tmp.append(parent)
        nodes=tmp #此时相当于进行了最底层的计算，将tmp中的节点复制给nodes
    #当nodes中只剩一个元素时，为根节点，补充其信息
    node_root=nodes[0]
    node_root.is_root=True
    return node_root

#以下为验证部分

#对于某一节点node，生成Hash值和其路径
def  track_path(node):
    path=[]
    hash_value_list=[]

    if node.parent :
        hash_value_list.append(node.value)
        path.append('0')
    
    while not node.is_root : #遍历节点
        hash_value_list.append(node.brother.hash_value)
        if node.is_left:
            path.append('l')
        else:
            path.append('r')
        node = node.parent
    hash_value_list.append(node.hash_value)

    path.reverse()
    hash_value_list.reverse()

    print('路径：',path) #输出路径
    print('Hash值列表：',hash_value_list) #输出路径上节点的Hash值
    return path,hash_value_list


def verify_path(path,hash_value_list,root):
    tmp_node = root
    #用'l'、'r'、'0'分别表示路径中左子节点、右子节点、终点
    for item in path:
        if item == 'l':
            tmp_node = tmp_node.left
        elif item == 'r':
            tmp_node = tmp_node.right
        elif item == '0':
            break
    
    for i in range(0,len(hash_value_list)):
        if i == 0:
            if hash_value_list[i] != tmp_node.value:
                #print('false') 调试中使用
                return False
            continue

        if tmp_node.is_root:
            return True
        if tmp_node.is_left:
            tmp_hash = hashlib.sha256(('0x01'+ tmp_node.hash_value + hash_value_list[i]).encode('utf-8')).hexdigest()
            if tmp_hash != tmp_node.parent.hash_value:
                return False
            tmp_node = tmp_node.parent
        else:
            tmp_hash = hashlib.sha256(('0x01' + hash_value_list[i] + tmp_node.hash_value).encode('utf-8')).hexdigest()
            if tmp_hash != tmp_node.parent.hash_value:
                return False
            tmp_node = tmp_node.parent

#生成含有10w个长度为10的字符串的列表
def  get_string_list():
    example_list=[]
    for j in range(0, 100000):
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))# 生成长度为10的随机字符
        example_list.append(random_str)
    return example_list

#测试函数，可在其中设置想要验证的节点
def test_func():
    leaves = get_string_list()
    root = construct_tree(leaves) #形成根节点
    print('根节点的Hash值:',root.hash_value)
    test_node = root.left.right.left.right  #设置需要验证的节点
    path, hash_values_list_ = track_path(test_node) #生成路径和Hash值列表，用于验证
    hash_values_list_.reverse()
    if verify_path(path, hash_values_list_, root): #调用验证函数进行验证
        print("路径有效，节点存在!")
    else:
        print("节点不存在!")



if __name__ == '__main__':
    test_func()

