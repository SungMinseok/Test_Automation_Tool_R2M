from re import T
import pyautogui as pag
import func.msdata as ms
from func.setappsize import SetAppSize
from time import sleep
import os.path
import time
import func.img2str as i2s
import random
import string
#import R2A
app_pos = [0,33,1428,805]
# def multicommand():
#     while True : 
#         ms.PrintUB_Bold()
#         print("※멀티 커맨드")
#         ms.PrintUB()      
#         print("[1]Item ID 입력 : +0 ~ +13강 장비 생성\n[2]TXT 파일 실행 : Item ID\n[3]TXT 파일 실행 : 명령어\n[4]Item ID 입력 : 직접 입력")
#         ms.PrintUB()      
#         print("[0]메인메뉴")
#         ms.PrintUB()      
#         num2 = int(ms.InputNum(5))
#         ms.clear()
#         if num2==0:
#             break
#         elif num2 ==1:
#             Command_Additem()
#         elif num2 ==2:
#             Command_Additems_Text()
#         elif num2 ==3:
#             Command_Text()
#         elif num2 ==4:
#             Command_Additems()
#     elif num2 ==5:
#        Command_Direct2()
    
#     #multicommand()


def Command_Additem():
    while True:
        ms.PrintUB_Bold()     
        print("※Item ID 입력 : +0 ~ +13강 장비 생성")
        ms.PrintUB()      
        print("+0강 Item ID를 입력하세요.")
        ms.PrintUB()      
        print("[0]뒤로가기")
        ms.PrintUB()    

        itemNum = (ms.InputNum(99999999))
        if itemNum=="0":
            ms.clear()
            return
        ms.ResetFirst()
        ms.CommandOpen()
        pag.typewrite("additems")
        for j in range(0,14):
            pag.press('space')
            temp = int(itemNum)+j
            pag.typewrite(str(temp))
        ms.CommandClose()


def autoAddItem(id, count):
    if count == "":
        count = 1

    ms.Command(f'additem {id} {count}')


def Command_Additems_Text():
    while True :
        ms.PrintUB_Bold()      
        print("※TXT 파일 실행 : Item ID")
        ms.PrintUB()      
        print("불러올 txt 파일명 입력하세요.\n([Enter]입력 시 additems.txt를 불러옵니다.)")
        ms.PrintUB()      
        print("[0]뒤로가기")
        ms.PrintUB() 

        while True  :           
            fileName = input(">")

            #종료 
            if fileName =="0":
                ms.clear()
                return
            #패스(기본 파일 있음)
            elif fileName =="":
                fileName = 'additems'
                break
            #패스(특정 파일 있음)
            elif os.path.isfile(fileName +".txt") :
                break
            else :
                print("파일이 없습니다.")

        with open(fileName +".txt") as f:
            lines = f.read().splitlines()
        f.close()

        ms.ResetFirst()

        ms.CommandOpen()
        pag.typewrite("additems")
        
        for line in lines:
            pag.typewrite(" "+line)
        ms.CommandClose()


#R2M_Alpha_Command : makeitem X N > X in txtFile
def autoMakeItemText(filePath):
    with open(filePath) as f:
        lines = f.read().splitlines()
    f.close()
    ms.ResetFirst()
    #pag.typewrite("additems")
    for line in lines:
        if line.find(",") != -1 :
            itemID, itemAmount = line.split(',')
            ms.Command("makeitem "+itemID+" "+itemAmount)

        else :
            ms.Command("makeitem "+line+" 1")


def Command_Text():
    while True :
#세팅값 불러오기&저장
        with open("info_mcmd.txt") as setFile:
            setValue = setFile.read().splitlines()
        setFile.close()

        term = int(setValue[0])
        count = int(setValue[1])

#UI 실행부
        ms.PrintUB_Bold()      
        print("※TXT 파일 실행 : 명령어")
        ms.PrintUB() 
        print("＊명령어 실행 간격 : ", setValue[0], "초")
        print("＊실행횟수 : ", setValue[1], "회")
        ms.PrintUB()  
        print("[9]설정변경")
        print("[0]뒤로가기")
        ms.PrintUB()          
        print("불러올 txt 파일명 입력해주세요\n([Enter]입력 시 multicommand.txt를 불러옵니다.)")
        ms.PrintUB()  

