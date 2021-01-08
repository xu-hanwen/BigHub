STACK   SEGMENT
    DB 256 DUP(0)
    TOP   LABEL WORD;TOP为栈顶偏移地址
STACK ENDS

DATA    SEGMENT
    TABLE DW G1,G2,G3,G4,G5
    STRING_1 DB '1.Upper and lower case conversion',0DH,0AH,'$'
    STRING_2 DB '2.Look for the maximum value in a string',0DH,0AH,'$' 
    STRING_3 DB '3.Data sorting',0DH,0AH,'$' 
    STRING_4 DB '4.Time showing',0DH,0AH,'$'  
    STRING_5 DB '5.Exit to Menu',0DH,0AH,'$'     
    STRINGN_c  DB 'Please input the function number(1-5):$'
    STR_IN   DB 'Please input character:',0DH,0AH,'$' 
    MAXELEM  DB 'The maximum is:$'
    IN_NUM   DB 'Please input the decimal number:',0DH,0AH,'$' 
    OUT_NUM  DB 'After sort:',0DH,0AH,'$' 
    IN_TIME  DB 'Correct times(HH:MM:SS):$'
    HINSTR   DB 'What do you want to do next [ESC/Any other key]:$' 
    KEYBUF   DB 61
             DB 20
             DB 61 DUP(0)
    NUMBUF   DB 20
             DB 20 DUP(0)
    DATA ENDS

CODE    SEGMENT
    ASSUME CS:CODE,DS:DATA,SS:STACK

START:
    MOV AX,DATA
    MOV DS,AX
    MOV AX,STACK
    MOV SS,AX
    MOV SP,OFFSET TOP
MAIN: CALL MENU
AGAIN:
    MOV AH,2
    MOV BH,0
    MOV DL,43
    MOV DH,10
    INT 10H
    MOV AH,01H
    INT 21H
    CMP AL,'1'
    JB  AGAIN
    CMP AL,'5'
    JA  AGAIN
    SUB AL,'1' 
    SHL AL,1
    CBW
    LEA BX,TABLE
    ADD BX,AX
    JMP WORD PTR [BX]
    
G1:
    CALL CHGLTR
    MOV AH,8
    INT 21H 
    CMP AL,1BH
    JZ MAIN
    JMP G1
G2:
    CALL MAXLTR
    MOV AH,8
    INT 21H
    CMP AL,1BH
    JZ MAIN
    JMP G2
G3:
    CALL SORTNUM
    MOV AH,8
    INT 21H
    CMP AL,1BH
    JZ MAIN
    JMP G3   
G4:
    CALL TIMCHK
    MOV AH,8
    INT 21H
    CMP AL,1BH
    JZ MAIN
    JMP G4     
G5:
    MOV AH,4CH
    INT 21H  

MENU PROC NEAR:   ;菜单页模块
    MOV AH,0
    MOV AL,3
    MOV BL,0
    INT 10H;中断调用,清屏
    
    MOV AH,2 ;菜单页功能一
    MOV BH,0
    MOV DL,5
    MOV DH,5
    INT 10H;BH页,DH列,DL行,设置光标位置
    MOV AH,9
    LEA DX,STRING_1
    INT 21H;
             ;菜单页功能二
    MOV AH,2
    MOV BH,0
    MOV DL,5
    MOV DH,6
    INT 10H
    MOV AH,9
    LEA DX,STRING_2
    INT 21H
    
    MOV AH,2 ;菜单页功能三
    MOV BH,0
    MOV DL,5
    MOV DH,7
    INT 10H
    MOV AH,9
    LEA DX,STRING_3
    INT 21H 
    
    MOV AH,2 ;菜单页功能四
    MOV BH,0
    MOV DL,5
    MOV DH,8
    INT 10H
    MOV AH,9
    LEA DX,STRING_4
    INT 21H
    
    MOV AH,2 ;菜单页功能五
    MOV BH,0
    MOV DL,5
    MOV DH,9
    INT 10H
    MOV AH,9
    LEA DX,STRING_5
    INT 21H
    
    MOV AH,2 ;菜单页功能选择
    MOV BH,0
    MOV DL,5
    MOV DH,10
    INT 10H
    MOV AH,9
    LEA DX,STRINGN_c
    INT 21H
    RET  
