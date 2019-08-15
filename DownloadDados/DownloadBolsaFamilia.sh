#!/bin/bash
FROM_ENCODING="iso-8859-1"
TO_ENCODING="UTF-8"
for i in $(seq 2013 2019); do

	for j in $(seq 1 12); do
		if [ $j -le 10 ]; then
            wget http://www.portaltransparencia.gov.br/download-de-dados/bolsa-familia-pagamentos/${i}0${j} -O ${i}0${j}.zip
            unzip ${i}0${j}.zip -p > ${i}0${j}.csv
            iconv -f $FROM_ENCODING -t $TO_ENCODING ${i}0${j}.csv -o ${i}0${j}.utf-8.csv
        else
        	wget http://www.portaltransparencia.gov.br/download-de-dados/bolsa-familia-pagamentos/$i$j -O $i$j.zip
        	unzip $i$j.zip -p > $i$j.csv
            iconv -f $FROM_ENCODING -t $TO_ENCODING $i$j.csv -o $i$j.utf-8.csv
		fi		
	done
done