#Input 입력부
        while True  :           
            fileName = input(">")
            #종료 
            if fileName =="0":
                ms.clear()
                return
            #설정변경
            elif fileName == "9":
                setMsg = ["명령어 실행 대기 간격(초)을 입력해 주세요(0~)","실행 횟수를 입력해주세요(1~)"]
                ms.ChangeSetValue("info_mcmd",setMsg)
                print("설정변경 완료!")
                sleep(1)
                ms.clear()
                break
            #패스(기본 파일 있음)
            elif fileName =="":
                fileName = "multicommand"
                break
            #패스(특정 파일 있음)
            elif os.path.isfile(fileName +".txt") :
                break

            else :
                print("파일이 없습니다.")
        
        #설정 변경 시 처음부터 시작
        if fileName == "9":
            continue

#기능 실행부
        with open(fileName +".txt") as f:
            lines = f.read().splitlines()
        f.close()

        startTime = ms.GetCurrentTime()
        indivRunTime = len(lines) * 2.5 + term

        ms.clear()
        ms.PrintUB_Bold()      
        print("※TXT 파일 실행 : 명령어")
        ms.PrintUB() 
        print("＊명령어 실행 간격 : ", setValue[0], "초")
        print("＊실행횟수 : ", setValue[1], "회")
        ms.PrintUB()  
        print("총 예상 소요 시간 : ", count * indivRunTime , "초")
        print("총 예상 종료 시각 : ", ms.GetElapsedTime(count * indivRunTime))
        ms.PrintUB()  


        ms.ResetFirst()

        for i in range(0,count) :

            #ms.PrintUB()  
            print(i+1 ,"번 째 실행", end='\r')
            for line in lines:
                ms.Command(line)
                sleep(1)
            
            if i < (count - 1) :
                ms.sleep(term)

#기능 종료부

        endTime = ms.GetCurrentTime()
        totalRuntime = endTime -startTime

        ms.PrintUB() 
        print("실행 완료.") 
        ms.PrintUB()  
        print("총 소요 시간 : ", totalRuntime , "초")
        print("종료 시각 : ", ms.GetCurrentTime())
        ms.PrintUB()  


def Command_Additems():
    while True :
    #UI 실행부
        ms.PrintUB_Bold()      
        print("※Item ID 입력 : 직접 입력")
        ms.PrintUB() 
        print("[0]뒤로가기")
        ms.PrintUB()          
        print("Item ID를 스페이스로 구분하여 입력해주세요.")
        ms.PrintUB() 
        
        itemNums = input(">")
        if itemNums =="0":
            ms.clear()
            return
        ms.ResetFirst()

        ms.CommandOpen()
        pag.typewrite("additems " + str(itemNums))
        ms.CommandClose()



def Command_Direct1():
    
    commandText = input("명령어 입력 : ")
    count = int(input("실행 횟수를 입력해주세요(1~) : "))

    try : 
        if count <= 0 :
                
            print("다시 입력해주세요.")
            Command_Direct1()

        else :
            print("실행 중 입니다...(예상 소요 시간 : " + str(count * 1.5) + " 초)")

            ms.ResetFirst()

            for i in range(0,count) :
                ms.Command(commandText)
    
    except : 
        print("다시 입력해주세요.")
        Command_Direct1()

def Command_Direct2():
    print("미완성")
    # commandCountText = "0"
    # commandText = "default"

    # while commandText != "0"
    #     commandCountText = str(int(commandCountText) + 1)
    #     commandText[int(commandCountText)-1] = input(commandCountText + "번째 명령어 입력(종료시 : 0) : ")
        
    # term = int(input("명령어 실행 대기 간격(초)을 입력해 주세요(0~) : "))

    # count = int(input("실행 횟수를 입력해주세요(1~) : "))

    # try : 
    #     if count <= 0 :
                
    #         print("다시 입력해주세요.")
    #         Command_Direct()

    #     else :
    #         print("실행 중 입니다...(예상 소요 시간 : " + str(count * 1.5) + " 초)")

    #         ms.ResetFirst()

    #         for i in range(0,count) :
    #             ms.Command(commandText)

    
    # except : 
    #     print("다시 입력해주세요.")
    #     Command_Direct()