MENU ENDP 
  

;大小写转换功能模块
CHGLTR PROC NEAR:
  RECHG:
    MOV AH,0
    MOV AL,3
    MOV BL,0
    INT 10H ;清屏  
    
    MOV AH,2 ;显示输入提示语句
    MOV BH,0
    MOV DL,5
    MOV DH,8
    INT 10H 
    MOV AH,9
    LEA DX,STR_IN
    INT 21H       
    
    MOV AH,2 ;显示键盘输入
    MOV BH,0
    MOV DL,28
    MOV DH,8
    INT 10H 
    MOV AH,0AH    ;键盘输入
    LEA DX,KEYBUF ;输入的字符串在缓冲区KEYBUF
    INT 21H   
    
    CMP KEYBUF+1,0
    JZ  RECHG 
    LEA BX,KEYBUF+2
    MOV AL,KEYBUF+1
    CBW
    MOV CX,AX
    ADD BX,AX
    MOV BYTE PTR [BX],'$' 
    
    MOV AH,2    ;屏幕显示原始输入语句
    MOV BH,0
    MOV DL,5
    MOV DH,9
    INT 10H 
    MOV AH,9
    LEA DX,KEYBUF+2
    INT 21H  
    LEA BX,KEYBUF+2
    
  LCHG:
    CMP BYTE PTR [BX],61H
    JB NOCHG
    AND BYTE PTR [BX],0DFH

  NOCHG:
    INC BX
    LOOP LCHG
    MOV AH,2   ;模块结果输出
    MOV BH,0
    MOV DL,5
    MOV DH,10
    INT 10H 
    MOV AH,9
    LEA DX,KEYBUF+2
    INT 21H   ;显示大写字符串 
    
    MOV AH,2  ;选择语句
    MOV BH,0
    MOV DL,5
    MOV DH,11
    INT 10H 
    MOV AH,9
    LEA DX,HINSTR 
    INT 21H
    RET
CHGLTR ENDP



;找最大元素功能模块
MAXLTR PROC NEAR: 
  REMAX:   
    MOV AH,0  ;清屏
    MOV AL,3
    MOV BL,0
    INT 10H  
    
    MOV AH,2  ;显示输入提示语句
    MOV BH,0
    MOV DL,5
    MOV DH,5
    INT 10H 
    MOV AH,9
    LEA DX,STR_IN
    INT 21H 
    
    MOV AH,2  ;显示键盘输入
    MOV DL,28
    MOV DH,5
    INT 10H ;设置输入光标位置  
    MOV AH,0AH    ;键盘缓冲输入
    LEA DX,KEYBUF
    INT 21H    
    
    CMP KEYBUF+1,0       ;模块结果输出
    JZ  REMAX
    LEA BX,KEYBUF+2
    MOV AL,KEYBUF+1
    CBW
    MOV CX,AX
    ADD BX,AX
    MOV BYTE PTR [BX],'$'
    MOV AH,2
    MOV BH,0
    MOV DL,5
    MOV DH,7
    INT 10H
    MOV AH,9
    LEA DX,MAXELEM
    INT 21H  
    
    MOV DL,0
    LEA BX,KEYBUF+2
  LCMP:  
    CMP [BX],DL
    JB  NOLCHG
    MOV DL,[BX]
  NOLCHG:
    INC BX
    LOOP LCMP
    MOV AH,2 ;字符输出功能
    INT 21H    
    
    MOV AH,2    ;选择语句
    MOV BH,0
    MOV DL,5
    MOV DH,8
    INT 10H 
    MOV AH,9
    LEA DX,HINSTR 
    INT 21H
    RET
