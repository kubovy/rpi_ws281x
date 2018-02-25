#!/bin/bash

LOG_FILE="/var/log/light-strip-refresh.log"
echo "" > $LOG_FILE 

function loop() {
	stty -F /dev/ttyGS0 sane
	MODE=0
	CONTENT=""
	while read line; do
		if [[ $line != "" ]]; then
			if [[ $MODE = 0 ]] && [[ $line = "START" ]]; then
				CONTENT=""
				MODE=1
				echo ">>Started<<" >> $LOG_FILE
			elif [[ $MODE = 0 ]] && [[ $line = "ID" ]]; then
				echo ">>Identifying...<<" >> $LOG_FILE
				echo -e "CONFIRMATION_BEGIN\nPOTERION IOT:{\"name\": \"Calvatia\", \"features\": [\"light-strip\"], \"properties\": [\"24x2+2\"]}\nCONFIRMATION_END\n" > /dev/ttyGS0
			elif [[ $MODE = 1 ]] && [[ $line == "END" ]]; then
				echo -e "<<BEGIN>>\n${CONTENT}\n<<END>>" >> $LOG_FILE
				echo -e "${CONTENT}" > /etc/light-strip/light.conf
				echo -e "CONFIRMATION_BEGIN\n${CONTENT}\nCONFIRMATION_END\n" > /dev/ttyGS0
				MODE=0
				echo ">>Finished<<" >> $LOG_FILE
			elif [[ $MODE = 1 ]]; then
				#echo ">>Read: ${line}<<"
				if [[ $CONTENT != "" ]]; then CONTENT="${CONTENT}\n"; fi
				CONTENT="${CONTENT}${line}"
			else
				echo ">>Ignored: ${line}<<" >> $LOG_FILE
			fi
		fi
	done < /dev/ttyGS0
	loop
}

loop