def autoTest_regist2market(marketType = 0,fileName = ""):#일반/통합,id텍스트파일명

    
#UI 실행부
    ms.PrintUB_Bold()      
    print("※거래소 아이템 등록 확인 테스트")
    # ms.PrintUB() 
    # print("＊명령어 실행 간격 : ", setValue[0], "초")
    # print("＊실행횟수 : ", setValue[1], "회")
    # ms.PrintUB()  
    # print("[9]설정변경")
    # print("[0]뒤로가기")
    ms.PrintUB()          
    fileName = input("[0]일반거래소 [1]통합거래소 : ")
    fileName = input("불러올 txt 파일명 : ")
    
    path = "./screenshot/autoTest_regist2market"+ time.strftime("_%m%d")
    if not os.path.isdir(path):                                                           
        os.mkdir(path)
        
    path_result = path + "/result"
    if not os.path.isdir(path_result):                                                           
        os.mkdir(path_result)

    with open(fileName +".txt") as f:
        lines = f.read().splitlines()
    f.close()

    totalCount = len(lines)
    count0, count1 = divmod(totalCount , 25)
    #count0 = totalCount/25
    #count1 = totalCount%25


    ms.ResetFirst()


    ms.Move(ms.menuPos3)
    sleep(2)
    if marketType == "world":
        ms.Move(ms.market_enterServerType1)
    else:
        ms.Move(ms.market_enterServerType0)
    sleep(2)

    for i in range(0,count0):

        ms.Move(ms.market_searchTab)
        sleep(2)

        ms.Command("cleanupinventory")
        ms.CommandOpen()
        pag.typewrite("additems ")
        for j in range(0,25):
            curID = lines[25*i+j]
            # if curID[len(curID)-1] == "8":
            #     pag.typewrite(str(int(curID)-1) + " ")
            pag.typewrite(curID + " ")
        ms.CommandClose()
        ms.Command("additem 999 10000000")

        ms.Move(ms.market_registTab)
        sleep(3)

        ms.Capture(path+ "/"+lines[25*i]+"_"+lines[25*i+24]+"_start",False)

        for k in range(0,25):
            ms.Move(ms.market_invenBtn0)
            sleep(2)
            ms.Move(ms.market_sellBtn0)
            sleep(0.5)
            ms.Move(ms.market_sellBtn1)
            sleep(0.5)
            ms.Move(ms.market_sellBtn2)
            sleep(3)
            
        ms.Capture(path+ "/"+lines[25*i]+"_"+lines[25*i+24]+"_end",False)
        getData = i2s.getNumberFromImg(ms.captureSomeBox2("market_totalSellPriceBox",path_result + "/result_" +str(i)))
        if getData == "250":
            testResult = "pass"
        else :
            testResult = "fail"

        testResultText =\
            '\n'\
            +lines[25*i]\
            +","+lines[25*i+24]\
            +","+getData\
            +","+testResult

        with open(path_result+"./result.txt",'a',encoding='utf-8') as tx:
            tx.write(testResultText)

        for l in range(0,25):
            ms.Move(ms.market_cancelRegist)
            sleep(2.2)
    
    #for i in range(0,count1):
    if count1 >0 : 
        
        ms.Move(ms.market_searchTab)
        sleep(3)

        ms.Command("cleanupinventory")
        ms.CommandOpen()
        pag.typewrite("additems ")
        for j in range(0,count1):
            curID = lines[25*count0+j]
            # if curID[len(curID)-1] == "8":
            #     pag.typewrite(str(int(curID)-1) + " ")
            pag.typewrite(lines[25*count0+j] + " ")
        ms.CommandClose()
        ms.Command("additem 999 10000000")

        ms.Move(ms.market_registTab)
        sleep(3)

        ms.Capture(path+ "/"+lines[25*count0]+"_"+lines[25*count0+count1-1]+"_start",False)

        for k in range(0,count1):
            ms.Move(ms.market_invenBtn0)
            sleep(2)
            ms.Move(ms.market_sellBtn0)
            sleep(0.5)
            ms.Move(ms.market_sellBtn1)
            sleep(0.5)
            ms.Move(ms.market_sellBtn2)
            sleep(3)

        ms.Capture(path+ "/"+lines[25*count0]+"_"+lines[25*count0+count1-1]+"_end",False)
        #i2s.Indiv_Num(path_result+".txt",ms.captureSomeBox2("market_totalSellPriceBox",path_result + "/result_f" ))
        getData = i2s.getNumberFromImg(ms.captureSomeBox2("market_totalSellPriceBox",path_result + "/result_f"))
        if getData == "250":
            testResult = "pass"
        else :
            testResult = "fail"

        testResultText =\
            '\n'\
            +lines[25*count0]\
            +","+lines[25*count0+count1-1]\
            +","+getData\
            +","+testResult

        with open(path_result+"./result.txt",'a',encoding='utf-8') as tx:
            tx.write(testResultText)

        for l in range(0,count1):
            ms.Move(ms.market_cancelRegist)
            sleep(2.2)

