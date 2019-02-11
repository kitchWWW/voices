import contextlib
import os
import random
import wave

timeStamp = "12345"

outfile = "part_no_{pNo}.wav"
outPath = "out/"+timeStamp+"/"
noOfSectionsModifer = 0 #-2 is shorter, 2 is longer, 0 is normal
noVoices=4
generateMP3 = True

try:
	os.mkdir(outPath)
except:
	pass


# start off by building the dictionary of how long the different audio files are
audioPath = "audio/"
lengths = {}
for file in os.listdir(audioPath):
	if file == ".DS_Store":
		continue
	fname = 'audio/'+file
	with contextlib.closing(wave.open(fname,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate) * 2
		finalName = file.split(".")[0]
		lengths[finalName] = int(duration)



# a couple of helper functions
def printAsTime(ticks):
	return "[" + str((ticks / 2) / 60)+":{:2d}".format((ticks/2)%60)+'] , '

def hasInfrequentBreaths(part):
	sinceLastBreath = 0
	for i in range(len(part)):
		if "in" not in part[i]:
			sinceLastBreath += 1
		if sinceLastBreath > 5:
			return True
	return False

def genPartFromTodo(toDo):
	partToAppend = []
	for i in range(len(toDo)):
		partToAppend.extend(getTheToDo(toDo[i]))
	return partToAppend

def levelsForPart(part):
	VOICE_L = HUM_BREATH_L
	VOICE_H = HUM_BREATH_H
	PERCUS = SNAP
	PERCUS_INTRO = SNAP_INTRO
	levs = introCount[part]
	if levs[0] == 1:
		VOICE_L = SING_BREATH_L
		VOICE_H = SING_BREATH_H
	if levs[1] == 1:
		PERCUS = CLAP
		PERCUS_INTRO = CLAP_INTRO
	if levs[1] > 1:
		PERCUS = CLAP
		PERCUS_INTRO = CLAP
	#yes, currently these are always the same
	introCount[part] = [levs[0]+1, levs[1]+1]

	return PERCUS,PERCUS_INTRO,VOICE_L,VOICE_H




# and all of our constants
MARKER = "**********"

lengths[MARKER]=0


HOLD = "hold"
NORMAL_BREATH = "NORMAL_BREATH"
QUICK_BREATH = "QUICK_BREATH"
REVER_BREATH = "REVER_BREATH"

HUM = "HUM"
HUM_BREATH_L = "HUM_BREATH_L"
HUM_BREATH_H = "HUM_BREATH_H"

SING = "SING"
SING_BREATH_L = "SING_BREATH_L"
SING_BREATH_H = "SING_BREATH_H"

CLAP_INTRO = "CLAP_INTRO"
CLAP = "CLAP"
SNAP_INTRO = "SNAP_INTRO"
SNAP = "SNAP"

# and like the most important helper function
def getTheToDo(partNo):
	ret = []
	if partNo == NORMAL_BREATH:
		ret.append("in")
		ret.append("out")
		ret.append("silence1")
	if partNo == QUICK_BREATH:
		ret.append("in")
		ret.append("out")
	if partNo == REVER_BREATH:
		ret.append("inMouth")
		ret.append("hold1")
		ret.append("outNose")
	if partNo in [HUM_BREATH_L, HUM_BREATH_H]:
		ret.append("in")
		ret.append("hum")
		ret.append("pitch7")

	if partNo in [SING_BREATH_L, SING_BREATH_H]:
		ret.append("in")
		ret.append("sing")
		ret.append("pitch7")
	if partNo == SNAP:
		ret.append("snapNow")
	if partNo == CLAP:
		ret.append("clapNow")

	if partNo == CLAP_INTRO:
		ret.append("clapIntro")
	if partNo == SNAP_INTRO:
		ret.append("snapIntro")
	return ret




### all the deffinitions of scenes. These all add directly to "parts" array!

def introduction():
	#STARTING
	for p in range(noVoices):
		parts[p].append("intro")
		parts[p].append(MARKER)

def allSilence(length):
	for p in range(noVoices):
		for i in range(length):
			parts[p].append("silence1")

	for p in range(noVoices):
		parts[p].append(MARKER)
	
def allUnisons(length):
	#SCENE ONE: "Everyone doing it together"
	for p in range(noVoices):
		for i in range(length):
			parts[p].append("inNose")
			parts[p].append("outMouth")
			parts[p].append("silence1")
	for p in range(noVoices):
		parts[p].append(MARKER)

def allSnap():
	for p in range(noVoices):
		parts[p].append("snapNow")
		parts[p].append(MARKER)

def staggeredUnison():
	# SCENE TWO: Mostly together but one person is offset
	for z in range(2):
		for i in range(2):
			for p in range(noVoices):
				parts[p].append("in")
				if p%3 == 1:
					parts[p].append("hold1")
				parts[p].append("out")
				if p%3 != 1:
					parts[p].append("silence1")
		for p in range(noVoices):
			parts[p].append("in")
			parts[p].append("out")
			parts[p].append("silence1")
			parts[p].append("silence1")
			parts[p].append("silence1")

	for p in range(noVoices):
		parts[p].append(MARKER)

def phasing():
	voiceAssignments = range(3)
	random.shuffle(voiceAssignments)

	# SCENE THREE: a whole conviluted phasing + 2 singing + Snap Intro
	for p in range(noVoices):
		PERCUS,PERCUS_INTRO,VOICE_L,VOICE_H = levelsForPart(p)

		# sings and recovers from singing
		if p%3 == voiceAssignments[0]:
			# We need 91 seconds
			# normal breaths are 7
			# short breaths are 6
			# singing breaths are 11
			# therefore we need 6 normal, 2 singing, 4 short
			toDo = [NORMAL_BREATH]*6
			toDo.extend([VOICE_L])
			toDo.extend([VOICE_H])
			toDo.extend([QUICK_BREATH]*4)
			random.shuffle(toDo)
			toDo.append(PERCUS_INTRO)
			toDo.append(PERCUS)
			for i in range(len(toDo)):
				parts[p].extend(getTheToDo(toDo[i]))
			parts[p].append("in")
			parts[p].append("hold1")
			parts[p].append("out")
		if p%3 == voiceAssignments[1]:
			# just keep the dang beat
			for i in range(13):
				parts[p].extend(getTheToDo(NORMAL_BREATH))	
			parts[p].append("in")
			parts[p].extend(getTheToDo(PERCUS_INTRO))
			parts[p].append("out")
					

		if p%3 == voiceAssignments[2]:
			# Phasing time!!!!!
			for i in range(14):
				parts[p].append("in")
				parts[p].append("out")
				parts[p].append("silence5")	
			parts[p].append("in")
			parts[p].extend(getTheToDo(PERCUS_INTRO))
			parts[p].append("out")
	for p in range(noVoices):
		parts[p].append(MARKER)

def randomHumPercuss():

	# INCLUDES CLAP AN DOING IT
	# SCENE FOUR: PRETTY RANDOM, INCLUDES SECOND INTRO + DOING THE FIRST
	for p in range(noVoices):
		PERCUS,PERCUS_INTRO,VOICE_L,VOICE_H = levelsForPart(p)
		toDo = [
			PERCUS,
			PERCUS,
			PERCUS,
			NORMAL_BREATH,
			NORMAL_BREATH,
			REVER_BREATH,
			REVER_BREATH,
			VOICE_L,
			VOICE_L,
			]
		random.shuffle(toDo)
		toDo.insert(random.randint(0,int(len(toDo)/2)),VOICE_H)
		toDo.insert(random.randint(int(len(toDo)/2),len(toDo)-1),VOICE_H)
		toDo.insert(toDo.index(PERCUS),PERCUS_INTRO)
		
		for do in toDo:
			parts[p].extend(getTheToDo(do))
	for p in range(noVoices):
		parts[p].append(MARKER)

def percussion():
	#SCENE FIVE: THE PERCUSSIVE ONE
	# just a bunch of snapping and clapping:
	for p in range(noVoices):
		toDo = [
			NORMAL_BREATH,
			NORMAL_BREATH,
			NORMAL_BREATH,
			NORMAL_BREATH,
			]
		partToAppend = genPartFromTodo(toDo)
		for i in range(3):
			partToAppend.insert(random.randint(0,len(partToAppend)-1), "snapNow")
		for i in range(3):
			partToAppend.insert(random.randint(0,len(partToAppend)-1), "clapNow")
		parts[p].extend(partToAppend)
	for p in range(noVoices):
		parts[p].append(MARKER)

def singingTime():
	#SCENE FIVE: THE PERCUSSIVE ONE
	# just a bunch of snapping and clapping:
	waitsBeforeStarting = range(noVoices)
	random.shuffle(waitsBeforeStarting)
	for p in range(noVoices):
		toDo = [
			NORMAL_BREATH,
			NORMAL_BREATH,
			HUM_BREATH_L,
			HUM_BREATH_H,
			SING_BREATH_L,
			SING_BREATH_H,
			]
		random.shuffle(toDo)
		partToAppend = ["silence1"] * waitsBeforeStarting[p]
		partToAppend.extend(genPartFromTodo(toDo))
		partToAppend.extend(["silence1"] * (noVoices - waitsBeforeStarting[p]))

		parts[p].extend(partToAppend)

	for p in range(noVoices):
		parts[p].append(MARKER)

def fadeIn():
	#SCENE SIX: FADE IN
	starter = random.randint(0,noVoices-1)
	startTimes = random.sample(range(1,3+noVoices),noVoices)	
	startTimes[starter] = 0
	for p in range(noVoices):
		for i in range(4+noVoices):
			if startTimes[p] == i:
				parts[p].append("inMouth")
				parts[p].append("outMouth")
			elif startTimes[p] < i:
				parts[p].append("inNose")
				parts[p].append("outMouth")
			elif i == 0:
				parts[p].append("jchill")
				parts[p].append("silence1")
				parts[p].append("silence1")
			else:
				for z in range(6):
					parts[p].append("silence1")
	for p in range(noVoices):
		parts[p].append(MARKER)		

def fadeOut():
	#SCENE SEVEN: FADE OUT
	starter = random.randint(0,noVoices-1)
	startTimes = random.sample(range(1,3+noVoices),noVoices)	
	startTimes[starter] = 4+noVoices
	for p in range(noVoices):
		for i in range(4+noVoices):
			if startTimes[p] == i:
				parts[p].append("inMouth")
				parts[p].append("outMouth")
			elif startTimes[p] > i:
				parts[p].append("inNose")
				parts[p].append("outMouth")
			elif startTimes[p] == i-1:
				parts[p].append("jchill")
				parts[p].append("silence1")
				parts[p].append("silence1")
			else:
				for z in range(6):
					parts[p].append("silence1")
	for p in range(noVoices):
		parts[p].append(MARKER)		





# initlize the parts and things to start actually making the piece!
parts = []
introCount = []
for i in range(noVoices):
	parts.append([])
	introCount.append([0,0])



# Find the order of things we are going to play

simpleSounds = [fadeIn, fadeOut, allUnisons,staggeredUnison]
goodToGo = False
while not goodToGo:
	toDo = [
		allUnisons,
		fadeIn,
		fadeOut,
		percussion,
		randomHumPercuss,
		phasing,
		staggeredUnison,
		singingTime,
	]
	toDouble = random.sample(toDo,max(0,2+noOfSectionsModifer))
	toRemove = random.sample(toDo,max(0,2-noOfSectionsModifer))
	for func in toRemove:
		toDo.remove(func)
	for func in toDouble:
		toDo.append(func)
	random.shuffle(toDo)
	goodToGo = True
	#make sure fades are not adjacent
	if toDo[0] not in simpleSounds:
		goodToGo = False

	for i in range(1,len(toDo)):
		if toDo[i] == toDo[i-1]:
			goodToGo = False

	#avoid simple sounds next to eachother
	for i in range(1,len(toDo)):
		if toDo[i] in simpleSounds:
			if toDo[i-1] in simpleSounds:
				goodToGo = False
	introsSoFar = 0
	# make sur we get two adds before percussion or singing time
	for i in range(len(toDo)):
		if toDo[i] in [randomHumPercuss,phasing]:
			introsSoFar +=1
		if toDo[i] in [percussion] and introsSoFar <2:
			goodToGo = False






#go through and actually build the piece, calling all the scene functions above
shortScore = []

introduction()
shortScore.append(introduction)

allSilence(random.randint(2,5))
shortScore.append(allSilence)

for i in range(len(toDo)):
	if i == len(toDo)-1:
		allSnap()
		shortScore.append(allSnap)
	if toDo[i] == allUnisons:
		toDo[i](random.randint(4,7))
		shortScore.append(toDo[i])
	else:
		toDo[i]()
		shortScore.append(toDo[i])
	if i < len(toDo)-1:
		if toDo[i] not in simpleSounds and toDo[i+1] not in simpleSounds:
			allUnisons(random.randint(1,3))
			shortScore.append(allUnisons)

allSnap()
shortScore.append(allSnap)










# now go through and replace every "pitch7" with an actual pitch. 7 is length










totalNumberOfPitchesToSing = 0
print parts
for p in range(noVoices):
	for i in range(len(parts[p])):
		print parts[p][i]
		if parts[p][i] == "pitch7":
			totalNumberOfPitchesToSing += 1

print totalNumberOfPitchesToSing

freePitches = totalNumberOfPitchesToSing-2

numberOfKeyAreas = freePitches / (3*noVoices)
lenOfKeyAreas = (3*noVoices)
print "numberOfKeyAreas", numberOfKeyAreas




keyAreas = [
	[0,4,5,7],
	[2,4,5,9],
	[0,4,5,9],
	[0,3,7,8],
	[0,2,5,9],
	[2,4,5,9]
]
noteNames = ['c','cis','d','dis','e','f','fis','g','gis','a','ais','b']

for i in range(len(keyAreas)):
	random.shuffle(keyAreas[i])

def getPitch():
	global pitchesSungSoFar
	if pitchesSungSoFar > freePitches or pitchesSungSoFar == 0:
		pitchesSungSoFar += 1
		return noteNames[0]
	keyArea = pitchesSungSoFar / lenOfKeyAreas
	ret = noteNames[keyAreas[keyArea][pitchesSungSoFar % 4] % len(noteNames)]
	print "hello help"
	print ret
	pitchesSungSoFar+=1
	return ret





pitchesSungSoFar = 0
for p in range(noVoices):
	for i in range(len(parts[p])):
		print parts[p][i]
		if parts[p][i] == "pitch7":
			parts[p][i] = "_pitch"+str(getPitch())










#now start outputing things


# this builds the map of who is doing exactly what at every half second
totalDoing = []
maxLen = 0
partLens = []

for p in range(noVoices):
	markerCount = 0
	toApp = []
	for i in range(len(parts[p])):
		durr = lengths[parts[p][i]]
		if parts[p][i] == MARKER:
			toApp.append(MARKER)
			markerCount += 1
		for z in range(durr):
			toApp.append(parts[p][i])
	partLens.append(len(toApp) - markerCount)
	if len(toApp)- markerCount > maxLen:
		maxLen = len(toApp)- markerCount
	totalDoing.append(toApp)


# This actually writes that information to a score and to a short_score
ticks = 0
toWriteTofile = []
for i in range(maxLen+ markerCount):
	toPrint = []
	for p in range(len(parts)):
		try:
			toPrint.append('{:10s}'.format(totalDoing[p][i]))
			if p == 0 and totalDoing[p][i] != MARKER:
				ticks+=1
		except:
			toPrint.append('{:10s}'.format(" "))
	timeBit = " "*7+", "
	if int(ticks/2.0) == ticks/2.0:
		timeBit = printAsTime(int(ticks))
	toWriteTofile.append(timeBit + " , ".join (toPrint))

fd = open(outPath+"score.csv",'w')
fd.write("\n".join(toWriteTofile))
fd.close()

fd = open(outPath+"short_score.txt","w")
fd.write("\n".join([x.__name__ for x in shortScore]))
fd.close()



# tell the user how long this whole shindig is taking
print "totalTime = " + printAsTime(maxLen).split(",")[0]
print "ticks:",str(partLens[0])
print "segments:", len(toDo)






# now make the actual audio files!
for p in range(len(parts)):
	data= []
	for infile in parts[p]:
		if infile == MARKER:
			continue 
		w = wave.open("audio/"+infile+".wav")
		data.append( [w.getparams(), w.readframes(w.getnframes())] )
		w.close()

	output = wave.open(outPath+outfile.format(pNo=str(p+1)), 'wb')
	output.setparams(data[0][0])
	# print parts[p]
	dataIndex = 0
	for i in range(len(parts[p])):
		if parts[p][i] == MARKER:
			continue
		output.writeframes(data[dataIndex][1])
		dataIndex+=1
	output.close()

# and convert it to an MP3?
if generateMP3:
	for p in range(len(parts)):
		pass
		#os.system("lame --preset insane "+outPath+outfile.format(pNo=str(p+1)) +" &" )





