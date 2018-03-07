#!/bin/bash

#LOG_FILE=/var/log/light-strip-reader.log
LOG_FILE=/dev/stdout
OUT_FILE=/etc/light-strip/light.conf
#CHK_FILE=/tmp/light-strip-checksum
PID_FILE=/tmp/light-strip.pids
FAST_SUCCESS=false

function log() {
	TAG=$1
	MESSAGE=$2
	#echo -e "$(date +%Y-%m-%dT%H:%M:%S.%N) [${TAG}]: ${MESSAGE}" #>> $LOG_FILE
	echo -e "[${TAG}]: ${MESSAGE}" #>> $LOG_FILE
}

function send() {
	DEVICE=$1
	MESSAGE=$2
	echo -e "${MESSAGE}\n" >> ${DEVICE}
}

function writeResult() {
	CONTENT=$1
	TMP_FILE="${OUT_FILE}.tmp"
	echo -e "${CONTENT}" > ${TMP_FILE}
	if [[ $(diff ${OUT_FILE} ${TMP_FILE}) ]]; then
		mv ${TMP_FILE} ${OUT_FILE}
	else
		rm ${TMP_FILE}
	fi
}

function loop() {
	DEVICE=$1
	WAIT_FOR_REMOVE=$2
	while true; do # LOOPER
		MODE=0
		CONTENT=""
		log "${DEVICE}(${MODE})" "Connecting..."
		while [[ ! -e ${DEVICE} ]]; do sleep 1; done
		#stty -F ${DEVICE} sane
		log "${DEVICE}(${MODE})" "Connected"

		cat ${DEVICE} | while read line; do
			if [[ $line != "" ]]; then
				line=$(echo $line | sed -E "s/[\r\n]//g")
				log "${DEVICE}(${MODE})" "Read: \"${line}\""

				if [[ $MODE = 0 ]] && [[ $line = "STX" ]]; then
					CONTENT=""
					MODE=1
					log "${DEVICE}(${MODE})" "Message START"
				elif [[ $MODE = 0 ]] && [[ $line = "ENQ" ]]; then
					log "${DEVICE}(${MODE})" "Identifying..."
					send ${DEVICE} "ACK:20180214"
				elif [[ $MODE = 1 ]] && [[ $line == "ETX" ]]; then
					log "${DEVICE}(${MODE})" "<<BEGIN>>\n${CONTENT}\n<<END>>"
					echo -n ${CONTENT} > /tmp/checksum
					#cat /tmp/checksum
					#CHECKSUM=$(cksfv /tmp/checksum | tail -1)
					#log "${DEVICE}(${MODE})" "Checksum A: ${CHECKSUM}"
					#CHECKSUM=$(echo ${CHECKSUM} | cut -d" " -f2)
					#log "${DEVICE}(${MODE})" "Checksum B: ${CHECKSUM}"
					#CHECKSUM=$(echo "ibase=16; ${CHECKSUM}" | bc)
					CHECKSUM=$(echo "ibase=16; $(cksfv /tmp/checksum | tail -1 | cut -d" " -f2)" | bc)
					log "${DEVICE}(${MODE})" "Checksum C: ${CHECKSUM}"
					#CHECKSUM=$((16#$(cksfv /tmp/checksum | grep "^/" | cut -d" " -f2))
					#rm /tmp/checksum
					#send ${DEVICE} "ACK:${CHECKSUM}"
					echo -e "ACK:${CHECKSUM}\n\r" >> ${DEVICE}
					log "${DEVICE}(${MODE})" "Checksum: ${CHECKSUM}"
					if [[ $FAST_SUCCESS ]]; then # FAST SUCCESS
						writeResult ${CONTENT}
					fi
					MODE=2
					log "${DEVICE}(${MODE})" "Waiting for acknowledgment..."
				elif [[ $MODE = 1 ]]; then
					#log "${DEVICE}(${MODE})" "Read: \"${line}\""
					CONTENT="${CONTENT}${line}"
				elif [[ $MODE = 2 ]] && [[ $line = "ACK" ]]; then
					log "${DEVICE}(${MODE})" "ACKNOWLEDGED"
					writeResult ${CONTENT}
					MODE=0
				elif [[ $line = "ETX" ]]; then
					MODE=0
				else
					log "${DEVICE}(${MODE})" "Ignored: ${line}"
				fi
			fi
		done #< ${DEVICE}
		log "${DEVICE}(${MODE})" "Disconnected"
		if [[ ${WAIT_FOR_REMOVE} = 1 ]]; then
			log "${DEVICE}(${MODE})" "Waiting for removal..."
			while [[ -e ${DEVICE} ]]; do sleep 1; done
		else
			sleep 1
		fi
	done
	log "${DEVICE}(${MODE})" "Restarting..."
	loop ${DEVICE}
}

log "MAIN" "Starting..."
rm ${PID_FILE}

loop /dev/ttyGS0 0 & 
echo $! >> ${PID_FILE}

loop /dev/rfcomm0 1 &
echo $! >> ${PID_FILE}

wait
log "MAIN" "Finishing up..."
cat ${PID_FILE} | while read pid; do
	log "MAIN" "Killing ${pid}"
	kill -9 ${pid}
done
rm ${PID_FILE}