def executeCmdPackage(cmd) :
    ms.ResetFirst()
    ms.Move(ms.menuPos4)
    ms.Move(ms.menuPos20)

def 캐릭터재접속():
    """
    캐릭터 재접속
    """
    
    #ms.Command("doteleport 0 550 250")
    #ms.sleep(5)

    ms.Move(ms.menuPos4)
    ms.Move(ms.menuPos20)
    ms.sleep(0.1)
    ms.Move(ms.menuMiddleUpperTab5)
    ms.Move(ms.goCharacterSelectPageBtn)
    ms.sleep(0.01)
    ms.Move(ms.okPos)
    ms.sleep(0.2)

    ms.sleep(1.5)

    ms.Move(ms.characterCreateBtn)

def 캐릭터선택창():
    """
    캐릭터 선택창
    """
    
    #ms.Command("doteleport 0 550 250")
    #ms.sleep(5)

    ms.Move(ms.menuPos4)
    ms.Move(ms.menuPos20)
    ms.sleep(0.1)
    ms.Move(ms.menuMiddleUpperTab5)
    ms.Move(ms.goCharacterSelectPageBtn)
    ms.sleep(0.01)
    ms.Move(ms.okPos)
    ms.sleep(0.2)

def 서버선택창():
    """
    서버 선택창
    """
    
    #ms.Command("doteleport 0 550 250")
    #ms.sleep(5)

    ms.Move(ms.menuPos4)
    ms.Move(ms.menuPos20)
    ms.sleep(0.1)
    ms.Move(ms.menuMiddleUpperTab5)
    ms.Move(ms.goServerSelectionBtn)
    ms.sleep(0.01)
    ms.Move(ms.okPos)
    ms.sleep(0.2)

def 서드파티창():
    """
    로그아웃&서드파티 선택창
    """
    
    #ms.Command("doteleport 0 550 250")
    #ms.sleep(5)

    ms.Move(ms.menuPos4)
    ms.Move(ms.menuPos20)
    ms.sleep(0.1)
    ms.Move(ms.menuMiddleUpperTab5)
    ms.Move(ms.logoutBtn)
    ms.sleep(0.01)
    ms.Move(ms.okPos)
    ms.sleep(0.2)


def 채팅및스샷저장(chat : str, screenshot_path = ""):
    """
    채팅팝업 내 채팅발생
    """
    ms.ResetFirst()
    ms.Click(ms.mainhud_chat_btn,0.2)
    ms.Click(ms.mainhud_chat_btn,0.1)

    pag.typewrite(chat)

    ms.Click(ms.send_chat_btn,0.1)
    ms.Click(ms.send_chat_btn,0.1)

    sleep(0.5)

    if screenshot_path == "" :
        ms.captureSomeBox("")
    else :
        ms.captureSomeBox2("chat_popup_box",screenshot_path)
    ms.ResetFirst()

def 캐릭터탈퇴():

    ms.ResetFirst()

    ms.Move(ms.menuPos4)
    ms.Move(ms.menuPos20)
    ms.Move(ms.menuMiddleUpperTab5)
    ms.Move(ms.deleteAccountBtn)
    ms.Move(ms.okPos)
    ms.sleep(1)
    codeResultFileName = ms.captureSomeBox("deleteAccountCodeBox")
    ms.sleep(0.5)
    codeID = i2s.Indiv_Eng_Return(codeResultFileName)
    print(codeID[0:4])
    ms.sleep(0.5)
    ms.Move(ms.deleteAccountCodeInput)

    ms.inputCommand(codeID[0:4])
    ms.sleep(0.1)
    ms.Move(ms.okPos)


