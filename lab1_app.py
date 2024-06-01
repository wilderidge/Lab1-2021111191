from lab1 import *

st.empty()
st.title('Lab1 App')
# 初始化 session_state
if "is_paused" not in st.session_state:
    st.session_state.is_paused = False
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "pause_button" not in st.session_state:
    st.session_state.pause_button = False

if st.sidebar.button('Show graph'):
    chong_zhi()
    st.session_state.stage = 0
    st.header('fun_1')  # 添加子标题
    G, pos, words = generate_directed_graph('input/1.txt')
    print_words(words)
    showDirectedGraph(G, 'output/1.png', pos)
    st.button('返回主页面',on_click=chong_zhi)

if st.sidebar.button('Run fun_3'):
    chong_zhi()
    st.header('fun_3')  # 添加子标题
    fun_3()

if st.sidebar.button('Run fun_4'):
    chong_zhi()
    st.header('fun_4')  # 添加子标题
    generate_new_text('input/2.txt')

if st.sidebar.button('Run fun_5'):
    chong_zhi()
    st.header('fun_5')  # 添加子标题
    fun_5('output/2.png')

if (st.sidebar.button('Run fun_6') or st.session_state.stage == 6):
    st.header('fun_6')  # 添加子标题
    fun_6_text = randomWalk()
    with open('output/3.txt', 'w') as f:
        f.write(fun_6_text)
    st.write(f"生成的运动路径为：{fun_6_text}")
