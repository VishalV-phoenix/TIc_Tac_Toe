import streamlit as st
import math
import random

st.set_page_config(page_title="TIC TAC TOE", page_icon="❌⭕")

def mode_change():
    game()
st.sidebar.title("Game mode")
st.sidebar.toggle("fun mode",key="modes",value=False,on_change=mode_change)

st.sidebar.markdown("---")
if st.session_state.modes:
    st.sidebar.subheader("Fun Mode Rules")
    st.sidebar.markdown("""
    - Normal Tic Tac Toe rules apply  
    - After early turns, a **hazard (@)** appears  
    - The hazard:
        - Blocks a cell
        - Can remove X or O
        - Moves every 2 turns
    - Only **one hazard** exists at a time  
    - Goal: Adapt to chaos and win
    """)
else:
    st.sidebar.subheader("Standard Mode Rules")
    st.sidebar.markdown("""
    - Classic Tic Tac Toe   
    - AI uses minimax (unbeatable)  
    - Perfect play leads to draw
    """)


def game():
    st.session_state.board=[""]*9
    st.session_state.winner=None
    st.session_state.gameover=False
    st.session_state.firstMove=False
    #hazard
    st.session_state.timer=0
    st.session_state.player3move=None
    st.session_state.count=0

def WinCheck(board):
    combos = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in combos:
        if board[a] == board[b] == board[c] !="":
            return board[a]
            
    if "" not in board:
        return "Draw!"
        
    return None



def minimax(board,isMaximizing):
    result=WinCheck(board)
    if result=="X":
        return -1
    if result=="O":
        return 1
    if result=="Draw!":
        return 0
    
    if isMaximizing:
        bestscore=-math.inf
        for i in range(9):
            if board[i]=="":
                board[i]="O"
                Score=minimax(board,False)
                board[i]=""
                bestscore=max(Score,bestscore)
        return bestscore
    else:
        bestscore=math.inf
        for i in range(9):
            if board[i]=="":
                board[i]="X"
                Score=minimax(board,True)
                board[i]=""
                bestscore=min(Score,bestscore)
        return bestscore
    
def bestMove():
    bestscore=-math.inf
    move = None
    for i in range(9):
        if st.session_state.board[i]=="":
            st.session_state.board[i]="O"
            score=minimax(st.session_state.board,False)
            st.session_state.board[i]=""
            if score>bestscore:
                bestscore=score
                move=i
    return move

def player3():
    if not st.session_state.modes:
        return
    if st.session_state.gameover:
        return
    turn=st.session_state.count//2

    if turn<=1:
        return
    if st.session_state.player3move==None:
        st.session_state.timer=2
        st.session_state.player3move=random.randint(0,8)
        return
    else:
        st.session_state.timer-=1
        if st.session_state.timer==0:
            st.session_state.board[st.session_state.player3move]=""
            st.session_state.player3move=random.randint(0,8)
            st.session_state.timer=2

def playerMove(i):
    if st.session_state.board[i]=="" and not st.session_state.gameover:
        st.session_state.board[i]="X"
        st.session_state.count+=1
        result=WinCheck(st.session_state.board)
        if result:
            st.session_state.winner=result
            st.session_state.gameover=True
            return
        
        #ai move
        move=bestMove()
        if move is not None:
            st.session_state.board[move]="O"
            st.session_state.count+=1

        result=WinCheck(st.session_state.board)
        if result:
            st.session_state.winner=result
            st.session_state.gameover=True 

        player3()

def Aimove():
    move=bestMove()
    if move is not None:
        st.session_state.board[move]="O"
        st.session_state.count+=1

    result=WinCheck(st.session_state.board)
    if result:
        st.session_state.winner=result
        st.session_state.gameover=True
        


st.title("🎮 Tic Tac Toe (AI – Minimax)")
st.caption("You are ❌ | AI is ⭕ (unbeatable)")
st.caption("Toggle to make AI go first")


if "board" not in st.session_state:
    game()

st.toggle("AI first",key="mover",value=False,on_change=game)

st.button("Restart",on_click=game)

if st.session_state.mover and not st.session_state.firstMove:
    Aimove()
    st.session_state.count+=1
    st.session_state.firstMove=True   

cols=st.columns(3)
for i in range(9):
    with cols[i%3]:
         

        is_played=(st.session_state.modes and i==st.session_state.player3move)
        if is_played:
            st.session_state.board[i]="@"

        st.button(
            st.session_state.board[i] or " ",
            key=i,
            on_click=playerMove,
            args=(i,),
            disabled=is_played,
            use_container_width=True
        )
   
if st.session_state.gameover:
    if st.session_state.winner=="Draw!":
        st.success("🤝 It's a Draw!")
    else:
        st.success(f"🏆 {st.session_state.winner} wins!")
else:
    st.info("Your turn (X)")



    