def 캐릭터생성_라이브():


    ms.Move(ms.appUpPos)
    sleep(0.01)
    ms.Move(ms.characterNameBtn)
    ms.sleep(0.5)
    ms.Move(ms.characterNameInput)

    randomName = ""
    for i in range(8):
        randomName += random.choice(string.ascii_letters)
    ms.sleep(1)

    ms.inputCommand(randomName)
    ms.Move(ms.okPos)
    ms.sleep(1)
    
    ms.Move(ms.characterCreateBtn)
    ms.sleep(0.5)

    ms.Move(ms.characterCreateBtn)



    ms.sleep(5)

    
    tempText = ""

    for i in range(5) :
        if tempText != "벨리타" :
            print("텍스트 대기 중:", tempText)
            belitaBoxName = ms.captureSomeBox("belitaBox")
            tempText = i2s.Indiv_Kor_Return(belitaBoxName)
            sleep(1)
        else:
            break

    ms.Move(ms.centerPos)
    ms.sleep(0.5)
    ms.Move(ms.getFirstQuestBtn)
    ms.sleep(0.5)
    ms.Move(ms.acceptQuestBtn)
    ms.sleep(1)


    pag.press('esc')
    ms.sleep(0.5)
    pag.press('esc')
    ms.sleep(0.5)
    pag.press('esc')
    ms.sleep(0.5)
    pag.press('esc')
    ms.sleep(1)
    ms.Move(ms.acceptQuestBtn)
    ms.sleep(1)

    pag.press('d')
    ms.sleep(0.5)

    pag.keyDown('w')
    pag.keyDown('a')

    while tempText != "벨켄" :
        print("텍스트 대기 중:", tempText)
        belitaBoxName = ms.captureSomeBox("belitaBox")
        tempText = i2s.Indiv_Kor_Return(belitaBoxName)
        sleep(1)

    pag.keyUp('w')
    pag.keyUp('a')

    
    for i in range(3):
        pag.press('esc')
        ms.sleep(0.5)

    #ms.Command("cleanupinventory")
    #ms.ResetFirst()
    ms.Move(ms.acceptQuestBtn)
    ms.sleep(0.5)

    ms.Move(ms.menuPos1)
    ms.sleep(0.5)
    ms.Move(ms.invenBtn3)
    ms.sleep(0.5)
    ms.Move(ms.invenBtn3)
    ms.sleep(0.5)
    ms.Move(ms.invenMainExitBtn)
    ms.sleep(0.5)
    for i in range(3):
        pag.press('esc')
        ms.sleep(0.5)
    ms.Move(ms.acceptQuestBtn)
    ms.sleep(0.5)
    ms.Move(ms.getFirstQuestBtn)
    ms.sleep(0.5)
    ms.Move(ms.okTeleportBtn)
    ms.sleep(0.5)
    ms.Move(ms.tutoMonPos)
    ms.sleep(0.5)
    ms.Move(ms.attackBtn)
    ms.sleep(0.5)

    while tempText != "호텐 플로츠" :
        print("텍스트 대기 중:", tempText)
        belitaBoxName = ms.captureSomeBox("belitaBox")
        tempText = i2s.Indiv_Kor_Return(belitaBoxName)
        sleep(1)

    for i in range(3):
        pag.press('esc')
        ms.sleep(0.5)

    ms.Move(ms.acceptQuestBtn)
    ms.sleep(0.5)
    ms.Move(ms.getFirstQuestBtn)
    ms.sleep(0.5)
    ms.Move(ms.okTeleportBtn)
    ms.sleep(0.5)

    ms.sleep(5)

    for i in range(4):
        pag.press('esc')
        ms.sleep(0.5)

    ms.Move(ms.acceptQuestBtn)

