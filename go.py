import os
import random
import wave

outfile = "part_no_{pNo}.wav"

audioPath = "audio/"

lengths = {}

import contextlib
for file in os.listdir(audioPath):
	if file == ".DS_Store":
		continue
	fname = 'audio/'+file
	with contextlib.closing(wave.open(fname,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate) * 2
		finalName = file.split(".")[0]
		print(finalName)
		print(duration)
		lengths[finalName] = int(duration)

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

MARKER = "**********"
lengths[MARKER]=0


HOLD = "hold"
NORMAL_BREATH = "NORMAL_BREATH"
QUICK_BREATH = "QUICK_BREATH"
REVER_BREATH = "REVER_BREATH"

HUM = "HUM"
HUM_BREATH_L = "HUM_BREATH_L"
HUM_BREATH_M = "HUM_BREATH_M"
HUM_BREATH_H = "HUM_BREATH_H"

SING = "SING"
SING_BREATH_L = "SING_BREATH_L"
SING_BREATH_M = "SING_BREATH_M"
SING_BREATH_H = "SING_BREATH_H"

CLAP_INTRO = "CLAP_INTRO"
CLAP = "CLAP"
SNAP_INTRO = "SNAP_INTRO"
SNAP = "SNAP"

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
	if partNo in [HUM_BREATH_L, HUM_BREATH_M, HUM_BREATH_H]:
		ret.append("in")
		if partNo == HUM_BREATH_L:
			ret.append("humLow")
		elif partNo == HUM_BREATH_M:
			ret.append("humMiddle")
		elif partNo == HUM_BREATH_H:
			ret.append("humHigh")
		ret.append("silence1")
		ret.append("silence1")
		ret.append("silence1")
		ret.append("silence1")
		ret.append("silence1")

	if partNo in [SING_BREATH_L, SING_BREATH_M, SING_BREATH_H]:
		ret.append("in")
		if partNo == SING_BREATH_L:
			ret.append("singLow")
		elif partNo == SING_BREATH_M:
			ret.append("singMiddle")
		elif partNo == SING_BREATH_H:
			ret.append("singHigh")
		ret.append("silence1")
		ret.append("silence1")
		ret.append("silence1")
		ret.append("silence1")
		ret.append("silence1")
	if partNo == SNAP:
		ret.append("snapNow")
	if partNo == CLAP:
		ret.append("clapNow")

	if partNo == CLAP_INTRO:
		ret.append("clapIntro")
	if partNo == SNAP_INTRO:
		ret.append("snapIntro")
	return ret





noVoices=4

parts = []
for i in range(noVoices):
	parts.append([])



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

def staggeredUnison():
	# SCENE TWO: Mostly together but one person is offset
	for z in range(2):
		for i in range(2):
			for p in range(noVoices):
				#parts[p].append("in")
				if p%3 == 1:
					parts[p].append("hold1")
				#parts[p].append("out")
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


def phasing(voiceLevel, percusLevel):
	if voiceLevel == SING:
		VOICE_L = SING_BREATH_L
		VOICE_M = SING_BREATH_M
		VOICE_H = SING_BREATH_H
	else:
		VOICE_L = HUM_BREATH_L
		VOICE_M = HUM_BREATH_M
		VOICE_H = HUM_BREATH_H

	if percusLevel == SNAP:
		PERCUS = SNAP
		PERCUS_INTRO = SNAP_INTRO
	else:
		PERCUS = CLAP
		PERCUS_INTRO = CLAP_INTRO

	# SCENE THREE: a whole conviluted phasing + 2 singing + Snap Intro
	for p in range(noVoices):
		# sings and recovers from singing
		if p%3 == 0:
			# We need 91 seconds
			# normal breaths are 7
			# short breaths are 6
			# singing breaths are 11
			# therefore we need 6 normal, 2 singing, 4 short
			toDo = [NORMAL_BREATH]*6
			toDo.extend([VOICE_L])
			toDo.extend([VOICE_M])
			toDo.extend([QUICK_BREATH]*4)
			random.shuffle(toDo)
			toDo.append(PERCUS_INTRO)
			toDo.append(PERCUS)
			for i in range(len(toDo)):
				parts[p].extend(getTheToDo(toDo[i]))
			parts[p].append("in")
			parts[p].append("hold1")
			parts[p].append("out")
		if p%3 == 1:
			# just keep the dang beat
			for i in range(13):
				parts[p].extend(getTheToDo(NORMAL_BREATH))	
			parts[p].append("in")
			parts[p].extend(getTheToDo(PERCUS_INTRO))
			parts[p].append("out")
					

		if p%3 == 2:
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


def randomHumPercuss(voiceLevel, percusLevel):
	if voiceLevel == SING:
		VOICE_L = SING_BREATH_L
		VOICE_M = SING_BREATH_M
		VOICE_H = SING_BREATH_H
	else:
		VOICE_L = HUM_BREATH_L
		VOICE_M = HUM_BREATH_M
		VOICE_H = HUM_BREATH_H

	if percusLevel == SNAP:
		PERCUS = SNAP
		PERCUS_INTRO = SNAP_INTRO
	else:
		PERCUS = CLAP
		PERCUS_INTRO = CLAP_INTRO

	# INCLUDES CLAP AN DOING IT
	# SCENE FOUR: PRETTY RANDOM, INCLUDES SECOND INTRO + DOING THE FIRST
	for p in range(noVoices):
		toDo = [
			PERCUS,
			PERCUS,
			PERCUS,
			NORMAL_BREATH,
			NORMAL_BREATH,
			REVER_BREATH,
			REVER_BREATH,
			VOICE_L,
			VOICE_M,
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
		print partToAppend
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










introduction()
allSilence(random.randint(2,5))

toDo = [
	fadeIn,
	fadeOut,
	percussion,
	randomHumPercuss,
	phasing,
	staggeredUnison,
]
goodToGo = False
while not goodToGo:
	random.shuffle(toDo)
	goodToGo = True

	#make sure fades are not adjacent
	for i in range(1,len(toDo)-1):
		if toDo[i] in [fadeIn, fadeOut]:
			if fadeIn in [toDo[i-1],toDo[i+1]] or fadeOut in [toDo[i-1],toDo[i+1]]:
				goodToGo = False
	introsSoFar = 0
	for i in range(len(toDo)):
		if toDo[i] in [randomHumPercuss,phasing]:
			introsSoFar +=1
		if toDo[i] == percussion and introsSoFar <2:
			goodToGo = False


allSilence(random.randint(2,5))



#go through and actually build the piece
for i in toDo:
	voiceLevel = HUM
	percusLevel = SNAP
	if i in [randomHumPercuss,phasing]:
		i(voiceLevel,percusLevel)
		voiceLevel = SING
		percusLevel = CLAP
	else:
		i()















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

for i in range(maxLen+15):
	toPrint = []
	for p in range(len(parts)):
		try:
			toPrint.append('{:10s}'.format(totalDoing[p][i]))
		except:
			toPrint.append('{:10s}'.format(" "))
	print " - ".join (toPrint)

print "totalTime = " + str((maxLen / 2) / 60)+":{:2d}".format((maxLen/2)%60)
print partLens






for p in range(len(parts)):
	data= []
	for infile in parts[p]:
		if infile == MARKER:
			continue
		w = wave.open("audio/"+infile+".wav")
		data.append( [w.getparams(), w.readframes(w.getnframes())] )
		w.close()

	output = wave.open(outfile.format(pNo=str(p+1)), 'wb')
	output.setparams(data[0][0])
	# print parts[p]
	dataIndex = 0
	for i in range(len(parts[p])):
		if parts[p][i] == MARKER:
			continue
		output.writeframes(data[dataIndex][1])
		dataIndex+=1
	output.close()