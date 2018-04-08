from random import randint
import re
# Minesweeper

def intz(thing):
   try:
       return int(thing)
   except ValueError:
       return 0

class MineObj:
   mine = "X"
   unknown = "?"
   no = "_"

def oc(x,left=False,right=False):
  if x<0:
      return False
  elif x>len(MINES) - 1:
      return False
  elif x%8==0 and left:
     return False
  elif x%8==7 and right:
     return False
  return True

def ocb(x):
   if x<0:
       return False
   elif x>len(MINES) - 1:
       return False
   elif MINES[x] != MineObj.no:
       return False
   return True
global MINES,FOUND_MINES
def setupMine():
   global MINES,FOUND_MINES
   MINES = list(MineObj.no * 64)
   FOUND_MINES = list(MineObj.unknown * 64)

   for i in range(randint(1,10)):
      mineid = randint(0,63)
      MINES[mineid] = MineObj.mine
      if oc(mineid - 1):
          MINES[mineid - 1] = str(1+intz(MINES[mineid - 1]))
      if oc(mineid + 1):
          MINES[mineid + 1] = str(1+intz(MINES[mineid + 1]))
      if oc(mineid - 9):
          MINES[mineid - 9] = str(1+intz(MINES[mineid - 9]))
      if oc(mineid - 8):
          MINES[mineid - 8] = str(1+intz(MINES[mineid - 8]))
      if oc(mineid - 7):
          MINES[mineid - 7] = str(1+intz(MINES[mineid - 7]))
      if oc(mineid + 9):
          MINES[mineid + 9] = str(1+intz(MINES[mineid + 9]))
      if oc(mineid + 8):
          MINES[mineid + 8] = str(1+intz(MINES[mineid + 8]))
      if oc(mineid + 7):
          MINES[mineid + 7] = str(1+intz(MINES[mineid + 7]))

async def printList(ctx):
   global FOUND_MINES
   output="```\n"
   for j in range(8):
       for k in range(8):
           output+=FOUND_MINES[8*j+k]
       output+="\n"
   output+="```"
   return await ctx.send(output)

async def updateList(ctx,status):
   global FOUND_MINES
   output="```\n"
   for j in range(8):
       for k in range(8):
           output+=FOUND_MINES[8*j+k]
       output+="\n"
   output+="```"
   await status.edit(content=output)
   return
async def checkCell(cellStr,ctx,status):
   global MINES,FOUND_MINES
   try:
       cellIds=list(map(intz,cellStr.split(" ")))
   except TypeError:
       return
   cellID = (cellIds[1] - 1) * 8 + cellIds[0] - 1
   if MINES[cellID] == MineObj.mine:
       await ctx.send("Game over!")
       FOUND_MINES = MINES
       await updateList(ctx,status)
       return (1,FOUND_MINES)
   elif FOUND_MINES[cellID] != MineObj.unknown:
       return (0,FOUND_MINES)
   elif MINES[cellID] == "1" or MINES[cellID] == "2" or MINES[cellID] == "3" or MINES[cellID] == MineObj.no:
       FOUND_MINES[cellID] = MINES[cellID]
       checkCell=[cellID]
       checkedCell = set()
       paths = 0
       while len(checkCell) != 0:
           paths += 1
           cellID=checkCell[0]
           if ocb(cellID - 1) and (cellID - 1) not in checkedCell:
               FOUND_MINES[cellID - 1] = MINES[cellID - 1]
               checkCell.append(cellID - 1)
           if ocb(cellID + 1) and (cellID + 1) not in checkedCell:
               FOUND_MINES[cellID + 1] = MINES[cellID + 1]
               checkCell.append(cellID + 1)
           if ocb(cellID - 9) and (cellID - 9) not in checkedCell:
               FOUND_MINES[cellID - 9] = MINES[cellID - 9]
               checkCell.append(cellID - 9)
           if ocb(cellID - 8) and (cellID - 8) not in checkedCell:
               FOUND_MINES[cellID - 8] = MINES[cellID - 8]
               checkCell.append(cellID - 8)
           if ocb(cellID - 7) and (cellID - 7) not in checkedCell:
               FOUND_MINES[cellID - 7] = MINES[cellID - 7]
               checkCell.append(cellID - 7)
           if ocb(cellID + 9) and (cellID + 9) not in checkedCell:
               FOUND_MINES[cellID + 9] = MINES[cellID + 9]
               checkCell.append(cellID + 9)
           if ocb(cellID + 8) and (cellID + 8) not in checkedCell:
               FOUND_MINES[cellID + 8] = MINES[cellID + 8]
               checkCell.append(cellID + 8)
           if ocb(cellID + 7) and (cellID + 7) not in checkedCell:
               FOUND_MINES[cellID + 7] = MINES[cellID + 7]
               checkCell.append(cellID + 7)
           checkedCell.add(cellID)
           checkCell.pop(0)
       await updateList(ctx,status)
       return (0,FOUND_MINES)
   else:
       return

async def play(ctx):
   global MINES,FOUND_MINES
   setupMine()
   status = await printList(ctx)
   guess = await ctx.bot.wait_for('message',check=lambda m: m.channel == ctx.channel and re.match("^[1-8] [1-8]$",m.content))
   inputStr = guess.content
   await guess.delete()
   ans=await checkCell(inputStr,ctx,status)
   while ans[0] == 0 :
       guess = await ctx.bot.wait_for('message',check=lambda m: m.channel == ctx.channel and re.match("^[1-8] [1-8]$",m.content))
       inputStr = guess.content
       await guess.delete()
       ans=await checkCell(inputStr,ctx,status)
       ans_str=str(list(map(str,FOUND_MINES)))
       ans_str=ans_str.replace(MineObj.unknown,MineObj.mine)
       mines_str=str(list(map(str,MINES)))
       if ans[0] == 1:
           break
       elif ans_str == mines_str:
           await ctx.send("You find all mines!")
           break
   return
