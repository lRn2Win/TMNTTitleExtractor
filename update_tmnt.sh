#dfile=../../tmnt.s4.data.clean.txt; 
#st="TMNT.S04.E";
#season="04"
#s=1;
dfile=${1}
st=${2}
season=${3}
s=${4}
dryrun=${5}
#for i in `ls title*.mp4`;
#do 
# s2d=$(printf '%02d' "$s");
# search=$(printf 'S%sE%s' "${season}" "${s2d}")
# n=$(cat "${dfile}" | grep ":${search}" | cut -d":" -f3 | sed -e 's/[^A-Za-z0-9._-]/\./g' | sed 's/^.//;s/.$//');
# newn=$(echo $i | sed "s/title_t[0-9]*/${st}${s2d}\.${n}/");
# echo "$i -------> $newn";
## echo "mv $i $newn";
# mv $i $newn;
# let s=$s+1;
#done

#while read -r i;
for i in $(ls *.mp4);
do 
 s2d=$(printf '%02d' "$s");
 dataline=$(python ./get_tmnt_title.py -f "${i}" -d "${dfile}")
 n=$(echo "${dataline}" | cut -d":" -f3 | sed -e 's/[^A-Za-z0-9._-]/\./g' | sed 's/^.//;s/.$//');
# newn=$(echo $i | sed "s/\(${st}${s2d}\)\..*\.mp4$/\1\.${n}\.mp4/");
 newn=$(echo $i | sed "s/.*\.mp4$/${st}${s2d}\.${n}\.mp4/");
 echo "$i -------> $newn";
 
if [ -z ${dryrun} ]
then
  mv $i $newn;
else
  echo "mv $i $newn";
fi 

 let s=$s+1;
done #< <(ls *.mp4)

#ffmpeg -i TMNT.S04.E09.Planet.of.the.Turtles.mp4 -ss 00:00:58 -to 00:01:10 -r 1/1 timage%03d.bmp