MAXLTR ENDP
 
 
;排序模块
SORTNUM PROC NEAR:
  RESORT:
    MOV AH,0  ;清屏
    MOV AL,3
    MOV BL,0
    INT 10H  
    
    MOV AH,2  ;显示字符串，提示输入
    MOV BH,0
    MOV DL,5
    MOV DH,5
    INT 10H 
    MOV AH,9
    LEA DX,IN_NUM
    INT 21H 
    
    MOV AH,2  ;显示键盘输入
    MOV DL,5
    MOV DH,6
    INT 10H  
    MOV AH,0AH
    LEA DX,KEYBUF
    INT 21H 
    CALL CIN_INT ;转换数据组  
    CMP AL,0
    JZ  RESORT
    CMP NUMBUF,0
    JZ  RESORT
    
    MOV AH,2
    MOV BH,0
    MOV DL,5
    MOV DH,7
    INT 10H 
    MOV AH,9 
    LEA DX,OUT_NUM  
    INT 21H 
    
    MOV AH,2
    MOV BH,0
    MOV DL,5
    MOV DH,8
    INT 10H 
    CALL MPSORT;排序输入
    CALL INT_OUT ;输出排序结果
    MOV AH,2
    MOV BH,0
    MOV DL,5
    MOV DH,9
    INT 10H 
    MOV AH,9 
    LEA DX,HINSTR 
    INT 21H
    RET
 SORTNUM ENDP   
     
    
CIN_INT PROC NEAR:
    MOV CL,KEYBUF+1
    LEA SI,KEYBUF+2
    MOV CH,0
    MOV DH,10
    MOV AL,0
    MOV DL,0
    
  FNDNUM:
    CMP BYTE PTR [SI],' '
    JZ  ADDNUM
    CMP BYTE PTR [SI],'0'
    JB  ERRNUM
    CMP BYTE PTR [SI],'9'
    JA  ERRNUM
    MOV DL,1
    MUL DH
    
    XOR BH,BH
    MOV BL,[SI]
    ADD AX,BX
    SUB AX,'0'
    CMP AH,0
    JA  ERRNUM
    JMP NEXT
    
  ADDNUM:
    CMP DL,1
    JNZ NEXT
    INC CH 
    CALL ADDNEW
    MOV DL,0
    MOV AL,0
    
  NEXT:
    INC SI
    DEC CL
    CMP CL,0
    JNZ FNDNUM
    CMP DL,1
    JNZ TOTAL
    INC CH
    CALL ADDNEW
  
  TOTAL:
    MOV NUMBUF,CH
    MOV AL,1
    JMP CRTNUM
   
  ERRNUM:
    MOV AL,0
  
  CRTNUM:
    RET
CIN_INT ENDP  
 


ADDNEW PROC NEAR:
    PUSH AX
    LEA BX,NUMBUF
    MOV AL,CH
    CBW
    ADD BX,AX
    POP AX
    MOV [BX],AL
    RET
ADDNEW ENDP

MPSORT PROC NEAR: ;排序
    MOV AL,NUMBUF
    CMP AL,1
    JBE NOSORT;只有一个元素，停止排序
    CBW
    MOV CX,AX
    LEA SI,NUMBUF
    ADD SI,CX
    DEC CX
  LP1:
    PUSH CX
    PUSH SI
    MOV DL,0
  LP2:
    MOV AL,[SI]
    CMP AL,[SI-1]
    JAE NOXCHG
    XCHG AL,[SI-1]
    MOV [SI],AL
    MOV DL,1
  NOXCHG:
    DEC SI
    LOOP LP2
    POP SI
    POP CX
    CMP DL,1
    JNZ NOSORT
    LOOP LP1
  NOSORT:RET
MPSORT ENDP

