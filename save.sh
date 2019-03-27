FILE_TO_SAVE=$1
[[ -z $FILE_TO_SAVE ]] && FILE_TO_SAVE="."

COMMENT=$2
[[ -z $COMMENT ]] && COMMENT="[AUTO] update"

git add $FILE_TO_SAVE
git commit -m $COMMENT
git push -u origin master