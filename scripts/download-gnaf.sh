#! /bin/bash
set -o allexport
source .env
set +o allexport

echo "downloading GNAF file"
if command -v curl &> /dev/null;  then
    curl -o data/gnaf.zip $GNAF_FILE_URL
elif command -v wget &> /dev/null; then
    wget -O data/gnaf.zip $GNAF_FILE_URL
else
    echo "Please install curl or wget before continuing"
    exit 1
fi

echo "unzipping GNAF file to data directory"
unzip data/gnaf.zip -d ./data

echo "done!"
