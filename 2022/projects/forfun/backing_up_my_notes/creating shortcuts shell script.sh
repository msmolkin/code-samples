# function move_files_and_rename_if_exist_in {
#     # if files exist in the new dir, rename before moving
# 	for f in *.md;
#         do
#             g="$1/${f%.md} new.md"
#             while
#                 [[ -f $g ]];
#             do
#                 g="${g%.md} new.md"
#             done
#         done
#         mv "$f" "$g"
#     for f in *;
#         do mv "$f" "$1";
# }

function move_files_and_rename_if_exist_in {
    for f in *.md;
        name=${f%.md}
        if [[ -e $f.md || -L $f.md ]] ; then # redundant
            i=0x    
            while [[ -e "$name $i.md" || -L "$name $i.md" ]] ; do
                let i++
            done
            name="$name $i"
        mv "$f" "$1/$name.md"
        for f in *;
            do mv "$f" "$1";
        fi
}

# Path: creating shortcuts shell script.sh

# ====================

OLD_IDEAS_DIR="/Users/michael/Library/Mobile Documents/iCloud~md~obsidian/Documents/Ideas/"
NEW_IDEAS_DIR="/Users/michael/OneDrive/Documents/Ideas/"

OLD_JOURNALING_DIR="/Users/michael/Library/Mobile Documents/iCloud~md~obsidian/Documents/Journaling/"
NEW_JOURNALING_DIR="/Users/michael/OneDrive/Documents/Journaling/"

# for each file
# if file exists in the new dir, rename it first
# move it to the new dir
function move_files_and_rename_if_exist_in {
	for f in *.md;
        do
            g="$1/${f%.md} new.md"
            while
                [[ -f $g ]];
            do
                g="${g%.md} new.md"
            done
        done
        mv "$f" "$g"
    for f in *;
        do mv "$f" "$1";
}

cd $OLD_IDEAS_DIR
for f in *.md; do mv -- "$f" "${f%.md} from phone.md"; done
# mv * $NEW_IDEAS_DIR
move_files_and_rename_if_exist_in $NEW_IDEAS_DIR


cd $OLD_JOURNALING_DIR
for f in *.md; do mv -- "$f" "${f%.md} from phone.md"; done
# mv * $NEW_JOURNALING_DIR

# https://stackoverflow.com/questions/12187859/create-new-file-but-add-number-if-filename-already-exists-in-bash

name=somefile
if [[ -e $name.ext || -L $name.ext ]] ; then
    i=0
    while [[ -e $name-$i.ext || -L $name-$i.ext ]] ; do
        let i++
    done
    name=$name-$i
fi
touch -- "$name".ext