def 캐릭터생성_알파():#명령어사용

    ms.Move(ms.appUpPos)
    sleep(0.01)
    ms.Move(ms.characterNameBtn)
    ms.sleep(0.5)
    ms.Move(ms.characterNameInput)

    randomName = ""
    for i in range(8):
        randomName += random.choice(string.ascii_letters)
    ms.sleep(1)

    ms.inputCommand(randomName)
    ms.Move(ms.okPos)
    ms.sleep(1)
    
    ms.Move(ms.characterCreateBtn)
    ms.sleep(0.5)

    ms.Move(ms.characterCreateBtn)



    ms.sleep(5)

    
    tempText = ""


    for i in range(5) :
        if tempText != "벨리타" :
            print("텍스트 대기 중:", tempText)
            belitaBoxName = ms.captureSomeBox("belitaBox")
            try:
                tempText = i2s.Indiv_Kor_Return(belitaBoxName)
            except:
                print('no tesseract may be')
                pass
            sleep(1)
        else:
            break

    ms.Move(ms.centerPos)
    ms.sleep(0.5)
    ms.Move(ms.getFirstQuestBtn)
    ms.sleep(0.5)
    ms.Move(ms.acceptQuestBtn)
    ms.sleep(1)


    pag.press('esc')
    ms.sleep(0.5)
    pag.press('esc')
    ms.sleep(0.5)
    pag.press('esc')
    ms.sleep(0.5)
    pag.press('esc')
    ms.sleep(1)
    ms.Move(ms.acceptQuestBtn)
    ms.sleep(1)

    pag.press('d')
    ms.sleep(0.5)

    pag.keyDown('w')
    pag.keyDown('a')

    ms.sleep(1)

    pag.keyUp('w')
    pag.keyUp('a')

    ms.sleep(1)
    ms.Command("flowcompletequest 100500")

    # ms.sleep(2)
    # ms.Move(ms.acceptQuestBtn)
    # ms.sleep(0.5)
    # #ms.Move(ms.getFirstQuestBtn)
    # pag.press('esc')
    # ms.sleep(2)
    # ms.Move(ms.acceptQuestBtn)
    # ms.sleep(0.5)
    # #ms.Move(ms.getFirstQuestBtn)
    # pag.press('esc')
    # ms.sleep(0.5)
    # ms.Move(ms.okTeleportBtn)
    # ms.sleep(0.5)
    # ms.Move(ms.tutoMonPos)
    # ms.sleep(0.5)
    # ms.Move(ms.attackBtn)
    # ms.sleep(0.5)

    ms.Command("lv 99")

def 카드먹기_라이브():
    ms.Click(ms.quickBtn1)
    ms.sleep(2)
    ms.Click(ms.quickBtn2)
    ms.sleep(0.1)
    ms.Click(ms.menuPos4)
    ms.Click(ms.menuPos5)
    ms.sleep(0.3)
    ms.Click(ms.uiTabBtn2_7)

    delay_sec = 0.3
    ms.Click(ms.quest_category_btn_0)
    ms.Click(ms.quest_get_reward_btn_0)
    ms.sleep(delay_sec)
    ms.Click(ms.centerPos)
    ms.sleep(delay_sec)
    ms.Click(ms.quest_get_reward_btn_0)#quest_category_btn_1
    ms.sleep(delay_sec)
    ms.Click(ms.centerPos)

    ms.Click(ms.quest_category_btn_1)
    ms.Click(ms.quest_get_reward_btn_0)
    ms.sleep(delay_sec)
    ms.Click(ms.centerPos)
    ms.sleep(delay_sec)
    ms.Click(ms.quest_get_reward_btn_0)
    ms.sleep(delay_sec)
    ms.Click(ms.centerPos)

    ms.Click(ms.quest_category_btn_2)
    ms.Click(ms.quest_get_reward_btn_0)
    ms.sleep(delay_sec)
    ms.Click(ms.centerPos)
    ms.sleep(delay_sec)
    ms.Click(ms.quest_get_reward_btn_0)
    ms.sleep(delay_sec)
    ms.Click(ms.centerPos)

    ms.ResetFirst()
# def GoCharacterSelectPage():
#     ms.ResetFirst()
#     ms.Move(ms.menuPos4)
#     ms.sleep(0.5)
#     ms.Move(ms.menuPos20)
#     ms.Move(ms.menuMiddleUpperTab5)
#     ms.Move(ms.goCharacterSelectPageBtn)
#     ms.Move(ms.okPos)

def 맨뒤캐릭터접속():
    ms.Move(ms.menuPos4)
    ms.Move(ms.menuPos20)
    ms.sleep(0.1)
    ms.Move(ms.menuMiddleUpperTab5)
    ms.Move(ms.goCharacterSelectPageBtn)
    ms.sleep(0.01)
    ms.Move(ms.okPos)
    ms.sleep(1)

    for i in range(0,4):
        if '캐릭터 선택' in i2s.extract_text_from_image(ms.captureSomeBox5(ms.box_select_character,app_pos)) :
            break
        ms.sleep(1)

        


    
    ms.Move(ms.characterPageBtn1)
    #ms.sleep(0.01)
    ms.Move(ms.characterSlotBtn1)

    ms.Move(ms.characterCreateBtn)

