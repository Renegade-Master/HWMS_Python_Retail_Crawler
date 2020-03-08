#!/bin/bash

# Script to create a ZIP package of the current development of HWMS
# retail crawler for uploading as a Lambda function.

if [ -e hwms_retailPriceCrawler.zip ]; then
    var=`date +"%FORMAT_STRING"`
    now=`date +"%Y%m%d-%H%M%S"`
    mv hwms_retailPriceCrawler.zip _backup/hwms_retailPriceCrawler_${now}.zip
fi

echo "Adding Dependancies..."
cd "RetailCrawler/.venv_hwms/lib/python3.7/site-packages"
zip -r9 ${OLDPWD}/hwms_retailPriceCrawler.zip .
echo "Adding Dependancies...DONE!"

echo "Adding Source..."
cd ${OLDPWD}/RetailCrawler
zip -g ../hwms_retailPriceCrawler.zip *py
echo "Adding Source...DONE!"

