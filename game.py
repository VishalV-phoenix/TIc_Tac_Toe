import streamlit as st
import math

st.set_page_config(page_title="TIC TAC TOE", page_icon="❌⭕")

def game():
    st.session_state.board=[""]*9
    st.session_state.winner=None
    st.session_state.gameover=False

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


def playerMove(i):
    if st.session_state.board[i]=="" and not st.session_state.gameover:
        st.session_state.board[i]="X"
        result=WinCheck(st.session_state.board)
        if result:
            st.session_state.winner=result
            st.session_state.gameover=True
            return
        
        #ai move
        move=bestMove()
        if move is not None:
            st.session_state.board[move]="O"

        result=WinCheck(st.session_state.board)
        if result:
            st.session_state.winner=result
            st.session_state.gameover=True     



st.title("🎮 Tic Tac Toe (AI – Minimax)")
st.caption("You are ❌ | AI is ⭕ (unbeatable)")

if "board" not in st.session_state:
    game()

cols=st.columns(3)
for i in range(9):
    with cols[i%3]:
        st.button(
            st.session_state.board[i] or " ",
            key=i,
            on_click=playerMove,
            args=(i,),
            use_container_width=True
        )
   
if st.session_state.gameover:
    if st.session_state.winner=="Draw!":
        st.success("🤝 It's a Draw!")
    else:
        st.success(f"🏆 {st.session_state.winner} wins!")
else:
    st.info("Your turn (X)")

st.button("🔄 Restart", on_click=game)


    