def 카드먹기_반복():
    count = input('반복횟수(마을에서 대기)')

    for i in range(0,int(count)):
        맨뒤캐릭터접속()
        ms.sleep(8)
        for i in range(0,15):
            if 'x' in i2s.extract_text_from_image(ms.captureSomeBox5(ms.box_webview_x,app_pos),'eng') :
                ms.Click(ms.btn_webview_x)
                break
            ms.sleep(1.5)
        카드먹기_라이브()


from PIL import Image, ImageDraw
import pytesseract

def find_text_coordinates():
    def visualize_text_boxes(image_path, text_bbox):
        try:
            # Open the image
            with Image.open(image_path) as img:
                # Create a drawing object
                draw = ImageDraw.Draw(img)

                # Draw rectangles around each character
                for bbox in text_bbox.splitlines():
                    bbox = bbox.split()
                    left, top, right, bottom = int(bbox[1]), int(bbox[2]), int(bbox[3]), int(bbox[4])
                    draw.rectangle([left, top, right, bottom], outline="red", width=2)

                # Save or show the image with bounding boxes
                img.save("visualized_image.jpg")
                img.show()

        except Exception as e:
            print(f"Error visualizing text boxes: {e}")
    # Example: Find the coordinates of the center of '상점' in the image
    image_path = "screenshot/temp/20231117_145944.jpg"
    target_text = input('target_text : ')
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Use pytesseract to extract text
            extracted_text = i2s.extract_text_from_image(image_path,'kor+eng')#pytesseract.image_to_string(img, lang='kor')

            # Find the position of the target text
            target_position = extracted_text.find(target_text)

            if target_position != -1:
                # If the target text is found, get the bounding box of the text
                text_bbox = pytesseract.image_to_boxes(img, lang='kor+eng')
                target_bbox = [bbox.split() for bbox in text_bbox.splitlines() if target_text in bbox]

                if target_bbox:                    
                    visualize_text_boxes(image_path, text_bbox)
                    # Calculate the center coordinates of the target text
                    center_x = (int(target_bbox[0][1]) + int(target_bbox[0][3])) // 2
                    center_y = (int(target_bbox[0][2]) + int(target_bbox[0][4])) // 2
                    print(center_x,center_y)
                    return center_x, center_y
                else:
                    print(f"Bounding box not found for the target text: {target_text}")
            else:
                print(f"Target text not found: {target_text}")

    except Exception as e:
        print(f"Error processing the image: {e}")

    return None

#coordinates = find_text_coordinates(image_path, target_text)

    if coordinates:
        print(f"Center coordinates of '{target_text}': {coordinates}")
    else:
        print(f"Failed to find '{target_text}' in the image.")











def 상자자동사용설정리스트확인():
    

    ms.captureSomeBox
    ms.DragFrom([0.7286,0.6027],0,-75,1)

    


    #ms.sleep(1.8)


    #ms.DragFrom([0.7286,0.6027],0,-308,0.5)










import inspect

def display_menu():
    functions = [func for func in globals() if callable(globals()[func]) and inspect.isfunction(globals()[func])]

    print("Menu:")
    for i, func_name in enumerate(functions, start=1):
        print(f"[{i}] {func_name}")

def execute_function_by_index(index):
    functions = [func for func in globals() if callable(globals()[func]) and inspect.isfunction(globals()[func])]

    if 1 <= index <= len(functions):
        selected_func_name = functions[index - 1]
        selected_func = globals()[selected_func_name]
        selected_func()
    else:
        print("Invalid index. Please select a valid option.")
        
if __name__ == "__main__":
    options = input('[0]LD [1]MIR\n>: ')

    # app_pos, app_type = ms.get_target_app_pos()
    # print(app_pos, app_type)
    # ms.appX, ms.appY, ms.appW, ms.appH = app_pos[0],app_pos[1],app_pos[2],app_pos[3]
    # ms.플레이어변경(app_type)
    if options == '0':
        ms.appX, ms.appY, ms.appW, ms.appH = 0,33,1428,805
        ms.플레이어변경('LDPlayer')
    elif options == '1':
        ms.appX, ms.appY, ms.appW, ms.appH = 145,33,1194,677
        ms.플레이어변경('Mirroid')
    while True:
        display_menu()
        user_input = input("Enter the index of the function to execute (or 'q' to quit): ")

        if user_input.lower() == 'q':
            break

        try:
            index = int(user_input)
            execute_function_by_index(index)
        except ValueError:
            print("Invalid input. Please enter a number.")
