#!/bin/bash

MCDIR=$1

rm -r $MCDIR/backup
echo backup erased

mv $MCDIR/running $MCDIR/backup
echo created new backup

mkdir $MCDIR/running
unzip $MCDIR/updater/bedrock-server* -d $MCDIR/running > /dev/null
rm $MCDIR/updater/bedrock-server*
echo new server unzipped

cp -r $MCDIR/backup/worlds/ $MCDIR/running
echo world migrated

cp $MCDIR/backup/allowlist.json $MCDIR/running
cp $MCDIR/backup/server.properties $MCDIR/running
echo server setting migrated