INT_OUT PROC NEAR:
    MOV AL,NUMBUF
    CBW
    MOV CX,AX
    MOV BL,10H
    LEA SI,NUMBUF+1
  PRINT:
    MOV AL,[SI]
    CALL OUTNUM
    INC SI
    MOV AH,2
    MOV DL,' '
    INT 21H
    LOOP PRINT
    RET
INT_OUT ENDP

OUTNUM PROC NEAR:
    MOV AH,0
    DIV BL
    PUSH AX
    CMP AH,10
    JB  PNUM
    ADD AH,7 
  PNUM:
    ADD AH,30H
    MOV DL,AH
    POP AX
    PUSH DX
    CMP AL,0
    JZ  OUTN
    CALL OUTNUM
  OUTN:
    POP DX
    MOV AH,2
    INT 21H
    RET
OUTNUM ENDP
  
  
  
TIMCHK PROC NEAR:
    MOV AH,0
    MOV AL,3
    MOV BL,0
    INT 10H ;清屏
    MOV AH,2
    MOV BH,0
    MOV DL,5
    MOV DH,5
    INT 10H ;设置输入光标位置
    MOV AH,9
    LEA DX,IN_TIME 
    INT 21H ;显示字符串，提示输入
    MOV AH,0AH
    LEA DX,KEYBUF 
    INT 21H
    
    
    MOV BL,10
    MOV AL,KEYBUF+2
    SUB AL,'0'
    MUL BL
    ADD AL,KEYBUF+3 
    SUB AL,'0'
    CMP AL,0
    JB  INVALID
    CMP AL,24
    JAE INVALID;时有效性
    MOV CH,AL
    MOV AL,KEYBUF+5
    SUB AL,'0'
    MUL BL
    ADD AL,KEYBUF+6
    SUB AL,'0'
    CMP AL,0
    JB  INVALID
    CMP AL,60
    JAE INVALID;分有效性  
    MOV CL,AL
    MOV AL,KEYBUF+8
    SUB AL,'0'
    MUL BL
    ADD AL,KEYBUF+9
    SUB AL,'0'
    CMP AL,0
    JB  INVALID
    CMP AL,60
    JAE INVALID;分有效性  
    MOV DH,AL
    MOV DL,0
    MOV AH,2DH
    INT 21H;置系统时间,CX=时,分DX=秒,百分秒
  INVALID:
    CALL TIME
    RET
TIMCHK ENDP


TIME PROC NEAR:
    MOV AH,0
    MOV AL,3
    MOV BL,0
    INT 10H
    MOV AH,2
    MOV BH,0
    MOV DL,10
    MOV DH,9
    INT 10H
    MOV AH,9
    LEA DX,HINSTR
    INT 21H
  DISP1:
    MOV AH,2
    MOV BH,0
    MOV DL,72
    MOV DH,0
    INT 10H
    MOV AH,2CH
    INT 21H;取系统时间
        MOV AL,CH
        CALL SHOWNUM
        MOV AH,2
        MOV DL,':'
    INT 21H
        MOV AL,CL
        CALL SHOWNUM
        MOV AH,2
        MOV DL,':'
    INT 21H
        MOV AL,DH
        CALL SHOWNUM
    MOV AH,02H
    MOV DX,090AH
    MOV BH,0
    INT 10H
    MOV BX,0018H
  RE: MOV CX,0FFFFH
  REA: 
    LOOP REA
    DEC BX
    JNZ RE
    MOV AH,0BH
    INT 21H
    CMP AL,0
    JZ  DISP1
    RET
TIME ENDP

SHOWNUM PROC NEAR:
    CBW
    PUSH CX
    PUSH DX
    MOV CL,10
    DIV CL
    ADD AH,'0'
    MOV BH,AH
    ADD AL,'0'
    MOV AH,2
    MOV DL,AL
    INT 21H
    MOV DL,BH
    INT 21H
    POP DX
    POP CX
    RET
SHOWNUM ENDP

CODE ENDS
    END   START      